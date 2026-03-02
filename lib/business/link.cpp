#include <iostream>

#include "link.hpp"

namespace scheduler_pp::lib::business {
    std::ostream& operator<<(std::ostream& out, const Link& link) {
        return out << link.mega_bits_per_second;
    }
}