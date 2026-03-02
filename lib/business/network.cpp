#include "network.hpp"

namespace scheduler_pp::lib::business {
    void Network::create_link(std::string src, std::string dst, int mega_bits_per_second, int delay, int macrotick) {
        auto newLink = Link{src, dst, mega_bits_per_second, delay, macrotick};
        this->network.emplace(this->create_map_key(newLink), newLink);
    }

    std::string Network::create_map_key(Link& link) const {
        return this->create_map_key(link.get_src(), link.get_dst());
    }

    std::string Network::create_map_key(std::string src, std::string dst) const {
        auto key = src;
        key.append(this->separator);
        key.append(dst);

        return key;
    }

    Link Network::get_link(std::string src, std::string dst) const {
        return network.at(this->create_map_key(src, dst));
    }
}