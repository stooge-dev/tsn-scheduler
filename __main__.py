#!/bin/bash/env python3

from .utils import parse_args, read_network_from_csv, read_streams_from_csv
from .scheduler import schedule

def generate_variables(network, streams):
    pass

args = parse_args()

# TODO: queues for every device are the same currently 
scheduled_queues = args.scheduled_queues
total_queues = args.total_queues
best_effort_queues = total_queues - scheduled_queues

network = read_network_from_csv(args.network_filename)
streams = read_streams_from_csv(args.streams_filename, network)

schedule(network, streams, scheduled_queues, total_queues, best_effort_queues)

# TODO: make a benchmark generator?
# TODO: generate GCL out of model
# TODO: visualize the GCL?
"""
import plotly.figure_factory as ff
import pandas as pd

df = []

for vl in vls:
    for link in vl.path:
        df.append(dict(Task=link.__repr__(), Start=s.model()[frame_offsets[vl][link]].as_long(), Finish=s.model()[frame_offsets[vl][link]].as_long()+vl.length, Resource=vl.name))

fig = ff.create_gantt(pd.DataFrame(df), index_col="Resource", show_colorbar=True)
fig.update_layout(xaxis_type="linear")
fig.show()
"""