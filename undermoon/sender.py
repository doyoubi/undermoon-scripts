class ConfigSender:
	def send(self, hosts):
		raise NotImplemented


class GeventBatchSender(ConfigSender):
	def send(self, hosts):
		pass
