#include <iostream>

#include <CLI/CLI.hpp>

#include "schedule.h"


int main(int argc, char **argv) {
    CLI::App app{"TSN scheduler"};

    int p = 0;
    app.add_option("-p", p, "Parameter");
    
    CLI::App* schedule_sub_command = app.add_subcommand("schedule", "Scheduling subcommand");
    for(auto&& scheduler: schedulers()) {
        CLI::App* scheduler_sub_command = schedule_sub_command->add_subcommand(scheduler->name(), "");
    }

    CLI11_PARSE(app, argc, argv);

    if(schedule_sub_command->parsed()) {
        std::cout << "Schedule command" << std::endl;
    }

    std::cout << "Parameter value: " << p << std::endl;
    return 0;
}