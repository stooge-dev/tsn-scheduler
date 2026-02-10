#include <iostream>

#include "subnet.h"
#include "scheduling/gracunias.h"


namespace scheduler_pp::experiments::subnet {
    int main(int argc, char** argv) {
        auto scheduler = GracuniasScheduler{};
        
        // TODO: make call correct
        scheduler.schedule();

        return 0;
    }
}