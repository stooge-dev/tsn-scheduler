# Graciunas
# Graciunas et. al 2016
# Scheduling Real-Time Communication in IEEE 802.1Qbv Time Sensitive Networks
import z3

import math
from typing import Sequence

from ..business import Network, Stream

class GracuniasScheduler:
    def __init__(self, network: Network, scheduled_queues, predefined_offsets={}):
        self.network = network
        self.queues_available = scheduled_queues
        self.configure_solver()
        self.frame_variable_dict = {}
        self.frame_count = {}

    def configure_solver(self):
        self.solver = z3.Solver()
        self.solver.set("unsat_core", True)
        # solver.set("smt.core.minimize", "true")
        
    def add_frame_constraints(self, streams):
        for stream in streams:
            for link in stream.path:
                for current_frame in range(self.frame_count[stream]):
                    frame_period_in_macroticks = stream.period / link.macrotick

                    # i don't need todo (stream.length / (link.speed * 1000 * 1000)) / 1000 / 1000
                    # 100 Mbytes per second == 100 bytes per microsecond
                    frame_transmission_duration_in_macroticks = (stream.length / link.speed) / link.macrotick
                    self.solver.add(z3.And(self.frame_variable_dict[stream][link][current_frame]["offset"] >= current_frame * frame_period_in_macroticks, 
                                           
                                           self.frame_variable_dict[stream][link][current_frame]["offset"] <= current_frame * frame_period_in_macroticks + frame_period_in_macroticks - frame_transmission_duration_in_macroticks))

    def add_link_constraints(self, streams):
        for stream1 in streams:
            for stream2 in streams:
                if stream2 == stream1:
                    continue
                
                for link_stream1 in stream1.path:
                    for link_stream2 in stream2.path:
                        if link_stream1 != link_stream2:
                            continue
                        
                        for current_frame_stream1 in range(self.frame_count[stream1]):
                            for current_frame_stream2 in range(self.frame_count[stream2]):
                                stream2_frame_transmission_duration_in_macroticks = (stream2.length / link_stream2.speed) / link_stream2.macrotick
                                stream1_frame_transmission_duration_in_macroticks = (stream1.length / link_stream1.speed) / link_stream1.macrotick
                                
                                stream2_period_in_macroticks = stream2.period / link_stream2.macrotick
                                stream1_period_in_macroticks = stream1.period / link_stream1.macrotick

                                hyperperiod_stream1_stream2 = math.lcm(stream2.deadline, stream1.deadline)

                                for stream1_i in range(int(hyperperiod_stream1_stream2 / stream1.period)):
                                    for stream2_i in range(int(hyperperiod_stream1_stream2 / stream2.period)):

                                        self.solver.add(z3.Or(
                                            self.frame_variable_dict[stream1][link_stream1][current_frame_stream1]["offset"] + stream1_i * stream1_period_in_macroticks
                                            >= 
                                            self.frame_variable_dict[stream2][link_stream2][current_frame_stream2]["offset"] + stream2_i * stream2_period_in_macroticks + stream2_frame_transmission_duration_in_macroticks,


                                            self.frame_variable_dict[stream2][link_stream2][current_frame_stream2]["offset"] + stream2_i * stream2_period_in_macroticks
                                            >= 
                                            self.frame_variable_dict[stream1][link_stream1][current_frame_stream1]["offset"] + stream1_i * stream1_period_in_macroticks + stream1_frame_transmission_duration_in_macroticks
                                        ))

    def add_stream_transmission_constraints(self, streams):
        for stream in streams:
            for (link1, link2) in stream.adjacent_link_pairs():
                for current_frame in range(self.frame_count[stream]):
                    # TODO: pheta for time precision
                    frame_transmission_duration_in_macroticks = int((stream.length / link1.speed) / link1.macrotick)
                    self.solver.add(self.frame_variable_dict[stream][link2][current_frame]["offset"] * link2.macrotick - link1.delay >= (self.frame_variable_dict[stream][link1][current_frame]["offset"] + frame_transmission_duration_in_macroticks) * link1.macrotick)
          
    def add_end_to_end_constraints(self, streams):
        for stream in streams:
            for current_frame in range(self.frame_count[stream]):
                src = stream.src()
                dst = stream.dst()
                frame_transmission_duration_in_macroticks = (stream.length / dst.speed) / dst.macrotick
                self.solver.add(src.macrotick * self.frame_variable_dict[stream][src][current_frame]["offset"] + stream.deadline >= dst.macrotick * self.frame_variable_dict[stream][dst][current_frame]["offset"] + frame_transmission_duration_in_macroticks)

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

                        hyperperiod_stream1_stream2 = math.lcm(stream2.deadline, stream1.deadline)

                        for stream1_i in range(int(hyperperiod_stream1_stream2 / stream1.period)):
                            for stream2_i in range(int(hyperperiod_stream1_stream2 / stream2.period)):
                                for current_frame_stream1 in range(self.frame_count[stream1]):
                                    for current_frame_stream2 in range(self.frame_count[stream2]):

                                        # FIXME: theta for time precision
                                        self.solver.add(z3.Or(
                                            self.frame_variable_dict[stream1][link_stream1][current_frame_stream1]["offset"] * link_stream1.macrotick + stream1_i * stream1.period
                                            <= 
                                            self.frame_variable_dict[stream2][previous_link_stream2][current_frame_stream2]["offset"] * previous_link_stream2.macrotick + stream2_i * stream2.period + previous_link_stream2.delay,

                                            self.frame_variable_dict[stream2][link_stream2][current_frame_stream2]["offset"] * link_stream2.macrotick + stream2_i * stream2.period
                                            <= 
                                            self.frame_variable_dict[stream1][previous_link_stream1][current_frame_stream1]["offset"] * previous_link_stream1.macrotick + stream1_i * stream1.period + previous_link_stream1.delay,

                                            self.frame_variable_dict[stream1][link_stream1]["queue"] 
                                            != 
                                            self.frame_variable_dict[stream2][link_stream2]["queue"]
                                        ))

    def add_queue_constraints(self, streams, retagging=True):
        for stream in streams:
            for link_idx, link in enumerate(stream.path):

                self.solver.add(z3.And(self.frame_variable_dict[stream][link]["queue"] >= 0, self.frame_variable_dict[stream][link]["queue"] <= self.queues_available))
                
                if link_idx > 0 and not retagging:
                    previous_link = stream.path[link_idx - 1]
                    self.solver.add(self.frame_variable_dict[stream][link]["queue"] == self.frame_variable_dict[stream][previous_link]["queue"])
                
    def viz_streams_as_gantt(self, streams):
        import plotly.figure_factory as ff
        import plotly.express as px
        import pandas as pd
        import random

        df = []

        for stream in streams:
            for link in stream.path:
                for current_frame in range(self.frame_count[stream]):
                    frame_transmission_length = stream.length / link.speed
                    task_str = link.__str__()
                    df.append(dict(Task=str(task_str), Start=self.solver.model()[self.frame_variable_dict[stream][link][current_frame]["offset"]].as_long(), Finish=self.solver.model()[self.frame_variable_dict[stream][link][current_frame]["offset"]].as_long()+frame_transmission_length, Resource=stream.name))

        df = pd.DataFrame(df)
        all_the_colors = list((x,y,z) for x in range(0, 256, 20) for y in range(0, 256, 20) for z in range(0, 256, 20))
        colors = [f"rgb({random.choice(all_the_colors)})" for _ in df.Resource.unique()]
        fig = ff.create_gantt(df, colors=colors, index_col="Resource", show_colorbar=True, group_tasks=True)
        #fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
        #fig.select_yaxes(selector="Task")
        fig.update_layout(xaxis_type="linear")
        fig.show()
        
    def schedule(self, streams: Sequence[Stream]):
        print(self.network)
        print("[~] Constraining...")
        
        periods = []
        for stream in streams:
            print(stream.name + ":" + str(stream.path) + ", deadline=" + str(stream.deadline) + ", period=" + str(stream.period))
            periods.append(stream.period)    
    
        import math
        self.streams_hyperperiod = math.lcm(*periods)

        # only one frame per stream is currently assumed
        # AND Li == s.L
        for stream in streams:
            self.frame_count[stream] = int(self.streams_hyperperiod / stream.period)

            self.frame_variable_dict.setdefault(stream, {})
            for current_frame in range(self.frame_count[stream]):
                for link in stream.path:
                    self.frame_variable_dict[stream].setdefault(link, {})
                    self.frame_variable_dict[stream][link].setdefault(current_frame, {})
                    self.frame_variable_dict[stream][link][current_frame]["offset"] = z3.Int('frame_' + str(current_frame) + '_offset_' + stream.name + "_link_" + link.src.name + "-" + link.dst.name)
                    self.frame_variable_dict[stream][link]["queue"] = z3.Int('stream_queue_' + stream.name + "_link_" + link.src.name + "-" + link.dst.name)


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