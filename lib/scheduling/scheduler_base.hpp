#ifndef SCHEDULER_PP_LIB_BUSINESS_SCHEDULING_SCHEDULER_BASE_H_
#define SCHEDULER_PP_LIB_BUSINESS_SCHEDULING_SCHEDULER_BASE_H_

#include <string>

#include "business/stream_set.hpp"

namespace scheduler_pp::lib::scheduling {
    /**
     * Implementing classes MUST have no scheduling state,
     * rather only configuration state. Such that multiple
     * calls to schedule(...) work regardless of e.g. order.
     */
    class SchedulerBase
    {
        public:
            virtual std::string name() = 0;
            virtual void schedule(scheduler_pp::lib::business::StreamSet streamSet, int scheduled_queues = 8) = 0;
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_SCHEDULING_SCHEDULER_BASE_H_ */