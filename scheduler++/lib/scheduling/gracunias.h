#ifndef SCHEDULER_PP_SCHEDULING_GRACUNIAS_H
#define SCHEDULER_PP_SCHEDULING_GRACUNIAS_H

#include <string>
#include <vector>

#include "schedule_interface.h"
#include "business/network.h"
#include "business/stream.h"

class GracuniasScheduler: public SchedulerBase
{
    void schedule(Network network, std::vector<Stream> streams, int scheduled_queues = 8) override;
    std::string name() override;
};

#endif /* SCHEDULER_PP_SCHEDULING_GRACUNIAS_H */