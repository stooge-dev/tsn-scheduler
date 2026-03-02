add_library(scheduler)

target_sources(scheduler
    PRIVATE
        schedule.cpp
        scheduling/gracunias.cpp
        business/link.cpp
        business/stream.cpp
        business/network.cpp
        business/stream_set.cpp
    
    PUBLIC
        FILE_SET libheaders
        TYPE HEADERS
        FILES 
            schedule.hpp
            scheduling/gracunias.hpp
            scheduling/scheduler_base.hpp
            business/link.hpp
            business/stream.hpp 
            business/network.hpp
            business/stream_set.hpp
)

include(FetchContent)
FetchContent_Declare(Z3
        GIT_REPOSITORY https://github.com/Z3Prover/z3
        GIT_TAG        z3-4.15.3
)
FetchContent_MakeAvailable(Z3)

# Add the C++ API include directory for z3++.h
if(TARGET libz3)
    target_include_directories(libz3 INTERFACE
        $<BUILD_INTERFACE:${z3_SOURCE_DIR}/src/api/c++>
    )
endif()

target_link_libraries(scheduler PRIVATE libz3)