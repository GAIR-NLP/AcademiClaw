"""
Rubric for kaiwentao-query2: Facial Emotion Recognition Model Improvement (TensorFlow/Keras)

Task: Improve a baseline 3-layer CNN for 5-class facial emotion recognition.
Deliverables:
  - train_improved_model.py  (training script)
  - emotion_model.h5         (trained Keras model)
  - metrics.json             (evaluation metrics: val_acc, train_acc, macro_f1, per_class_f1)

Total: 100 points
  1. File Delivery          15 pts
  2. Code Quality           15 pts
  3. Overall Accuracy       30 pts  (val_acc)
  4. Class Balance          20 pts  (macro_f1 + min per-class f1)
  5. Generalization         10 pts  (overfitting gap)
  6. Methodology (LLM)     10 pts  (improvement strategies used)
"""

from __future__ import annotations

import ast
import json
import os
from typing import Any, Dict, List, Tuple

try:
    import openai
except ImportError:
    openai = None


# ---------------------------------------------------------------------------
# Env / LLM helpers
# ---------------------------------------------------------------------------

def _load_env(answer_dir: str) -> dict:
    """Load .env from answer_dir and query root directory."""
    values: dict = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() not in values:
                        values[k.strip()] = v.strip().strip("'\"")
    return values


def _get_text_eval_config(answer_dir: str) -> dict:
    env = _load_env(answer_dir)

    def g(key: str, default: str = "") -> str:
        return os.environ.get(key) or env.get(key) or default

    return {
        "api_key": g("EVAL_TEXT_API_KEY", g("ANTHROPIC_API_KEY")),
        "api_base": g("EVAL_TEXT_API_BASE_URL", g("ANTHROPIC_BASE_URL")),
        "model": g("EVAL_TEXT_MODEL", "openai/gpt-5.2"),
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


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def _linear(value: float, lo: float, hi: float, max_pts: float) -> float:
    """Higher value -> more points. Below lo=0, above hi=max."""
    if value <= lo:
        return 0.0
    if value >= hi:
        return max_pts
    return (value - lo) / (hi - lo) * max_pts


def _linear_inv(value: float, lo: float, hi: float, max_pts: float) -> float:
    """Lower value -> more points. At lo=max, at hi=0."""
    if value <= lo:
        return max_pts
    if value >= hi:
        return 0.0
    return (hi - value) / (hi - lo) * max_pts


# ---------------------------------------------------------------------------
# 1. File Delivery (15 pts)
# ---------------------------------------------------------------------------

def _eval_file_delivery(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, str] = {}
    pts = 0.0

    all_files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []

    # 1a. train_improved_model.py (5 pts)
    script = os.path.join(answer_dir, "train_improved_model.py")
    if os.path.isfile(script):
        size = os.path.getsize(script)
        if size > 200:
            pts += 5
            details["train_improved_model.py"] = f"5/5 - exists ({size} bytes)"
        else:
            pts += 2
            details["train_improved_model.py"] = f"2/5 - exists but very small ({size} bytes)"
    else:
        alt = [f for f in all_files if f.endswith(".py") and "train" in f.lower()]
        if alt:
            pts += 2
            details["train_improved_model.py"] = f"2/5 - wrong name, found {alt[0]}"
        else:
            details["train_improved_model.py"] = "0/5 - missing"

    # 1b. emotion_model.h5 (5 pts)
    model_path = os.path.join(answer_dir, "emotion_model.h5")
    if os.path.isfile(model_path):
        fsize = os.path.getsize(model_path)
        if fsize > 100_000:
            pts += 5
            details["emotion_model.h5"] = f"5/5 - exists ({fsize / 1024 / 1024:.1f} MB)"
        else:
            pts += 2
            details["emotion_model.h5"] = f"2/5 - suspiciously small ({fsize} bytes)"
    else:
        alt = [f for f in all_files if f.endswith((".h5", ".keras", ".savedmodel"))]
        if alt:
            pts += 2
            details["emotion_model.h5"] = f"2/5 - wrong name, found {alt[0]}"
        else:
            details["emotion_model.h5"] = "0/5 - missing"

    # 1c. metrics.json (5 pts)
    metrics_path = os.path.join(answer_dir, "metrics.json")
    if os.path.isfile(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                m = json.load(f)
            required = {"val_acc", "train_acc", "macro_f1", "per_class_f1"}
            present = required & set(m.keys())
            if present == required:
                # Validate types
                ok = True
                for k in ("val_acc", "train_acc", "macro_f1"):
                    v = m[k]
                    if not isinstance(v, (int, float)):
                        ok = False
                pcf = m.get("per_class_f1", [])
                if not isinstance(pcf, list) or len(pcf) == 0:
                    ok = False
                if ok:
                    pts += 5
                    details["metrics.json"] = "5/5 - all required keys with valid types"
                else:
                    pts += 3
                    details["metrics.json"] = "3/5 - all keys present but some have invalid types"
            else:
                missing = required - present
                pts += 2
                details["metrics.json"] = f"2/5 - missing keys: {missing}"
        except Exception as e:
            pts += 1
            details["metrics.json"] = f"1/5 - parse error: {e}"
    else:
        details["metrics.json"] = "0/5 - missing"

    return pts, details


# ---------------------------------------------------------------------------
# 2. Code Quality (15 pts)
# ---------------------------------------------------------------------------

def _find_training_script(answer_dir: str) -> str:
    """Locate the training script, preferring exact name."""
    exact = os.path.join(answer_dir, "train_improved_model.py")
    if os.path.isfile(exact):
        return exact
    all_files = os.listdir(answer_dir) if os.path.isdir(answer_dir) else []
    alt = [f for f in all_files if f.endswith(".py") and "train" in f.lower()]
    if alt:
        return os.path.join(answer_dir, alt[0])
    return ""


def _eval_code_quality(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    details: Dict[str, str] = {}
    pts = 0.0

    script_path = _find_training_script(answer_dir)
    if not script_path:
        return 0.0, {"error": "no training script found"}

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return 0.0, {"error": f"cannot read script: {e}"}

    # 2a. Valid Python syntax (5 pts)
    try:
        ast.parse(code)
        pts += 5
        details["syntax"] = "5/5 - valid Python"
    except SyntaxError as e:
        details["syntax"] = f"0/5 - SyntaxError: {e}"
        return pts, details

    code_lower = code.lower()

    # 2b. TensorFlow/Keras imports (3 pts)
    has_tf = "import tensorflow" in code_lower or "from tensorflow" in code_lower
    has_keras = "keras" in code_lower
    if has_tf and has_keras:
        pts += 3
        details["tf_keras"] = "3/3 - TensorFlow + Keras detected"
    elif has_tf or has_keras:
        pts += 2
        details["tf_keras"] = "2/3 - partial TF/Keras import"
    else:
        details["tf_keras"] = "0/3 - no TF/Keras import"

    # 2c. Model saving logic (3 pts)
    save_pts = 0
    has_model_save = ("save" in code_lower and
                      (".h5" in code or ".keras" in code or "emotion_model" in code))
    has_metrics_save = ("metrics.json" in code or
                        ("json" in code_lower and "dump" in code_lower))
    if has_model_save:
        save_pts += 2
    if has_metrics_save:
        save_pts += 1
    pts += save_pts
    details["save_logic"] = (
        f"{save_pts}/3 - model save: {'yes' if has_model_save else 'no'}, "
        f"metrics save: {'yes' if has_metrics_save else 'no'}"
    )

    # 2d. Training pipeline (4 pts)
    fit_pts = 0
    has_fit = ".fit(" in code or ".fit_generator(" in code
    has_compile = ".compile(" in code
    has_data_load = any(k in code_lower for k in [
        "image_dataset_from_directory", "imagedatagenerator",
        "flow_from_directory", "kagglehub",
    ])
    has_metrics_compute = any(k in code_lower for k in [
        "f1_score", "classification_report", "f1",
        "sklearn", "scikit",
    ])
    if has_fit:
        fit_pts += 1
    if has_compile:
        fit_pts += 1
    if has_data_load:
        fit_pts += 1
    if has_metrics_compute:
        fit_pts += 1
    pts += fit_pts
    details["training_pipeline"] = (
        f"{fit_pts}/4 - fit: {'y' if has_fit else 'n'}, "
        f"compile: {'y' if has_compile else 'n'}, "
        f"data_load: {'y' if has_data_load else 'n'}, "
        f"metrics_compute: {'y' if has_metrics_compute else 'n'}"
    )

    return pts, details


# ---------------------------------------------------------------------------
# 3. Overall Accuracy (30 pts) - val_acc
# ---------------------------------------------------------------------------

def _eval_accuracy(metrics: dict) -> Tuple[float, Dict[str, Any]]:
    val_acc = float(metrics.get("val_acc", 0.0))
    pts = _linear(val_acc, 0.50, 0.90, 30.0)
    return pts, {"val_acc": f"{val_acc:.4f}", "score": f"{pts:.1f}/30"}


# ---------------------------------------------------------------------------
# 4. Class Balance (20 pts) - macro_f1 (12) + min per-class f1 (8)
# ---------------------------------------------------------------------------

def _eval_class_balance(metrics: dict) -> Tuple[float, Dict[str, Any]]:
    macro_f1 = float(metrics.get("macro_f1", 0.0))
    per_class_f1 = [float(x) for x in metrics.get("per_class_f1", [])]
    min_f1 = min(per_class_f1) if per_class_f1 else 0.0

    macro_pts = _linear(macro_f1, 0.45, 0.85, 12.0)
    min_pts = _linear(min_f1, 0.30, 0.70, 8.0)

    return macro_pts + min_pts, {
        "macro_f1": f"{macro_f1:.4f}",
        "macro_f1_score": f"{macro_pts:.1f}/12",
        "min_per_class_f1": f"{min_f1:.4f}",
        "min_f1_score": f"{min_pts:.1f}/8",
        "per_class_f1": [f"{x:.4f}" for x in per_class_f1],
    }


# ---------------------------------------------------------------------------
# 5. Generalization (10 pts) - overfitting gap
# ---------------------------------------------------------------------------

def _eval_generalization(metrics: dict) -> Tuple[float, Dict[str, Any]]:
    train_acc = float(metrics.get("train_acc", 0.0))
    val_acc = float(metrics.get("val_acc", 0.0))
    gap = max(0.0, train_acc - val_acc)
    pts = _linear_inv(gap, 0.05, 0.15, 10.0)
    return pts, {
        "train_acc": f"{train_acc:.4f}",
        "val_acc": f"{val_acc:.4f}",
        "gap": f"{gap:.4f}",
        "score": f"{pts:.1f}/10",
    }


# ---------------------------------------------------------------------------
# 6. Methodology - LLM Judge (10 pts)
# ---------------------------------------------------------------------------

_METHODOLOGY_PROMPT = """\
You are a strict ML code reviewer evaluating a facial emotion recognition training script.

The baseline is a simple 3-layer CNN (Conv2D 32->64->128, Dropout 0.4, Dense 64->5) \
trained on 128x128 RGB images from the human-face-emotions Kaggle dataset (5 classes). \
The student was asked to improve this baseline.

Possible improvement strategies include:
1. Transfer learning (pretrained backbone: MobileNetV2, EfficientNet, ResNet, etc.)
2. Data augmentation (RandomFlip, RandomRotation, RandomZoom, RandomContrast, etc.)
3. Advanced architecture (deeper CNN, residual connections, attention mechanisms, SE blocks)
4. Regularization (Dropout tuning, L2 regularization, BatchNormalization)
5. Optimization (learning rate scheduling, ReduceLROnPlateau, cosine annealing, tuned Adam)
6. Callbacks (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau)

Below is the training script:

```python
{code}
```

Score from 0-10 based on the number and quality of improvement strategies:
- 0-2: No meaningful improvement over baseline, or code just fabricates metrics
- 3-4: Uses 1 basic strategy (e.g., only data augmentation or only more layers)
- 5-6: Uses 2 strategies reasonably well
- 7-8: Uses 3+ strategies, shows solid ML engineering practice
- 9-10: Comprehensive approach with multiple well-implemented strategies

Reply ONLY with a JSON object:
{{"score": <int 0-10>, "strategies_found": [<list of strategy names>], "reason": "<brief explanation>"}}
"""


def _eval_methodology(answer_dir: str) -> Tuple[float, Dict[str, Any]]:
    script_path = _find_training_script(answer_dir)
    if not script_path:
        return 0.0, {"error": "no training script found"}

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception:
        return 0.0, {"error": "cannot read script"}

    # Try LLM evaluation first
    config = _get_text_eval_config(answer_dir)
    prompt = _METHODOLOGY_PROMPT.format(code=code[:12000])
    raw = _call_llm_judge(prompt, config)

    if raw:
        try:
            text = raw
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            result = json.loads(text)
            score = max(0, min(10, int(result.get("score", 0))))
            return float(score), {
                "source": "llm",
                "llm_score": score,
                "strategies": result.get("strategies_found", []),
                "reason": result.get("reason", ""),
            }
        except Exception as e:
            print(f"[RUBRIC] LLM response parse error: {e}")

    # Fallback: keyword-based heuristic (conservative, max 6/10)
    code_lower = code.lower()
    found: List[str] = []

    if any(k in code_lower for k in [
        "mobilenetv2", "efficientnet", "resnet", "vgg", "inception",
        "densenet", "xception", "nasnet", "pretrained",
        "include_top=false", "applications.",
    ]):
        found.append("transfer_learning")

    if any(k in code_lower for k in [
        "randomflip", "randomrotation", "randomzoom", "randomcontrast",
        "randombrightness", "imagedatagenerator", "augment",
        "data_augmentation", "horizontal_flip", "rotation_range",
    ]):
        found.append("data_augmentation")

    if any(k in code_lower for k in [
        "batchnormalization", "batch_normalization",
        "l2(", "regularizers.l2", "kernel_regularizer",
    ]):
        found.append("regularization")

    if any(k in code_lower for k in [
        "reducelronplateau", "learningratescheduler",
        "cosine", "warmup", "exponentialdecay",
        "learning_rate=", "lr_schedule",
    ]):
        found.append("lr_scheduling")

    if any(k in code_lower for k in [
        "earlystopping", "modelcheckpoint",
        "early_stopping", "model_checkpoint",
    ]):
        found.append("callbacks")

    if any(k in code_lower for k in [
        "residual", "attention", "se_block", "squeeze",
        "skip_connection", "globalaveragepooling",
    ]):
        found.append("advanced_architecture")

    # Dropout is already in baseline, only count if tuned or additional
    dropout_count = code_lower.count("dropout")
    if dropout_count >= 3:
        if "regularization" not in found:
            found.append("regularization")

    score = min(6, len(found) * 2)
    return float(score), {
        "source": "fallback_heuristic",
        "strategies_found": found,
        "score": score,
    }


# ===========================================================================
# Main evaluate / print_report
# ===========================================================================

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate agent output for facial emotion recognition model improvement.

    Args:
        answer_dir: absolute path to the agent output directory

    Returns:
        (score, report) where score is int 0-100
    """
    report: Dict[str, Any] = {}

    # 1. File delivery (15 pts)
    s1, r1 = _eval_file_delivery(answer_dir)
    report["1_file_delivery"] = {"score": round(s1, 1), "max": 15, "details": r1}

    # 2. Code quality (15 pts)
    s2, r2 = _eval_code_quality(answer_dir)
    report["2_code_quality"] = {"score": round(s2, 1), "max": 15, "details": r2}

    # Load metrics for dimensions 3-5
    metrics_path = os.path.join(answer_dir, "metrics.json")
    metrics: dict = {}
    metrics_ok = False
    if os.path.isfile(metrics_path):
        try:
            with open(metrics_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)
            # Validate minimum required keys
            if all(k in metrics for k in ("val_acc", "train_acc", "macro_f1", "per_class_f1")):
                metrics_ok = True
        except Exception:
            pass

    if metrics_ok:
        s3, r3 = _eval_accuracy(metrics)
        report["3_overall_accuracy"] = {"score": round(s3, 1), "max": 30, "details": r3}

        s4, r4 = _eval_class_balance(metrics)
        report["4_class_balance"] = {"score": round(s4, 1), "max": 20, "details": r4}

        s5, r5 = _eval_generalization(metrics)
        report["5_generalization"] = {"score": round(s5, 1), "max": 10, "details": r5}
    else:
        s3 = s4 = s5 = 0.0
        err_msg = "metrics.json missing or invalid (missing required keys)"
        report["3_overall_accuracy"] = {"score": 0, "max": 30, "details": {"error": err_msg}}
        report["4_class_balance"] = {"score": 0, "max": 20, "details": {"error": err_msg}}
        report["5_generalization"] = {"score": 0, "max": 10, "details": {"error": err_msg}}

    # 6. Methodology LLM (10 pts)
    s6, r6 = _eval_methodology(answer_dir)
    report["6_methodology"] = {"score": round(s6, 1), "max": 10, "details": r6}

    total = s1 + s2 + s3 + s4 + s5 + s6
    total = int(max(0, min(100, round(total))))

    report["total"] = total
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("=" * 60)
    print("Rubric Report: Facial Emotion Recognition Model Improvement")
    print("=" * 60)
    print(f"\nTotal Score: {score}/100\n")

    sections = [
        ("1_file_delivery", "1. File Delivery (15)"),
        ("2_code_quality", "2. Code Quality (15)"),
        ("3_overall_accuracy", "3. Overall Accuracy - val_acc (30)"),
        ("4_class_balance", "4. Class Balance - macro_f1 + min_f1 (20)"),
        ("5_generalization", "5. Generalization - overfitting gap (10)"),
        ("6_methodology", "6. Methodology - improvement strategies (10)"),
    ]

    for key, label in sections:
        sec = report.get(key, {})
        s = sec.get("score", 0)
        m = sec.get("max", 0)
        print(f"  {label}: {s}/{m}")
        details = sec.get("details", {})
        if isinstance(details, dict):
            for dk, dv in details.items():
                print(f"    {dk}: {dv}")
        print()

    print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = os.path.join(
            os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
        )

    if os.path.isdir(test_dir):
        print(f"Evaluating: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory not found: {test_dir}")
    sys.exit(0)
