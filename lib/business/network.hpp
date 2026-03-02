#ifndef SCHEDULER_PP_LIB_BUSINESS_NETWORK_H_
#define SCHEDULER_PP_LIB_BUSINESS_NETWORK_H_

#include <map>
#include <string>

#include "link.hpp"

namespace scheduler_pp::lib::business {
    class Network {
        private: 
            const std::string separator = ";";
            std::map<std::string, Link> network;
            std::string create_map_key(Link& link_to_create_key_for) const;
            std::string create_map_key(std::string src, std::string dst) const;
        public:
            void create_link(std::string src, std::string dst, int mega_bits_per_second, int delay, int macrotick);
            Link get_link(std::string src, std::string dst) const;
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_NETWORK_H_ */