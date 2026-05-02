Goal: Write a reproducible Dockerfile to provide a consistent runnable environment for `context/VARSTok/`.

Minimum requirements:
- Explicitly choose a Python base image version (3.10+ recommended) and ensure `python`/`pip` are available
- Set a working directory and copy VARSTok project files into the image
- Install dependencies from `context/VARSTok/requirements.txt`

Verification suggestions (choose one or combine):
- Image builds successfully: `docker build .`
- Container can import key modules: `python -c "import torch, numpy"` (based on actual project dependencies)
- Can run project entry scripts or example commands (refer to `context/VARSTok/README.md` / `run.sh`)
