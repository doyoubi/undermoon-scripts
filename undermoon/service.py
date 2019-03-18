from .config import Config
from .coordinator import Coordinator
from .sender import Sender


class CoordinatorService:
	def __init__(self, config: Config, coordinator: Coordinator, sender: Sender):
		self.config = config
		self.sender = sender
		self.coordinator = coordinator

	def run(self) -> None:
		return
