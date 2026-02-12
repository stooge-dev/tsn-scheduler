#ifndef SCHEDULER_PP_LIB_BUSINESS_NODE_H
#define SCHEDULER_PP_LIB_BUSINESS_NODE_H

#include <string>
#include <iostream>

//enum class NodeType { Endsystem, Switch };

class Node 
{
    private:
        const std::string name;
        //const NodeType type;
    public:
        Node(std::string name)
            : name(name) {};
        friend std::ostream& operator<<(std::ostream& out, const Node& node);
        std::string get_name() const { return this->name; };
};

#endif /* SCHEDULER_PP_LIB_BUSINESS_NODE_H */