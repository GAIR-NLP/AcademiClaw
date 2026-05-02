cmake_minimum_required(VERSION 3.10)  
project(Renderer)  
  
set(CMAKE_CXX_STANDARD 17)  
  
add_executable(renderer main.cpp Object.hpp Vector.cpp Vector.hpp Sphere.hpp global.hpp Triangle.hpp Scene.cpp  
        Scene.hpp Light.hpp AreaLight.hpp BVH.cpp BVH.hpp Bounds3.hpp Ray.hpp Material.hpp Intersection.hpp  
        Renderer.cpp Renderer.hpp)  
  
# Ensure models are available at runtime (../models relative to build dir)  
file(COPY ${CMAKE_SOURCE_DIR}/models DESTINATION ${CMAKE_BINARY_DIR}/..)  
