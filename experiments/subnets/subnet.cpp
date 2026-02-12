#include <iostream>

#include "subnet.h"
#include "scheduling/gracunias.h"
#include "business/network.h"
#include "business/link.h"
#include "business/node.h"
#include "business/stream.h"

namespace scheduler_pp::experiments::subnet {
    int main(int argc, char** argv) {
        auto scheduler = GracuniasScheduler{};

        auto nodeA = Node{"A"};
        auto nodeB = Node{"B"};
        auto nodeC = Node{"C"};
        auto nodeD = Node{"D"};
        auto nodeE = Node{"E"};
        auto nodeF = Node{"F"};
        auto nodeG = Node{"G"};
        auto nodeH = Node{"H"};
        auto nodeJ = Node{"J"};

        // TODO: schedule XYZ in one big network
        auto linksFull = std::vector<Link>{};
        linksFull.emplace_back(nodeA, nodeB, 100, 0, 1);
        linksFull.emplace_back(nodeB, nodeA, 100, 0, 1);
        linksFull.emplace_back(nodeB, nodeD, 100, 0, 1);
        linksFull.emplace_back(nodeD, nodeB, 100, 0, 1);
        linksFull.emplace_back(nodeD, nodeC, 100, 0, 1);
        linksFull.emplace_back(nodeC, nodeD, 100, 0, 1);

        linksFull.emplace_back(nodeB, nodeE, 100, 0, 1);
        linksFull.emplace_back(nodeE, nodeG, 100, 0, 1);
        linksFull.emplace_back(nodeG, nodeF, 100, 0, 1);
        linksFull.emplace_back(nodeF, nodeD, 100, 0, 1);
        
        linksFull.emplace_back(nodeG, nodeH, 100, 0, 1);
        linksFull.emplace_back(nodeH, nodeG, 100, 0, 1);
        linksFull.emplace_back(nodeG, nodeJ, 100, 0, 1);
        linksFull.emplace_back(nodeJ, nodeG, 100, 0, 1);

        auto networkFull = Network{linksFull};

        auto streamsFull = std::vector<Stream>{};
        auto streamPathVideo = std::vector<Link>{};
        streamPathVideo.emplace_back(linksFull.at(0));
        streamPathVideo.emplace_back(linksFull.at(6));
        streamPathVideo.emplace_back(linksFull.at(7));
        streamPathVideo.emplace_back(linksFull.at(10));
        streamsFull.emplace_back("video", 1000, streamPathVideo, 1000, 1000);

        auto streamPathCommand = std::vector<Link>{};
        streamPathCommand.emplace_back(linksFull.at(0));
        streamPathCommand.emplace_back(linksFull.at(6));
        streamPathCommand.emplace_back(linksFull.at(7));
        streamsFull.emplace_back("command", 1000, streamPathCommand, 1000, 1000);
        
        scheduler.schedule(networkFull, streamsFull);

        auto linksZ = std::vector<Link>{};
        linksZ.emplace_back(nodeB, nodeE, 100, 0, 1);
        linksZ.emplace_back(nodeE, nodeG, 100, 0, 1);
        linksZ.emplace_back(nodeG, nodeF, 100, 0, 1);
        linksZ.emplace_back(nodeF, nodeD, 100, 0, 1);

        auto streamsZ = std::vector<Stream>{};

        
        
        
        // TODO: schedule Z
        // scheduler.schedule();

        // TODO: get offsets
        // TODO: make offsets limits for streams in X and Y
        // TODO: schedule X and Y

        auto linksX = std::vector<Link>{};
        linksX.emplace_back(nodeA, nodeB, 100, 0, 1);
        linksX.emplace_back(nodeB, nodeA, 100, 0, 1);
        linksX.emplace_back(nodeB, nodeD, 100, 0, 1);
        linksX.emplace_back(nodeD, nodeB, 100, 0, 1);
        linksX.emplace_back(nodeC, nodeD, 100, 0, 1);
        linksX.emplace_back(nodeC, nodeD, 100, 0, 1);

        auto streamsX = std::vector<Stream>{};
        auto linksY = std::vector<Link>{};
        linksY.emplace_back(nodeH, nodeG, 100, 0, 1);
        linksY.emplace_back(nodeG, nodeH, 100, 0, 1);
        linksY.emplace_back(nodeJ, nodeG, 100, 0, 1);
        linksY.emplace_back(nodeG, nodeJ, 100, 0, 1);

        auto streamsY = std::vector<Stream>{};

        

        return 0;
    }
}