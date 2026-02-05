#ifndef SCHEDULER_PP_LIB_BUSINESS_STREAM_H
#define SCHEDULER_PP_LIB_BUSINESS_STREAM_H

#include <string>
#include <vector>
#include <iostream>
#include "link.h"

class Stream
{
    public:
        Stream(std::string name, int bytes, std::vector<Link> path, int deadline, int period)
            : name(name), bytes(bytes), path(path), deadline(deadline), period(period) {};
        const Link& dst() { return path.back(); }
        const Link& src() { return path.front(); }
        friend std::ostream& operator<<(std::ostream& out, const Stream& stream);
    private:
        const std::string name;
        const int bytes;
        // orderded list of the path
        const std::vector<Link> path;
        const int deadline;
        const int period;
};

#endif /* SCHEDULER_PP_LIB_BUSINESS_STREAM_H */