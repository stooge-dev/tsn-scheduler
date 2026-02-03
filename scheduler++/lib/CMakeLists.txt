add_library(scheduler)

target_sources(scheduler
    PRIVATE
        schedule.cpp
    
    PUBLIC
        FILE_SET libheaders
        TYPE HEADERS
        FILES 
            schedule.h
)