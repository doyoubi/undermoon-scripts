from typing import Mapping, Sequence

from .core import Cluster, Node, Host, SlotRange


class Config:
    def __init__(self, cluster_name: str, proxy_map: Mapping[str, Sequence[str]]):
        self.cluster_name = cluster_name
        self.proxy_map = proxy_map


def get_config() -> Config:
    proxy_map = {
        '127.0.0.1:7001': ['127.0.0.1:8001', '127.0.0.1:8002'],
        '127.0.0.1:7002': ['127.0.0.1:8003', '127.0.0.1:8004'],
        '127.0.0.1:7003': ['127.0.0.1:8005', '127.0.0.1:8006'],
    }
    return Config('mycluster', proxy_map)
