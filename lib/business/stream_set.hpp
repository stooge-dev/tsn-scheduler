#ifndef SCHEDULER_PP_LIB_BUSINESS_STREAM_SET_H_
#define SCHEDULER_PP_LIB_BUSINESS_STREAM_SET_H_

#include <cstddef>

#include "network.hpp"
#include "stream.hpp"

namespace scheduler_pp::lib::business {
    class StreamSet {
        private:
            Network network;
            std::vector<Stream> streams;
        public:
            StreamSet(Network network): network(network) {};
            void create_stream(std::string name, int bytes, std::vector<std::string> path, int deadline, int period);
            const std::vector<Stream>& get_streams() const { return this->streams; };
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_STREAM_SET_H_ */