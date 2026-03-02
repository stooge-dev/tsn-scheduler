#ifndef SCHEDULER_PP_LIB_SCHEDULE_H_
#define SCHEDULER_PP_LIB_SCHEDULE_H_

#include <vector>
#include <memory>

#include "scheduling/scheduler_base.hpp"

namespace scheduler_pp::lib {
    std::vector<std::unique_ptr<scheduling::SchedulerBase>> schedulers();
}

#endif /* SCHEDULER_PP_LIB_SCHEDULE_H_ */