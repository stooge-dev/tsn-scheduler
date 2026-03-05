#ifndef SCHEDULER_PP_LIB_BUSINESS_STREAM_SET_H_
#define SCHEDULER_PP_LIB_BUSINESS_STREAM_SET_H_

#include <cstddef>

#include "network.hpp"
#include "stream.hpp"

namespace scheduler_pp::lib::business {
    class StreamSet {
        private:
            Network network_;
            std::vector<Stream> streams_;
        public:
            StreamSet(Network network): network_(network) {};
            void create_stream(std::string name, int bytes, std::vector<std::string> path, int deadline, int period);
            void create_stream(std::string name, int bytes, std::vector<std::string> path, int deadline, int period, const int offset_start);
            const std::vector<Stream>& get_streams() const { return this->streams_; };
            const int FrameTransmissionTimeInMicroseconds(std::string stream_name, const int frame_idx, std::string src, std::string dst) const;
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_STREAM_SET_H_ */