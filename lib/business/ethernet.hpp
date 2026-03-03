#ifndef SCHEDULER_PP_LIB_BUSINESS_ETHERNET_H_
#define SCHEDULER_PP_LIB_BUSINESS_ETHERNET_H_

namespace scheduler_pp::lib::business {
    constexpr auto kEthernetMTUSizeInBytes = 1500;
    constexpr auto kMaxEthernetFrameSizeInBytes = kEthernetMTUSizeInBytes + 18;
}

#endif /* SCHEDULER_PP_LIB_BUSINESS_ETHERNET_H_ */