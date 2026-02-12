#include <iostream>

#include "link.h"

std::ostream& operator<<(std::ostream& out, const Link& link) {
    return out << link.mega_bits_per_second;
}