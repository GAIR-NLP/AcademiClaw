"""
BVH Path Tracing Renderer - Grading Script

Task overview:
  The agent must complete three TODO sections in the BVH path tracing renderer:
    1. BVH.cpp       - getIntersection: BVH tree traversal for ray intersection
    2. Bounds3.hpp   - IntersectP:      ray-AABB intersection test
    3. Renderer.cpp  - Render loop:     generate ray directions, normalize, cast, write framebuffer, output output.png
  Deliverables: BVH.cpp, Bounds3.hpp, Renderer.cpp, README.md, output.png

Total score: 100 points, divided into five dimensions:
  1. File delivery        10 points
  2. Build compilation    20 points
  3. Code correctness     30 points
  4. Render output quality 25 points
  5. README quality       15 points
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import base64
import traceback
from typing import Any, Dict, Tuple

try:
    import openai
except ImportError:
    openai = None

try:
    from PIL import Image
except ImportError:
    Image = None

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
QUERY_ROOT = os.path.dirname(EVAL_DIR)
GOLD_DIR = os.path.join(EVAL_DIR, "gold")

# ---------------------------------------------------------------------------
# Environment / LLM utilities
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    values: dict = {}
    for env_dir in [answer_dir, QUERY_ROOT]:
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
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
    }


def _get_vision_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)

    def g(key, default=""):
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_VISION_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_VISION_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_VISION_MODEL", "openai/gpt-5.2"),
    }


def _call_llm_judge(prompt: str, config: dict) -> str:
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


def _call_vision_llm(image_path: str, prompt: str, config: dict) -> str:
    if not openai or not config.get("api_key"):
        return ""
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(image_path)[1].lower()
        mime_map = {
            ".png": "image/png", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg", ".ppm": "image/x-portable-pixmap",
        }
        mime = mime_map.get(ext, "image/png")
    except Exception:
        return ""
    try:
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                ],
            }],
            max_tokens=1024,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] Vision LLM call failed: {e}")
        return ""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def _find_submission_dir(answer_dir: str) -> str:
    """Locate the submission subdirectory; fall back to answer_dir if it does not exist."""
    sub = os.path.join(answer_dir, "submission")
    if os.path.isdir(sub):
        return sub
    return answer_dir


def _find_output_image(answer_dir: str) -> str:
    """Search multiple possible locations for the rendered output image (output.png or binary.ppm)."""
    sub_dir = _find_submission_dir(answer_dir)
    candidates = []

    # Direct locations
    for d in [answer_dir, sub_dir]:
        candidates.append(os.path.join(d, "output.png"))
        candidates.append(os.path.join(d, "binary.ppm"))

    # build subdirectory
    for d in [answer_dir, sub_dir]:
        build_dir = os.path.join(d, "build")
        if os.path.isdir(build_dir):
            for root, _dirs, files in os.walk(build_dir):
                for fname in files:
                    if fname in ("output.png", "binary.ppm"):
                        candidates.append(os.path.join(root, fname))

    for c in candidates:
        if os.path.isfile(c) and os.path.getsize(c) > 100:
            return c
    return ""


def _token_similarity(text_a: str, text_b: str) -> float:
    """Token-set-based Jaccard similarity."""
    def tokenize(txt):
        for c in "{}();,<>\"'":
            txt = txt.replace(c, " ")
        return set(txt.split())

    a_set = tokenize(text_a)
    b_set = tokenize(text_b)
    if not a_set and not b_set:
        return 1.0
    if not a_set or not b_set:
        return 0.0
    return len(a_set & b_set) / max(len(a_set | b_set), 1)


# ===================================================================
# 1. File delivery (10 points)
# ===================================================================

def _eval_file_delivery(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    sub_dir = _find_submission_dir(answer_dir)

    file_points = {
        "BVH.cpp": 2,
        "Bounds3.hpp": 2,
        "Renderer.cpp": 2,
        "README.md": 2,
    }

    for fname, pts in file_points.items():
        path = os.path.join(sub_dir, fname)
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            score += pts
            details[fname] = f"{pts}/{pts} - present"
        else:
            details[fname] = f"0/{pts} - missing"

    img_path = _find_output_image(answer_dir)
    if img_path:
        score += 2
        rel = os.path.relpath(img_path, answer_dir)
        details["output.png"] = f"2/2 - present ({rel})"
    else:
        details["output.png"] = "0/2 - missing"

    return score, details


# ===================================================================
# 2. Build compilation (20 points)
# ===================================================================

def _eval_build(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    sub_dir = _find_submission_dir(answer_dir)

    cmake_file = os.path.join(sub_dir, "CMakeLists.txt")
    if not os.path.isfile(cmake_file):
        details["cmake"] = "0/10 - CMakeLists.txt does not exist"
        details["make"] = "0/10 - cannot compile"
        return 0, details

    build_dir = os.path.join(answer_dir, "_eval_build")
    try:
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir, exist_ok=True)

        # Ensure models directory exists in submission
        models_dst = os.path.join(sub_dir, "models")
        if not os.path.isdir(models_dst):
            for src_dir in [
                os.path.join(QUERY_ROOT, "context", "models"),
                os.path.join(GOLD_DIR, "models"),
            ]:
                if os.path.isdir(src_dir):
                    shutil.copytree(src_dir, models_dst)
                    break

        # cmake
        result = subprocess.run(
            ["cmake", sub_dir],
            cwd=build_dir,
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            score += 10
            details["cmake"] = "10/10 - CMake configuration succeeded"
        else:
            details["cmake"] = f"0/10 - CMake failed: {result.stderr[:200]}"
            details["make"] = "0/10 - CMake failed, skipped"
            return score, details

        # make
        result = subprocess.run(
            ["make", "-j4"],
            cwd=build_dir,
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode == 0:
            score += 10
            details["make"] = "10/10 - compilation succeeded"
        else:
            err = (result.stderr or result.stdout)[:300]
            details["make"] = f"0/10 - compilation failed: {err}"

    except subprocess.TimeoutExpired:
        details["build_error"] = "build timed out"
    except Exception as e:
        details["build_error"] = f"build exception: {str(e)[:200]}"
    finally:
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)

    return score, details


# ===================================================================
# 3. Code correctness (30 points)
# ===================================================================

def _eval_code_correctness(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    sub_dir = _find_submission_dir(answer_dir)

    # ---- 3.1 Code structure completeness (5 points) ----
    struct_pts = 0
    required_files = ["BVH.cpp", "BVH.hpp", "Bounds3.hpp"]
    all_exist = all(
        os.path.isfile(os.path.join(sub_dir, f)) for f in required_files
    )
    if all_exist:
        struct_pts += 2

    all_cpp = ""
    for f in ("BVH.cpp", "Bounds3.hpp", "Renderer.cpp"):
        all_cpp += _read_file(os.path.join(sub_dir, f))

    required_symbols = ["BVHAccel", "Intersect", "recursiveBuild", "IntersectP"]
    found_symbols = [s for s in required_symbols if s in all_cpp]
    if len(found_symbols) >= 4:
        struct_pts += 3
    elif len(found_symbols) >= 3:
        struct_pts += 2
    elif len(found_symbols) >= 2:
        struct_pts += 1

    score += struct_pts
    details["3.1 code_structure (5pts)"] = (
        f"{struct_pts}/5 - files: {'OK' if all_exist else 'MISSING'}, "
        f"symbols: {len(found_symbols)}/{len(required_symbols)}"
    )

    # ---- 3.2 BVH.cpp: getIntersection (10 points) ----
    bvh_pts = 0
    bvh_code = _read_file(os.path.join(sub_dir, "BVH.cpp"))

    if bvh_code:
        m = re.search(
            r'BVHAccel::getIntersection\s*\([^)]*\)\s*const\s*\{(.+)',
            bvh_code, re.DOTALL,
        )
        if m:
            body = m.group(1)
            end_match = re.search(r'\n(?:Intersection|BVHBuildNode|void|bool|int)\s', body)
            if end_match:
                body = body[:end_match.start()]
            stripped = re.sub(r'//.*|/\*.*?\*/', '', body).strip()

            if len(stripped) < 15:
                details["3.2 BVH getIntersection (10pts)"] = "0/10 - TODO not implemented"
            else:
                checks = {
                    "bounds_check": bool(re.search(r'IntersectP|bounds', body)),
                    "leaf_check": bool(re.search(
                        r'left\s*==\s*nullptr|right\s*==\s*nullptr|->object', body)),
                    "recursive": bool(re.search(r'getIntersection', body)),
                    "distance_compare": bool(re.search(r'distance|happened', body)),
                    "left_right": ("left" in body and "right" in body),
                }
                n_found = sum(checks.values())
                if n_found >= 5:
                    bvh_pts = 10
                elif n_found >= 4:
                    bvh_pts = 8
                elif n_found >= 3:
                    bvh_pts = 6
                elif n_found >= 2:
                    bvh_pts = 4
                else:
                    bvh_pts = 2

                el = ", ".join(f"{k}={'Y' if v else 'N'}" for k, v in checks.items())
                details["3.2 BVH getIntersection (10pts)"] = (
                    f"{bvh_pts}/10 - key elements {n_found}/5 ({el})"
                )
        else:
            details["3.2 BVH getIntersection (10pts)"] = "0/10 - getIntersection function not found"
    else:
        details["3.2 BVH getIntersection (10pts)"] = "0/10 - BVH.cpp does not exist"

    score += bvh_pts

    # ---- 3.3 Bounds3.hpp: IntersectP (10 points) ----
    bounds_pts = 0
    bounds_code = _read_file(os.path.join(sub_dir, "Bounds3.hpp"))

    if bounds_code:
        m = re.search(
            r'Bounds3::IntersectP\s*\([^)]*\)\s*const\s*\{(.+?)(?=\ninline\s+Bounds3\s+Union|\Z)',
            bounds_code, re.DOTALL,
        )
        if m:
            body = m.group(1)
            stripped = re.sub(r'//.*|/\*.*?\*/', '', body).strip()

            if len(stripped) < 15:
                details["3.3 Bounds3 IntersectP (10pts)"] = "0/10 - TODO not implemented"
            else:
                checks = {
                    "invDir_usage": "invDir" in body,
                    "tmin_tmax": bool(re.search(
                        r't[Mm]in|t[Mm]ax|tEnter|tExit|t_min|t_max', body)),
                    "origin": "origin" in body,
                    "compare": bool(re.search(
                        r'std::max|std::min|fmax|fmin|>|<', body)),
                    "return_bool": bool(re.search(r'return\s+', body)),
                }
                n_found = sum(checks.values())
                if n_found >= 5:
                    bounds_pts = 10
                elif n_found >= 4:
                    bounds_pts = 8
                elif n_found >= 3:
                    bounds_pts = 6
                elif n_found >= 2:
                    bounds_pts = 4
                else:
                    bounds_pts = 2

                el = ", ".join(f"{k}={'Y' if v else 'N'}" for k, v in checks.items())
                details["3.3 Bounds3 IntersectP (10pts)"] = (
                    f"{bounds_pts}/10 - key elements {n_found}/5 ({el})"
                )
        else:
            details["3.3 Bounds3 IntersectP (10pts)"] = "0/10 - IntersectP function not found"
    else:
        details["3.3 Bounds3 IntersectP (10pts)"] = "0/10 - Bounds3.hpp does not exist"

    score += bounds_pts

    # ---- 3.4 Renderer.cpp: Render loop (5 points) ----
    ren_pts = 0
    ren_code = _read_file(os.path.join(sub_dir, "Renderer.cpp"))

    if ren_code:
        checks = {
            "normalize_dir": bool(re.search(r'normalize\s*\(', ren_code)),
            "cast_ray": "castRay" in ren_code,
            "framebuffer_write": ("framebuffer" in ren_code and "m++" in ren_code),
            "output_file": "output.png" in ren_code,
            "file_write": ("fopen" in ren_code or "ofstream" in ren_code),
        }
        n_found = sum(checks.values())

        if n_found >= 5:
            ren_pts = 5
        elif n_found >= 4:
            ren_pts = 4
        elif n_found >= 3:
            ren_pts = 3
        elif n_found >= 2:
            ren_pts = 2
        elif n_found >= 1:
            ren_pts = 1

        if "binary.ppm" in ren_code and "output.png" not in ren_code:
            ren_pts = max(0, ren_pts - 1)
            details["3.4 Renderer render_loop (5pts)"] = (
                f"{ren_pts}/5 - did not change binary.ppm to output.png"
            )
        else:
            el = ", ".join(f"{k}={'Y' if v else 'N'}" for k, v in checks.items())
            details["3.4 Renderer render_loop (5pts)"] = (
                f"{ren_pts}/5 - key elements {n_found}/5 ({el})"
            )
    else:
        details["3.4 Renderer render_loop (5pts)"] = "0/5 - Renderer.cpp does not exist"

    score += ren_pts
    return score, details


# ===================================================================
# 4. Render output quality (25 points)
# ===================================================================

_VISION_PROMPT = """\
You are a strict image evaluation expert. This image should be the output of a BVH path tracing renderer.
Expected content: A Stanford Bunny model rendered in a Cornell Box-style scene,
including colored walls (red/green), a top area light source, and soft shadows from the bunny.

Please score strictly (integers) on the following dimensions and provide brief justifications:

**Dimension 1: Scene content (0-10 points)**
  9-10: Clear Cornell Box + Bunny with lighting and shadows
  6-8:  Recognizable 3D scene with basic geometry and lighting
  3-5:  Has rendered content but incomplete or with obvious defects
  0-2:  Blank / pure noise / completely wrong

**Dimension 2: Render quality (0-10 points)**
  9-10: Correct lighting, natural shadows, reasonable colors
  6-8:  Mostly correct with minor flaws
  3-5:  Obvious problems (wrong colors, missing parts, etc.)
  0-2:  Very poor quality or essentially unrecognizable

Please respond strictly in the following JSON format:
```json
{"scene_content": {"score": 0, "reason": ""}, "render_quality": {"score": 0, "reason": ""}}
```"""


def _fallback_image_eval(img_path: str) -> int:
    """Fallback evaluation when Vision LLM is unavailable; max 12/20."""
    try:
        fsize = os.path.getsize(img_path)
        if not Image:
            return 4 if fsize >= 50 * 1024 else (2 if fsize >= 1024 else 0)

        img = Image.open(img_path)
        w, h = img.size
        pixels = list(img.convert("RGB").getdata())
        unique_colors = len(set(pixels[:5000]))

        pts = 0
        if w >= 400 and h >= 400:
            pts += 4
        elif w >= 100 and h >= 100:
            pts += 2
        if fsize >= 50 * 1024:
            pts += 3
        elif fsize >= 10 * 1024:
            pts += 2
        if unique_colors > 500:
            pts += 5
        elif unique_colors > 100:
            pts += 3
        elif unique_colors > 10:
            pts += 1
        return min(12, pts)
    except Exception:
        return 0


def _eval_render_output(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, Any] = {}

    img_path = _find_output_image(answer_dir)
    if not img_path:
        details["output"] = "0/25 - output.png or binary.ppm not found"
        return 0, details

    # 4.1 File validity (5 points)
    try:
        fsize = os.path.getsize(img_path)
        if fsize < 100:
            details["4.1 file_validity (5pts)"] = f"0/5 - file too small ({fsize} bytes)"
            return 0, details

        if Image:
            try:
                img = Image.open(img_path)
                w, h = img.size
                if w >= 100 and h >= 100:
                    score += 5
                    details["4.1 file_validity (5pts)"] = f"5/5 - {w}x{h}, {fsize/1024:.0f}KB"
                elif w >= 10 and h >= 10:
                    score += 3
                    details["4.1 file_validity (5pts)"] = f"3/5 - dimensions too small {w}x{h}"
                else:
                    details["4.1 file_validity (5pts)"] = f"0/5 - dimensions too small {w}x{h}"
                    return score, details
            except Exception:
                if fsize > 1000:
                    score += 3
                    details["4.1 file_validity (5pts)"] = (
                        f"3/5 - PIL cannot open but file is non-empty ({fsize/1024:.0f}KB)"
                    )
                else:
                    details["4.1 file_validity (5pts)"] = "0/5 - cannot read"
                    return score, details
        else:
            if fsize > 1000:
                score += 3
                details["4.1 file_validity (5pts)"] = (
                    f"3/5 - PIL unavailable, size check only ({fsize/1024:.0f}KB)"
                )
            else:
                details["4.1 file_validity (5pts)"] = "0/5 - file too small"
                return score, details
    except Exception as e:
        details["4.1 file_validity (5pts)"] = f"0/5 - exception: {str(e)[:100]}"
        return 0, details

    # 4.2 Image content quality (20 points) - Vision LLM
    config = _get_vision_eval_config(answer_dir)
    llm_result = _call_vision_llm(img_path, _VISION_PROMPT, config)

    if llm_result:
        try:
            text = llm_result
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(text)

            scene_pts = max(0, min(10, int(
                parsed.get("scene_content", {}).get("score", 0))))
            quality_pts = max(0, min(10, int(
                parsed.get("render_quality", {}).get("score", 0))))
            vision_total = scene_pts + quality_pts
            score += vision_total

            details["4.2 image_content (20pts)"] = {
                "scene_content": (
                    f"{scene_pts}/10 - "
                    f"{parsed.get('scene_content', {}).get('reason', '')}"
                ),
                "render_quality": (
                    f"{quality_pts}/10 - "
                    f"{parsed.get('render_quality', {}).get('reason', '')}"
                ),
                "total_score": f"{vision_total}/20",
            }
        except (json.JSONDecodeError, Exception):
            fb = _fallback_image_eval(img_path)
            score += fb
            details["4.2 image_content (20pts)"] = (
                f"{fb}/20 - Vision LLM returned invalid format, fallback evaluation"
            )
    else:
        fb = _fallback_image_eval(img_path)
        score += fb
        details["4.2 image_content (20pts)"] = (
            f"{fb}/20 - Vision LLM unavailable, fallback evaluation"
        )

    return score, details


# ===================================================================
# 5. README quality (15 points)
# ===================================================================

def _eval_readme(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    score = 0
    details: Dict[str, str] = {}
    sub_dir = _find_submission_dir(answer_dir)

    readme_path = os.path.join(sub_dir, "README.md")
    if not os.path.isfile(readme_path):
        details["README"] = "0/15 - README.md does not exist"
        return 0, details

    content = _read_file(readme_path).strip()
    if not content:
        details["README"] = "0/15 - README.md is empty"
        return 0, details

    # 5.1 Basic existence (5 points)
    word_count = len(content.split())
    if word_count >= 50:
        score += 5
        details["5.1 content_existence (5pts)"] = f"5/5 - {word_count} words"
    elif word_count >= 20:
        score += 3
        details["5.1 content_existence (5pts)"] = f"3/5 - {word_count} words (short)"
    elif word_count >= 5:
        score += 1
        details["5.1 content_existence (5pts)"] = f"1/5 - {word_count} words (too short)"
    else:
        details["5.1 content_existence (5pts)"] = f"0/5 - {word_count} words"

    # 5.2 LLM evaluation of document quality (10 points)
    config = _get_text_eval_config(answer_dir)
    prompt = f"""\
You are a strict documentation evaluation expert. Below is the README.md for a BVH path tracing renderer project.
The project requires implementing:
1. BVH tree ray intersection traversal (BVH.cpp - getIntersection)
2. Ray-bounding box intersection test (Bounds3.hpp - IntersectP)
3. Render main loop: compute ray directions and cast rays (Renderer.cpp)

Please evaluate the README quality (0-10 points):
  9-10: Detailed description of algorithm principles, implementation methods, problems encountered and solutions
  6-8:  Has basic description but lacks details
  3-5:  Simple description or partially off-topic
  0-2:  Too little content or completely irrelevant

Please respond strictly in the following JSON format:
```json
{{"score": 0, "reason": ""}}
```

README content:
---
{content[:2000]}
---"""

    llm_result = _call_llm_judge(prompt, config)
    if llm_result:
        try:
            text = llm_result
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(text)
            readme_pts = max(0, min(10, int(parsed.get("score", 0))))
            score += readme_pts
            details["5.2 doc_quality (10pts)"] = (
                f"{readme_pts}/10 - {parsed.get('reason', '')}"
            )
        except Exception:
            fb = min(5, word_count // 30)
            score += fb
            details["5.2 doc_quality (10pts)"] = (
                f"{fb}/10 - LLM returned invalid format, fallback evaluation"
            )
    else:
        fb = min(5, word_count // 30)
        score += fb
        details["5.2 doc_quality (10pts)"] = f"{fb}/10 - LLM unavailable, fallback evaluation"

    return score, details


# ===================================================================
# Entry point
# ===================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report)
        - score: integer from 0-100
        - report: dict containing the detailed evaluation report
    """
    s1, r1 = _eval_file_delivery(answer_dir)
    s2, r2 = _eval_build(answer_dir)
    s3, r3 = _eval_code_correctness(answer_dir)
    s4, r4 = _eval_render_output(answer_dir)
    s5, r5 = _eval_readme(answer_dir)

    total = int(min(100, s1 + s2 + s3 + s4 + s5))

    report = {
        "total_score": total,
        "section_scores": {
            "1. File delivery (10pts)": s1,
            "2. Build compilation (20pts)": s2,
            "3. Code correctness (30pts)": s3,
            "4. Render output (25pts)": s4,
            "5. README (15pts)": s5,
        },
        "details": {
            "1. File delivery": r1,
            "2. Build compilation": r2,
            "3. Code correctness": r3,
            "4. Render output": r4,
            "5. README": r5,
        },
    }

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print the formatted grading report."""
    print("=" * 70)
    print("BVH Path Tracing Renderer - Grading Report")
    print("=" * 70)
    print(f"\nTotal score: {score}/100\n")

    scores = report.get("section_scores", {})
    if scores:
        print("Section scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for section, items in report.get("details", {}).items():
        print(f"\n{'─' * 50}")
        print(f"【{section}】")
        print(f"{'─' * 50}")
        if isinstance(items, dict):
            for k, v in items.items():
                if isinstance(v, dict):
                    print(f"  {k}:")
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"  {items}")

    print(f"\n{'=' * 70}")


# ===================================================================
# CLI
# ===================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(QUERY_ROOT, "gpt-5", "attempt_1")

    if not os.path.isabs(test_dir):
        test_dir = os.path.join(QUERY_ROOT, test_dir)

    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
