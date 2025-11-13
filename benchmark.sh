#!/bin/bash
python3 -m scheduler schedule -nf ./benchmarks/2_switches_6_devices/network.csv -sf ./benchmarks/2_switches_6_devices/streams.csv --save_offset_file test.json graciunas 
