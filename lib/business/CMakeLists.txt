target_sources(scheduler
    PRIVATE
        link.cpp
        stream.cpp
        network.cpp
        stream_set.cpp
        offset.cpp
    
    PUBLIC
        FILE_SET libheaders
        TYPE HEADERS
        FILES 
           link.hpp
            stream.hpp 
            network.hpp
            stream_set.hpp
            offset.hpp
)