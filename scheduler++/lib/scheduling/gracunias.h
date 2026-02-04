#ifndef SCHEDULER_PP_SCHEDULING_GRACUNIAS_H
#define SCHEDULER_PP_SCHEDULING_GRACUNIAS_H

#include <string>

#include "schedule_interface.h"

class GracuniasScheduler: public SchedulerBase
{
    void schedule() override;
    std::string name() override;
};

#endif /* SCHEDULER_PP_SCHEDULING_GRACUNIAS_H */