#ifndef SCHEDULER_PP_SCHEDULING_SCHEDULE_INTERFACE_H
#define SCHEDULER_PP_SCHEDULING_SCHEDULE_INTERFACE_H

#include <string>

class SchedulerBase
{
    public:
        virtual std::string name() = 0;
        virtual void schedule() = 0;
};

#endif /* SCHEDULER_PP_SCHEDULING_SCHEDULE_INTERFACE_H */