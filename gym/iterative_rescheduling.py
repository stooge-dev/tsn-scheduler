# TODO: wtf is this voodoo?
import sys
sys.path.append("/home/tisc06/RESI-TSN-DFKI/tsnscheduler")
from scheduler import generate_streams

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
    

    ...