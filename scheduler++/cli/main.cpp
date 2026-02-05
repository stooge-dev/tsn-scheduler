#include <iostream>
#include <map>
#include <memory>

#include "CLI/CLI.hpp"

#include "commands.h"
#include "schedule.h"

namespace scheduler_pp::cli 
{
    int main(int argc, char **argv) 
    {
        auto cli = CLI::App{ "TSN scheduler"};
        
        auto schedule_sub_command = cli.add_subcommand("schedule", "Scheduling subcommand");
        for(const auto& scheduler: schedulers()) {
            schedule_sub_command->add_subcommand(scheduler->name(), "");
        }

        CLI11_PARSE(cli, argc, argv);
    
        if(schedule_sub_command->parsed()) {
            for(const auto& sub_command: schedule_sub_command->get_subcommands()) {
                if(sub_command->parsed()) {
                    for(const auto& scheduler: schedulers()) {
                        if(sub_command->get_name() == scheduler->name()) {
                            scheduler->schedule();
                        }
                    }
                }
            }
        }

        return 0;
    }
}

int main(int argc, char **argv)
{
    scheduler_pp::cli::main(argc, argv);
}