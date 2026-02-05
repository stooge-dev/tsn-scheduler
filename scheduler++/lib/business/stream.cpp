#include "stream.h"

std::ostream& operator<<(std::ostream& out, const Stream& stream)
{
    return out << stream.name;
}