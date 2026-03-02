#ifndef SCHEDULER_PP_LIB_BUSINESS_STREAM_H_
#define SCHEDULER_PP_LIB_BUSINESS_STREAM_H_

#include <string>
#include <vector>
#include <iostream>

#include "link.hpp"

namespace scheduler_pp::lib::business {
    class Stream
    {
        public:
            Stream(std::string name, int bytes, std::vector<Link> path, int deadline, int period)
                : name(name), bytes(bytes), path(path), deadline(deadline), period(period) {};
            const Link& dst() { return path.back(); };
            const Link& src() { return path.front(); };
            friend std::ostream& operator<<(std::ostream& out, const Stream& stream);
            const std::vector<Link>& get_path() const { return this->path; };
            const std::string& get_name() const { return this->name; };
            const int get_period() const { return this->period; };
            const int get_bytes() const { return this->bytes; };
            const int get_deadline() const { return this->deadline; };
            std::vector<std::tuple<Link, Link>> get_adjacent_link_pairs() const;
            const Link& get_dst() const { return this->path.at(this->path.size() - 1); };
            const Link& get_src() const { return this->path.at(0); };
        private:
            const std::string name;
            const int bytes;
            // orderded list of the path
            const std::vector<Link> path;
            const int deadline;
            const int period;
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_STREAM_H_ */