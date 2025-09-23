import z3

from typing import Sequence

from .business import Network, Stream


def schedule(network: Network, streams: Sequence[Stream], scheduled_queues, total_queues, best_effort_queues):
    print(network)
    print(streams)
    
    for stream in streams:
        print(stream.name + ":" + str(stream.path))
    
    solver = z3.Solver()
    # solver.set("smt.core.minimize", "true")

    # only one frame per stream is currently assumed
    # AND Li == s.L

    frame_variable_dict = {}
    for stream in streams:
        frame_variable_dict.setdefault(stream, {})
        for link in stream.path:
            frame_variable_dict[stream].setdefault(link, {})
            frame_variable_dict[stream][link]["offset"] = z3.Int('frame_offset_' + stream.name + "_link_" + link.src.name + "-" + link.dst.name)
            frame_variable_dict[stream][link]["queue"] = z3.Int('stream_queue_' + stream.name + "_link_" + link.src.name + "-" + link.dst.name)

    

    """
    Frame Constraint
    """
    for stream in streams:
        for link in stream.path:
            frame_period_in_macroticks = stream.period / link.macrotick
            frame_transmission_duration_in_macroticks = stream.length / link.macrotick # TODO: speed of link is missing
            solver.add(z3.And(frame_variable_dict[stream][link]["offset"] >= 0, frame_variable_dict[stream][link]["offset"] <= frame_period_in_macroticks - frame_transmission_duration_in_macroticks))

    """
    Link Constraint
    """
    for stream1 in streams:
        for stream2 in streams:
            if stream2 == stream1:
                continue
            
            for link_stream1 in stream1.path:
                for link_stream2 in stream2.path:
                    if link_stream1 == link_stream2:

                        stream2_frame_length_in_macroticks = stream2.length / link_stream2.macrotick # TODO: speed of link is missing
                        stream1_frame_length_in_macroticks = stream1.length / link_stream1.macrotick # TODO: speed of link is missing
                        
                        solver.add(z3.Or(
                            frame_variable_dict[stream1][link_stream1]["offset"] >= frame_variable_dict[stream2][link_stream2]["offset"] + stream2_frame_length_in_macroticks,
                            frame_variable_dict[stream2][link_stream2]["offset"] >= frame_variable_dict[stream1][link_stream1]["offset"] + stream1_frame_length_in_macroticks
                        ))
                    else:
                        continue

    """
    Stream Transmission Constraint
    """
    for stream in streams:
        for (link1, link2) in stream.adjacent_link_pairs():
            if link1.dst == link2.src:
                # TODO: pheta for time precision
                frame_length_in_macroticks = stream.length / link1.macrotick
                solver.add(frame_variable_dict[stream][link2]["offset"] * link2.macrotick - link1.delay >= (frame_variable_dict[stream][link1]["offset"] + frame_length_in_macroticks) * link1.macrotick)
            else:
                continue

    """
    End-to-End Constraint
    """
    for stream in streams:
        src = stream.src()
        dst = stream.dst()
        solver.add(src.macrotick * frame_variable_dict[stream][src]["offset"] + stream.deadline >= dst.macrotick * frame_variable_dict[stream][dst]["offset"] + stream.length)

    """
    802.1Qbv Constraint
    Stream Isolation
    """
    for stream1 in streams:
        for stream2 in streams:
            if stream1 == stream2:
                continue

            for link_idx_stream1, link_stream1 in enumerate(stream1.path):
                for link_idx_stream2, link_stream2 in enumerate(stream2.path):
                    if link_stream2 != link_stream2:
                        continue

                    if link_idx_stream2 == 0 or link_idx_stream1 == 0:
                        continue

                    previous_link_stream1 = stream1.path[link_idx_stream1 - 1]
                    previous_link_stream2 = stream2.path[link_idx_stream2 - 1]

                    solver.add(z3.Or(
                        frame_variable_dict[stream1][link_stream1]["offset"] * link_stream1.macrotick <= frame_variable_dict[stream2][previous_link_stream2]["offset"] * previous_link_stream2.macrotick + previous_link_stream2.delay,
                        frame_variable_dict[stream2][link_stream2]["offset"] * link_stream2.macrotick <= frame_variable_dict[stream1][previous_link_stream1]["offset"] * previous_link_stream1.macrotick + previous_link_stream1.delay,
                        frame_variable_dict[stream1][link_stream1]["queue"] != frame_variable_dict[stream2][link_stream2]["queue"]
                    ))

    """
    Queue Constraint
    """
    for stream in streams:
        for link_idx, link in enumerate(stream.path):

            solver.add(z3.And(frame_variable_dict[stream][link]["queue"] >= 0, frame_variable_dict[stream][link]["queue"] <= scheduled_queues))
            """
            if link_idx > 0:
                previous_link = stream.path[link_idx - 1]
                solver.add(frame_variable_dict[stream][link]["queue"] == frame_variable_dict[stream][previous_link]["queue"])
            """
    
    """
    Results printing
    """
    print("[~] Statistics")
    print(solver.statistics())
    print("")
    check = solver.check()
    if str(check) == "sat":
        print(solver.model())
    else:
        print("[-] Unsatisfiable schedule parameter")
        print(solver.unsat_core())

    return schedule