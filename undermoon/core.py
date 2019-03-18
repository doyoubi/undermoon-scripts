from typing import Sequence


class Node:
	def __init__(self, address: str, proxy_address: str, cluster_name: str, slots: Sequence[SlotRange]):
		self.address = address
		self.proxy_address = proxy_address
		self.cluster_name = cluster_name
		self.slots = slots


class SlotRange:
	def __init__(self, start: int, end: int):
		self.start = start
		self.end = end


class Cluster:
	def __init__(self, name: str, epoch: int, nodes: Sequence[Node]):
		self.name = name
		self.epoch = epoch
		self.nodes = nodes


class Host:
	def __init__(self, address: str, epoch: int, nodes: Sequence[Node]):
		self.address = address
		self.epoch = epoch
		self.nodes = nodes
