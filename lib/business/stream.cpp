#include <iostream>
#include <vector>
#include <tuple>

#include "stream.hpp"
#include "link.hpp"

namespace scheduler_pp::lib::business {
    std::ostream& operator<<(std::ostream& out, const Stream& stream)
    {
        return out << stream.name;
    }
    
    std::vector<std::tuple<Link, Link>> Stream::get_adjacent_link_pairs() const {
        auto alp = std::vector<std::tuple<Link, Link>>{};
    
        for(auto current_idx = 0; current_idx < this->path.size() - 1; current_idx++) {
            auto link1 = this->path[current_idx];
            auto link2 = this->path[current_idx + 1];
    
            alp.push_back(std::make_tuple(link1, link2));
        }
    
        return alp;
    }
}