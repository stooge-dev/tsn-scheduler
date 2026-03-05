#ifndef SCHEDULER_PP_LIB_BUSINESS_OFFSET_H_
#define SCHEDULER_PP_LIB_BUSINESS_OFFSET_H_

#include "link.hpp"

namespace scheduler_pp::lib::business {
    class Offset {
        private:
            const Link link_;
            const std::string stream_name_;
            const int frame_idx_;
            const int value_;
        public:
            Offset(Link link, std::string stream_name, int frame_idx, int value): 
                link_(link), stream_name_(stream_name), frame_idx_(frame_idx), value_(value) {};
            friend std::ostream& operator<<(std::ostream& out, const Offset& offset);
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_OFFSET_H_ */