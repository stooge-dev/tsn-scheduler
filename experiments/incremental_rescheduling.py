# voodoo magic
import sys
sys.path.append("/home/tisc06/RESI-TSN-DFKI/tsnscheduler")

if sys.prefix == sys.base_prefix:
    print("Virtualenv not loaded")
    exit(-1)

from scheduler import generate_streams, read_network_from_csv, GracuniasScheduler

class SameLinkSchedulingStreamDependencyGraph():
    def __init__(self, streams):
        self.streams = streams

        self._calculate_dependencies()
    
    def _calculate_dependencies(self):
        self.graph = {}
        for stream1 in self.streams:
            self.graph.setdefault(stream1, {})
            for stream2 in self.streams:
                self.graph.setdefault(stream2, {})
                if stream1 == stream2:
                    continue

                weight = 0
                for link1 in stream1.path:
                    for link2 in stream2.path:
                        if link1 != link2:
                            continue

                        weight += 1

                self.graph[stream1][stream2] = weight
                self.graph[stream2][stream1] = weight


def lower_deadline_faster_solving():
    network = read_network_from_csv("benchmarks/2_switches_6_devices/network.csv")
    scheduler = GracuniasScheduler(network, scheduled_queues=7)

    streams = generate_streams(20, network=network, seed=1)
    scheduler.schedule(streams)

    changed_stream = streams[5]
    changed_stream.deadline = int(changed_stream.deadline / 2)
    streams[5] = changed_stream

    graph = SameLinkSchedulingStreamDependencyGraph(streams)
    scheduler.configure_solver()
    scheduler.schedule(streams)

if __name__ == "__main__":
    # What do I wanna do?
    # Generate different network and streams with different utilization (TODO: how is utilization defined?) values
    # Schedule streams and record results (TODO: what results do I wanna collect?)
    # Select a stream(s) which QoS or path has changed
    # Reschedule with only this/these stream(s) missing from preset offsets
    # Is rescheduling faster than one-shot scheduling?
    # If rescheduling with only these streams missing does not work,
    # select streams to also remove from prescheduled set and try rescheduling
    # Can we see from these removed streams, which streams have had the most impact on schedulability of the new stream characteristics?
    # What changes to streams make it the most difficult to reschedule?
    # Other questions?

    # Can I use this approach easily with other ground algorithms for scheduling, like HERMES?

    network = read_network_from_csv("benchmarks/2_switches_6_devices/network.csv")
    scheduler = GracuniasScheduler(network, scheduled_queues=7)

    for i in [4, 5, 6, 7, 8]:
        print(i, "---"*40)
        streams = generate_streams(i*2, network=network, seed=i)
        scheduler.configure_solver()
        scheduler.schedule(streams)
        print("Rescheduling ---"*5)
        changed_stream = streams[i]
        changed_stream.deadline = int(changed_stream.deadline / 2)
        streams[i] = changed_stream

        # TODO: generate streams on network such that target utilization is hit
        # TODO: implement measure of utilization

        graph = SameLinkSchedulingStreamDependencyGraph(streams)
        scheduler.configure_solver()
        scheduler.schedule(streams)
        

    
