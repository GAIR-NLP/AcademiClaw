#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rubric for dengjianbin-query1: Robocasa Camera Movement Implementation

Total score: 100 points, allocated across the following dimensions:

1. File Delivery (15 points)
   - Python example script exists (5)
   - Functionality documentation exists (5)
   - Camera trajectory video exists (5)

2. Code Quality (25 points)
   - Syntax correctness (5)
   - MuJoCo camera API usage (8)
   - Base frame coordinate transform logic (8)
   - Rendering and video generation code (4)

3. Functional Correctness (30 points)
   - Dynamic camera pose setting (10) -- update at each step in loop
   - Base frame absolute coordinate scheme (10) -- base-to-world transform
   - Environment creation and rendering pipeline (10) -- robosuite.make, offscreen, step

4. Documentation Quality (20 points)
   - Format and structure (5) -- deterministic check
   - Content completeness (15) -- LLM-as-Judge

5. Video Output (10 points)
   - File validity (5)
   - Format and quality (5)
"""

from __future__ import annotations

import ast
import glob as glob_mod
import json
import os
import re
import struct
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# ============================================================================
# Environment Configuration / LLM Tools
# ============================================================================

def _load_env(answer_dir: str) -> dict:
    """Load .env configuration from answer_dir and query root directory"""
    values: Dict[str, str] = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        if k.strip() not in values:
                            values[k.strip()] = v.strip().strip("'\"")
            except Exception:
                pass
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    """Get text evaluation LLM configuration"""
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
    """Call LLM for text evaluation"""
    if not openai or not config.get("api_key"):
        return ""
    try:
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge call failed: {e}")
        return ""


# ============================================================================
# Helper Functions
# ============================================================================

def _read_file(filepath: str) -> str:
    """Safely read file text content"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def _find_files(directory: str, extensions: List[str]) -> List[str]:
    """Recursively find files with specified extensions in a directory"""
    results = []
    for ext in extensions:
        results.extend(glob_mod.glob(os.path.join(directory, f"*.{ext}")))
        results.extend(
            glob_mod.glob(os.path.join(directory, f"**/*.{ext}"), recursive=True)
        )
    return sorted(set(results))


def _file_size(filepath: str) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(filepath)
    except Exception:
        return 0


def _collect_py_code(answer_dir: str) -> Tuple[List[str], str]:
    """Collect all Python file paths and concatenated source code"""
    py_files = _find_files(answer_dir, ["py"])
    all_code = ""
    for pf in py_files:
        all_code += _read_file(pf) + "\n"
    return py_files, all_code


# ============================================================================
# 1. File Delivery (15 points)
# ============================================================================

def _check_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    py_files = _find_files(answer_dir, ["py"])
    md_files = _find_files(answer_dir, ["md"])
    video_files = _find_files(answer_dir, ["mp4", "avi", "mov", "mkv", "webm"])

    # Filter out md files from the robocasa repo (agent may have cloned the robocasa repo)
    own_md = [
        f
        for f in md_files
        if "/robocasa/" not in f.replace("\\", "/")
        and "/robosuite/" not in f.replace("\\", "/")
    ]

    # 1a. Python script (5 points)
    if py_files:
        score += 5
        details["python_script"] = f"5/5 -- Found {len(py_files)} .py file(s)"
    else:
        details["python_script"] = "0/5 -- No Python scripts found"
        deductions.append("Missing Python example script")

    # 1b. Markdown documentation (5 points)
    if own_md:
        score += 5
        details["markdown_doc"] = f"5/5 -- Found {len(own_md)} .md file(s)"
    else:
        details["markdown_doc"] = "0/5 -- No functionality documentation found"
        deductions.append("Missing functionality documentation (.md)")

    # 1c. Video file (5 points)
    valid_videos = [v for v in video_files if _file_size(v) >= 1024]
    if valid_videos:
        score += 5
        details["video_file"] = f"5/5 -- Found {len(valid_videos)} valid video file(s)"
    elif video_files:
        score += 2
        details["video_file"] = "2/5 -- Video file exists but is smaller than 1KB"
        deductions.append("Video file may be invalid (<1KB)")
    else:
        details["video_file"] = "0/5 -- No video files found"
        deductions.append("Missing camera trajectory video (.mp4)")

    return score, {
        "score": score,
        "max": 15,
        "details": details,
        "deductions": deductions,
    }


# ============================================================================
# 2. Code Quality (25 points)
# ============================================================================

def _check_code_quality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    py_files, all_code = _collect_py_code(answer_dir)
    if not py_files:
        return 0, {
            "score": 0,
            "max": 25,
            "details": {"error": "No Python files"},
            "deductions": ["No code to evaluate"],
        }

    # 2a. Syntax correctness (5 points)
    syntax_ok = True
    for pf in py_files:
        content = _read_file(pf)
        if not content.strip():
            continue
        try:
            ast.parse(content)
        except SyntaxError as e:
            syntax_ok = False
            details["syntax_error"] = f"{os.path.basename(pf)}: {str(e)[:120]}"
            deductions.append(f"Syntax error: {os.path.basename(pf)}")
            break

    if syntax_ok:
        score += 5
        details["syntax"] = "5/5 -- All scripts have valid syntax"
    else:
        details["syntax"] = "0/5 -- Syntax errors found"

    # 2b. MuJoCo camera API usage (8 points)
    api_score = 0

    # cam_pos / cam_mat0 / cam_quat (core MuJoCo camera model attributes)
    if re.search(r"cam_pos|cam_mat0|cam_quat", all_code):
        api_score += 4
        details["mujoco_cam_attrs"] = "Uses MuJoCo camera model attributes"
    elif re.search(r"camera.*pos|camera.*quat|camera.*config", all_code, re.I):
        api_score += 2
        details["mujoco_cam_attrs"] = "Has camera pose related code but does not directly use cam_pos/cam_mat0"
    else:
        deductions.append("Does not use MuJoCo camera model attributes (cam_pos/cam_mat0)")

    # sim.model / sim.data / env.sim
    if re.search(r"sim\.model|sim\.data|env\.sim", all_code):
        api_score += 4
        details["sim_access"] = "Correctly uses sim.model/sim.data interfaces"
    elif re.search(r"mujoco|MujocoEnv|mujoco_py", all_code, re.I):
        api_score += 2
        details["sim_access"] = "Mentions MuJoCo but does not directly operate on sim object"
    else:
        deductions.append("Does not use sim.model/sim.data interfaces")

    score += api_score
    details["mujoco_api"] = f"{api_score}/8"

    # 2c. Base frame coordinate transform logic (8 points)
    base_score = 0

    has_base_ref = bool(
        re.search(
            r"base.*frame|base.*body|robot.*base|base_body|robot0_base|base_pos|base_rot|base_mat",
            all_code,
            re.I,
        )
    )
    has_transform = bool(
        re.search(
            r"quat_to_mat|mat.*mul|mat.*vec|euler_to_quat|transforms3d|"
            r"pyquaternion|rotmat|rotation.*matrix|quat_to_mat3|mat3_mul|mat3_vec",
            all_code,
            re.I,
        )
    )
    has_coord_convert = bool(
        re.search(
            r"pos_in_base|quat_in_base|cam_pos_b|pos_w|world.*pos|xpos|xmat",
            all_code,
            re.I,
        )
    )

    if has_base_ref:
        base_score += 3
    else:
        deductions.append("Does not reference robot base frame")

    if has_transform:
        base_score += 3
    else:
        deductions.append("Missing coordinate/rotation transform logic")

    if has_coord_convert:
        base_score += 2

    score += base_score
    details["base_frame_transform"] = f"{base_score}/8"

    # 2d. Rendering and video generation code (4 points)
    render_score = 0
    has_render = bool(
        re.search(r"sim\.render|\.render\(|render_rgb|offscreen|get_image", all_code)
    )
    has_video_write = bool(
        re.search(
            r"imageio|cv2\.VideoWriter|ffmpeg|moviepy|get_writer",
            all_code,
            re.I,
        )
    )

    if has_render:
        render_score += 2
    else:
        deductions.append("No offscreen rendering call implemented")

    if has_video_write:
        render_score += 2
    else:
        deductions.append("No video writing logic implemented")

    score += render_score
    details["rendering_code"] = f"{render_score}/4"

    return score, {
        "score": score,
        "max": 25,
        "details": details,
        "deductions": deductions,
    }


# ============================================================================
# 3. Functional Correctness (30 points)
# ============================================================================

def _check_functionality(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    py_files, all_code = _collect_py_code(answer_dir)
    if not py_files:
        return 0, {
            "score": 0,
            "max": 30,
            "details": {"error": "No Python files"},
            "deductions": ["No code to evaluate"],
        }

    # 3a. Dynamic camera pose setting (10 points)
    # Core: update camera pose at each step in a loop
    dynamic_score = 0

    has_loop = bool(re.search(r"for\s+\w+\s+in\s+range|while\s+", all_code))
    has_pose_update = bool(
        re.search(
            r"cam_pos\[|cam_mat0\[|cam_quat\[|set_camera_pose|set_camera.*pos",
            all_code,
            re.I,
        )
    )
    has_trajectory = bool(
        re.search(
            r"math\.(sin|cos)|np\.(sin|cos)|theta|angle|orbit|trajectory|"
            r"circular|interp|look_at",
            all_code,
            re.I,
        )
    )

    if has_loop and has_pose_update:
        dynamic_score += 6
    elif has_pose_update:
        dynamic_score += 3
        deductions.append("Camera pose is not dynamically updated within a loop")
    else:
        deductions.append("Dynamic camera pose setting at each timestep not implemented")

    if has_trajectory:
        dynamic_score += 4
    elif has_loop:
        dynamic_score += 2
    else:
        deductions.append("Continuous smooth camera trajectory not implemented")

    score += dynamic_score
    details["dynamic_camera"] = f"{dynamic_score}/10"

    # 3b. Base frame absolute coordinate scheme (10 points)
    base_func_score = 0

    has_base_to_world = bool(
        re.search(
            r"def\s+set_camera_pose_in_base|pos_in_base|quat_in_base|base_frame|"
            r"base_pos_w.*base_rot_w|get_body_pose.*base|xpos\[.*bid\]",
            all_code,
            re.I,
        )
    )
    has_body_lookup = bool(
        re.search(
            r"body_name2id|mj_name2id.*BODY|body.*name|robot0_base|base_body_name",
            all_code,
            re.I,
        )
    )
    has_forward = bool(re.search(r"mj_forward|sim\.forward|forward\(\)", all_code))

    if has_base_to_world:
        base_func_score += 5
    else:
        deductions.append("Base frame to world frame transform not implemented")

    if has_body_lookup:
        base_func_score += 3
    else:
        deductions.append("Base body name lookup not implemented")

    if has_forward:
        base_func_score += 2
    else:
        deductions.append("mj_forward/sim.forward not called to apply pose update")

    score += base_func_score
    details["base_frame_func"] = f"{base_func_score}/10"

    # 3c. Environment creation and rendering pipeline (10 points)
    env_score = 0

    has_env_create = bool(
        re.search(
            r"suite\.make|robosuite\.make|RobocasaEnv|make_env", all_code, re.I
        )
    )
    has_offscreen = bool(
        re.search(
            r"has_offscreen_renderer\s*=\s*True|offscreen.*True|"
            r"use_camera_obs\s*=\s*True",
            all_code,
            re.I,
        )
    )
    has_camera_names = bool(
        re.search(
            r"camera_names|camera_name|agentview|frontview|sideview",
            all_code,
            re.I,
        )
    )
    has_env_step = bool(re.search(r"env\.step|env\.reset|\.step\(|\.reset\(", all_code))
    has_render_call = bool(
        re.search(
            r"sim\.render|env\.render|render_rgb|_get_observations", all_code
        )
    )

    if has_env_create:
        env_score += 3
    else:
        deductions.append("robosuite/robocasa environment not created")

    if has_offscreen:
        env_score += 2
    elif has_render_call:
        env_score += 1
    else:
        deductions.append("Offscreen rendering not configured")

    if has_camera_names:
        env_score += 2

    if has_env_step:
        env_score += 1

    if has_render_call:
        env_score += 2
    else:
        deductions.append("Render function not called")

    score += env_score
    details["env_render_pipeline"] = f"{env_score}/10"

    return score, {
        "score": score,
        "max": 30,
        "details": details,
        "deductions": deductions,
    }


# ============================================================================
# 4. Documentation Quality (20 points)
# ============================================================================

def _check_documentation(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    md_files = _find_files(answer_dir, ["md"])
    own_md = [
        f
        for f in md_files
        if "/robocasa/" not in f.replace("\\", "/")
        and "/robosuite/" not in f.replace("\\", "/")
    ]

    if not own_md:
        return 0, {
            "score": 0,
            "max": 20,
            "details": {"error": "No functionality documentation found"},
            "deductions": ["Missing functionality documentation"],
        }

    # Read document content
    doc_content = ""
    for f in own_md:
        doc_content += _read_file(f) + "\n"

    if len(doc_content.strip()) < 50:
        return 1, {
            "score": 1,
            "max": 20,
            "details": {"error": "Document content too short (<50 characters)"},
            "deductions": ["Insufficient document content"],
        }

    # 4a. Format and structure (5 points) -- deterministic check
    struct_score = 0

    has_title = bool(re.search(r"^#\s+", doc_content, re.MULTILINE))
    section_count = len(re.findall(r"^#{1,3}\s+", doc_content, re.MULTILINE))
    has_code_block = "```" in doc_content
    doc_len = len(doc_content)

    if has_title:
        struct_score += 1
    if section_count >= 3:
        struct_score += 2
    elif section_count >= 2:
        struct_score += 1
    if has_code_block:
        struct_score += 1
    if doc_len >= 500:
        struct_score += 1

    score += struct_score
    details["structure"] = f"{struct_score}/5 -- title={'yes' if has_title else 'no'}, sections={section_count}, code_blocks={'yes' if has_code_block else 'no'}, length={doc_len}"

    # 4b. Content completeness (15 points) -- LLM-as-Judge
    config = _get_text_eval_config(answer_dir)
    llm_prompt = f"""You are a technical documentation evaluation expert. Please evaluate the following documentation about camera movement functionality in the Robocasa/Robosuite simulation environment.

Document content:
---
{doc_content[:4000]}
---

This task requires implementing camera pose setting using absolute coordinates in the robot base frame within the Robocasa simulation environment, supporting pose updates for the same camera at each timestep.

Please score strictly on the following dimensions (total 15 points):

1. Camera pose setting interface description (5 points):
   - 5 points: Clearly explains how to set position + orientation, uses MuJoCo model attributes like cam_pos/cam_mat0, explains coordinate frame transformation
   - 3-4 points: Describes pose setting method but missing key details (e.g., no explanation of rotation representation or transform logic)
   - 1-2 points: Only briefly mentioned
   - 0 points: Not covered at all

2. Offscreen rendering description (3 points):
   - 3 points: Explains offscreen rendering method (sim.render / env.render etc.)
   - 1-2 points: Mentioned but not specific enough
   - 0 points: Not covered

3. Robomimic integration description (4 points):
   - 4 points: Explains how to access the underlying robosuite environment within the Robomimic framework and call camera interfaces, includes example code
   - 2-3 points: Mentioned but lacks examples or not clear enough
   - 0-1 points: Not covered

4. Notes and caveats (3 points):
   - 3 points: Covers coordinate frame conventions (base frame vs world frame), quaternion format (w,x,y,z), and usage limitations
   - 1-2 points: Partially covered
   - 0 points: Not covered

Please respond strictly in the following JSON format:
```json
{{"camera_api": {{"score": 0, "reason": ""}}, "offscreen_render": {{"score": 0, "reason": ""}}, "robomimic": {{"score": 0, "reason": ""}}, "notes": {{"score": 0, "reason": ""}}, "total": 0}}
```"""

    llm_result = _call_llm_judge(llm_prompt, config)
    llm_score = 0

    if llm_result:
        try:
            text = llm_result
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(text)
            cam_s = max(0, min(5, int(parsed.get("camera_api", {}).get("score", 0))))
            render_s = max(0, min(3, int(parsed.get("offscreen_render", {}).get("score", 0))))
            robo_s = max(0, min(4, int(parsed.get("robomimic", {}).get("score", 0))))
            notes_s = max(0, min(3, int(parsed.get("notes", {}).get("score", 0))))
            llm_score = cam_s + render_s + robo_s + notes_s
            details["llm_camera_api"] = f"{cam_s}/5 — {parsed.get('camera_api', {}).get('reason', '')}"
            details["llm_offscreen"] = f"{render_s}/3 — {parsed.get('offscreen_render', {}).get('reason', '')}"
            details["llm_robomimic"] = f"{robo_s}/4 — {parsed.get('robomimic', {}).get('reason', '')}"
            details["llm_notes"] = f"{notes_s}/3 — {parsed.get('notes', {}).get('reason', '')}"
        except (json.JSONDecodeError, Exception) as e:
            details["llm_parse_error"] = str(e)[:120]
            llm_score = 5
            details["llm_fallback"] = "LLM response parsing failed, giving conservative score 5/15"
    else:
        # LLM unavailable, give conservative score based on keywords
        kw_score = 0
        if re.search(r"set_camera_pose|cam_pos|cam_mat0", doc_content):
            kw_score += 2
        if re.search(r"robomimic|Robomimic", doc_content):
            kw_score += 2
        if re.search(r"四元数|quat|quaternion|坐标系|coordinate", doc_content, re.I):
            kw_score += 1
        if re.search(r"render|渲染|offscreen", doc_content, re.I):
            kw_score += 1
        if re.search(r"sim\.render|env\.render|render_rgb", doc_content):
            kw_score += 1
        llm_score = min(8, kw_score)
        details["llm_unavailable"] = f"LLM unavailable, keyword-based score {llm_score}/15"

    score += llm_score
    details["content_score"] = f"{llm_score}/15"

    return score, {
        "score": score,
        "max": 20,
        "details": details,
        "deductions": deductions,
    }


# ============================================================================
# 5. Video Output (10 points)
# ============================================================================

def _check_video(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}
    deductions: List[str] = []

    video_files = _find_files(answer_dir, ["mp4", "avi", "mov", "mkv", "webm"])

    if not video_files:
        return 0, {
            "score": 0,
            "max": 10,
            "details": {"error": "No video files"},
            "deductions": ["Missing camera trajectory video"],
        }

    # Select the largest video
    best_video = max(video_files, key=_file_size)
    best_size = _file_size(best_video)

    details["video_path"] = os.path.relpath(best_video, answer_dir)
    details["video_size_kb"] = round(best_size / 1024, 1)

    # 5a. File validity (5 points) -- based on file size
    if best_size >= 100 * 1024:
        score += 5
        details["validity"] = "5/5 -- Video file >= 100KB"
    elif best_size >= 10 * 1024:
        score += 3
        details["validity"] = "3/5 -- Video file 10-100KB (small)"
    elif best_size >= 1024:
        score += 2
        details["validity"] = "2/5 -- Video file 1-10KB (very small)"
    else:
        score += 1
        details["validity"] = "1/5 -- Video file < 1KB (possibly invalid)"
        deductions.append("Video file too small")

    # 5b. Format and quality (5 points)
    fmt_score = 0

    # .mp4 format (task requirement)
    if best_video.endswith(".mp4"):
        fmt_score += 2
    else:
        fmt_score += 1
        deductions.append("Video is not in .mp4 format")

    # Check file header for valid MP4 (ftyp box)
    try:
        with open(best_video, "rb") as f:
            header = f.read(12)
        if b"ftyp" in header:
            fmt_score += 2
            details["format_check"] = "MP4 ftyp box detected"
        elif len(header) >= 8:
            fmt_score += 1
            details["format_check"] = "File header: ftyp box not detected"
    except Exception:
        details["format_check"] = "Unable to read video file header"

    # Path reasonableness (in root directory or outputs/ subdirectory)
    rel_path = os.path.relpath(best_video, answer_dir)
    if "/" not in rel_path or rel_path.startswith("outputs/") or rel_path.startswith("output/"):
        fmt_score += 1

    score += fmt_score
    details["format_naming"] = f"{fmt_score}/5"

    return score, {
        "score": score,
        "max": 10,
        "details": details,
        "deductions": deductions,
    }


# ============================================================================
# Entry Point
# ============================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report) -- score: integer 0-100, report: detailed evaluation report
    """
    answer_dir = os.path.abspath(answer_dir)

    s1, r1 = _check_file_delivery(answer_dir)
    s2, r2 = _check_code_quality(answer_dir)
    s3, r3 = _check_functionality(answer_dir)
    s4, r4 = _check_documentation(answer_dir)
    s5, r5 = _check_video(answer_dir)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    all_deductions = (
        r1.get("deductions", [])
        + r2.get("deductions", [])
        + r3.get("deductions", [])
        + r4.get("deductions", [])
        + r5.get("deductions", [])
    )

    if total >= 85:
        comment = "Excellent. Fully implemented camera movement functionality with clean code, clear documentation, and valid video."
    elif total >= 70:
        comment = "Good. Task mostly completed, but some dimensions have room for improvement."
    elif total >= 50:
        comment = "Passing. Core functionality implemented but with notable deficiencies."
    elif total >= 30:
        comment = "Partially completed. Key functionality missing or incorrectly implemented."
    else:
        comment = "Failing. Task completion severely insufficient."

    report = {
        "total_score": total,
        "section_scores": {
            "File Delivery": f"{s1}/15",
            "Code Quality": f"{s2}/25",
            "Functional Correctness": f"{s3}/30",
            "Documentation Quality": f"{s4}/20",
            "Video Output": f"{s5}/10",
        },
        "result_score": {
            "score": s1 + s5,
            "max_score": 25,
            "deductions": r1.get("deductions", []) + r5.get("deductions", []),
        },
        "process_score": {
            "score": s2 + s3 + s4,
            "max_score": 75,
            "deductions": (
                r2.get("deductions", [])
                + r3.get("deductions", [])
                + r4.get("deductions", [])
            ),
        },
        "breakdown": {
            "1_File_Delivery": r1,
            "2_Code_Quality": r2,
            "3_Functional_Correctness": r3,
            "4_Documentation_Quality": r4,
            "5_Video_Output": r5,
        },
        "comment": comment,
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print formatted evaluation report"""
    print("=" * 70)
    print("ROBOCASA Camera Movement -- Evaluation Report")
    print("=" * 70)

    print(f"\nTotal score: {score}/100")
    print(f"Comment: {report.get('comment', '')}")

    print("\nSection scores:")
    for k, v in report.get("section_scores", {}).items():
        print(f"  {k}: {v}")

    for section_key, section_label in [
        ("result_score", "Result Score (File Delivery + Video)"),
        ("process_score", "Process Score (Code + Functionality + Documentation)"),
    ]:
        section = report.get(section_key, {})
        print(f"\n{'─' * 50}")
        print(
            f"[{section_label}] {section.get('score', 0)}/{section.get('max_score', 0)}"
        )
        deds = section.get("deductions", [])
        if deds:
            print("  Deductions:")
            for i, d in enumerate(deds, 1):
                print(f"    {i}. {d}")

    print(f"\n{'─' * 50}")
    print("Detailed evaluation:")
    for section_name, section_data in report.get("breakdown", {}).items():
        s = section_data.get("score", "?")
        m = section_data.get("max", "?")
        print(f"\n  [{section_name}] ({s}/{m})")
        for k, v in section_data.get("details", {}).items():
            print(f"    {k}: {v}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(os.path.dirname(__file__), "..", "workspace")

    if os.path.exists(test_dir):
        s, r = evaluate(test_dir)
        print_report(s, r)
        sys.exit(0)
    else:
        print(f"Directory does not exist: {test_dir}")
        sys.exit(0)
