# OS Course Lab - Lab3 Debugging Task

## Task Description

Your task is to find and fix bugs in the Lab3 code located in the `context/OS-Course-Lab` directory. After fixing, the code must pass the `make grade` tests.

## Background

This is an operating system course lab project containing a buggy Lab3 implementation. You need to:

1. Analyze the code and locate the bugs
2. Fix the bugs so that the code passes `make grade` tests

## How to Run

**Important: Due to the special build environment, it is recommended to run tests inside Docker**

```bash
# Run in the current directory (mount OS-Course-Lab into the container)
docker run --rm -i --platform=linux/amd64 \
  -e LAB=3 -e TIMEOUT=20 \
  -v "$(pwd)/OS-Course-Lab:/workspaces/OS-Course-Lab" \
  -w /workspaces/OS-Course-Lab/Lab3 \
  ipads/oslab:25.03 \
  bash -lc 'set -euxo pipefail; rm -rf build; make DOCKER_RUN= V=2 grade'
```

## Project Structure

The `context/OS-Course-Lab/` directory contains the buggy Lab3 code.

## Submission Requirements

1. **Fixed code**: Save the fixed `OS-Course-Lab` directory in the current working directory (do not place it under context/)
2. **Bug analysis report**: Create a `bug_report.md` file describing the bugs found and the fix solutions

## Evaluation Method

The evaluation script will run `make grade` to verify whether the fixes are correct.
