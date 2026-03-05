#include <string>
#include <iostream>
#include <iomanip>
#include <vector>
#include <map>
#include <format>
#include <numeric>
#include <ranges>
#include <stdexcept>

#include "z3++.h"

#include "gracunias.hpp"
#include "business/stream_set.hpp"
#include "business/offset.hpp"

namespace scheduler_pp::lib::scheduling {

    void GracuniasScheduler::schedule(scheduler_pp::lib::business::StreamSet streamSet, int scheduled_queues) 
    {

        const auto streams = streamSet.get_streams();
        // assert streams is not 0
        if(streams.size() == 0) {
            std::cout << "[-] Zero streams were given to schedule, aborting." << std::endl;
            throw std::runtime_error("streams is 0");
        }
        auto config = z3::config();
        config.set("unsat_core", true);
    
        auto context = z3::context(config);
    
        int hyperperiod = streams[0].get_period();
        for(auto i = 1; i < streams.size(); i++) {
            hyperperiod = std::lcm(streams[i-1].get_period(), streams[i].get_period());
        }
    
        std::cout << "[~] " << std::setw(15) << hyperperiod << " μs (hyperperiod)." << std::endl; 
    
        using FrameCountMap = std::map<std::string, int>;
        auto frame_counts = FrameCountMap{};
    
        using FrameMap = std::map<int, z3::expr>;
        using LinkMap = std::map<std::string, FrameMap>;
        using StreamMap = std::map<std::string, LinkMap>;
        auto frame_variables = StreamMap{};
    
        std::cout << "[+] Creating variables..." << std::endl;
        std::cout << "[~] " << std::setw(15) << streams.size() << " stream(s)." << std::endl;
        int created_frame_variables = 0;
        for(auto& stream: streams) {
            // TODO: explicit conversion, we want an int. if we did the LCM calculation correct it will be an int.
            frame_counts[stream.get_name()] = hyperperiod / stream.get_period();
    
            std::cout << "   [~] " << std::setw(12) << stream.get_name() << " (stream name)." << std::endl;
            std::cout << "   [~] " << std::setw(12) << frame_counts[stream.get_name()] << " frame(s)." << std::endl;
    
            frame_variables.emplace(stream.get_name(), LinkMap{});
            for(auto& link: stream.get_path()) {
                frame_variables[stream.get_name()].emplace(link.get_key(), FrameMap{});
    
                // TODO: missing frame count
                auto frame_variable_name = std::format("frame_{}_stream_{}_link_{}_offset", stream.get_name(), 0, link.get_key());
                std::cout << "   [~] " << std::setw(12) << frame_variable_name << " (frame variable name)" << std::endl; 
                frame_variables[stream.get_name()][link.get_key()].emplace(0, context.int_const(frame_variable_name.c_str()));
                created_frame_variables++;
            }
        }
        std::cout << "[~] " << std::setw(15) << created_frame_variables << " (created frame variables)." << std::endl;
        std::cout << "[+] Creating variables, complete." << std::endl;
        
    
        auto solver = z3::solver(context);
    
        std::cout << "[~] Creating frame constraints..." << std::endl;
        for(auto& stream: streams) {
            std::cout << "   [~] " << std::setw(12) << stream.get_name() << " (stream name)." << std::endl;
            for(auto& link: stream.get_path()) {
                std::cout << "      [~] " << std::setw(9) << link.get_key() << " (link key)." << std::endl;
                for(auto current_frame = 0; current_frame < frame_counts[stream.get_name()]; current_frame++) {
                    std::cout << "         [~] " << std::setw(6) <<  current_frame << " (frame idx)." << std::endl; 
                    const int frame_period_in_macroticks = stream.get_period() / link.get_macrotick();
                    std::cout << "         [~] " << std::setw(6) << frame_period_in_macroticks << " (frame period in macroticks)." << std::endl;
                
                    // i don't need todo (stream.length / (link.speed * 1000 * 1000)) / 1000 / 1000
                    // 100 Mbytes per second == 100 bytes per microsecond
                    const int frame_transmission_duration_in_macroticks = (stream.get_bytes() / link.get_bytes_per_microsecond()) / link.get_macrotick();
                    std::cout << "         [~] " << std::setw(6) << frame_transmission_duration_in_macroticks << " (frame transmission duration in macroticks)." << std::endl;
                
                    auto frame_must_be_send_in_period_it_belongs_to_and_respect_offset = frame_variables[stream.get_name()][link.get_key()].at(current_frame) >= current_frame * frame_period_in_macroticks + stream.get_offset_start();
                    auto frame_must_be_send_before_period_is_over_minus_transmission_time = frame_variables[stream.get_name()][link.get_key()].at(current_frame) <= current_frame * frame_period_in_macroticks + stream.get_offset_start() + frame_period_in_macroticks - frame_transmission_duration_in_macroticks;
                    solver.add( frame_must_be_send_in_period_it_belongs_to_and_respect_offset
                                &&
                                frame_must_be_send_before_period_is_over_minus_transmission_time);
                }
            }
        }
        std::cout << "[+] Creating frame constraints, complete." << std::endl;
    
    
        std::cout << "[~] Creating link constraints..." << std::endl;
        for(auto& stream1: streams) 
        {
            std::cout << "   [~] " << std::setw(12) << stream1.get_name() << " (stream1)." << std::endl;
    
            for(auto& stream2: streams) 
            {
                std::cout << "   [~] " << std::setw(12) << stream2.get_name() << " (stream2)." << std::endl;
    
                if(stream2.get_name() == stream1.get_name()) 
                {
                    std:: cout << "   [~] Is same stream, skipping." << std::endl;
                    continue;
                }
    
                for(auto& link_stream1: stream1.get_path()) 
                {
                    std::cout << "      [~] " << std::setw(9) << link_stream1.get_key() << " (link_stream1)." << std::endl;
    
                    for(auto& link_stream2: stream2.get_path()) 
                    {
                        std::cout << "      [~] " << std::setw(9) << link_stream2.get_key() << " (link_stream2)." << std::endl;
    
                        if(link_stream1.get_key() != link_stream2.get_key()) 
                        {
                            std::cout << "      [~] Same link, skipping." << std::endl;
                            continue;
                        }
    
                        for(auto current_frame_stream1 = 0; current_frame_stream1 < frame_counts[stream1.get_name()]; current_frame_stream1++) 
                        {
                            for(auto current_frame_stream2 = 0; current_frame_stream2 < frame_counts[stream2.get_name()]; current_frame_stream2++) 
                            {
                                const int frame_transmission_duration_in_macroticks_stream1 = (stream1.get_bytes() / link_stream1.get_bytes_per_microsecond()) / link_stream1.get_macrotick();
                                const int frame_transmission_duration_in_macroticks_stream2 = (stream2.get_bytes() / link_stream2.get_bytes_per_microsecond()) / link_stream2.get_macrotick();
    
                                const int frame_period_in_macroticks_stream1 = stream1.get_period() / link_stream1.get_macrotick();
                                const int frame_period_in_macroticks_stream2 = stream2.get_period() / link_stream2.get_macrotick();
    
                                const int hyperperiod_stream1_stream2 = std::lcm(stream1.get_deadline(), stream2.get_deadline());
    
                                for(auto stream1_i = 0; stream1_i < hyperperiod_stream1_stream2 / stream1.get_period(); stream1_i++) 
                                {
                                    for(auto stream2_i = 0; stream2_i < hyperperiod_stream1_stream2 / stream2.get_period(); stream2_i++) 
                                    {
                                        solver.add( (frame_variables[stream1.get_name()][link_stream1.get_key()].at(current_frame_stream1) + stream1_i * frame_period_in_macroticks_stream1
                                                    >=
                                                    frame_variables[stream2.get_name()][link_stream2.get_key()].at(current_frame_stream2) + stream2_i * frame_period_in_macroticks_stream2 + frame_transmission_duration_in_macroticks_stream2)
                                                        ||
                                                    (frame_variables[stream2.get_name()][link_stream2.get_key()].at(current_frame_stream2) + stream2_i * frame_period_in_macroticks_stream2
                                                    >=
                                                    frame_variables[stream1.get_name()][link_stream1.get_key()].at(current_frame_stream1) + stream1_i * frame_period_in_macroticks_stream1 + frame_transmission_duration_in_macroticks_stream1));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        std::cout << "[+] Creating link constraints, complete." << std::endl;
    
        std::cout << "[~] Creating stream transmission constraints..." << std::endl;
        for(auto& stream: streams) 
        {
            std::cout << "   [~] " << std::setw(12) << stream.get_name() << " (stream name)." << std::endl;
    
            for(auto [link1, link2]: stream.get_adjacent_link_pairs()) 
            {
                std::cout << "      [~] " << std::setw(9) << link1.get_key() << " (link1)." << std::endl;
                std::cout << "      [~] " << std::setw(9) << link2.get_key() << " (link2)." << std::endl;
    
                for(auto current_frame = 0; current_frame < frame_counts[stream.get_name()]; current_frame++) 
                {
                    const int frame_transmission_duration_in_macroticks = (stream.get_bytes() / link1.get_bytes_per_microsecond()) / link1.get_macrotick();
                    std::cout << "         [~] " << std::setw(6) << frame_transmission_duration_in_macroticks << " (frame transmission duration in macroticks)" << std::endl;
    
                    solver.add(frame_variables[stream.get_name()][link2.get_key()].at(current_frame) * link2.get_macrotick() - link1.get_delay() >= (frame_variables[stream.get_name()][link1.get_key()].at(current_frame) + frame_transmission_duration_in_macroticks) * link1.get_macrotick());
                }
            }
        }
        std::cout << "[+] Creating stream transmission constraints, complete." << std::endl;
    
        std::cout << "[~] Creating end-to-end constraints..." << std::endl;
        for(auto& stream: streams) 
        {
            std::cout << "   [~] " << std::setw(12) << stream.get_name() << " (stream name)." << std::endl;
    
            for(auto current_frame = 0; current_frame < frame_counts[stream.get_name()]; current_frame++) 
            {
                std::cout << "      [~] " << std::setw(9) << current_frame << " (current frame idx)." << std::endl;
    
                auto& src = stream.get_src();
                auto& dst = stream.get_dst();
                std::cout << "      [~] " << std::setw(9) << src.get_key() << " (src)." << std::endl;
                std::cout << "      [~] " << std::setw(9) << dst.get_key() << " (dst)." << std::endl;
                
                const int frame_transmission_duration_in_macroticks = (stream.get_bytes() / dst.get_bytes_per_microsecond()) / dst.get_macrotick();
                std::cout << "      [~] " << std::setw(9) << frame_transmission_duration_in_macroticks << " (frame transmission duration in macroticks)." << std::endl;
    
                solver.add( frame_variables[stream.get_name()][src.get_key()].at(current_frame) * src.get_macrotick() + stream.get_deadline() 
                            >= 
                            frame_variables[stream.get_name()][dst.get_key()].at(current_frame) * dst.get_macrotick() + frame_transmission_duration_in_macroticks);
            }
        }
        std::cout << "[+] Creating end-to-end constraints, complete." << std::endl;
    
    
        std::cout << "[~] Creating stream isolation constraints..." << std::endl;
        for(auto& stream1: streams) {
            for(auto& stream2: streams) {
                if(stream1.get_name() == stream2.get_name()) {
                    continue;
                }
    
                // TODO: enumerate links
                for(auto const [link_idx_stream1, link_stream1]: std::views::enumerate(stream1.get_path())) {
                    for(auto const [link_idx_stream2, link_stream2]: std::views::enumerate(stream2.get_path())) {
                        const auto links_are_different = link_stream1.get_key() != link_stream2.get_key();
                        if(links_are_different) continue;
    
                        const auto one_idx_is_zero = link_idx_stream1 == 0 || link_idx_stream2 == 0;
                        if(one_idx_is_zero) continue;
    
                        auto& previous_link_stream1 = stream1.get_path()[link_idx_stream1 - 1];
                        auto& previous_link_stream2 = stream2.get_path()[link_idx_stream2 - 1];
    
                        auto hyperperiod_stream1_stream2 = std::lcm(stream1.get_deadline(), stream2.get_deadline());
    
                        for(auto stream1_i = 0; stream1_i < hyperperiod_stream1_stream2 / stream1.get_period(); stream1_i++) {
                            for(auto stream2_i = 0; stream2_i < hyperperiod_stream1_stream2 / stream2.get_period(); stream2_i++) {
                                for(auto current_frame_stream1 = 0; current_frame_stream1 < frame_counts[stream1.get_name()]; current_frame_stream1++) {
                                    for(auto current_frame_stream2 = 0; current_frame_stream2 < frame_counts[stream2.get_name()]; current_frame_stream2++) {
                                        solver.add( (frame_variables[stream1.get_name()][link_stream1.get_key()].at(current_frame_stream1) * link_stream1.get_macrotick() + stream1_i * stream1.get_period()
                                                    <=
                                                    frame_variables[stream2.get_name()][previous_link_stream2.get_key()].at(current_frame_stream2) * previous_link_stream2.get_macrotick() + stream2_i * stream2.get_period() + previous_link_stream2.get_delay())
                                                        ||
                                                    (frame_variables[stream2.get_name()][link_stream2.get_key()].at(current_frame_stream2) * link_stream2.get_macrotick() + stream2_i * stream2.get_period()
                                                    <=
                                                    frame_variables[stream1.get_name()][previous_link_stream1.get_key()].at(current_frame_stream1) * previous_link_stream1.get_macrotick() + stream1_i * stream1.get_period() + previous_link_stream1.get_delay())
                                                        /*
                                                        ||
                                                    frame_variables[stream1.get_name()][link_stream1.get_key()]["queue"]
                                                    !=
                                                    frame_variables[stream2.get_name()][link_stream2.get_key()]["queue"]
                                                        
                                                        */ 
    
                                                );
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        std::cout << "[+] Creating stream isolation constraints, complete." << std::endl;
    
        std::cout << "[~] Creating queue constraints..." << std::endl;
        for(auto& stream: streams) {
            // TODO: enumerate links
            for(auto const [link_idx, link]: std::views::enumerate(stream.get_path())) {
                /*
                solver.add(frame_variables[stream.get_name()][link.get_key()]["queue"] >= 0 && frame_variables[stream.get_name()][link.get_key()]["queue"] <= queues_available)
    
                if(link_idx > 0 && !retagging) {
                    auto const previous_link = stream.get_path()[link_idx - 1];
                    solver.add(frame_variables[stream.get_name()][link.get_key()]["queue"] == frame_variables[stream.get_name()][link.get_key()]["queue"])
                }*/
            }
        }
        std::cout << "[+] Creating queue constraints, complete (the queue constraints are a lie)." << std::endl;
    
        std::cout << "[~] Solving..." << std::endl;
        auto result = solver.check();
        std::cout << "[~] " << std::setw(15) << result << std::endl;
    
        // TODO: calculate offsets 
        // TODO: and give them back, changing SchedulerBase
        const auto model = solver.get_model();
        auto offsets = std::vector<scheduler_pp::lib::business::Offset>{};
        for(auto& stream: streams) {
            for(auto& link: stream.get_path()) {
                const auto offset = model.eval(frame_variables[stream.get_name()][link.get_key()].at(0));

                offsets.emplace_back(link, stream.get_name(), 0, offset.get_numeral_int());
            }
        }

        for(auto& offset: offsets) {
            std::cout << offset << std::endl;
        }
    }
    
    std::string GracuniasScheduler::name() 
    {
        return "gracunias";
    }
}
