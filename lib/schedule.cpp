#include <memory>
#include <vector>

#include "scheduling/scheduler_base.hpp"
#include "scheduling/gracunias.hpp"

namespace scheduler_pp::lib {
    std::vector<std::unique_ptr<scheduling::SchedulerBase>> schedulers() {
        std::vector<std::unique_ptr<scheduling::SchedulerBase>> schedulerBases;
    
        std::unique_ptr<scheduling::GracuniasScheduler> gracunias = std::make_unique<scheduling::GracuniasScheduler>();
        schedulerBases.push_back(std::move(gracunias));
    
        return schedulerBases;
    }
}