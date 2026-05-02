# -*- coding: utf-8 -*-
"""
Rubric for Time Tracking Dashboard Frontend Implementation

Total: 100 points

Scoring dimensions:
  I. Functionality (40 pts)
    1.1 JSON data correctly loaded and parsed (10 pts)
    1.2 Activity cards dynamically generated from JSON data (10 pts)
    1.3 View switching correctly updates all cards (10 pts)
    1.4 Error handling for missing/invalid JSON data (10 pts)
  II. Design and Layout (30 pts)
    2.1 Layout, colors, fonts, spacing match design guide (8 pts)
    2.2 Responsive design (8 pts)
    2.3 Hover and focus states (7 pts)
    2.4 No content overflow or layout issues (7 pts)
  III. Interactivity (15 pts)
    3.1 Buttons function properly and provide feedback (5 pts)
    3.2 Keyboard navigation and ARIA labels (5 pts)
    3.3 Transitions and animations (5 pts)
  IV. Code Quality (15 pts)
    4.1 Code is modular with well-defined functions (5 pts)
    4.2 Code is readable and follows best practices (5 pts)
    4.3 No redundant or unused code (5 pts)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import openai
except ImportError:
    openai = None


# ─────────────────────────────────────────────────────────
# Environment / LLM helpers
# ─────────────────────────────────────────────────────────

def _load_env(answer_dir: str) -> dict:
    values: Dict[str, str] = {}
    for env_dir in [answer_dir, os.path.join(os.path.dirname(__file__), "..")]:
        env_path = os.path.join(env_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
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


def _safe_read(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────
# Reference data (ground truth)
# ─────────────────────────────────────────────────────────

EXPECTED_DATA = [
    {"title": "Work", "weekly": 32, "daily": 5, "monthly": 103},
    {"title": "Play", "weekly": 10, "daily": 1, "monthly": 23},
    {"title": "Study", "weekly": 4, "daily": 0, "monthly": 13},
    {"title": "Exercise", "weekly": 4, "daily": 1, "monthly": 11},
    {"title": "Social", "weekly": 5, "daily": 1, "monthly": 21},
    {"title": "Self Care", "weekly": 2, "daily": 0, "monthly": 7},
]


# ─────────────────────────────────────────────────────────
# Embedded Playwright Test (Node.js)
# Runs a local HTTP server and tests the dashboard
# ─────────────────────────────────────────────────────────

EMBEDDED_TEST_JS = r"""
const http = require('http');
const fs = require('fs');
const path = require('path');

let chromium;
try { chromium = require('playwright').chromium; } catch(e) {
  try { chromium = require('playwright-core').chromium; } catch(e2) {
    console.error('Playwright not available'); process.exit(1);
  }
}

const ROOT = __dirname;
const PORT = 18787;
const DATA = JSON.parse(fs.readFileSync(path.join(ROOT, 'data.json'), 'utf-8'));

function ct(fp) {
  const ext = path.extname(fp).toLowerCase();
  const m = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8',
    '.js':'application/javascript; charset=utf-8','.json':'application/json; charset=utf-8',
    '.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg'};
  return m[ext] || 'application/octet-stream';
}

function startServer() {
  const srv = http.createServer((req, res) => {
    let u = decodeURIComponent(req.url.split('?')[0]);
    if (u === '/') u = '/index.html';
    const fp = path.join(ROOT, u);
    fs.stat(fp, (err, stat) => {
      if (err || !stat.isFile()) { res.writeHead(404); res.end('Not found'); return; }
      res.writeHead(200, {'Content-Type': ct(fp)});
      fs.createReadStream(fp).pipe(res);
    });
  });
  return new Promise(r => srv.listen(PORT, () => r(srv)));
}

async function run() {
  const report = {timestamp: new Date().toISOString(), results: [], summary: {passed:0, failed:0}};

  function add(name, pass, details) {
    report.results.push({name, status: pass ? 'pass' : 'fail', details: details || {}});
    if (pass) report.summary.passed++; else report.summary.failed++;
  }

  const server = await startServer();
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage();

  try {
    await page.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'load', timeout:15000});
    await page.waitForTimeout(1000);

    // 1) Cards rendered
    await page.waitForSelector('.card, .activity-card, [class*="card"]', {timeout:5000}).catch(()=>{});
    const cardCount = await page.locator('.card, .activity-card').count();
    add('cards_rendered', cardCount >= DATA.length, {cardCount, expected: DATA.length});

    // 2) Default weekly view
    let defaultWeekly = false;
    try {
      const weeklyBtn = page.getByRole('radio', {name: /weekly/i})
        .or(page.locator('[data-view="weekly"], [data-range="weekly"]')).first();
      const checked = await weeklyBtn.getAttribute('aria-checked').catch(()=>'');
      const hasActive = await weeklyBtn.evaluate(el =>
        el.classList.contains('is-active') || el.classList.contains('active')
      ).catch(()=>false);
      defaultWeekly = checked === 'true' || hasActive;
    } catch(_){}
    add('default_weekly', defaultWeekly, {});

    // Helper: get text from current/previous elements
    async function getCardTexts() {
      const cur = await page.$$eval(
        '.current-hours, .card__current, .card-current, [class*="current"]',
        els => els.map(e => (e.textContent||'').trim())
      );
      const prev = await page.$$eval(
        '.previous-hours, .card__previous, .card-previous, [class*="previous"]',
        els => els.map(e => (e.textContent||'').trim())
      );
      return {cur, prev};
    }

    // 3) Weekly data validation
    let weeklyDataOk = false;
    try {
      const weeklyBtn = page.getByRole('radio', {name: /weekly/i})
        .or(page.locator('[data-view="weekly"], [data-range="weekly"]')).first();
      await weeklyBtn.click();
      await page.waitForTimeout(400);
      const {cur} = await getCardTexts();
      weeklyDataOk = cur.length >= DATA.length;
      for (let i = 0; i < DATA.length && weeklyDataOk; i++) {
        const expected = String(DATA[i].timeframes.weekly.current);
        if (!cur[i] || !cur[i].includes(expected)) weeklyDataOk = false;
      }
    } catch(_){}
    add('weekly_data', weeklyDataOk, {});

    // 4) Daily data validation
    let dailyDataOk = false;
    try {
      const dailyBtn = page.getByRole('radio', {name: /daily/i})
        .or(page.locator('[data-view="daily"], [data-range="daily"]')).first();
      await dailyBtn.click();
      await page.waitForTimeout(400);
      const {cur, prev} = await getCardTexts();
      dailyDataOk = cur.length >= DATA.length;
      for (let i = 0; i < DATA.length && dailyDataOk; i++) {
        const expected = String(DATA[i].timeframes.daily.current);
        if (!cur[i] || !cur[i].includes(expected)) dailyDataOk = false;
      }
      if (prev.length > 0 && !prev[0].toLowerCase().includes('yesterday')) dailyDataOk = false;
    } catch(_){}
    add('daily_data', dailyDataOk, {});

    // 5) Monthly data validation
    let monthlyDataOk = false;
    try {
      const monthlyBtn = page.getByRole('radio', {name: /monthly/i})
        .or(page.locator('[data-view="monthly"], [data-range="monthly"]')).first();
      await monthlyBtn.click();
      await page.waitForTimeout(400);
      const {cur, prev} = await getCardTexts();
      monthlyDataOk = cur.length >= DATA.length;
      for (let i = 0; i < DATA.length && monthlyDataOk; i++) {
        const expected = String(DATA[i].timeframes.monthly.current);
        if (!cur[i] || !cur[i].includes(expected)) monthlyDataOk = false;
      }
      if (prev.length > 0 && !prev[0].toLowerCase().includes('last month')) monthlyDataOk = false;
    } catch(_){}
    add('monthly_data', monthlyDataOk, {});

    // 6) ARIA radiogroup
    const rgCount = await page.locator('[role="radiogroup"]').count();
    add('aria_radiogroup', rgCount >= 1, {count: rgCount});

    // 7) Keyboard navigation
    let kbOk = false;
    try {
      const dailyBtn = page.getByRole('radio', {name: /daily/i})
        .or(page.locator('[data-view="daily"]')).first();
      await dailyBtn.focus();
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(200);
      const focused = await page.evaluate(() => (document.activeElement?.textContent||'').trim());
      kbOk = !!focused && focused.toLowerCase() !== 'daily';
    } catch(_){}
    add('keyboard_nav', kbOk, {});

    // 8) Error handling — block data.json and reload
    let errorOk = false;
    try {
      await page.route('**/data.json', route =>
        route.fulfill({status:404, body:'{}', contentType:'application/json'})
      );
      await page.reload({waitUntil:'load'});
      await page.waitForTimeout(1500);
      const errVis = await page.locator('#error-region, .load-error, [role="alert"]')
        .isVisible().catch(()=>false);
      const bodyText = await page.locator('body').textContent();
      errorOk = errVis || (bodyText && (
        bodyText.includes('\u52a0\u8f7d') || bodyText.includes('error') ||
        bodyText.includes('Error') || bodyText.includes('fail') ||
        bodyText.includes('\u65e0\u6cd5')
      ));
    } catch(_){}
    add('error_handling', !!errorOk, {});

    // Restore data.json for remaining tests
    await page.unrouteAll().catch(()=>{});
    await page.reload({waitUntil:'load'}).catch(()=>{});
    await page.waitForTimeout(800);

    // 9) CSS Grid usage
    let gridUsed = false;
    try {
      gridUsed = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('*')).some(
          el => getComputedStyle(el).display === 'grid'
        );
      });
    } catch(_){}
    add('css_grid', gridUsed, {});

    // 10) Responsive layout
    let responsiveOk = false;
    try {
      await page.setViewportSize({width:1440, height:900});
      await page.waitForTimeout(300);
      const dBox = await page.locator('.card, .activity-card').first().boundingBox();
      await page.setViewportSize({width:375, height:667});
      await page.waitForTimeout(300);
      const mBox = await page.locator('.card, .activity-card').first().boundingBox();
      if (dBox && mBox && Math.abs(dBox.width - mBox.width) > 40) responsiveOk = true;
    } catch(_){}
    add('responsive', responsiveOk, {});

    // 11) Hover state
    let hoverOk = false;
    try {
      await page.setViewportSize({width:1024, height:768});
      await page.waitForTimeout(200);
      const btn = page.getByRole('radio', {name: /weekly/i})
        .or(page.locator('[data-view="weekly"]')).first();
      const before = await btn.evaluate(el => getComputedStyle(el).backgroundColor);
      await btn.hover();
      await page.waitForTimeout(300);
      const after = await btn.evaluate(el => getComputedStyle(el).backgroundColor);
      hoverOk = before !== after;
    } catch(_){}
    add('hover_state', hoverOk, {});

    // 12) Card titles
    let titlesOk = false;
    try {
      const titles = await page.$$eval(
        '.card-title, .card__title, .activity-title, h2',
        els => els.map(e => (e.textContent||'').trim())
      );
      const expected = ['Work','Play','Study','Exercise','Social','Self Care'];
      titlesOk = expected.every(t => titles.some(tt => tt.includes(t)));
    } catch(_){}
    add('card_titles', titlesOk, {});

  } catch(e) {
    add('test_error', false, {error: String(e)});
  } finally {
    await browser.close();
    server.close();
  }

  fs.writeFileSync(
    path.join(ROOT, '_rubric_report.json'),
    JSON.stringify(report, null, 2), 'utf-8'
  );
  console.log(JSON.stringify({summary: report.summary}));
  return report;
}

run().catch(err => { console.error(err); process.exit(1); });
"""


# ─────────────────────────────────────────────────────────
# File existence check
# ─────────────────────────────────────────────────────────

def _check_deliverables(ad: Path) -> Dict[str, bool]:
    required = ["index.html", "styles.css", "script.js"]
    found = {}
    for f in required:
        found[f] = (ad / f).exists()
    found["data.json"] = (ad / "data.json").exists()
    return found


# ─────────────────────────────────────────────────────────
# Run Playwright tests
# ─────────────────────────────────────────────────────────

def _run_playwright_test(ad: Path) -> Tuple[bool, dict]:
    node = shutil.which("node")
    if not node:
        return False, {}

    test_path = ad / "_rubric_test.js"
    report_path = ad / "_rubric_report.json"
    try:
        test_path.write_text(EMBEDDED_TEST_JS, encoding="utf-8")
    except Exception:
        return False, {}

    env = dict(os.environ)
    if "PLAYWRIGHT_BROWSERS_PATH" not in env:
        env["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/pw-browsers"

    try:
        subprocess.run(
            [node, str(test_path)],
            cwd=str(ad),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            text=True,
            env=env,
        )
    except Exception as e:
        print(f"[RUBRIC] Playwright test execution failed: {e}")
        _cleanup_test_files(ad)
        return False, {}

    report = {}
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass

    _cleanup_test_files(ad)

    if report and isinstance(report.get("results"), list) and len(report["results"]) > 0:
        return True, report
    return False, {}


def _cleanup_test_files(ad: Path):
    for f in ["_rubric_test.js", "_rubric_report.json"]:
        try:
            (ad / f).unlink(missing_ok=True)
        except Exception:
            pass


# Name mapping: our test names -> possible agent report name aliases
_NAME_ALIASES = {
    "cards_rendered": ["cards_rendered", "JSON data load and render card count", "card rendering", "load and render"],
    "default_weekly": ["default_weekly", "default view is weekly", "default view", "default"],
    "weekly_data": ["weekly_data", "weekly view data validation", "weekly view", "weekly"],
    "daily_data": ["daily_data", "daily view data validation", "daily view", "daily"],
    "monthly_data": ["monthly_data", "monthly view data validation", "monthly view", "monthly"],
    "aria_radiogroup": ["aria_radiogroup", "ARIA radiogroup exists", "ARIA radiogroup", "radiogroup"],
    "keyboard_nav": ["keyboard_nav", "keyboard navigation", "keyboard"],
    "error_handling": ["error_handling", "missing JSON error handling", "error handling", "error"],
    "css_grid": ["css_grid", "CSS Grid layout used", "CSS Grid", "grid"],
    "responsive": ["responsive", "responsive layout", "responsive"],
    "hover_state": ["hover_state", "hover state style change", "hover state", "hover"],
    "card_titles": ["card_titles", "title check", "card titles"],
}


def _find_result(results: list, name_key: str) -> Optional[dict]:
    # Exact match first
    for r in results:
        if r.get("name") == name_key:
            return r
    # Try aliases
    aliases = _NAME_ALIASES.get(name_key, [])
    for r in results:
        rname = r.get("name", "")
        for alias in aliases:
            if alias in rname or rname in alias:
                return r
    return None


def _result_passed(results: list, name_key: str) -> bool:
    r = _find_result(results, name_key)
    return r is not None and r.get("status") == "pass"


# ─────────────────────────────────────────────────────────
# Load agent's existing dashboard_report.json
# ─────────────────────────────────────────────────────────

def _load_agent_report(ad: Path) -> Optional[dict]:
    rp = ad / "dashboard_report.json"
    if not rp.exists():
        return None
    try:
        data = json.loads(rp.read_text(encoding="utf-8", errors="ignore"))
        if isinstance(data, dict) and isinstance(data.get("results"), list):
            return data
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────────────────
# Score from Playwright/report results
# ─────────────────────────────────────────────────────────

def _score_from_results(results: list) -> Tuple[Dict[str, float], Dict[str, str]]:
    scores: Dict[str, float] = {}
    details: Dict[str, str] = {}

    # 1.1 JSON load + render cards (10pts)
    if _result_passed(results, "cards_rendered"):
        scores["1.1"] = 10
        details["1.1 JSON load/render"] = "10/10 - 6 cards correctly rendered"
    else:
        r = _find_result(results, "cards_rendered")
        cnt = r.get("details", {}).get("cardCount", 0) if r else 0
        if cnt > 0:
            scores["1.1"] = 4
            details["1.1 JSON load/render"] = f"4/10 - Rendered {cnt} cards (expected 6)"
        else:
            scores["1.1"] = 0
            details["1.1 JSON load/render"] = "0/10 - No cards detected"

    # 1.2 Dynamic cards from JSON (10pts)
    if _result_passed(results, "weekly_data"):
        scores["1.2"] = 10
        details["1.2 Dynamic cards"] = "10/10 - Weekly data correct"
    elif _result_passed(results, "cards_rendered"):
        scores["1.2"] = 3
        details["1.2 Dynamic cards"] = "3/10 - Cards present but data incorrect"
    else:
        scores["1.2"] = 0
        details["1.2 Dynamic cards"] = "0/10"

    # 1.3 View switching (10pts)
    d_ok = _result_passed(results, "daily_data")
    m_ok = _result_passed(results, "monthly_data")
    if d_ok and m_ok:
        scores["1.3"] = 10
        details["1.3 View switching"] = "10/10 - Daily/Monthly switching both correct"
    elif d_ok or m_ok:
        scores["1.3"] = 5
        which = "Daily" if d_ok else "Monthly"
        details["1.3 View switching"] = f"5/10 - Only {which} view correct"
    else:
        scores["1.3"] = 0
        details["1.3 View switching"] = "0/10 - View switching not working"

    # 1.4 Error handling (10pts)
    if _result_passed(results, "error_handling"):
        scores["1.4"] = 10
        details["1.4 Error handling"] = "10/10 - Correctly handles JSON load failure"
    else:
        scores["1.4"] = 0
        details["1.4 Error handling"] = "0/10 - Does not handle JSON load error"

    # 2.1 Layout conformance (8pts)
    if _result_passed(results, "css_grid"):
        scores["2.1"] = 6
        details["2.1 Layout"] = "6/8 - Uses CSS Grid"
    else:
        scores["2.1"] = 0
        details["2.1 Layout"] = "0/8 - CSS Grid not detected"

    # 2.2 Responsive (8pts)
    if _result_passed(results, "responsive"):
        scores["2.2"] = 8
        details["2.2 Responsive"] = "8/8 - Clear desktop/mobile layout difference"
    else:
        scores["2.2"] = 0
        details["2.2 Responsive"] = "0/8 - No responsive difference detected"

    # 2.3 Hover/focus (7pts)
    if _result_passed(results, "hover_state"):
        scores["2.3"] = 7
        details["2.3 Hover/focus"] = "7/7 - Buttons have hover state change"
    else:
        scores["2.3"] = 0
        details["2.3 Hover/focus"] = "0/7 - No hover state detected"

    # 2.4 No overflow (7pts) — partial auto score
    if _result_passed(results, "cards_rendered") and _result_passed(results, "responsive"):
        scores["2.4"] = 5
        details["2.4 No overflow"] = "5/7 - Cards correctly rendered and responsive"
    elif _result_passed(results, "cards_rendered"):
        scores["2.4"] = 3
        details["2.4 No overflow"] = "3/7 - Cards rendered but responsive not verified"
    else:
        scores["2.4"] = 0
        details["2.4 No overflow"] = "0/7"

    # 3.1 Button feedback (5pts)
    if _result_passed(results, "default_weekly"):
        scores["3.1"] = 5
        details["3.1 Buttons"] = "5/5 - Default view correct and buttons provide feedback"
    elif _result_passed(results, "weekly_data") or _result_passed(results, "daily_data"):
        scores["3.1"] = 3
        details["3.1 Buttons"] = "3/5 - Buttons can switch but default state unclear"
    else:
        scores["3.1"] = 0
        details["3.1 Buttons"] = "0/5"

    # 3.2 ARIA / keyboard (5pts)
    aria_ok = _result_passed(results, "aria_radiogroup")
    kb_ok = _result_passed(results, "keyboard_nav")
    s = 0
    parts = []
    if aria_ok:
        s += 3
        parts.append("radiogroup exists")
    if kb_ok:
        s += 2
        parts.append("keyboard nav works")
    scores["3.2"] = s
    details["3.2 ARIA/keyboard"] = f"{s}/5" + ((" - " + " + ".join(parts)) if parts else "")

    # 3.3 Transitions (5pts) — auto-test gives partial
    scores["3.3"] = 2
    details["3.3 Transitions"] = "2/5 - Auto-test baseline score"

    return scores, details


# ─────────────────────────────────────────────────────────
# Static fallback analysis
# ─────────────────────────────────────────────────────────

def _static_analysis(ad: Path) -> Tuple[Dict[str, float], Dict[str, str]]:
    index = _safe_read(str(ad / "index.html"))
    script = _safe_read(str(ad / "script.js"))
    styles = _safe_read(str(ad / "styles.css"))

    scores: Dict[str, float] = {}
    details: Dict[str, str] = {"mode": "static_fallback (Playwright unavailable)"}

    # 1.1 JSON load (10)
    if re.search(r"fetch\s*\(\s*['\"].*data\.json['\"]", script, re.I):
        scores["1.1"] = 8
        details["1.1 JSON load"] = "8/10 - Code has fetch data.json"
    elif "data.json" in script:
        scores["1.1"] = 4
        details["1.1 JSON load"] = "4/10 - References data.json but non-standard fetch"
    else:
        scores["1.1"] = 0
        details["1.1 JSON load"] = "0/10"

    # 1.2 Dynamic cards (10)
    if re.search(r"createElement|innerHTML|insertAdjacentHTML|template", script, re.I):
        scores["1.2"] = 6
        details["1.2 Dynamic generation"] = "6/10 - Has DOM dynamic generation logic"
    else:
        scores["1.2"] = 0
        details["1.2 Dynamic generation"] = "0/10"

    # 1.3 View switching (10)
    views = sum(1 for v in ["daily", "weekly", "monthly"] if re.search(v, script, re.I))
    if views == 3:
        scores["1.3"] = 7
        details["1.3 View switching"] = "7/10 - Code contains references to all three views"
    elif views >= 2:
        scores["1.3"] = 3
        details["1.3 View switching"] = "3/10"
    else:
        scores["1.3"] = 0
        details["1.3 View switching"] = "0/10"

    # 1.4 Error handling (10)
    has_try = bool(re.search(r"try\s*\{", script) and re.search(r"catch", script))
    has_err = bool(re.search(r"error", index, re.I) or re.search(r"error|load failed", script, re.I))
    if has_try and has_err:
        scores["1.4"] = 7
        details["1.4 Error handling"] = "7/10 - Has try/catch + error message"
    elif has_try:
        scores["1.4"] = 3
        details["1.4 Error handling"] = "3/10 - Has try/catch"
    else:
        scores["1.4"] = 0
        details["1.4 Error handling"] = "0/10"

    # 2.1 Layout (8)
    if re.search(r"display\s*:\s*grid", styles, re.I):
        scores["2.1"] = 5
        details["2.1 Layout"] = "5/8 - CSS has grid"
    else:
        scores["2.1"] = 0
        details["2.1 Layout"] = "0/8"

    # 2.2 Responsive (8)
    media_count = len(re.findall(r"@media", styles, re.I))
    if media_count >= 2:
        scores["2.2"] = 6
        details["2.2 Responsive"] = f"6/8 - {media_count} @media queries"
    elif media_count >= 1:
        scores["2.2"] = 3
        details["2.2 Responsive"] = "3/8"
    else:
        scores["2.2"] = 0
        details["2.2 Responsive"] = "0/8"

    # 2.3 Hover/focus (7)
    if re.search(r":hover|:focus|focus-visible|focus-within", styles, re.I):
        scores["2.3"] = 5
        details["2.3 Hover/focus"] = "5/7 - CSS has hover/focus"
    else:
        scores["2.3"] = 0
        details["2.3 Hover/focus"] = "0/7"

    # 2.4 No overflow (7)
    if len(styles) > 200:
        scores["2.4"] = 3
        details["2.4 No overflow"] = "3/7"
    else:
        scores["2.4"] = 0
        details["2.4 No overflow"] = "0/7"

    # 3.1 Buttons (5)
    if re.search(r"addEventListener.*click|onclick", script, re.I):
        scores["3.1"] = 3
        details["3.1 Buttons"] = "3/5"
    else:
        scores["3.1"] = 0
        details["3.1 Buttons"] = "0/5"

    # 3.2 ARIA/keyboard (5)
    has_aria = bool(re.search(r'aria-|role=', index, re.I))
    has_kb = bool(re.search(r"ArrowLeft|ArrowRight|keydown", script, re.I))
    s = 0
    if has_aria:
        s += 3
    if has_kb:
        s += 2
    scores["3.2"] = s
    details["3.2 ARIA/keyboard"] = f"{s}/5"

    # 3.3 Transitions (5)
    if re.search(r"transition|animation|@keyframes", styles, re.I):
        scores["3.3"] = 3
        details["3.3 Transitions"] = "3/5"
    else:
        scores["3.3"] = 1
        details["3.3 Transitions"] = "1/5"

    return scores, details


# ─────────────────────────────────────────────────────────
# Code quality (LLM + heuristic fallback)
# ─────────────────────────────────────────────────────────

def _score_code_quality(ad: Path, config: dict) -> Tuple[float, Dict[str, str]]:
    script = _safe_read(str(ad / "script.js"))
    styles = _safe_read(str(ad / "styles.css"))
    index = _safe_read(str(ad / "index.html"))

    if not script and not index:
        return 0, {"error": "No code files"}

    prompt = (
        "You are a strict frontend code review expert. Please evaluate the quality of the following time tracking dashboard frontend code.\n\n"
        "Task requirements: Build a time tracking dashboard based on a Frontend Mentor challenge, using data.json as data source, "
        "implementing Daily/Weekly/Monthly view switching, using CSS Grid responsive layout.\n\n"
        "Score on the following three dimensions (integers):\n\n"
        "**4.1 Code Modularity (0-5 pts)**\n"
        "- 5: Functions have single responsibility, clear logic, appropriate abstraction\n"
        "- 3-4: Has function organization but some logic coupling\n"
        "- 1-2: Few functions, lots of logic piled together\n"
        "- 0: No function organization\n\n"
        "**4.2 Readability and Best Practices (0-5 pts)**\n"
        "- 5: Clear variable naming, consistent indentation, semantic HTML, follows modern JS best practices\n"
        "- 3-4: Basically readable but some non-standard patterns\n"
        "- 1-2: Poor readability\n"
        "- 0: Chaotic\n\n"
        "**4.3 No Redundant Code (0-5 pts)**\n"
        "- 5: Concise and efficient, no unused code\n"
        "- 3-4: Minor redundancy\n"
        "- 1-2: Obvious redundancy\n"
        "- 0: Large amount of unused code\n\n"
        "Reply strictly in the following JSON format (do not include anything else):\n"
        "```json\n"
        '{"modularity": {"score": 0, "reason": ""}, '
        '"readability": {"score": 0, "reason": ""}, '
        '"no_redundancy": {"score": 0, "reason": ""}, '
        '"total": 0}\n'
        "```\n\n"
        f"=== script.js (first 5000 chars) ===\n{script[:5000]}\n\n"
        f"=== styles.css (first 2500 chars) ===\n{styles[:2500]}\n\n"
        f"=== index.html (first 2500 chars) ===\n{index[:2500]}"
    )

    llm_response = _call_llm_judge(prompt, config)
    if llm_response:
        try:
            text = llm_response
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(text)
            mod = max(0, min(5, int(parsed.get("modularity", {}).get("score", 0))))
            read = max(0, min(5, int(parsed.get("readability", {}).get("score", 0))))
            nored = max(0, min(5, int(parsed.get("no_redundancy", {}).get("score", 0))))
            total = mod + read + nored
            return total, {
                "4.1 Modularity": f"{mod}/5 - {parsed.get('modularity', {}).get('reason', '')}",
                "4.2 Readability": f"{read}/5 - {parsed.get('readability', {}).get('reason', '')}",
                "4.3 No redundancy": f"{nored}/5 - {parsed.get('no_redundancy', {}).get('reason', '')}",
                "evaluator": "LLM",
            }
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass

    # Heuristic fallback
    score = 0.0
    details: Dict[str, str] = {"evaluator": "heuristic"}

    func_count = len(re.findall(
        r"function\s+\w+|const\s+\w+\s*=\s*(?:async\s+)?\(", script
    ))
    if func_count >= 5:
        score += 4
        details["4.1 Modularity"] = f"4/5 - {func_count} functions"
    elif func_count >= 3:
        score += 2
        details["4.1 Modularity"] = f"2/5 - {func_count} functions"
    else:
        details["4.1 Modularity"] = f"0/5 - {func_count} functions"

    if len(script) > 200 and script.count("\n") > 10:
        score += 3
        details["4.2 Readability"] = "3/5 - Code has basic structure"
    else:
        details["4.2 Readability"] = "0/5"

    score += 2
    details["4.3 No redundancy"] = "2/5 - Conservative score"

    return score, details


# ─────────────────────────────────────────────────────────
# Main evaluate function
# ─────────────────────────────────────────────────────────

def evaluate(answer_dir: str) -> Tuple[int, Dict[str, Any]]:
    ad = Path(answer_dir).resolve()

    # Check deliverables
    file_check = _check_deliverables(ad)
    if not file_check.get("index.html"):
        return 0, {
            "total_score": 0,
            "result_score": {
                "score": 0,
                "details": {"missing_files": file_check},
                "deductions": ["Missing core file index.html"],
            },
            "process_score": {"score": 0, "details": {}, "deductions": []},
            "comment": "Missing index.html, cannot evaluate.",
        }

    config = _get_text_eval_config(answer_dir)
    test_mode = "none"
    dim_scores: Dict[str, float] = {}
    dim_details: Dict[str, str] = {}

    # Strategy: try Playwright first, then agent report, then static
    pw_ok, pw_report = _run_playwright_test(ad)

    if pw_ok and pw_report.get("results"):
        test_mode = "playwright"
        dim_scores, dim_details = _score_from_results(pw_report["results"])
    else:
        agent_report = _load_agent_report(ad)
        if agent_report and agent_report.get("results"):
            test_mode = "agent_report"
            dim_scores, dim_details = _score_from_results(agent_report["results"])
        else:
            test_mode = "static_fallback"
            dim_scores, dim_details = _static_analysis(ad)

    # File missing penalty
    missing_files = [f for f, ok in file_check.items() if not ok and f != "data.json"]
    file_penalty = 0
    for mf in missing_files:
        file_penalty += 5
    if file_penalty > 0:
        dim_details["File missing penalty"] = f"-{file_penalty} pts (missing: {', '.join(missing_files)})"

    # Code quality
    code_score, code_details = _score_code_quality(ad, config)

    # Calculate dimension totals
    func_score = sum(dim_scores.get(k, 0) for k in ["1.1", "1.2", "1.3", "1.4"])
    design_score = sum(dim_scores.get(k, 0) for k in ["2.1", "2.2", "2.3", "2.4"])
    interact_score = sum(dim_scores.get(k, 0) for k in ["3.1", "3.2", "3.3"])

    total_raw = func_score + design_score + interact_score + code_score - file_penalty
    total = int(max(0, min(100, round(total_raw))))

    report: Dict[str, Any] = {
        "total_score": total,
        "test_mode": test_mode,
        "result_score": {
            "score": round(func_score + design_score, 1),
            "details": {
                "I. Functionality (40 pts)": {
                    k: v for k, v in dim_details.items() if k.startswith("1.")
                },
                "II. Design and Layout (30 pts)": {
                    k: v for k, v in dim_details.items() if k.startswith("2.")
                },
            },
            "deductions": [],
        },
        "process_score": {
            "score": round(interact_score + code_score, 1),
            "details": {
                "III. Interactivity (15 pts)": {
                    k: v for k, v in dim_details.items() if k.startswith("3.")
                },
                "IV. Code Quality (15 pts)": code_details,
            },
            "deductions": [],
        },
        "section_scores": {
            "Functionality": f"{func_score:.0f}/40",
            "Design/Layout": f"{design_score:.0f}/30",
            "Interactivity": f"{interact_score:.0f}/15",
            "Code Quality": f"{code_score:.0f}/15",
        },
        "comment": "",
    }

    if missing_files:
        report["result_score"]["deductions"].append(
            f"Missing files: {', '.join(missing_files)} (-{file_penalty} pts)"
        )

    if total >= 90:
        report["comment"] = "Excellent! Dashboard is fully functional, well-designed, and code is well-structured."
    elif total >= 75:
        report["comment"] = "Good. Task basically completed, some dimensions have room for improvement."
    elif total >= 60:
        report["comment"] = "Passing. Core features implemented but notable deficiencies exist."
    elif total >= 40:
        report["comment"] = "Partially completed. Key functionality or design has significant flaws."
    else:
        report["comment"] = "Failing. Task completion is seriously insufficient."

    return total, report


def print_report(score: int, report: Dict[str, Any]) -> None:
    print("=" * 70)
    print("Time Tracking Dashboard - Scoring Report")
    print("=" * 70)
    print(f"\nTotal Score: {score}/100  (Test mode: {report.get('test_mode', 'unknown')})")

    scores = report.get("section_scores", {})
    if scores:
        print("\nSection Scores:")
        for k, v in scores.items():
            print(f"  {k}: {v}")

    for key, label in [
        ("result_score", "Result Score (Functionality + Design)"),
        ("process_score", "Process Score (Interactivity + Code)"),
    ]:
        section = report.get(key, {})
        print(f"\n{'─' * 50}")
        print(f"[{label}] {section.get('score', 0)} pts")
        for cat, items in section.get("details", {}).items():
            print(f"\n  {cat}:")
            if isinstance(items, dict):
                for k2, v2 in items.items():
                    print(f"    {k2}: {v2}")
            else:
                print(f"    {items}")
        deds = section.get("deductions", [])
        for i, r in enumerate(deds, 1):
            print(f"  Deduction {i}: {r}")

    print(f"\n{'=' * 50}")
    print(f"Comment: {report.get('comment', '')}")
    print("=" * 70)


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
