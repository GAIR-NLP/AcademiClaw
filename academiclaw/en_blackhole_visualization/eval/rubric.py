"""
Three.js Black Hole Visualization - Scoring Script (rubric.py)
Total: 100 points

Scoring Dimensions:
  1. File Delivery and Basic Check   (10 points)
  2. Technical Architecture           (15 points)
  3. Physics/Visual Logic Audit       (25 points) - LLM-as-Judge
  4. Interaction and UI               (25 points) - Static + Playwright Dynamic
  5. Visual Similarity                (25 points) - Vision LLM-as-Judge
"""

import os
import re
import sys
import json
import time
import base64
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from playwright.sync_api import sync_playwright
    _PW = True
except ImportError:
    _PW = False


# ─────────────────────────────────────────────────────────────────────────────
# Environment / LLM Utilities
# ─────────────────────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    values = {}
    rubric_dir = os.path.dirname(os.path.abspath(__file__))
    query_root = os.path.dirname(rubric_dir)
    for d in [answer_dir, query_root]:
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
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
            messages=[
                {"role": "system", "content": "You are a rigorous AI grading assistant. Output ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2048,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] LLM Judge error: {e}")
        return ""


def _call_vision_llm(prompt: str, image_paths: list, config: dict) -> str:
    if not openai or not config.get("api_key"):
        return ""
    try:
        base = config["api_base"].rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        client = openai.OpenAI(api_key=config["api_key"], base_url=base)
        content = [{"type": "text", "text": prompt}]
        for img_path in image_paths:
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                ext = os.path.splitext(img_path)[1].lower()
                mime = {".png": "image/png", ".jpg": "image/jpeg",
                        ".jpeg": "image/jpeg"}.get(ext, "image/png")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime};base64,{b64}", "detail": "high"},
                })
        resp = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": content}],
            max_tokens=1024,
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[RUBRIC] Vision LLM error: {e}")
        return ""


def _extract_json(text: str) -> dict:
    if not text:
        return {}
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except Exception:
                        break
    return {}


# ─────────────────────────────────────────────────────────────────────────────
# Playwright helpers
# ─────────────────────────────────────────────────────────────────────────────

def _launch_browser(pw):
    import subprocess
    has_gpu = False
    try:
        r = subprocess.run(["nvidia-smi"], capture_output=True, timeout=5)
        has_gpu = r.returncode == 0
    except Exception:
        pass
    args = [
        "--no-sandbox", "--disable-dev-shm-usage",
        "--no-zygote", "--disable-setuid-sandbox",
    ]
    if not has_gpu:
        args += ["--disable-gpu", "--use-angle=swiftshader-webgl", "--use-gl=angle"]
    try:
        return pw.chromium.launch(headless=True, args=args)
    except Exception as e1:
        try:
            return pw.webkit.launch(headless=True)
        except Exception:
            raise e1


def _wait_for_render(page):
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    time.sleep(1)
    try:
        page.evaluate("""() => new Promise(r => {
            let n = 0;
            function tick() { requestAnimationFrame(() => { n++; if (n >= 10) r(); else tick(); }); }
            tick();
        })""")
    except Exception:
        pass
    time.sleep(2)


def _calc_mse(p1: str, p2: str) -> float:
    if not os.path.exists(p1) or not os.path.exists(p2):
        return 999.0
    try:
        import numpy as np
        a1 = np.array(Image.open(p1).convert("RGB")).astype(float)
        a2 = np.array(Image.open(p2).convert("RGB")).astype(float)
        return float(np.mean((a1 - a2) ** 2))
    except Exception:
        return 999.0


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _is_viz_html(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(30000)
        return any(k in head for k in ["THREE.", "ShaderMaterial", "three.module.js", "OrbitControls"])
    except Exception:
        return False


def _find_html(answer_dir: str) -> str:
    files = os.listdir(answer_dir)
    htmls = [f for f in files if f.lower().endswith(".html")]
    if not htmls:
        return ""
    full = [os.path.join(answer_dir, f) for f in htmls]
    viz = [p for p in full if _is_viz_html(p)]
    return viz[0] if viz else full[0]


def _find_ref_image() -> str:
    rubric_dir = os.path.dirname(os.path.abspath(__file__))
    query_root = os.path.dirname(rubric_dir)
    for name in ["query1_Reference_Image.jpg", "query1_Reference_Image.png"]:
        p = os.path.join(query_root, "context", name)
        if os.path.exists(p):
            return p
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# 1. File Delivery and Basic Check (10 points)
# ─────────────────────────────────────────────────────────────────────────────

def _eval_delivery(answer_dir: str) -> Tuple[int, dict]:
    score = 0
    d = {}
    files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    # 1a. HTML file exists (5 points)
    htmls = [f for f in files if f.lower().endswith(".html")]
    if htmls:
        html_path = os.path.join(answer_dir, htmls[0])
        if _is_viz_html(html_path):
            score += 5
            d["HTML_file"] = f"5/5 - {htmls[0]} contains Three.js visualization code"
        else:
            score += 2
            d["HTML_file"] = f"2/5 - {htmls[0]} exists but does not contain Three.js code"
    else:
        d["HTML_file"] = "0/5 - No HTML file found"

    # 1b. operation_sequence.json (3 points)
    if "operation_sequence.json" in files:
        try:
            with open(os.path.join(answer_dir, "operation_sequence.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "operations" in data:
                score += 3
                d["operation_sequence.json"] = "3/3 - Format correct"
            else:
                score += 1
                d["operation_sequence.json"] = "1/3 - JSON parseable but structure incomplete"
        except Exception:
            score += 1
            d["operation_sequence.json"] = "1/3 - File exists but parsing failed"
    else:
        d["operation_sequence.json"] = "0/3 - Not found"

    # 1c. Screenshot file (optional, 2 points)
    img_exts = {".png", ".jpg", ".jpeg"}
    imgs = [f for f in files if os.path.splitext(f)[1].lower() in img_exts]
    if imgs:
        score += 2
        d["screenshot_file"] = f"2/2 - {imgs[0]}"
    else:
        d["screenshot_file"] = "0/2 - Not found (optional)"

    return score, d


# ─────────────────────────────────────────────────────────────────────────────
# 2. Technical Architecture (15 points)
# ─────────────────────────────────────────────────────────────────────────────

def _eval_tech(html_content: str) -> Tuple[int, dict]:
    score = 0
    d = {}

    # 2a. ShaderMaterial / RawShaderMaterial (4 points)
    has_shader = bool(re.search(r"(ShaderMaterial|RawShaderMaterial)", html_content))
    if has_shader:
        score += 4
        d["ShaderMaterial"] = "4/4"
    else:
        d["ShaderMaterial"] = "0/4 - ShaderMaterial not used"

    # 2b. OrbitControls (3 points)
    has_orbit = "OrbitControls" in html_content
    if has_orbit:
        score += 3
        d["OrbitControls"] = "3/3"
    else:
        d["OrbitControls"] = "0/3 - OrbitControls not used"

    # 2c. Key uniform per-frame updates (5 points)
    checks = {
        "iCameraPos": bool(re.search(r"iCameraPos", html_content)),
        "iCameraDir": bool(re.search(r"iCameraDir", html_content)),
        "getWorldDirection": bool(re.search(r"getWorldDirection", html_content)),
        "iResolution": bool(re.search(r"iResolution", html_content)),
        "iTime": bool(re.search(r"iTime", html_content)),
        "iFov": bool(re.search(r"iFov", html_content)),
    }
    passed = sum(1 for v in checks.values() if v)
    if passed >= 5:
        u_score = 5
    elif passed >= 3:
        u_score = 3
    elif passed >= 1:
        u_score = 1
    else:
        u_score = 0
    score += u_score
    d["uniform_updates"] = f"{u_score}/5 - Detected {passed}/{len(checks)} key uniforms"

    # 2d. controls.update() called every frame (3 points)
    has_cu = bool(re.search(r"controls\.update\s*\(", html_content))
    if has_cu:
        score += 3
        d["controls.update"] = "3/3"
    else:
        d["controls.update"] = "0/3 - controls.update() not detected"

    return score, d


# ─────────────────────────────────────────────────────────────────────────────
# 3. Physics/Visual Logic Audit (25 points) - LLM + deterministic fallback
# ─────────────────────────────────────────────────────────────────────────────

def _eval_physics(html_content: str, config: dict) -> Tuple[int, dict]:
    d = {}
    scripts = "\n".join(re.findall(r"<script[^>]*>([\s\S]*?)</script>", html_content))
    if not scripts.strip():
        d["physics_logic"] = "0/25 - No script content found"
        return 0, d

    # Deterministic fallback
    has_gravity = bool(re.search(
        r"(force|gravity|geodesic|lensing|schwarzschild|r\s*\*\s*r|1\.5\s*/|"
        r"normalize\s*\(\s*pos\s*\)|ray.*march|ray.*trac)",
        scripts, re.IGNORECASE,
    ))
    has_doppler = bool(re.search(
        r"(doppler|dot\s*\(.*velocity|brightness|tangent.*speed)",
        scripts, re.IGNORECASE,
    ))
    has_stars = bool(re.search(
        r"(star|hash|fract\s*\(\s*sin|noise|rand|twinkle|breathing)",
        scripts, re.IGNORECASE,
    ))
    det_score = 0
    if has_gravity:
        det_score += 5
    if has_doppler:
        det_score += 5
    if has_stars:
        det_score += 3

    # LLM audit
    snippet = scripts[:12000]
    prompt = f"""Please audit the following Three.js black hole visualization shader/JS code for physics and visual logic.

Scoring criteria:
1. **Gravitational lensing/geodesic/ray bending** (0-10 points):
   - 10: Implemented ray deflection based on Schwarzschild metric (e.g., force=-pos*k/r^2) or equivalent geodesic integration
   - 5-9: Has ray bending but precision or method has flaws
   - 0-4: No ray bending or only simple geometric approximation
2. **Doppler effect** (0-10 points):
   - 10: Brightness shift based on dot product of line of sight and tangential velocity (brighter left, darker right)
   - 5-9: Has Doppler-related calculations but incomplete
   - 0-4: No Doppler or only hardcoded
3. **Procedural starfield** (0-5 points):
   - 5: Noise/hash generated star points with twinkling/breathing, color differentiation
   - 3-4: Has procedural starfield but missing twinkling or color differentiation
   - 0-2: No starfield or uses texture map

Code:
```
{snippet}
```

Return JSON: {{"lensing": 0, "doppler": 0, "stars": 0, "reasoning": ""}}"""

    raw = _call_llm_judge(prompt, config)
    result = _extract_json(raw)

    if result and any(k in result for k in ("lensing", "doppler", "stars")):
        lensing = max(0, min(10, int(result.get("lensing", 0))))
        doppler = max(0, min(10, int(result.get("doppler", 0))))
        stars = max(0, min(5, int(result.get("stars", 0))))
        total = lensing + doppler + stars
        d["gravitational_lensing"] = f"{lensing}/10"
        d["doppler_effect"] = f"{doppler}/10"
        d["procedural_starfield"] = f"{stars}/5"
        d["LLM_audit_notes"] = result.get("reasoning", "")[:200]
        return total, d
    else:
        d["deterministic_check(LLM_unavailable)"] = (
            f"{det_score}/25 - Gravity:{'yes' if has_gravity else 'no'}, "
            f"Doppler:{'yes' if has_doppler else 'no'}, "
            f"Starfield:{'yes' if has_stars else 'no'}"
        )
        return det_score, d


# ─────────────────────────────────────────────────────────────────────────────
# 4. Interaction and UI (25 points)
# ─────────────────────────────────────────────────────────────────────────────

def _eval_interaction(html_path: str, html_content: str, answer_dir: str) -> Tuple[int, dict]:
    score = 0
    d = {}

    # 4a. #anim-toggle element (5 points)
    has_input = bool(re.search(r'<input[^>]*id\s*=\s*["\']anim-toggle["\']', html_content, re.IGNORECASE))
    has_checkbox = bool(re.search(r'type\s*=\s*["\']checkbox["\']', html_content, re.IGNORECASE))
    has_toggle_logic = bool(re.search(
        r"getElementById\s*\(\s*['\"]anim-toggle['\"]\s*\).*checked|anim-toggle.*checked",
        html_content, re.IGNORECASE | re.DOTALL,
    ))
    if has_input and has_checkbox and has_toggle_logic:
        t_score = 5
    elif has_input and has_checkbox:
        t_score = 3
    elif "anim-toggle" in html_content:
        t_score = 1
    else:
        t_score = 0
    score += t_score
    d["#anim-toggle"] = f"{t_score}/5"

    # 4b. UI card: GARGANTUA + frosted glass + interaction instructions (5 points)
    ui = 0
    has_gargantua = bool(re.search(r"GARGANTUA", html_content, re.IGNORECASE))
    has_glass = bool(re.search(r"(backdrop-filter|blur|glassmorphism)", html_content, re.IGNORECASE))
    has_instructions = bool(re.search(r"(rotat|pan|zoom|scroll|left.click|right.click|drag)", html_content, re.IGNORECASE))
    if has_gargantua:
        ui += 2
    if has_glass:
        ui += 2
    if has_instructions:
        ui += 1
    score += ui
    d["UI_card"] = (
        f"{ui}/5 - GARGANTUA:{'yes' if has_gargantua else 'no'}, "
        f"Frosted glass:{'yes' if has_glass else 'no'}, "
        f"Instructions:{'yes' if has_instructions else 'no'}"
    )

    # 4c. OrbitControls interaction code static check (5 points)
    orbit_s = 0
    if "OrbitControls" in html_content and bool(re.search(r"controls\.update\s*\(", html_content)):
        orbit_s += 3
    elif "OrbitControls" in html_content:
        orbit_s += 1
    has_zoom = bool(re.search(r"(minDistance|maxDistance|enableZoom)", html_content, re.IGNORECASE))
    has_pan = bool(re.search(r"(enablePan|enableRotate)", html_content, re.IGNORECASE))
    if has_zoom:
        orbit_s += 1
    if has_pan:
        orbit_s += 1
    orbit_s = min(5, orbit_s)
    score += orbit_s
    d["OrbitControls_interaction"] = f"{orbit_s}/5"

    # 4d. Playwright dynamic verification (10 points: rotation 5 + toggle 5)
    pw_score = 0
    pw_log = ""
    if _PW and html_path and _is_viz_html(html_path):
        abs_path = os.path.abspath(html_path)
        url = f"file://{abs_path}"
        p1 = os.path.join(answer_dir, "_pw_r1.png")
        p2 = os.path.join(answer_dir, "_pw_r2.png")
        s1 = os.path.join(answer_dir, "_pw_s1.png")
        s2 = os.path.join(answer_dir, "_pw_s2.png")
        s3 = os.path.join(answer_dir, "_pw_s3.png")
        s4 = os.path.join(answer_dir, "_pw_s4.png")
        temps = [p1, p2, s1, s2, s3, s4]
        try:
            with sync_playwright() as pw:
                browser = _launch_browser(pw)
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                _wait_for_render(page)
                time.sleep(2)

                # Rotation
                page.screenshot(path=p1)
                page.mouse.move(640, 450)
                page.mouse.down()
                page.mouse.move(200, 200, steps=50)
                page.mouse.up()
                time.sleep(1)
                page.screenshot(path=p2)
                rot_mse = _calc_mse(p1, p2)
                if rot_mse > 0.5:
                    pw_score += 5
                    pw_log += f"Rotation OK (MSE={rot_mse:.1f}); "
                else:
                    pw_log += f"Rotation unchanged (MSE={rot_mse:.2f}); "

                # Toggle
                target = None
                for sel in ["#anim-toggle", "input[type='checkbox']"]:
                    try:
                        if page.locator(sel).count() > 0:
                            target = page.locator(sel).first
                            break
                    except Exception:
                        continue
                if target:
                    page.screenshot(path=s1)
                    time.sleep(1.5)
                    page.screenshot(path=s2)
                    mse_move = _calc_mse(s1, s2)
                    target.dispatch_event("click")
                    time.sleep(2.5)
                    page.screenshot(path=s3)
                    time.sleep(1.5)
                    page.screenshot(path=s4)
                    mse_static = _calc_mse(s3, s4)
                    if mse_move > 0.5 and mse_static < 0.3:
                        pw_score += 5
                        pw_log += f"Toggle OK (M:{mse_move:.1f},S:{mse_static:.2f}); "
                    else:
                        pw_log += f"Toggle uncertain (M:{mse_move:.2f},S:{mse_static:.2f}); "
                else:
                    pw_log += "Toggle element not found; "

                browser.close()
            for f in temps:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception:
                        pass
        except Exception as e:
            pw_log += f"Playwright error: {type(e).__name__}: {str(e)[:80]}"
    else:
        if not _PW:
            pw_log = "Playwright not available"
        elif not html_path:
            pw_log = "No HTML file"
        else:
            pw_log = "HTML is not a visualization page"

    score += pw_score
    d["Playwright_dynamic_verification"] = f"{pw_score}/10 - {pw_log}"

    return score, d


# ─────────────────────────────────────────────────────────────────────────────
# 5. Visual Similarity (25 points) - Vision LLM
# ─────────────────────────────────────────────────────────────────────────────

def _eval_visual(html_path: str, answer_dir: str, config: dict) -> Tuple[int, dict]:
    d = {}

    if not html_path or not _is_viz_html(html_path):
        d["visual_similarity"] = "0/25 - HTML is not a visualization page or does not exist"
        return 0, d

    ref_img = _find_ref_image()
    screenshot_path = os.path.join(answer_dir, "eval_vision_screenshot.png")

    # Take screenshot
    screenshot_ok = False
    if _PW:
        try:
            with sync_playwright() as pw:
                browser = _launch_browser(pw)
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.goto(f"file://{os.path.abspath(html_path)}", wait_until="domcontentloaded", timeout=60000)
                _wait_for_render(page)
                time.sleep(2)
                page.screenshot(path=screenshot_path)
                browser.close()
            if os.path.exists(screenshot_path):
                screenshot_ok = True
        except Exception as e:
            print(f"[RUBRIC] Screenshot failed: {e}", file=sys.stderr)

    if not screenshot_ok:
        for f in os.listdir(answer_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg")) and "screenshot" in f.lower():
                screenshot_path = os.path.join(answer_dir, f)
                screenshot_ok = True
                break

    # Black screen detection
    is_black = False
    if screenshot_ok and Image:
        try:
            import numpy as np
            arr = np.array(Image.open(screenshot_path).convert("RGB"))
            if arr.mean() < 5:
                is_black = True
        except Exception:
            pass

    if is_black:
        d["visual_similarity"] = "0/25 - Screenshot is completely black"
        return 0, d

    # Vision LLM
    images = []
    if ref_img and os.path.exists(ref_img):
        images.append(ref_img)
    if screenshot_ok:
        images.append(screenshot_path)

    if not images or (len(images) == 1 and not screenshot_ok):
        fallback = 5 if screenshot_ok else 0
        d["visual_similarity"] = f"{fallback}/25 - Cannot perform visual comparison"
        return fallback, d

    vision_prompt = """Please evaluate the black hole visualization rendering result. If there are two images, the first is the reference image and the second is the rendering screenshot.

Please completely ignore differences in hue, saturation, brightness, and starfield density.
Focus on the following geometric structures:
1. Is there a gravitational lensing structure (curved light ring surrounding the center)?
2. Is the center a black circular area (event horizon)?
3. Is there an accretion disk with one side brighter and one side darker (Doppler effect)?
4. Is there actual non-black rendered content?

Scoring:
- 22-25: Highly similar structure, lens ring, accretion disk, dark area clearly visible
- 17-21: Main structures present but details differ
- 10-16: Some structures present but missing key elements
- 4-9: Has rendered content but significantly different from reference
- 0-3: Completely black or unrelated content

Return JSON: {"score": 0, "reasoning": ""}"""

    raw = _call_vision_llm(vision_prompt, images, config)
    result = _extract_json(raw)

    if result and "score" in result:
        v = max(0, min(25, int(result["score"])))
        d["visual_similarity"] = f"{v}/25 - {result.get('reasoning', '')[:150]}"
        return v, d

    # fallback
    if screenshot_ok and not is_black:
        d["visual_similarity"] = "10/25 - Vision LLM unavailable, conservative score for non-black screenshot"
        return 10, d
    d["visual_similarity"] = "0/25 - Vision LLM unavailable and no valid screenshot"
    return 0, d


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the Three.js black hole visualization answer.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report) - score 0-100, report with detailed scoring
    """
    html_path = _find_html(answer_dir)
    html_content = ""
    if html_path and os.path.exists(html_path):
        try:
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                html_content = f.read()
        except Exception:
            pass

    text_cfg = _get_text_eval_config(answer_dir)
    vision_cfg = _get_vision_eval_config(answer_dir)

    s1, d1 = _eval_delivery(answer_dir)
    s2, d2 = _eval_tech(html_content)
    s3, d3 = _eval_physics(html_content, text_cfg)
    s4, d4 = _eval_interaction(html_path, html_content, answer_dir)
    s5, d5 = _eval_visual(html_path, answer_dir, vision_cfg)

    total = max(0, min(100, s1 + s2 + s3 + s4 + s5))

    report = {
        "total_score": total,
        "result_score": {
            "score": s1 + s5,
            "details": {"1. File Delivery": d1, "5. Visual Similarity": d5},
            "deductions": [],
        },
        "process_score": {
            "score": s2 + s3 + s4,
            "details": {"2. Technical Architecture": d2, "3. Physics/Visual Logic": d3, "4. Interaction and UI": d4},
            "deductions": [],
        },
        "dimension_scores": {
            "File Delivery": f"{s1}/10",
            "Technical Architecture": f"{s2}/15",
            "Physics/Visual Logic": f"{s3}/25",
            "Interaction and UI": f"{s4}/25",
            "Visual Similarity": f"{s5}/25",
        },
        "additional_info": {
            "HTML_file": os.path.basename(html_path) if html_path else "Not found",
        },
        "comment": "",
    }

    if total >= 90:
        report["comment"] = "Excellent! Black hole visualization is complete, physics logic and interaction both meet standards."
    elif total >= 75:
        report["comment"] = "Good. Basically complete, some dimensions have room for improvement."
    elif total >= 60:
        report["comment"] = "Passing. Core functionality present, but physics logic or interaction has deficiencies."
    elif total >= 40:
        report["comment"] = "Partially complete. Has implementation but key items are missing."
    else:
        report["comment"] = "Failing. Please check HTML output, interaction, and physics logic."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 70)
    print("Three.js Black Hole Visualization - Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100")

    scores = report.get("dimension_scores", {})
    if scores:
        print("\nDimension Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for key, label in [
        ("result_score", "Result Score (File Delivery + Visual Similarity)"),
        ("process_score", "Process Score (Technical Architecture + Physics Logic + Interaction UI)"),
    ]:
        section = report.get(key, {})
        print(f"\n{'─' * 50}")
        print(f"[{label}] {section.get('score', 0)} pts")
        print(f"{'─' * 50}")
        for cat, items in section.get("details", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k2, v2 in items.items():
                    print(f"    {k2}: {v2}")
            else:
                print(f"    {items}")
        deds = section.get("deductions", [])
        if deds:
            print("\n  Deductions:")
            for i, r in enumerate(deds, 1):
                print(f"    {i}. {r}")

    extra = report.get("additional_info", {})
    if extra:
        print(f"\n{'─' * 50}")
        print("Additional Info:")
        for k, v in extra.items():
            print(f"  {k}: {v}")

    print(f"\n{'=' * 50}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1",
    )
    test_dir = os.path.abspath(test_dir)
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
