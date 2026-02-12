#ifndef SCHEDULER_PP_LIB_BUSINESS_NETWORK_H
#define SCHEDULER_PP_LIB_BUSINESS_NETWORK_H

#include <vector>
#include <iostream>
#include "link.h"

class Network 
{
    public:
        Network(std::vector<Link> links): links(links) {};
        friend std::ostream& operator<<(std::ostream& out, const Network& network);
    private:
        const std::vector<Link> links;
};

#endif /* SCHEDULER_PP_LIB_BUSINESS_NETWORK_H */