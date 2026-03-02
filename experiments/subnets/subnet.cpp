#include <iostream>

#include "subnet.hpp"
#include "scheduling/gracunias.hpp"
#include "business/link.hpp"
#include "business/stream.hpp"

namespace scheduler_pp::experiments::subnet {
    int main(int argc, char** argv) {
        auto scheduler = scheduler_pp::lib::scheduling::GracuniasScheduler{};
        auto network = scheduler_pp::lib::business::Network{};

        // TODO: schedule XYZ in one big network
        network.create_link("A", "B", 100, 0, 1);
        network.create_link("B", "A", 100, 0, 1);
        network.create_link("B", "D", 100, 0, 1);
        network.create_link("D", "B", 100, 0, 1);
        network.create_link("D", "C", 100, 0, 1);
        network.create_link("C", "D", 100, 0, 1);

        network.create_link("B", "E", 100, 0, 1);
        network.create_link("E", "G", 100, 0, 1);
        network.create_link("G", "F", 100, 0, 1);
        network.create_link("F", "D", 100, 0, 1);

        network.create_link("G", "H", 100, 0, 1);
        network.create_link("H", "G", 100, 0, 1);
        network.create_link("G", "J", 100, 0, 1);
        network.create_link("J", "G", 100, 0, 1);

        auto streamSet = scheduler_pp::lib::business::StreamSet{network};

        streamSet.create_stream("video", 1000, {"A", "B", "E", "G", "H"}, 1000, 1000);
        streamSet.create_stream("command", 1000, {"A", "B", "E", "G", "H"}, 1000, 1000);
        
        /** schedule XYZ **/
        scheduler.schedule(streamSet);

        // TODO: schedule Z
        auto networkZ = scheduler_pp::lib::business::Network{};
        networkZ.create_link("B", "E", 100, 0, 1);
        networkZ.create_link("E", "G", 100, 0, 1);
        networkZ.create_link("G", "F", 100, 0, 1);
        networkZ.create_link("F", "D", 100, 0, 1);

        // TODO: define streamSet for Z
        auto streamSetZ = scheduler_pp::lib::business::StreamSet{networkZ};

        // TODO: get offsets
        // TODO: make offsets limits for streams in X and Y
        // TODO: schedule X and Y
        auto networkX = scheduler_pp::lib::business::Network{};
        networkX.create_link("A", "B", 100, 0, 1);
        networkX.create_link("B", "A", 100, 0, 1);
        networkX.create_link("B", "D", 100, 0, 1);
        networkX.create_link("D", "B", 100, 0, 1);
        networkX.create_link("D", "C", 100, 0, 1);
        networkX.create_link("C", "D", 100, 0, 1);

        auto streamSetX = scheduler_pp::lib::business::StreamSet{networkX};

        auto networkY = scheduler_pp::lib::business::Network{};
        networkY.create_link("G", "H", 100, 0, 1);
        networkY.create_link("H", "G", 100, 0, 1);
        networkY.create_link("G", "J", 100, 0, 1);
        networkY.create_link("J", "G", 100, 0, 1);
  
        auto streamSetY = scheduler_pp::lib::business::StreamSet{networkY};
        

        return 0;
    }
}