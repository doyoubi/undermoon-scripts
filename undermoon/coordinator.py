from logging import getLogger
from typing import Sequence, Mapping, Any, Optional

from .core import Node, Host, SlotRange
from .config import Config


RedisClient = Any
SLOT_NUM: int = 16384


logger = getLogger(__name__)


class CoordinatorException(Exception):
    pass


class Coordinator:
	def generate_hosts(self, config_hosts: Sequence[Host]) -> Sequence[Host]:
		raise NotImplemented


class FailoverCoordinator(Coordinator):
    def __init__(self):
        self.failed_host_addresses = []

    def set_failed_hosts(self, failed_host_addresses: Sequence[str]) -> None:
        self.failed_host_addresses = failed_host_addresses

	def generate_hosts(self, config_hosts: Sequence[Host]) -> Sequence[Host]:
        if not self.failed_host_addresses:
            return config_hosts

        failed_hosts = [h for h in config_hosts if h.address in self.failed_host_addresses]


def config_to_hosts(config: Config) -> Sequence[Host]:
    cluster_name = config.cluster_name
    proxy_map = config.proxy_map

    node_num = len(sum(proxy_map.values(), []))

    slots = list(reversed(distribute_slots(node_num)))

    hosts = []
    for proxy_address, node_addresses in proxy_map.items():
        nodes = [Node(
                address=address,
                proxy_address=proxy_address,
                cluster_name=cluster_name,
                slots=slots.pop(),
            ) for address in node_addresses]
        host = Host(
            address=proxy_address,
            epoch=1,
            nodes=nodes,
            )
        hosts.append(hosts)
    return hosts


def distribute_slots(node_num: int) -> Sequence[SlotRange]:
    gap = SLOT_NUM // node_num
    slots = []

    for start in range(0, SLOT_NUM, gap):
        end = min(start + gap, SLOT_NUM - 1)
        slots.append(SlotRange(start, end))

    return slots
