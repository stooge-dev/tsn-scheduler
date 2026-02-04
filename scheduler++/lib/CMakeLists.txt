add_library(scheduler)

target_sources(scheduler
    PRIVATE
        schedule.cpp
        scheduling/gracunias.cpp
    
    PUBLIC
        FILE_SET libheaders
        TYPE HEADERS
        FILES 
            schedule.h
            scheduling/gracunias.h
            scheduling/schedule_interface.h
)