#ifndef SCHEDULER_PP_LIB_BUSINESS_LINK_H
#define SCHEDULER_PP_LIB_BUSINESS_LINK_H

#include <iostream>
#include <string>

#include "node.h"

class Link
{
    public:
        // TODO: is auto generated copy-constructor enough?
        Link(Node src, Node dst, int mega_bits_per_second, int delay, int macrotick):
            src(src),
            dst(dst),
            mega_bits_per_second(mega_bits_per_second), 
            bits_per_second(mega_bits_per_second * 1000 * 1000),
            bits_per_microsecond(mega_bits_per_second),
            bytes_per_microsecond(mega_bits_per_second / 8.f), // TODO this was an implicit conversion, why?
            bytes_per_second(this->bits_per_second / 8.f),
            delay(delay), 
            macrotick(macrotick) 
        {};
        friend std::ostream& operator<<(std::ostream& out, const Link& link);
        const Node& get_src() const { return this->src; };
        const Node& get_dst() const { return this->dst; };
        std::string get_key() const { return std::string(this->get_src().get_name()) += this->get_dst().get_name(); };
        const int get_macrotick() const { return this->macrotick; };
        const float get_bytes_per_microsecond() const { return this->bytes_per_microsecond; };
        const int get_delay() const { return this->delay; };
    private:
        const Node dst;
        const Node src;

        const int mega_bits_per_second;
        const int bits_per_second;
        const int bits_per_microsecond;
        
        const float bytes_per_microsecond;
        const float bytes_per_second;

        const int delay;
        const int macrotick;
    };

#endif /* SCHEDULER_PP_LIB_BUSINESS_LINK_H */