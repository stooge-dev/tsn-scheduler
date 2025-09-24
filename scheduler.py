import z3

from typing import Sequence

from .business import Network, Stream

class Scheduler:
    def __init__(self, network: Network, scheduled_queues):
        self.network = network
        self.queues_available = scheduled_queues

    def schedule(self, streams: Sequence[Stream]):
        print(self.network)
        
        for stream in streams:
            print(stream.name + ":" + str(stream.path) + ", deadline=" + str(stream.deadline) + ", period=" + str(stream.period))
        
        solver = z3.Solver()
        solver.set("unsat_core", True)
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

                # i don't need todo (stream.length / (link.speed * 1000 * 1000)) / 1000 / 1000
                # 100 Mbytes per second == 100 bytes per microsecond
                frame_transmission_duration_in_macroticks = (stream.length / link.speed) / link.macrotick
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
                        if link_stream1 != link_stream2:
                            continue
                            
                        stream2_frame_transmission_duration_in_macroticks = (stream2.length / link_stream2.speed) / link_stream2.macrotick
                        stream1_frame_transmission_duration_in_macroticks = (stream1.length / link_stream1.speed) / link_stream1.macrotick
                        
                        solver.add(z3.Or(
                            frame_variable_dict[stream1][link_stream1]["offset"] >= frame_variable_dict[stream2][link_stream2]["offset"] + stream2_frame_transmission_duration_in_macroticks,
                            frame_variable_dict[stream2][link_stream2]["offset"] >= frame_variable_dict[stream1][link_stream1]["offset"] + stream1_frame_transmission_duration_in_macroticks
                        ))

        """
        Stream Transmission Constraint
        """
        for stream in streams:
            for (link1, link2) in stream.adjacent_link_pairs():
                # TODO: pheta for time precision
                frame_transmission_duration_in_macroticks = int((stream.length / link1.speed) / link1.macrotick)
                solver.add(frame_variable_dict[stream][link2]["offset"] * link2.macrotick - link1.delay >= (frame_variable_dict[stream][link1]["offset"] + frame_transmission_duration_in_macroticks) * link1.macrotick)
                

        """
        End-to-End Constraint
        """
        for stream in streams:
            src = stream.src()
            dst = stream.dst()
            frame_transmission_duration_in_macroticks = (stream.length / dst.speed) / dst.macrotick
            solver.add(src.macrotick * frame_variable_dict[stream][src]["offset"] + stream.deadline >= dst.macrotick * frame_variable_dict[stream][dst]["offset"] + frame_transmission_duration_in_macroticks)

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

                solver.add(z3.And(frame_variable_dict[stream][link]["queue"] >= 0, frame_variable_dict[stream][link]["queue"] <= self.queues_available))
                """
                if link_idx > 0:
                    previous_link = stream.path[link_idx - 1]
                    solver.add(frame_variable_dict[stream][link]["queue"] == frame_variable_dict[stream][previous_link]["queue"])
                """
        
        """
        Results printing
        """
        
        print("[~] Solving...")
        check = solver.check()
        print("[~] Statistics")
        print(solver.statistics())
        print("")
        if str(check) == "sat":
            print(solver.model())

            import plotly.figure_factory as ff
            import pandas as pd
            import random

            df = []

            for stream in streams:
                for link in stream.path:
                    frame_transmission_length = stream.length / link.speed
                    df.append(dict(Task=link.__repr__(), Start=solver.model()[frame_variable_dict[stream][link]["offset"]].as_long(), Finish=solver.model()[frame_variable_dict[stream][link]["offset"]].as_long()+frame_transmission_length, Resource=stream.name))

            df = pd.DataFrame(df)
            all_the_colors = list((x,y,z) for x in range(256) for y in range(256) for z in range(256))
            colors = [f"rgb({random.choice(all_the_colors)})" for x in df.Resource.unique()]
            fig = ff.create_gantt(df, colors=colors, index_col="Resource", show_colorbar=True)
            fig.update_layout(xaxis_type="linear")
            fig.show()
        else:
            print("[-] Unsatisfiable schedule parameter")
            print(solver.unsat_core())

    # return GCL