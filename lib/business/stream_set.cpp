#include "stream_set.hpp"

namespace scheduler_pp::lib::business {
    void StreamSet::create_stream(std::string name, int bytes, std::vector<std::string> path, int deadline, int period) {
        // TODO: if stream is already in set, do not add

        std::vector<scheduler_pp::lib::business::Link> path_in_network;
        for(int i = 0; i < path.size() - 1; i++) {
            auto src = path.at(i);
            auto dst = path.at(i + 1);

            path_in_network.emplace_back(this->network_.get_link(src, dst));
        }
        this->streams_.emplace_back(name, bytes, path_in_network, deadline, period);
    };

    void StreamSet::create_stream(std::string name, int bytes, std::vector<std::string> path, int deadline, int period, const int offset_start) {
        // TODO: if stream is already in set, do not add

        std::vector<scheduler_pp::lib::business::Link> path_in_network;
        for(int i = 0; i < path.size() - 1; i++) {
            auto src = path.at(i);
            auto dst = path.at(i + 1);

            path_in_network.emplace_back(this->network_.get_link(src, dst));
        }

        this->streams_.emplace_back(name, bytes, path_in_network, deadline, period, offset_start);
    };

    const int StreamSet::FrameTransmissionTimeInMicroseconds(std::string stream_name, const int frame_idx, std::string src, std::string dst) const {
        // TODO: what todo for frame idx?
        for(auto& stream: this->streams_) {
            if(stream.get_name().compare(stream_name) == 0) {
                const int bpm = this->network_.get_link(src, dst).get_bytes_per_microsecond();
                const int bytes = stream.get_bytes();

                return bytes / bpm;
            }
        }
    };
}