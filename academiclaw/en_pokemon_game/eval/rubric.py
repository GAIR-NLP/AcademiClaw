"""
Pokémon Gen 3 Style HTML5 Web Battle — Scoring Script (rewritten from scratch)
task_id: write_game_zijianhu_query3

Scoring Dimensions (Total: 100):
  1. functional_fidelity  (35 pts) — Gen3 battle mechanics completeness
     - 1a File delivery (5)
     - 1b Physical/Special type split (8)
     - 1c Damage formula (10)
     - 1d Critical hit/STAB/Type effectiveness (7)
     - 1e Enemy AI (5)
  2. physical_fidelity    (30 pts) — Visual assets & UI fidelity
     - 2a PokeAPI Sprite loading (10)
     - 2b Battle menu UI (5)
     - 2c HP bar rendering (5)
     - 2d Dialog box & pixel art style (3)
     - 2e Asset loader (4)
     - 2f Map engine + NPC (3)
  3. nostalgic_ritual      (20 pts) — GBA nostalgia
     - 3a Encounter transition effects (8)
     - 3b Text typewriter effect (6)
     - 3c Battle text messages (6)
  4. temporal_consistency  (15 pts) — Temporal correctness
     - 4a Lerp / easing animations (5)
     - 4b Input locking (5)
     - 4c Hit feedback animations (5)

Strategy: Static HTML source analysis + regex/keyword detection (deterministic scoring)
         + LLM-as-Judge comprehensive review (fine-tune ±5)
"""

import os
import re
import json
from typing import Tuple, Dict, Any

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────────
# Environment Config & LLM Tools
# ─────────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    """Load .env config from answer_dir and the query root directory"""
    values = {}
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

    def g(key, default=""):
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


# ─────────────────────────────────────────────────────────────
# HTML Reading & Regex Helpers
# ─────────────────────────────────────────────────────────────

def _read_html(answer_dir: str) -> str:
    """Read game.html, fallback to other .html files"""
    for name in ("game.html", "Game.html", "index.html"):
        p = os.path.join(answer_dir, name)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    if os.path.isdir(answer_dir):
        for name in sorted(os.listdir(answer_dir)):
            if name.lower().endswith(".html"):
                with open(os.path.join(answer_dir, name), "r",
                          encoding="utf-8", errors="ignore") as f:
                    return f.read()
    return ""


def _has(html: str, pattern: str, flags=re.IGNORECASE) -> bool:
    return bool(re.search(pattern, html, flags))


# ─────────────────────────────────────────────────────────────
# Dimension 1: Functional Fidelity (35 pts)
# ─────────────────────────────────────────────────────────────

def _score_functional(html: str) -> Tuple[int, dict]:
    pts = 0
    details = {}

    # 1a — File delivery (5 pts): Complete HTML structure
    has_html = _has(html, r"<html")
    has_script = _has(html, r"<script")
    has_canvas = _has(html, r"<canvas")
    s = 0
    if has_html and has_script and has_canvas:
        s = 5
    elif has_html and has_script:
        s = 4
    elif has_script:
        s = 2
    elif html.strip():
        s = 1
    pts += s
    details["1a_file_structure"] = (
        f"{s}/5 — html={'Y' if has_html else 'N'}, "
        f"script={'Y' if has_script else 'N'}, "
        f"canvas={'Y' if has_canvas else 'N'}"
    )

    # 1b — Physical/Special type split (8 pts)
    SPECIAL = ["fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark"]
    PHYSICAL = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel"]

    has_set_keyword = _has(html, r"(SpecialTypes|specialTypes|SPECIAL_TYPES|special_types)")
    has_is_fn = _has(html, r"(isSpecial|is_special|isPhysical|is_physical)")

    html_lower = html.lower()
    spec_cnt = sum(1 for t in SPECIAL if t in html_lower)
    phys_cnt = sum(1 for t in PHYSICAL if t in html_lower)

    s = 0
    if has_set_keyword and has_is_fn and spec_cnt >= 6 and phys_cnt >= 4:
        s = 8
    elif has_set_keyword and spec_cnt >= 5:
        s = 6
    elif (has_is_fn or has_set_keyword) and spec_cnt >= 4:
        s = 4
    elif spec_cnt >= 4 and phys_cnt >= 3:
        s = 3
    elif spec_cnt >= 3:
        s = 1
    pts += s
    details["1b_type_split"] = (
        f"{s}/8 — set/map={'Y' if has_set_keyword else 'N'}, "
        f"isSpecial={'Y' if has_is_fn else 'N'}, "
        f"spec={spec_cnt}/8, phys={phys_cnt}/9"
    )

    # 1c — Damage formula (10 pts): ((2*Lv/5+2)*Power*A/D)/50+2
    flat = html.replace("\n", " ")
    full_formulas = [
        r"\(\s*2\s*\*\s*[\w.]+\s*/\s*5\s*\+\s*2\s*\).*\*.*\*.*\/.*\/\s*50.*\+\s*2",
        r"2\s*\*\s*[\w.]+\s*/\s*5\s*\+\s*2\).*\*\s*[\w.]+\s*\*\s*[\w.]+\s*/\s*[\w.]+.*\/\s*50.*\+\s*2",
    ]
    has_full = any(_has(flat, p) for p in full_formulas)
    has_lv_frag = _has(html, r"2\s*\*\s*[\w.]*(level|lv|lvl)[\w.]*\s*/\s*5")
    has_50_frag = _has(html, r"/\s*50\s*[\)\s]*\+\s*2")

    s = 0
    if has_full:
        s = 10
    elif has_lv_frag and has_50_frag:
        s = 8
    elif has_lv_frag or has_50_frag:
        s = 4
    pts += s
    details["1c_damage_formula"] = (
        f"{s}/10 — full={'Y' if has_full else 'N'}, "
        f"2*lv/5={'Y' if has_lv_frag else 'N'}, "
        f"/50+2={'Y' if has_50_frag else 'N'}"
    )

    # 1d — Critical hit / STAB / Type effectiveness (7 pts)
    has_crit = _has(html, r"(crit|critical|暴击|critical hit)")
    has_stab = _has(html, r"(stab|same.?type.?attack|同属性加成)")
    has_chart = _has(html, r"(typeChart|type_chart|TypeChart|effectiveness|getEffective|type.*multiplier|属性克制)")
    has_crit_2x = _has(html, r"\*\s*2.*crit|crit.*\*\s*2|critMult.*=\s*2")
    has_stab_15 = _has(html, r"\*\s*1\.5|1\.5\s*.*stab|stab.*1\.5")

    s = 0
    if has_crit:
        s += 2
    if has_stab or has_stab_15:
        s += 2
    if has_chart:
        s += 2
    if has_crit_2x or has_stab_15:
        s += 1
    s = min(7, s)
    pts += s
    details["1d_mechanics"] = (
        f"{s}/7 — crit={'Y' if has_crit else 'N'}, "
        f"stab={'Y' if has_stab else 'N'}, "
        f"chart={'Y' if has_chart else 'N'}, "
        f"2x_crit={'Y' if has_crit_2x else 'N'}, "
        f"1.5_stab={'Y' if has_stab_15 else 'N'}"
    )

    # 1e — Enemy AI (5 pts)
    has_ai = _has(html, r"(selectEnemyMove|enemyAI|aiSelectMove|enemy.*move.*select|ai.*choose|chooseMove)")
    has_eff_pref = _has(html, r"(super\s*effective|type.*advantage|effectiveness.*>\s*1|克制)")
    has_ko = _has(html, r"(ko\b|kill|faint|斩杀|>=\s*\w+\.hp|hp\s*<=\s*0|lethal)")

    s = 0
    if has_ai and has_eff_pref and has_ko:
        s = 5
    elif has_ai and (has_eff_pref or has_ko):
        s = 3
    elif has_ai:
        s = 2
    elif has_eff_pref:
        s = 1
    pts += s
    details["1e_enemy_ai"] = (
        f"{s}/5 — ai_fn={'Y' if has_ai else 'N'}, "
        f"eff_pref={'Y' if has_eff_pref else 'N'}, "
        f"ko_check={'Y' if has_ko else 'N'}"
    )

    return pts, {"score": pts, "max": 35, "details": details}


# ─────────────────────────────────────────────────────────────
# Dimension 2: Physical Fidelity (30 pts)
# ─────────────────────────────────────────────────────────────

def _score_physical(html: str) -> Tuple[int, dict]:
    pts = 0
    details = {}

    # 2a — PokeAPI Sprite loading (10 pts)
    has_pokeapi = _has(html, r"raw\.githubusercontent\.com/PokeAPI/sprites")
    has_front = _has(html, r"sprites/pokemon/\d+\.png|sprites/pokemon/\$|sprites/pokemon/['\"`]?\s*\+")
    has_back = _has(html, r"sprites/pokemon/back/")
    has_emerald = _has(html, r"generation-iii/emerald")

    s = 0
    if has_pokeapi and has_front and has_back:
        s = 10
    elif has_pokeapi and (has_front or has_back):
        s = 7
    elif has_pokeapi:
        s = 5
    elif has_front or has_back:
        s = 3
    pts += s
    details["2a_sprites"] = (
        f"{s}/10 — pokeapi={'Y' if has_pokeapi else 'N'}, "
        f"front={'Y' if has_front else 'N'}, "
        f"back={'Y' if has_back else 'N'}, "
        f"emerald={'Y' if has_emerald else 'N'}"
    )

    # 2b — Battle menu UI: FIGHT / BAG / RUN (5 pts)
    has_fight = _has(html, r"(?i)\bfight\b")
    has_bag = _has(html, r"(?i)\bbag\b")
    has_run = _has(html, r"(?i)\brun\b")
    menu_cnt = sum([has_fight, has_bag, has_run])

    s = 0
    if menu_cnt == 3:
        s = 5
    elif menu_cnt == 2:
        s = 3
    elif menu_cnt >= 1:
        s = 1
    pts += s
    details["2b_battle_menu"] = (
        f"{s}/5 — FIGHT={'Y' if has_fight else 'N'}, "
        f"BAG={'Y' if has_bag else 'N'}, "
        f"RUN={'Y' if has_run else 'N'}"
    )

    # 2c — HP bar rendering (5 pts)
    has_hp_bar = _has(html, r"(hp|health|HP).*bar|drawHp|hpBar|hp_bar|血条")
    has_hp_color = _has(html, r"(green|yellow|red|#[0-9a-fA-F]{3,6}).*(hp|health|bar)|hp.*(green|yellow|red)")
    has_hp_num = _has(html, r"(hp|HP)\s*[:/]\s*\w*(max|Max)|currentHp|current_hp|displayHp|\d+\s*/\s*\d+.*hp")
    has_trapezoid = _has(html, r"(trapezoid|梯形|beginPath.*lineTo.*lineTo.*lineTo)")

    s = 0
    if has_hp_bar and has_hp_color:
        s += 3
    elif has_hp_bar:
        s += 2
    if has_hp_num:
        s += 1
    if has_trapezoid:
        s += 1
    s = min(5, s)
    pts += s
    details["2c_hp_bar"] = (
        f"{s}/5 — bar={'Y' if has_hp_bar else 'N'}, "
        f"color={'Y' if has_hp_color else 'N'}, "
        f"numeric={'Y' if has_hp_num else 'N'}, "
        f"trapezoid={'Y' if has_trapezoid else 'N'}"
    )

    # 2d — Dialog box & pixel art style (3 pts)
    has_dialog = _has(html, r"(dialog|textbox|dialogue|对话框|messageBox|TextPrinter|Printer)")
    has_pixel = _has(html, r"image-rendering\s*:\s*pixelated")

    s = 0
    if has_dialog:
        s += 2
    if has_pixel:
        s += 1
    s = min(3, s)
    pts += s
    details["2d_dialog_pixel"] = (
        f"{s}/3 — dialog={'Y' if has_dialog else 'N'}, "
        f"pixelated={'Y' if has_pixel else 'N'}"
    )

    # 2e — Asset loader / Preloader (4 pts)
    has_loader_cls = _has(html, r"(AssetLoader|assetLoader|AssetManager|ResourceLoader|Preloader)")
    has_loading_txt = _has(html, r"(Loading\.\.\.|Press Start|加载中)")
    has_fallback = _has(html, r"(fallback|placeholder|onerror|onError)")
    has_cache = _has(html, r"(cache|Map\(\).*set|\.has\(url\))")

    s = 0
    if has_loader_cls:
        s += 2
    if has_loading_txt:
        s += 1
    if has_fallback:
        s += 1
    s = min(4, s)
    pts += s
    details["2e_asset_loader"] = (
        f"{s}/4 — class={'Y' if has_loader_cls else 'N'}, "
        f"loading_screen={'Y' if has_loading_txt else 'N'}, "
        f"fallback={'Y' if has_fallback else 'N'}, "
        f"cache={'Y' if has_cache else 'N'}"
    )

    # 2f — Map engine + NPC (3 pts)
    has_tile = _has(html, r"(MapEngine|mapEngine|tileSize|tile_size|tileMap|TILE)")
    has_npc = _has(html, r"(NPC|npc|rival|Rival)")
    has_grid = _has(html, r"(grid|tiles|mapData|map_data)\s*[=:]")

    s = 0
    if has_tile and has_npc:
        s = 3
    elif has_tile or (has_grid and has_npc):
        s = 2
    elif has_npc or has_grid:
        s = 1
    pts += s
    details["2f_map_npc"] = (
        f"{s}/3 — tile_engine={'Y' if has_tile else 'N'}, "
        f"NPC={'Y' if has_npc else 'N'}, "
        f"grid={'Y' if has_grid else 'N'}"
    )

    return pts, {"score": pts, "max": 30, "details": details}


# ─────────────────────────────────────────────────────────────
# Dimension 3: Nostalgic Ritual (20 pts)
# ─────────────────────────────────────────────────────────────

def _score_ritual(html: str) -> Tuple[int, dict]:
    pts = 0
    details = {}

    # 3a — Encounter transition effects (8 pts)
    has_trans_cls = _has(html, r"(Transition|transition|BattleTransition)")
    has_flash = _has(html, r"(flash|flicker|闪烁|white.*screen|fillStyle.*['\"]#?fff|fillRect.*white)")
    has_mosaic = _has(html, r"(mosaic|shutter|马赛克|horizontal.*bar|cell.*expand|pixelate)")
    has_fade = _has(html, r"(fade|fadeIn|fadeOut|alpha.*transition|淡入|淡出|globalAlpha)")

    s = 0
    if has_trans_cls:
        s += 3
    if has_flash:
        s += 2
    if has_mosaic:
        s += 2
    if has_fade:
        s += 1
    s = min(8, s)
    pts += s
    details["3a_transition"] = (
        f"{s}/8 — class={'Y' if has_trans_cls else 'N'}, "
        f"flash={'Y' if has_flash else 'N'}, "
        f"mosaic={'Y' if has_mosaic else 'N'}, "
        f"fade={'Y' if has_fade else 'N'}"
    )

    # 3b — Text typewriter effect (6 pts)
    has_tw_cls = _has(html, r"(TextPrinter|typewriter|TypeWriter|textPrinter|CharReveal)")
    has_char_by_char = _has(
        html,
        r"(charAt|substring|\.slice\s*\(\s*0|charIndex|char.*reveal|逐字|charIdx|displayedText)"
    )
    has_text_speed = _has(html, r"(speed|textSpeed|text_speed|delay|interval)\s*[=:]\s*\d")
    has_queue = _has(html, r"(queue|messages|textQueue|lines)\s*[=:]")

    s = 0
    if has_tw_cls and has_char_by_char:
        s = 6
    elif has_tw_cls or has_char_by_char:
        s = 4
    elif has_text_speed:
        s = 2
    pts += s
    details["3b_typewriter"] = (
        f"{s}/6 — class={'Y' if has_tw_cls else 'N'}, "
        f"char_iter={'Y' if has_char_by_char else 'N'}, "
        f"speed={'Y' if has_text_speed else 'N'}, "
        f"queue={'Y' if has_queue else 'N'}"
    )

    # 3c — Battle text messages (6 pts)
    checks = [
        ("super_eff", r"(super\s*effective|效果拔群|It's super effective|superEffective)"),
        ("not_eff", r"(not very effective|效果不佳|not effective|收效甚微|没有效果)"),
        ("crit_msg", r"(critical hit|暴击|A critical hit|要害攻击|要害)"),
        ("miss", r"(miss|未命中|attack missed|missed|没有命中|闪避)"),
        ("faint", r"(faint|倒下|knocked out|defeated|失去.*战斗能力|战斗不能)"),
    ]
    found_msgs = {name: _has(html, pat) for name, pat in checks}
    msg_cnt = sum(found_msgs.values())

    s = 0
    if msg_cnt >= 4:
        s = 6
    elif msg_cnt >= 3:
        s = 5
    elif msg_cnt >= 2:
        s = 3
    elif msg_cnt >= 1:
        s = 1
    pts += s
    msg_str = ", ".join(f"{k}={'Y' if v else 'N'}" for k, v in found_msgs.items())
    details["3c_battle_text"] = f"{s}/6 — {msg_str} (hit {msg_cnt}/5)"

    return pts, {"score": pts, "max": 20, "details": details}


# ─────────────────────────────────────────────────────────────
# Dimension 4: Temporal Consistency (15 pts)
# ─────────────────────────────────────────────────────────────

def _score_temporal(html: str) -> Tuple[int, dict]:
    pts = 0
    details = {}

    # 4a — Lerp / easing animations (5 pts)
    has_lerp = _has(html, r"\blerp\b")
    has_easing = _has(html, r"(easeOut|easeIn|easeInOut|easeCubic|easeOutCubic|easeInOutQuad)")
    has_hp_anim = _has(html, r"(animateHp|hpLerp|hp.*lerp|hp.*animate|displayHp|animatingHp|血条.*动画)")
    has_raf = _has(html, r"requestAnimationFrame")

    s = 0
    if has_lerp and has_easing:
        s += 3
    elif has_lerp or has_easing:
        s += 2
    if has_hp_anim:
        s += 1
    if has_raf:
        s += 1
    s = min(5, s)
    pts += s
    details["4a_animation"] = (
        f"{s}/5 — lerp={'Y' if has_lerp else 'N'}, "
        f"easing={'Y' if has_easing else 'N'}, "
        f"hp_anim={'Y' if has_hp_anim else 'N'}, "
        f"rAF={'Y' if has_raf else 'N'}"
    )

    # 4b — Input locking (5 pts)
    has_lock_var = _has(html, r"(inputLock|input_lock|lockInput|lock_input|isLocked|inputDisabled|canInput)")
    has_lock_on = _has(html, r"(inputLock|isLocked|canInput|input_lock)\s*=\s*(true|false)")
    # Check for both setting and clearing the lock
    has_lock_true = _has(html, r"(inputLock|isLocked|input_lock)\s*=\s*true|(canInput)\s*=\s*false")
    has_lock_false = _has(html, r"(inputLock|isLocked|input_lock)\s*=\s*false|(canInput)\s*=\s*true")

    s = 0
    if has_lock_var and has_lock_true and has_lock_false:
        s = 5
    elif has_lock_var and (has_lock_true or has_lock_false):
        s = 3
    elif has_lock_var:
        s = 2
    pts += s
    details["4b_input_lock"] = (
        f"{s}/5 — lock_var={'Y' if has_lock_var else 'N'}, "
        f"set_true={'Y' if has_lock_true else 'N'}, "
        f"set_false={'Y' if has_lock_false else 'N'}"
    )

    # 4c — Hit feedback animations (5 pts)
    has_shake = _has(html, r"(shake|震动|vibrate|shakeAnim)")
    has_blink = _has(html, r"(blink|hitFlash|flash.*sprite|visible\s*=\s*!|alpha.*toggle)")
    has_slide = _has(html, r"(slideIn|slide.*in|appear.*anim|entrance)")
    has_dmg_fx = _has(html, r"(damageAnim|hitAnim|knockback|hit.*effect|hitEffect)")

    fx_cnt = sum([has_shake, has_blink, has_slide, has_dmg_fx])
    s = 0
    if fx_cnt >= 3:
        s = 5
    elif fx_cnt >= 2:
        s = 4
    elif fx_cnt >= 1:
        s = 2
    pts += s
    details["4c_hit_feedback"] = (
        f"{s}/5 — shake={'Y' if has_shake else 'N'}, "
        f"blink={'Y' if has_blink else 'N'}, "
        f"slide={'Y' if has_slide else 'N'}, "
        f"dmg_fx={'Y' if has_dmg_fx else 'N'} (hit {fx_cnt}/4)"
    )

    return pts, {"score": pts, "max": 15, "details": details}


# ─────────────────────────────────────────────────────────────
# LLM-as-Judge Comprehensive Review (fine-tune ±5)
# ─────────────────────────────────────────────────────────────

_LLM_PROMPT = """\
You are an expert reviewer of Game Boy Advance / Pokémon Gen 3 style HTML5 games.
Please evaluate the Gen 3 fidelity of this game based on the following source code snippet (first 8000 characters).

### Source Code (excerpt)
```
{snippet}
```

### Scoring Dimensions
Please provide a score of 0-3 (integer) and a brief justification for each of the following four aspects:

1. **Mechanics Accuracy** (0-3): Is the damage formula implemented per Gen3 standards? Physical/Special split by type?
2. **Visual Fidelity** (0-3): Are PokeAPI Sprites used? Does the UI replicate GBA style (HP bar, menus)?
3. **Nostalgia** (0-3): Are transition effects GBA-style? Typewriter text effect?
4. **Code Structure** (0-3): Is there a clear layered architecture (MapEngine/BattleEngine/GameLoop/AssetManager)?

Please return strictly the following JSON (no other content):
```json
{{
  "mechanics": {{"score": 0, "reason": ""}},
  "visuals": {{"score": 0, "reason": ""}},
  "ritual": {{"score": 0, "reason": ""}},
  "code_quality": {{"score": 0, "reason": ""}},
  "total_adjustment": 0,
  "comment": ""
}}
```
`total_adjustment` is the suggested overall adjustment (-5 to +5). Positive means static detection may have underscored, negative means it may have overscored.
"""


def _llm_review(html: str, config: dict) -> Tuple[int, dict]:
    snippet = html[:8000]
    prompt = _LLM_PROMPT.format(snippet=snippet)
    raw = _call_llm_judge(prompt, config)
    if not raw:
        return 0, {"llm_available": False, "reason": "LLM unavailable, skipping review"}

    try:
        text = raw
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        result = json.loads(text)
        adj = max(-5, min(5, int(result.get("total_adjustment", 0))))
        return adj, {
            "llm_available": True,
            "mechanics": result.get("mechanics", {}),
            "visuals": result.get("visuals", {}),
            "ritual": result.get("ritual", {}),
            "code_quality": result.get("code_quality", {}),
            "adjustment": adj,
            "comment": result.get("comment", ""),
        }
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        return 0, {"llm_available": True, "parse_error": str(e), "raw": raw[:300]}


# ─────────────────────────────────────────────────────────────
# Main Entry Point
# ─────────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    """
    Evaluate the agent's output.

    Args:
        answer_dir: Absolute path to the agent output directory

    Returns:
        (score, report) — score: 0-100 integer, report: detailed report dict
    """
    html = _read_html(answer_dir)

    if not html:
        return 0, {
            "total": 0,
            "functional_fidelity": {"score": 0, "max": 35, "details": {"error": "No HTML file found"}},
            "physical_fidelity": {"score": 0, "max": 30, "details": {}},
            "nostalgic_ritual": {"score": 0, "max": 20, "details": {}},
            "temporal_consistency": {"score": 0, "max": 15, "details": {}},
            "llm_review": {},
            "comment": "No game.html submitted, cannot evaluate.",
        }

    f_pts, f_rep = _score_functional(html)
    p_pts, p_rep = _score_physical(html)
    n_pts, n_rep = _score_ritual(html)
    t_pts, t_rep = _score_temporal(html)

    static_total = f_pts + p_pts + n_pts + t_pts

    config = _get_text_eval_config(answer_dir)
    llm_adj, llm_info = _llm_review(html, config)

    total = max(0, min(100, static_total + llm_adj))

    if total >= 90:
        comment = "Excellent. Highly faithful Gen 3 visuals and mechanics, polished interaction feel."
    elif total >= 75:
        comment = "Good. Complete flow, mostly correct mechanics, room for improvement."
    elif total >= 60:
        comment = "Passing. Core flow is runnable, but fidelity is insufficient."
    elif total >= 40:
        comment = "Partially complete. Key mechanics or visual assets are missing."
    else:
        comment = "Failing. Missing critical mechanics or asset loading."

    report = {
        "total": total,
        "static_total": static_total,
        "functional_fidelity": f_rep,
        "physical_fidelity": p_rep,
        "nostalgic_ritual": n_rep,
        "temporal_consistency": t_rep,
        "llm_review": llm_info,
        "comment": comment,
    }
    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    """Print a formatted scoring report"""
    print("=" * 65)
    print("Pokémon Gen 3 HTML5 Web Battle — Scoring Report")
    print("=" * 65)
    adj = report.get("llm_review", {}).get("adjustment", 0)
    print(f"Total: {score}/100  (Static: {report.get('static_total', score)}, LLM adjustment: {adj:+d})")
    print()

    sections = [
        ("functional_fidelity", "1. Functional Fidelity (35 pts) — Gen3 battle mechanics"),
        ("physical_fidelity",   "2. Physical Fidelity (30 pts) — Visuals & UI fidelity"),
        ("nostalgic_ritual",    "3. Nostalgic Ritual (20 pts) — Transitions/typewriter/messages"),
        ("temporal_consistency","4. Temporal Consistency (15 pts) — Animation/input locking"),
    ]

    for key, label in sections:
        sec = report.get(key, {})
        sec_score = sec.get("score", 0)
        sec_max = sec.get("max", 0)
        print(f"{'─' * 55}")
        print(f"  {label}: {sec_score}/{sec_max}")
        for dk, dv in sec.get("details", {}).items():
            print(f"    {dk}: {dv}")
        print()

    llm = report.get("llm_review", {})
    if llm:
        print(f"{'─' * 55}")
        print("  LLM Comprehensive Review:")
        if llm.get("llm_available"):
            for k in ("mechanics", "visuals", "ritual", "code_quality"):
                item = llm.get(k, {})
                if isinstance(item, dict) and item:
                    print(f"    {k}: {item.get('score', '?')}/3 — {item.get('reason', '')}")
            print(f"    Adjustment: {llm.get('adjustment', 0):+d}")
            if llm.get("comment"):
                print(f"    Comment: {llm['comment']}")
        else:
            print(f"    {llm.get('reason', 'N/A')}")

    print()
    print(f"{'=' * 55}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 65)


if __name__ == "__main__":
    import sys

    test_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "gpt-5", "attempt_1"
    )
    if os.path.exists(test_dir):
        print(f"Evaluating directory: {test_dir}\n")
        s, r = evaluate(test_dir)
        print_report(s, r)
    else:
        print(f"Directory does not exist: {test_dir}")
    sys.exit(0)
