#include <iostream>

#include "offset.hpp"

namespace scheduler_pp::lib::business {
    std::ostream& operator<<(std::ostream& out, const Offset& offset)
    {
        return out << offset.stream_name_ << " on link " << offset.link_ << " frame idx: " << offset.frame_idx_ << ", value: " << offset.value_; 
    }
}