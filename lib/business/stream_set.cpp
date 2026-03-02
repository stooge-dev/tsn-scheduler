#include "stream_set.hpp"

namespace scheduler_pp::lib::business {
    void StreamSet::create_stream(std::string name, int bytes, std::vector<std::string> path, int deadline, int period) {
        std::vector<scheduler_pp::lib::business::Link> path_in_network;
        for(int i = 0; i < path.size() - 1; i++) {
            auto src = path.at(i);
            auto dst = path.at(i + 1);

            path_in_network.emplace_back(this->network.get_link(src, dst));
        }
        this->streams.emplace_back(name, bytes, path_in_network, deadline, period);
    };
}