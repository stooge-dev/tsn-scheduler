add_executable(scheduler_cli)

target_sources(scheduler_cli PRIVATE main.cpp)

target_link_libraries(scheduler_cli PRIVATE scheduler)

include(FetchContent)
FetchContent_Declare(CLI11
    GIT_REPOSITORY  https://github.com/CLIUtils/CLI11
    GIT_TAG         bfffd37e1f804ca4fae1caae106935791696b6a9 #v2.6.1
)
FetchContent_MakeAvailable(CLI11)

target_link_libraries(scheduler_cli PRIVATE CLI11::CLI11)