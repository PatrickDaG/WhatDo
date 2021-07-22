# vim: set ts=4 sw=4 sts=-1 noet:
# Set minimum required cmake version
cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

# Set module path
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
	"${CMAKE_CURRENT_SOURCE_DIR}/cmake")

# ---- Project ----
project(WhatDo VERSION 0.0.1 LANGUAGES CXX)

# ---- Fetch CPM ----
set(CPM_DOWNLOAD_VERSION 0.27.2)
set(CPM_DOWNLOAD_LOCATION "${CMAKE_BINARY_DIR}/cmake/CPM_${CPM_DOWNLOAD_VERSION}.cmake")

if(NOT (EXISTS ${CPM_DOWNLOAD_LOCATION}))
	message(STATUS "Downloading CPM.cmake v${CPM_DOWNLOAD_VERSION}")
	file(DOWNLOAD https://github.com/TheLartians/CPM.cmake/releases/download/v${CPM_DOWNLOAD_VERSION}/CPM.cmake ${CPM_DOWNLOAD_LOCATION})
endif()

include(${CPM_DOWNLOAD_LOCATION})

# ---- Add dependencies via CPM ----
# See https://github.com/TheLartians/CPM.cmake for details and examples

CPMAddPackage(
    NAME magic_enum
    GITHUB_REPOSITORY Neargye/magic_enum
	VERSION 0.7.2
)

CPMAddPackage(
	NAME cpr
	GITHUB_REPOSITORY whoshuu/cpr
	GIT_TAG 1.5.2
)

CPMAddPackage(
  NAME fmt
  GITHUB_REPOSITORY fmtlib/fmt
  GIT_TAG 7.1.3
)

CPMAddPackage(
  NAME json
  GITHUB_REPOSITORY nlohmann/json
  VERSION 3.9.1
  OPTIONS "JSON_BuildTests Off"
	"JSON_Install Off"
)

# ---- Create executable ----

include(FindCompilerFlags)

# List of library sources
set(SOURCES
	src/main.cpp
)

add_executable(WhatDo src/main.cpp src/cli.cpp src/util.cpp)
target_include_directories(WhatDo PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_compile_features(WhatDo PUBLIC cxx_std_20)
target_compile_options(WhatDo PRIVATE ${CXXFLAGS_PEDANTIC_COMPILE_FLAGS})
target_link_libraries(WhatDo fmt::fmt nlohmann_json::nlohmann_json cpr::cpr magic_enum::magic_enum)
