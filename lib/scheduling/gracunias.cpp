#include <string>
#include <iostream>
#include <vector>
#include <map>
#include <format>
#include <numeric>
#include <ranges>

#include "z3++.h"

#include "gracunias.h"
#include "business/network.h"
#include "business/stream.h"

void GracuniasScheduler::schedule(Network network, std::vector<Stream> streams, int scheduled_queues) 
{
    auto config = z3::config();
    config.set("unsat_core", true);

    auto context = z3::context(config);

    int hyperperiod = 0;
    for(auto i = 1; i < streams.size(); i++) {
        hyperperiod = std::lcm(streams[i-1].get_period(), streams[i].get_period());
    }

    using FrameCountMap = std::map<std::string, int>;
    auto frame_counts = FrameCountMap{};

    using FrameMap = std::map<int, z3::expr>;
    using LinkMap = std::map<std::string, FrameMap>;
    using StreamMap = std::map<std::string, LinkMap>;
    auto frame_variables = StreamMap{};

    for(auto& stream: streams) {
        // TODO: explicit conversion, we want an int. if we did the LCM calculation correct it will be an int.
        frame_counts[stream.get_name()] = hyperperiod / stream.get_period();

        frame_variables.emplace(stream.get_name(), LinkMap{});
        for(auto& link: stream.get_path()) {
            frame_variables[stream.get_name()].emplace(link.get_key(), FrameMap{});

            auto frame_variable_name = std::format("frame_{}_stream_{}_link_{}", stream.get_name(), 0, link.get_key());
            frame_variables[stream.get_name()][link.get_key()].emplace(0, context.int_const(frame_variable_name.c_str()));
        }
    }

    auto solver = z3::solver(context);

    // TODO: frame constraints
    for(auto& stream: streams) {
        for(auto& link: stream.get_path()) {
            for(auto current_frame = 0; current_frame < frame_counts[stream.get_name()]; current_frame++) {
                const int frame_period_in_macroticks = stream.get_period() / link.get_macrotick();
            
                // i don't need todo (stream.length / (link.speed * 1000 * 1000)) / 1000 / 1000
                // 100 Mbytes per second == 100 bytes per microsecond
                const int frame_transmission_duration_in_macroticks = (stream.get_bytes() / link.get_bytes_per_microsecond()) / link.get_macrotick();
            
                solver.add( frame_variables[stream.get_name()][link.get_key()].at(current_frame) >= current_frame * frame_period_in_macroticks
                            &&
                            frame_variables[stream.get_name()][link.get_key()].at(current_frame) <= current_frame * frame_period_in_macroticks + frame_transmission_duration_in_macroticks);
            }
        }
    }

    // link constraints
    for(auto& stream1: streams) {
        for(auto& stream2: streams) {
            if(stream2.get_name() == stream1.get_name()) {
                continue;
            }

            for(auto& link_stream1: stream1.get_path()) {
                for(auto& link_stream2: stream2.get_path()) {
                    if(link_stream1.get_key() != link_stream2.get_key()) {
                        continue;
                    }

                    for(auto current_frame_stream1 = 0; current_frame_stream1 < frame_counts[stream1.get_name()]; current_frame_stream1++) {
                        for(auto current_frame_stream2 = 0; current_frame_stream2 < frame_counts[stream2.get_name()]; current_frame_stream2++) {
                            const int frame_transmission_duration_in_macroticks_stream1 = (stream1.get_bytes() / link_stream1.get_bytes_per_microsecond()) / link_stream1.get_macrotick();
                            const int frame_transmission_duration_in_macroticks_stream2 = (stream2.get_bytes() / link_stream2.get_bytes_per_microsecond()) / link_stream2.get_macrotick();

                            const int frame_period_in_macroticks_stream1 = stream1.get_period() / link_stream1.get_macrotick();
                            const int frame_period_in_macroticks_stream2 = stream2.get_period() / link_stream2.get_macrotick();

                            const int hyperperiod_stream1_stream2 = std::lcm(stream1.get_deadline(), stream2.get_deadline());

                            for(auto stream1_i = 0; stream1_i < hyperperiod_stream1_stream2 / stream1.get_period(); stream1_i++) {
                                for(auto stream2_i = 0; stream2_i < hyperperiod_stream1_stream2 / stream2.get_period(); stream2_i++) {
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

    // Stream Transmission Constraints
    for(auto& stream: streams) {
        for(auto [link1, link2]: stream.get_adjacent_link_pairs()) {
            for(auto current_frame = 0; current_frame < frame_counts[stream.get_name()]; current_frame++) {
                const int frame_transmission_duration_in_macroticks = (stream.get_bytes() / link1.get_bytes_per_microsecond()) / link1.get_macrotick();
                solver.add(frame_variables[stream.get_name()][link2.get_key()].at(current_frame) * link2.get_macrotick() - link1.get_delay() >= (frame_variables[stream.get_name()][link1.get_key()].at(current_frame) + frame_transmission_duration_in_macroticks) * link1.get_macrotick());
            }
        }
    }

    // end to end constraints
    for(auto& stream: streams) {
        for(auto current_frame = 0; current_frame < frame_counts[stream.get_name()]; current_frame++) {
            auto& src = stream.get_src();
            auto& dst = stream.get_dst();
            const int frame_transmission_duration_in_macroticks = (stream.get_bytes() / dst.get_bytes_per_microsecond()) / dst.get_macrotick();
            solver.add(frame_variables[stream.get_name()][src.get_key()].at(current_frame) * src.get_macrotick() + stream.get_deadline() >= frame_variables[stream.get_name()][dst.get_key()].at(current_frame) * dst.get_macrotick() + frame_transmission_duration_in_macroticks);
        }
    }

    // stream isolation constraints
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
    
    // TODO: queue constraints
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

    // TODO: solve
    auto result = solver.check();
    std::cout << "Result: " << result << std::endl;

    // TODO: calculate offsets 

}

std::string GracuniasScheduler::name() 
{
    return "gracunias";
}
