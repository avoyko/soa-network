cmake_minimum_required(VERSION 3.14)
project(userver-network-api CXX)

# /// [find_userver]
find_package(userver COMPONENTS core chaotic REQUIRED)
# Note: If userver was added via add_subdirectory(path/to/userver), then
# the userver_setup_environment() should be called here.
# /// [find_userver]

# /// [objects]
add_library(${PROJECT_NAME}_objs OBJECT
    src/clients/network_users_client.hpp
    src/clients/network_users_client.cpp
    src/custom/dependencies.hpp
    src/custom/dependencies.cpp
    src/fetchers/network_users.hpp
    src/fetchers/network_users.cpp
    src/handlers/users/login.hpp
    src/handlers/users/login.cpp
    src/handlers/users/signup.hpp
    src/handlers/users/signup.cpp
    src/handlers/users/profile_info.hpp
    src/handlers/users/profile_info.cpp
    src/handlers/users/update_profile.hpp
    src/handlers/users/update_profile.cpp
)
target_link_libraries(${PROJECT_NAME}_objs userver::core)
target_include_directories(${PROJECT_NAME}_objs PUBLIC src)
# /// [objects]

# /// [chaotic]
# cmake
file(GLOB_RECURSE SCHEMAS ${CMAKE_CURRENT_SOURCE_DIR}/schemas/*.yaml)
userver_target_generate_chaotic(${PROJECT_NAME}-chgen
    ARGS
        # Map '/components/schemas/*' JSONSchema types to C++ types in 'samples::hello' namespace
        -n "/components/schemas/([^/]*)/=handlers::users::{0}"
        # Generate serializers for responses
        --generate-serializers
    OUTPUT_DIR
        ${CMAKE_CURRENT_BINARY_DIR}/src
    SCHEMAS
        ${SCHEMAS}
    RELATIVE_TO
        ${CMAKE_CURRENT_SOURCE_DIR}
)
target_link_libraries(${PROJECT_NAME}_objs ${PROJECT_NAME}-chgen)
# /// [chaotic]


# /// [executable]
add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} ${PROJECT_NAME}_objs)
# /// [executable]

# /// [testsuite]
# Makes a virtualenv suitable for running pytests from `test` directory and integrates with `ctest`.
userver_testsuite_add_simple()
# /// [testsuite]
