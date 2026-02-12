#ifndef SCHEDULER_PP_SCHEDULING_SCHEDULE_INTERFACE_H
#define SCHEDULER_PP_SCHEDULING_SCHEDULE_INTERFACE_H

#include <string>
#include <vector>

#include "business/network.h"
#include "business/stream.h"

class SchedulerBase
{
    public:
        virtual std::string name() = 0;
        virtual void schedule(Network network, std::vector<Stream> streams, int scheduled_queues = 8) = 0;
};

#endif /* SCHEDULER_PP_SCHEDULING_SCHEDULE_INTERFACE_H */