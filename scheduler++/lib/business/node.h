#ifndef SCHEDULER_PP_LIB_BUSINESS_NODE_H
#define SCHEDULER_PP_LIB_BUSINESS_NODE_H

#include <string>
#include <iostream>

enum class NodeType { Endsystem, Switch };

class Node 
{
    public:
        Node(std::string name, NodeType type)
            : name(name), type(type) {}
        friend std::ostream& operator<<(std::ostream& out, const Node& node);
    private:
        const std::string name;
        const NodeType type;
};

#endif /* SCHEDULER_PP_LIB_BUSINESS_NODE_H */