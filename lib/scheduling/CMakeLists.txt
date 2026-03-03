target_sources(scheduler
    PRIVATE
        gracunias.cpp
    
    PUBLIC
        FILE_SET libheaders
        TYPE HEADERS
        FILES 
            gracunias.hpp
            scheduler_base.hpp
)