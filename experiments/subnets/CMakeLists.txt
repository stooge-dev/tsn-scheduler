add_executable(subnets)

target_sources(subnets 
    PRIVATE 
        subnet.cpp
)

target_link_libraries(subnets PRIVATE scheduler)