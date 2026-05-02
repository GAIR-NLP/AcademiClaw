# task1
In this task, you need to read data_rgb.png and data_depth.png, and save them as two .npy point cloud files following the Sphere UFormer input format.
Before starting the coding task, please set up the environment first. If conda is not available, use .venv instead.
For data_rgb.png, save it as rgb.npy, which is a 2D array with n rows and 6 columns. Each row has the first three dimensions as unit sphere xyz coordinates, and the last three dimensions as rgb values conforming to the model input standard.
For data_depth.png, save it as depth.npy, which is a 2D array with n rows and 4 columns. Each row has the first three dimensions as unit sphere xyz coordinates, followed by the depth value conforming to the model input standard.
Note: You need to ensure the data format and applied processing are identical to the original model's default processing method. Required files such as valid_mask can be found under sphere_uformer; please locate them by examining the code yourself. You may need to use trimesh_utils.py.
The final required files for this task are: rgb.npy, depth.npy, and your export script. Please place the script under sphere_uformer/export/. When running, execute `python export/export.py` from within task1/sphere_uformer/src.
