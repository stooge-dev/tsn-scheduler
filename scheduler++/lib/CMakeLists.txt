add_library(scheduler)

target_sources(scheduler
    PRIVATE
        schedule.cpp
        scheduling/gracunias.cpp
        business/link.cpp
        business/node.cpp
        business/network.cpp 
        business/stream.cpp 
    
    PUBLIC
        FILE_SET libheaders
        TYPE HEADERS
        FILES 
            schedule.h
            scheduling/gracunias.h
            scheduling/schedule_interface.h
            business/link.h 
            business/node.h
            business/stream.h 
            business/network.h
)