[Local Build and Run Operation Sequence]

1. Enter the workspace/submission directory
   - This directory contains the C++ source code and CMakeLists.txt that need to be modified

2. Create build directory and configure
   - Create a build directory
   - Run cmake .. to generate build files

3. Compile
   - Run make to compile
   - Generate the executable renderer

4. Run the rendering program
   - Execute ./renderer
   - The program should generate output.png

5. Result verification
   - Confirm that output.png has been generated
   - Verify the output image content is correct and readable
