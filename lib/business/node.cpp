#include "node.h"
#include <iostream>

std::ostream& operator<<(std::ostream& out, const Node& node) {
    return out << node.name;
}