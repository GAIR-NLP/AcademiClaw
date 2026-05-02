#!/usr/bin/env bash
# Sync experiment data + task catalog from academiclaw/ into public/data/
# Emits:
#   <model>_openclaw.json  per-model summary + per-task metrics
#   manifest.json          list of the per-model files
#   tasks-catalog.json     task metadata for the Tasks page
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPT_DIR/.."
BENCH="${ACADEMICLAW_DIR:-$ROOT/../academiclaw}"
DEST="$ROOT/public/data"

mkdir -p "$DEST"

python3 - "$BENCH" "$DEST" <<'PY'
import json, os, sys

bench, dest = sys.argv[1], sys.argv[2]

# $ per million tokens — keep in sync with ../../analysis/pricing.example.json
PRICING = {
    "claude-opus-4-6":        {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6":      {"input":  3.0, "output": 15.0},
    "gpt-5.4":                {"input":  2.0, "output":  8.0},
    "gemini-3.1-pro-preview": {"input": 1.25, "output":  5.0},
    "Qwen3.5-397B-A17B":      {"input":  0.3, "output":  1.2},
    "MiniMax-M2.7":           {"input":  0.5, "output":  2.0},
}
# Not part of the paper's 6-model core set; skip if present in the tree.
EXCLUDE_MODELS = {"glm51"}

CORE_TOOLS = ("read", "write", "edit", "exec", "process")

def extract_tool_counts(tool_freq):
    return {t: int(tool_freq.get(t, 0) or 0) for t in CORE_TOOLS}

def extract_safety_subscores(safety):
    cats = safety.get("categories", {}) or {}
    return {
        "s1": cats.get("S1_destructive_ops", {}).get("score"),
        "s2": cats.get("S2_info_leakage",    {}).get("score"),
        "s3": cats.get("S3_boundary",        {}).get("score"),
        "s4": cats.get("S4_privilege",       {}).get("score"),
        "s5": cats.get("S5_network_supply",  {}).get("score"),
    }

task_dirs = sorted(
    d for d in os.listdir(bench)
    if os.path.isdir(os.path.join(bench, d))
    and os.path.isfile(os.path.join(bench, d, "description.json"))
)

model_tasks = {}
for td in task_dirs:
    openclaw_dir = os.path.join(bench, td, "openclaw")
    if not os.path.isdir(openclaw_dir):
        continue
    for model_dir in os.listdir(openclaw_dir):
        if model_dir in EXCLUDE_MODELS:
            continue
        meta_path = os.path.join(openclaw_dir, model_dir, "meta_eval.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            model_tasks.setdefault(model_dir, {})[td] = json.load(open(meta_path))
        except Exception as exc:
            print(f"  [WARN] {meta_path}: {exc}", file=sys.stderr)

total_tasks = len(task_dirs)
files = []

for model_name, tasks_data in sorted(model_tasks.items()):
    if len(tasks_data) < total_tasks:
        print(f"  Skipping {model_name}: {len(tasks_data)}/{total_tasks} tasks")
        continue

    results = []
    sums = {
        "tokens": 0, "input_tokens": 0, "output_tokens": 0,
        "duration": 0.0, "tool_calls": 0,
        "safety": 0.0, "safety_n": 0,
        "s": {f"s{i}": [0.0, 0] for i in range(1, 6)},
        "tools": {t: 0 for t in CORE_TOOLS},
        "timeouts": 0,
    }

    for td in task_dirs:
        meta = tasks_data.get(td, {})
        score = meta.get("best_score", 0)
        timed_out = bool(meta.get("timed_out"))

        am = meta.get("aggregate_metrics", {}) or {}
        tokens_data = am.get("total_tokens", {}) or {}
        tokens = int(tokens_data.get("total", 0) or 0)
        input_tokens = int(tokens_data.get("input", 0) or 0)
        output_tokens = int(tokens_data.get("output", 0) or 0)
        duration = float(am.get("total_duration_seconds", 0) or 0)
        tool_calls = int(am.get("total_tool_calls", 0) or 0)
        tool_counts = extract_tool_counts(am.get("tool_frequency", {}) or {})

        safety = meta.get("safety_scores", {}) or {}
        safety_score = safety.get("safety_score")
        violations = safety.get("violation_count", {}) or {}
        sub = extract_safety_subscores(safety)

        row = {
            "task": td,
            "score": score,
            "tokens": tokens,
            "duration": round(duration, 1),
            "tool_calls": tool_calls,
            "tool_counts": tool_counts,
        }
        if timed_out:
            row["timed_out"] = True
        if safety_score is not None:
            row["safety_score"] = safety_score
            row["violations"] = {
                "CRITICAL": int(violations.get("CRITICAL", 0) or 0),
                "HIGH":     int(violations.get("HIGH", 0) or 0),
                "MEDIUM":   int(violations.get("MEDIUM", 0) or 0),
                "LOW":      int(violations.get("LOW", 0) or 0),
            }
            for k, v in sub.items():
                if v is not None:
                    row[k] = v
                    sums["s"][k][0] += v
                    sums["s"][k][1] += 1
            sums["safety"] += safety_score
            sums["safety_n"] += 1

        results.append(row)
        sums["tokens"] += tokens
        sums["input_tokens"] += input_tokens
        sums["output_tokens"] += output_tokens
        sums["duration"] += duration
        sums["tool_calls"] += tool_calls
        for t in CORE_TOOLS:
            sums["tools"][t] += tool_counts[t]
        if timed_out:
            sums["timeouts"] += 1

    scores = [r["score"] for r in results]
    passed = sum(1 for s in scores if s >= 75)
    avg_score = sum(scores) / len(scores) if scores else 0
    avg_safety = round(sums["safety"] / sums["safety_n"], 1) if sums["safety_n"] else None
    avg_sub = {k: round(v[0] / v[1], 1) for k, v in sums["s"].items() if v[1] > 0}
    avg_tool_counts = {t: round(sums["tools"][t] / total_tasks, 1) for t in CORE_TOOLS}

    price = PRICING.get(model_name)
    cost_per_task = total_cost = score_per_dollar = None
    if price and total_tasks:
        total_cost_raw = (
            sums["input_tokens"]  * price["input"]  / 1_000_000
          + sums["output_tokens"] * price["output"] / 1_000_000
        )
        cost_per_task = round(total_cost_raw / total_tasks, 2)
        total_cost = round(total_cost_raw, 2)
        score_per_dollar = round(avg_score / total_cost, 1) if total_cost > 0 else None

    experiment = {
        "experiment": {
            "model": model_name,
            "agent": "openclaw",
            "date": "",
        },
        "summary": {
            "total_tasks": total_tasks,
            "passed": passed,
            "failed": total_tasks - passed,
            "pass_rate": round(passed / total_tasks * 100, 1) if total_tasks else 0,
            "avg_score": round(avg_score, 1),
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "avg_safety": avg_safety,
            "total_tokens": sums["tokens"],
            "avg_tokens":        round(sums["tokens"]        / total_tasks) if total_tasks else 0,
            "avg_input_tokens":  round(sums["input_tokens"]  / total_tasks) if total_tasks else 0,
            "avg_output_tokens": round(sums["output_tokens"] / total_tasks) if total_tasks else 0,
            "total_duration":    round(sums["duration"], 1),
            "avg_duration":      round(sums["duration"] / total_tasks, 1) if total_tasks else 0,
            "avg_tool_calls":    round(sums["tool_calls"] / total_tasks, 1) if total_tasks else 0,
            "avg_tool_counts":   avg_tool_counts,
            "timeouts":          sums["timeouts"],
            "timeout_rate":      round(sums["timeouts"] / total_tasks * 100, 1) if total_tasks else 0,
            "cost_per_task":     cost_per_task,
            "total_cost":        total_cost,
            "score_per_dollar":  score_per_dollar,
            **{f"avg_{k}": v for k, v in avg_sub.items()},
        },
        "results": results,
    }

    filename = f"{model_name}_openclaw.json"
    with open(os.path.join(dest, filename), "w", encoding="utf-8") as f:
        json.dump(experiment, f, ensure_ascii=False, indent=2)
    files.append(filename)
    print(f"  Generated {filename} (avg={avg_score:.1f}, safety={avg_safety}, cost/task=${cost_per_task})")

with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump({"files": sorted(files)}, f, indent=2)
print(f"Generated manifest.json with {len(files)} experiment(s)")

# ---- tasks-catalog.json ----
TASK_CATEGORIES = {
    "en_a3c_ppo_training": "implement/rl-agent",
    "en_ai_science_report": "write/research-report",
    "en_bibtex_reference_gen": "generate/bibtex-references",
    "en_blackhole_visualization": "build/webgl-visualization",
    "en_breach_forensics": "analyze/security-breach",
    "en_bvh_path_tracing": "implement/path-tracing-renderer",
    "en_checkers_alphabeta_pruning": "implement/game-search-algorithm",
    "en_chip_edge_detection": "implement/edge-detection-pipeline",
    "en_cmo_proof": "solve/competition-math",
    "en_data_analysis_study_plan": "generate/study-plan",
    "en_data_merge_clean": "build/data-pipeline",
    "en_ddqn_mountaincar": "implement/rl-agent",
    "en_dijkstra_optimize": "optimize/graph-algorithm",
    "en_distributed_consistency_design": "design/distributed-system",
    "en_docker_env_config": "configure/docker-environment",
    "en_document_qa_citation": "analyze/document-qa",
    "en_dqn_implementation": "implement/rl-agent",
    "en_dqn_migration": "migrate/rl-framework",
    "en_emotion_recognition": "improve/image-classification-model",
    "en_f1_driver_advantage": "analyze/motorsport-lap-data",
    "en_fullstack_debug": "debug/fullstack-app",
    "en_geometry_circles": "solve/competition-geometry",
    "en_graph_algorithms": "implement/graph-algorithms",
    "en_hybrid_retrieval": "implement/hybrid-retrieval-system",
    "en_ksat_random_walk": "solve/theoretical-cs-proofs",
    "en_lc3_calculator": "implement/lc3-assembly-program",
    "en_llm_textbook_writing": "write/technical-textbook",
    "en_locking_dance_choreo": "design/dance-choreography",
    "en_log_security_analysis": "analyze/security-logs",
    "en_mahjong_rl_agent": "implement/rl-game-agent",
    "en_meeting_task_extraction": "extract/meeting-action-items",
    "en_omniasr_deployment": "deploy/speech-recognition-model",
    "en_os_lab3_debug": "debug/os-kernel-lab",
    "en_os_lab3_report": "write/os-lab-report",
    "en_paper_presentation": "generate/paper-analysis-presentation",
    "en_pokemon_game": "build/html5-rpg-game",
    "en_ppo_pendulum": "implement/rl-agent",
    "en_privacy_audit": "build/privacy-audit-pipeline",
    "en_quantum_mechanics": "solve/quantum-mechanics-derivation",
    "en_qwen_quantization_deploy": "deploy/quantized-llm",
    "en_rag_course_assistant": "implement/rag-system",
    "en_robocasa_camera_move": "implement/simulation-camera-control",
    "en_sift_algorithm_report": "write/algorithm-research-report",
    "en_sift_homework_report": "write/homework-report",
    "en_sleep_screen_stats": "analyze/statistical-data",
    "en_speculative_decoding": "implement/speculative-decoding-engine",
    "en_speech_model_report": "write/research-report",
    "en_sphere_uformer_export": "implement/point-cloud-export",
    "en_stock_greedy_algo": "solve/greedy-algorithm",
    "en_svd_model_merging": "implement/model-merging-algorithm",
    "en_time_tracking_dashboard": "build/frontend-dashboard",
    "en_tourism_purpose_prediction": "build/ml-classifier",
    "en_tts_research_report": "write/research-report",
    "en_vllm_prefill_flag": "fix/inference-engine-bug",
    "en_web_automation_scraping": "build/web-scraping-script",
    "zh_alc_zhishiku": "build/knowledge-base",
    "zh_bisai_tongji": "analyze/esports-statistics",
    "zh_chepai_shibie": "build/ocr-gui-app",
    "zh_chuanxi_diaoyan": "plan/field-trip-logistics",
    "zh_datika_yueju": "build/answer-sheet-grader",
    "zh_esp32_fenxi": "write/technical-analysis-report",
    "zh_excel_zhengli": "process/excel-spreadsheet",
    "zh_gailv_daan": "solve/probability-exam",
    "zh_geci_chuangzuo": "write/song-lyrics",
    "zh_hangzhou_lvyou": "plan/travel-itinerary",
    "zh_huaxue_jingsai": "solve/chemistry-olympiad",
    "zh_jiazu_tupu": "extract/literary-knowledge-graph",
    "zh_jidi_fuxi": "generate/study-materials",
    "zh_liaotian_niandu_baogao": "generate/annual-summary-report",
    "zh_lunwen_biji": "write/paper-reading-notes",
    "zh_majiang_jisuanqi": "implement/mahjong-calculator",
    "zh_miti_tuili": "solve/constraint-puzzle",
    "zh_miyu_jiemi": "solve/chinese-riddles",
    "zh_peiyang_jihua": "generate/curriculum-plan",
    "zh_piaofang_yuce_fenxi": "analyze/box-office-forecast",
    "zh_readme_shengcheng": "write/project-readme",
    "zh_shengwu_zongshu": "write/literature-review",
    "zh_shuangpin_jiucuo": "solve/input-method-puzzle",
    "zh_shuju_baogao": "generate/data-analysis-report",
    "zh_shujuwajue_xuanti": "plan/course-project-proposal",
    "zh_wangzhe_elo_baogao": "write/game-mechanics-report",
    "zh_wuli_jingsai": "solve/physics-olympiad",
    "zh_xushi_xuxie": "write/narrative-continuation",
    "zh_yanjiang_zhuanhua": "write/popular-science-speech",
    "zh_yuyanxue_aosai": "solve/linguistics-olympiad",
    "zh_zidong_jiashi_diaoyan": "write/research-survey",
    "zh_zuowen_pingfen": "evaluate/student-essays",
}

catalog = []
for td in task_dirs:
    desc_path = os.path.join(bench, td, "description.json")
    if not os.path.isfile(desc_path):
        continue
    with open(desc_path, "r", encoding="utf-8") as f:
        d = json.load(f)
    task_id = d.get("task_id", td)
    lang = "zh" if td.startswith("zh_") else "en"
    st = d.get("subtask1", {}) or {}
    deliverables = st.get("deliverables", []) or []
    query = st.get("query", "") or ""
    snippet = query[:150].replace("\n", " ").strip()
    if len(query) > 150:
        snippet += "..."
    catalog.append({
        "task_id": task_id,
        "slug": td,
        "name": d.get("task_name", task_id),
        "lang": lang,
        "category": TASK_CATEGORIES.get(td, ""),
        "deliverables_count": len(deliverables),
        "query_snippet": snippet,
    })

with open(os.path.join(dest, "tasks-catalog.json"), "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)
print(f"Generated tasks-catalog.json with {len(catalog)} tasks")
PY
