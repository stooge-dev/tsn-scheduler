#ifndef SCHEDULER_PP_LIB_BUSINESS_SCHEDULING_GRACUNIAS_H_
#define SCHEDULER_PP_LIB_BUSINESS_SCHEDULING_GRACUNIAS_H_

#include <string>
#include <vector>

#include "scheduler_base.hpp"
#include "business/stream_set.hpp"

namespace scheduler_pp::lib::scheduling {
    class GracuniasScheduler: public SchedulerBase
    {
        public:
            void schedule(scheduler_pp::lib::business::StreamSet streamSet, int scheduled_queues = 8) override;
            std::string name() override;
    };
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_SCHEDULING_GRACUNIAS_H_ */