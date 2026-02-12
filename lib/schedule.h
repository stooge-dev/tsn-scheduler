#ifndef SCHEDULER_PP_SCHEDULE_H
#define SCHEDULER_PP_SCHEDULE_H

#include <vector>
#include <memory>

#include "scheduling/schedule_interface.h"

std::vector<std::unique_ptr<SchedulerBase>> schedulers();

#endif /* SCHEDULER_PP_SCHEDULE_H */