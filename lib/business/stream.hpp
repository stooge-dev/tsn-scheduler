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
            Stream(std::string name, int bytes, std::vector<Link> path, int deadline, int period, int offset_start)
                : name_(name), bytes_(bytes), path_(path), deadline_(deadline), period_(period), offset_start_(offset_start) {};
            Stream(std::string name, int bytes, std::vector<Link> path, int deadline, int period)
                : name_(name), bytes_(bytes), path_(path), deadline_(deadline), period_(period), offset_start_(0) {};
            const Link& dst() { return this->path_.back(); };
            const Link& src() { return this->path_.front(); };
            friend std::ostream& operator<<(std::ostream& out, const Stream& stream);
            const std::vector<Link>& get_path() const { return this->path_; };
            const std::string& get_name() const { return this->name_; };
            const int get_period() const { return this->period_; };
            const int get_bytes() const { return this->bytes_; };
            const int get_deadline() const { return this->deadline_; };
            const int get_offset_start() const { return this->offset_start_; };
            std::vector<std::tuple<Link, Link>> get_adjacent_link_pairs() const;
            const Link& get_dst() const { return this->path_.at(this->path_.size() - 1); };
            const Link& get_src() const { return this->path_.at(0); };
        private:
            const std::string name_;
            const int bytes_;
            // orderded list of the path
            const std::vector<Link> path_;
            const int deadline_;
            const int period_;
            const int offset_start_;
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_STREAM_H_ */