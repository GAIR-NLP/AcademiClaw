# Query: Configure Compatible Python Project Environment

## [Query Description]
Dependency management and environment configuration for Python projects is one of the most common yet challenging issues in daily development work. Package version conflicts, environment inconsistencies, and platform compatibility issues frequently cause projects to behave differently across environments.

**Task Background**: During software development, environment configuration problems are frequently encountered: new team members cannot quickly set up development environments, environments are inconsistent across different machines, and project dependency version conflicts arise. These common Python environment dependency issues need to be resolved.

**Task Objective**: Resolve the Python environment dependency issues for the target project, ensuring the project can run properly in a new environment.

**Recommended Technical Approach**: Use Docker containerization technology by writing a Dockerfile script to create a reproducible runtime environment. Docker can package applications and their dependencies into a lightweight, portable container, ensuring consistent runtime behavior across different environments.

**Expected Input**: A Python project.

**Specific Requirements**:
1. **Project Analysis**: Analyze the Python project's dependency configuration and runtime requirements
2. **Base Image Selection**: Choose an appropriate Python base image based on project needs
3. **Environment Configuration**: Configure the Python environment and system dependencies within the container
4. **Dependency Installation**: Install the required Python packages in the Dockerfile

**Expected Output**: A runnable Dockerfile script that can successfully configure the environment required by the input project.

## [Context]

We **recommend** using any open-source project from GitHub to complete the task. We also provide a project source code for your use.

File list:
- `context/VARSTok/` - VARSTok speech synthesis project directory
  - `README.md` - Project documentation
  - `requirements.txt` - Python dependency package list
  - `run.sh` - Run script
  - `train.py` - Training script
  - `infer.py` - Inference script
  - `configs/` - Model configuration files
  - `encoder/` - Encoder module (including speech feature extraction, etc.)
  - `decoder/` - Decoder module (including acoustic model, etc.)
  - `metrics/` - Evaluation metrics module

- `environment_requirements.md` - Specific environment configuration requirements
