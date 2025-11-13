# HERMES
# Bujosa et al. 2022
# HERMES: Heuristic Multi-queue Scheduler for TSN Time-Triggered Traffic with Zero Reception Jitter Capabilities
from scheduler.business import Network

class HermesScheduler:
    def __init__(self, network: Network, scheduled_queues):
        self.network = network
        
    def generate_frames_on_links(self):
        pass
        