cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(kVTube)

find_package(Geant4 REQUIRED ui_all vis_all)

include(${Geant4_USE_FILE})

include_directories(${PROJECT_SOURCE_DIR}/include 
                    ${Geant4_INCLUDE_DIR})
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

add_executable(tube tube.cc ${sources} ${headers})
target_link_libraries(tube ${Geant4_LIBRARIES})

file(GLOB MACRO_FILES
  "*.mac"
)

file(COPY ${MACRO_FILES} DESTINATION ${PROJECT_BINARY_DIR})
file(COPY ${MACRO_FILES} DESTINATION ${PROJECT_SOURCE_DIR})

#add_custom_target(kVTube DEPENDS tube)
install(TARGETS tube DESTINATION bin)



