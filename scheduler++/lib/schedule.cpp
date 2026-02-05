#include <memory>
#include <vector>

#include "scheduling/schedule_interface.h"
#include "scheduling/gracunias.h"

std::vector<std::unique_ptr<SchedulerBase>> schedulers() {
    std::vector<std::unique_ptr<SchedulerBase>> schedulerBases;

    std::unique_ptr<GracuniasScheduler> gracunias = std::make_unique<GracuniasScheduler>();
    schedulerBases.push_back(std::move(gracunias));

    return schedulerBases;
}