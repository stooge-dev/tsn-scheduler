#ifndef SCHEDULER_PP_LIB_BUSINESS_LINK_H
#define SCHEDULER_PP_LIB_BUSINESS_LINK_H

#include <iostream>

class Link
{
    public:
        Link(int mega_bits_per_second, int delay, int macrotick)
            : mega_bits_per_second(mega_bits_per_second), delay(delay), macrotick(macrotick) {
                bits_per_second = mega_bits_per_second * 1000 * 1000;
                bits_per_microsecond = mega_bits_per_second;
                bytes_per_microsecond = mega_bits_per_second / 8;
            };
        friend std::ostream& operator<<(std::ostream& out, const Link& link);
    private:
        const int mega_bits_per_second;
        int bits_per_second;
        int bits_per_microsecond;
        
        int bytes_per_microsecond;
        int bytes_per_second;

        int delay;
        int macrotick;
};

#endif /* SCHEDULER_PP_LIB_BUSINESS_LINK_H */