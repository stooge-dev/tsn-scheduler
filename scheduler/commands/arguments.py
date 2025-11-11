#!/bin/usr/env python3

import argparse

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="tsnscheduler", description="Schedules frames for streams for the given network")
        self.generate_arguments()
        self.schedule_commands = None
        self.add_scheduler_command_subparsers()

    def generate_arguments(self):
        """
        Argument needs a file which contains the following content:
        src,dst,speed,delay,marcotick
        ...

        src meaning the source node of the link
        dst meaning the destination node of the link
        speed the speed in MBs of the link
        delay the e.g. propagation or processing delay of the link (in ) TODO: unit missing
        marcotick the time granularity of the physical link (in ) TODO: unit missing
        """
        main_commands = self.parser.add_subparsers(help="commands", dest="command", required=True)
        self.schedule_command = main_commands.add_parser("schedule")
        self.schedule_command.add_argument("-nf", "--network_filename", action="store", required=True, help="Filename of network csv")

        self.schedule_command.add_argument("-sf", "--streams_filename", action="store", required=True, help="Filename of stream csv")
        self.schedule_command.add_argument("-nsf", "--new_streams_filename", action="store", required=False)

        self.schedule_command.add_argument("-sq", "--scheduled_queues", action="store", required=False, default=7)
        self.schedule_command.add_argument("-tq", "--total_queues", action="store", required=False, default=8)

        offset_file_group = self.schedule_command.add_mutually_exclusive_group()
        offset_file_group.add_argument("-sof", "--save_offset_file", action="store", required=False, default=None)
        offset_file_group.add_argument("-lof", "--load_offset_file", action="store", required=False, default=None)

        self.generate_streams_parser = main_commands.add_parser("streams")
        self.generate_streams_parser.add_argument("-c", "--count", action="store", type=int, required=True)

        self.generate_streams_parser.add_argument("-nf", "--network_filename", action="store", required=True, help="Filename of network csv")
        self.generate_streams_parser.add_argument("-st", "--save_to", action="store", required=True)

        self.generate_streams_parser.add_argument("--seed", action="store", type=int, required=False, default=1)

        self.api_parser = main_commands.add_parser("api")

    def add_scheduler_command(self, schedulername: str):
        if self.schedule_commands == None:
            self.schedule_commands = self.schedule_command.add_subparsers(help="commands", dest="method", required=True)

        return self.schedule_commands.add_parser(schedulername)

    def add_scheduler_command_subparsers(self):
        self.hermes = self.add_scheduler_command("hermes")
        self.graciunas = self.add_scheduler_command("graciunas")

    def parse_arguments(self):
        return self.parser.parse_args()


