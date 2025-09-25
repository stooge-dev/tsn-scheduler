import z3

from typing import Sequence

from .business import Network, Stream

class Scheduler:
    def __init__(self, network: Network, scheduled_queues):
        self.network = network
        self.queues_available = scheduled_queues
        self.solver = z3.Solver()
        self.configure_solver()
        self.frame_variable_dict = {}

    def configure_solver(self):
        self.solver.set("unsat_core", True)
        # solver.set("smt.core.minimize", "true")

    def generate_frame_variables(self, streams):
        # only one frame per stream is currently assumed
        # AND Li == s.L
        for stream in streams:
            self.frame_variable_dict.setdefault(stream, {})
            for link in stream.path:
                self.frame_variable_dict[stream].setdefault(link, {})
                self.frame_variable_dict[stream][link]["offset"] = z3.Int('frame_offset_' + stream.name + "_link_" + link.src.name + "-" + link.dst.name)
                self.frame_variable_dict[stream][link]["queue"] = z3.Int('stream_queue_' + stream.name + "_link_" + link.src.name + "-" + link.dst.name)

    def add_frame_constraints(self, streams):
        for stream in streams:
            for link in stream.path:
                frame_period_in_macroticks = stream.period / link.macrotick

                # i don't need todo (stream.length / (link.speed * 1000 * 1000)) / 1000 / 1000
                # 100 Mbytes per second == 100 bytes per microsecond
                frame_transmission_duration_in_macroticks = (stream.length / link.speed) / link.macrotick
                self.solver.add(z3.And(self.frame_variable_dict[stream][link]["offset"] >= 0, self.frame_variable_dict[stream][link]["offset"] <= frame_period_in_macroticks - frame_transmission_duration_in_macroticks))

    def add_link_constraints(self, streams):
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
                        
                        self.solver.add(z3.Or(
                            self.frame_variable_dict[stream1][link_stream1]["offset"] >= self.frame_variable_dict[stream2][link_stream2]["offset"] + stream2_frame_transmission_duration_in_macroticks,
                            self.frame_variable_dict[stream2][link_stream2]["offset"] >= self.frame_variable_dict[stream1][link_stream1]["offset"] + stream1_frame_transmission_duration_in_macroticks
                        ))

    def add_stream_transmission_constraints(self, streams):
        for stream in streams:
            for (link1, link2) in stream.adjacent_link_pairs():
                # TODO: pheta for time precision
                frame_transmission_duration_in_macroticks = int((stream.length / link1.speed) / link1.macrotick)
                self.solver.add(self.frame_variable_dict[stream][link2]["offset"] * link2.macrotick - link1.delay >= (self.frame_variable_dict[stream][link1]["offset"] + frame_transmission_duration_in_macroticks) * link1.macrotick)
          
    def add_end_to_end_constraints(self, streams):
        for stream in streams:
            src = stream.src()
            dst = stream.dst()
            frame_transmission_duration_in_macroticks = (stream.length / dst.speed) / dst.macrotick
            self.solver.add(src.macrotick * self.frame_variable_dict[stream][src]["offset"] + stream.deadline >= dst.macrotick * self.frame_variable_dict[stream][dst]["offset"] + frame_transmission_duration_in_macroticks)

    def add_stream_isolation_constraints(self, streams):
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

                        self.solver.add(z3.Or(
                            self.frame_variable_dict[stream1][link_stream1]["offset"] * link_stream1.macrotick <= self.frame_variable_dict[stream2][previous_link_stream2]["offset"] * previous_link_stream2.macrotick + previous_link_stream2.delay,
                            self.frame_variable_dict[stream2][link_stream2]["offset"] * link_stream2.macrotick <= self.frame_variable_dict[stream1][previous_link_stream1]["offset"] * previous_link_stream1.macrotick + previous_link_stream1.delay,
                            self.frame_variable_dict[stream1][link_stream1]["queue"] != self.frame_variable_dict[stream2][link_stream2]["queue"]
                        ))

    def add_queue_constraints(self, streams, no_retagging=False):
        for stream in streams:
            for link_idx, link in enumerate(stream.path):

                self.solver.add(z3.And(self.frame_variable_dict[stream][link]["queue"] >= 0, self.frame_variable_dict[stream][link]["queue"] <= self.queues_available))
                
                if link_idx > 0 and no_retagging:
                    previous_link = stream.path[link_idx - 1]
                    self.solver.add(self.frame_variable_dict[stream][link]["queue"] == self.frame_variable_dict[stream][previous_link]["queue"])
                
    def viz_streams_as_gantt(self, streams):
        import plotly.figure_factory as ff
        import pandas as pd
        import random

        df = []

        for stream in streams:
            for link in stream.path:
                frame_transmission_length = stream.length / link.speed
                df.append(dict(Task=link.__repr__(), Start=self.solver.model()[self.frame_variable_dict[stream][link]["offset"]].as_long(), Finish=self.solver.model()[self.frame_variable_dict[stream][link]["offset"]].as_long()+frame_transmission_length, Resource=stream.name))

        df = pd.DataFrame(df)
        all_the_colors = list((x,y,z) for x in range(0, 256, 10) for y in range(0, 256, 10) for z in range(0, 256, 10))
        colors = [f"rgb({random.choice(all_the_colors)})" for _ in df.Resource.unique()]
        fig = ff.create_gantt(df, colors=colors, index_col="Resource", show_colorbar=True)
        fig.update_layout(xaxis_type="linear")
        fig.show()
        
    def schedule(self, streams: Sequence[Stream]):
        print(self.network)
        
        for stream in streams:
            print(stream.name + ":" + str(stream.path) + ", deadline=" + str(stream.deadline) + ", period=" + str(stream.period))
        
        self.generate_frame_variables(streams)

        self.add_frame_constraints(streams)
        self.add_link_constraints(streams)
        self.add_stream_transmission_constraints(streams)
        self.add_end_to_end_constraints(streams)
        self.add_stream_isolation_constraints(streams)
        self.add_queue_constraints(streams)
        
        print("[~] Solving...")
        check = self.solver.check()
        print("[~] Statistics")
        print(self.solver.statistics())
        print("")
        if str(check) == "sat":
            # print(self.solver.model())

            self.viz_streams_as_gantt(streams)
        else:
            print("[-] Unsatisfiable schedule parameter")
            print(self.solver.unsat_core())

        # TODO: return GCL

    def reschedule(self, streams: Sequence[Stream], changed_stream: Stream):
        print("[~] Resolving...")
        # TODO: current assumption is path is not changed
        last_model = self.solver.model()
        self.solver = z3.Solver()

        self.generate_frame_variables(streams)

        self.add_frame_constraints(streams)
        self.add_link_constraints(streams)
        self.add_stream_transmission_constraints(streams)
        self.add_end_to_end_constraints(streams)
        self.add_stream_isolation_constraints(streams)
        self.add_queue_constraints(streams)

        # from .business import SameLinkSchedulingStreamDependencyGraph
        # dependency_graph = SameLinkSchedulingStreamDependencyGraph(streams)

        for stream in streams:
            if stream == changed_stream:
                continue

            for link in stream.path:
                self.solver.add(self.frame_variable_dict[stream][link]["offset"] == last_model[self.frame_variable_dict[stream][link]["offset"]])
        
        print("[~] Solving...")
        check = self.solver.check()
        print("[~] Statistics")
        print(self.solver.statistics())
        print("")
        if str(check) == "sat":
            # print(self.solver.model())

            self.viz_streams_as_gantt(streams)
        else:
            print("[-] Unsatisfiable schedule parameter")
            print(self.solver.unsat_core())