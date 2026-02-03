add_executable(scheduler_cli)

target_sources(scheduler_cli PRIVATE main.cpp)

target_link_libraries(scheduler_cli PRIVATE scheduler)