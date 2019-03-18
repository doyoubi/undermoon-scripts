from redis import StrictRedis


RedisClient = Any


class RedisClientException(Exception):
    pass


class RedisClientFactory:
    def gen_redis_client(self, address: str, timeout: int) -> RedisClient:
        raise NotImplemented


class CachedRedisClientFactory:
    def __init__(self):
        self.pool: Dict[str, StrictRedis] = {}

    def gen_redis_client(self, address: str, timeout: int) -> RedisClient:
        if address in self.pool:
            return self.pool[address]

        segs = address.split(':')
        if len(segs) != 2:
            raise RedisClientException('invalid address {}'.format(address))

        ip = segs[0]
        try:
            port = int(segs[1])
        except ValueError:
            raise RedisClientException('invalid address {}'.format(address))

        client = StrictRedis(ip, port, socket_timeout=timeout)
        self.pool[address] = client
        return client
