import time
from typing import Sequence, Mapping, Any, Optional

from .client import RedisClientFactory


class FailureDetector:
    def detect(self, address) -> Optional[str]:
        raise NotImplemented


class PingFailureDetector(FailureDetector):
    def __init__(self, redis_client_factory: RedisClientFactory, timeout: int):
        self.timeout = timeout
        self.redis_client_factory = redis_client_factory

    def detect(self, address) -> Optional[str]:
        redis_client = self.redis_client_factory.gen_redis_client(address, self.timeout)
        try:
            redis_client.ping()
            return None
        except Exception as e:
            logger.error("Failed to ping redis %s", address)
            return address


class FailureStore:
    def __init__(self, addresses: Sequence[str], expired: int):
        self.failure_addresses = {}
        self.stopped = False

        self.addresses = addresses
        self.expired = expired

    def add_failure(self, address, failed_time):
        self.failure_addresses[address] = failed_time

    def get_failed_addresses(self) -> Sequence[str]:
        now = time.time()
        return [addr for addr, failed_time in self.failure_addresses.items() \
            if now - failed_time < self.expired]


class FailureReporter:
    def __init__(self, detector: FailureDetector, failure_store: FailureStore):
        self.detector = detector
        self.failure_store = failure_store

    def loop_check(self) -> None:
        while self.stopped:
            for address in self.addresses:
                if self.detector.detect(address):
                    self.failure_store.add_failure(address, time.time())
            time.sleep(1)
