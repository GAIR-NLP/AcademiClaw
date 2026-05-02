# AcademiClaw (ClawBench) — 全部 Query 详细内容

> 本文件列出 AcademiClaw benchmark 中全部 80 个 query 的完整内容，按语言（English / 中文）和任务名称字母序排列。

## 目录

### English Tasks (49)

- [en_a3c_ppo_training](#en_a3c_ppo_training)
- [en_ai_science_report](#en_ai_science_report)
- [en_bibtex_reference_gen](#en_bibtex_reference_gen)
- [en_blackhole_visualization](#en_blackhole_visualization)
- [en_breach_forensics](#en_breach_forensics)
- [en_bvh_path_tracing](#en_bvh_path_tracing)
- [en_checkers_alphabeta_pruning](#en_checkers_alphabeta_pruning)
- [en_chip_edge_detection](#en_chip_edge_detection)
- [en_cmo_proof](#en_cmo_proof)
- [en_data_analysis_study_plan](#en_data_analysis_study_plan)
- [en_ddqn_mountaincar](#en_ddqn_mountaincar)
- [en_dijkstra_optimize](#en_dijkstra_optimize)
- [en_distributed_consistency_design](#en_distributed_consistency_design)
- [en_docker_env_config](#en_docker_env_config)
- [en_document_qa_citation](#en_document_qa_citation)
- [en_dqn_implementation](#en_dqn_implementation)
- [en_dqn_migration](#en_dqn_migration)
- [en_emotion_recognition](#en_emotion_recognition)
- [en_f1_driver_advantage](#en_f1_driver_advantage)
- [en_fullstack_debug](#en_fullstack_debug)
- [en_geometry_circles](#en_geometry_circles)
- [en_graph_algorithms](#en_graph_algorithms)
- [en_ksat_random_walk](#en_ksat_random_walk)
- [en_lc3_calculator](#en_lc3_calculator)
- [en_locking_dance_choreo](#en_locking_dance_choreo)
- [en_log_security_analysis](#en_log_security_analysis)
- [en_mahjong_rl_agent](#en_mahjong_rl_agent)
- [en_meeting_task_extraction](#en_meeting_task_extraction)
- [en_omniasr_deployment](#en_omniasr_deployment)
- [en_os_lab3_debug](#en_os_lab3_debug)
- [en_os_lab3_report](#en_os_lab3_report)
- [en_paper_presentation](#en_paper_presentation)
- [en_pokemon_game](#en_pokemon_game)
- [en_ppo_pendulum](#en_ppo_pendulum)
- [en_privacy_audit](#en_privacy_audit)
- [en_qwen_quantization_deploy](#en_qwen_quantization_deploy)
- [en_rag_course_assistant](#en_rag_course_assistant)
- [en_robocasa_camera_move](#en_robocasa_camera_move)
- [en_sift_algorithm_report](#en_sift_algorithm_report)
- [en_sift_homework_report](#en_sift_homework_report)
- [en_sleep_screen_stats](#en_sleep_screen_stats)
- [en_speculative_decoding](#en_speculative_decoding)
- [en_speech_model_report](#en_speech_model_report)
- [en_sphere_uformer_export](#en_sphere_uformer_export)
- [en_stock_greedy_algo](#en_stock_greedy_algo)
- [en_svd_model_merging](#en_svd_model_merging)
- [en_time_tracking_dashboard](#en_time_tracking_dashboard)
- [en_tts_research_report](#en_tts_research_report)
- [en_web_automation_scraping](#en_web_automation_scraping)

### 中文 Tasks (31)

- [zh_alc_zhishiku](#zh_alc_zhishiku)
- [zh_bisai_tongji](#zh_bisai_tongji)
- [zh_chepai_shibie](#zh_chepai_shibie)
- [zh_chuanxi_diaoyan](#zh_chuanxi_diaoyan)
- [zh_datika_yueju](#zh_datika_yueju)
- [zh_esp32_fenxi](#zh_esp32_fenxi)
- [zh_excel_zhengli](#zh_excel_zhengli)
- [zh_gailv_daan](#zh_gailv_daan)
- [zh_geci_chuangzuo](#zh_geci_chuangzuo)
- [zh_hangzhou_lvyou](#zh_hangzhou_lvyou)
- [zh_huaxue_jingsai](#zh_huaxue_jingsai)
- [zh_jiazu_tupu](#zh_jiazu_tupu)
- [zh_jidi_fuxi](#zh_jidi_fuxi)
- [zh_liaotian_niandu_baogao](#zh_liaotian_niandu_baogao)
- [zh_majiang_jisuanqi](#zh_majiang_jisuanqi)
- [zh_miti_tuili](#zh_miti_tuili)
- [zh_miyu_jiemi](#zh_miyu_jiemi)
- [zh_peiyang_jihua](#zh_peiyang_jihua)
- [zh_piaofang_yuce_fenxi](#zh_piaofang_yuce_fenxi)
- [zh_readme_shengcheng](#zh_readme_shengcheng)
- [zh_shengwu_zongshu](#zh_shengwu_zongshu)
- [zh_shuangpin_jiucuo](#zh_shuangpin_jiucuo)
- [zh_shuju_baogao](#zh_shuju_baogao)
- [zh_shujuwajue_xuanti](#zh_shujuwajue_xuanti)
- [zh_wangzhe_elo_baogao](#zh_wangzhe_elo_baogao)
- [zh_wuli_jingsai](#zh_wuli_jingsai)
- [zh_xushi_xuxie](#zh_xushi_xuxie)
- [zh_yanjiang_zhuanhua](#zh_yanjiang_zhuanhua)
- [zh_yuyanxue_aosai](#zh_yuyanxue_aosai)
- [zh_zidong_jiashi_diaoyan](#zh_zidong_jiashi_diaoyan)
- [zh_zuowen_pingfen](#zh_zuowen_pingfen)

---

## English Tasks

### en_a3c_ppo_training

Query 2: A3C + PPO on Pendulum-v1

You are a deep reinforcement learning expert. Implement and train both A3C and PPO algorithms in this working directory, using Gymnasium's Pendulum-v1 environment.

Requirements and deliverables:
- train.py: Training entry point. Supports --algo a3c|ppo, sets hyperparameters, and calls the corresponding algorithm.
- a3c.py: A3C training implementation (torch.multiprocessing for multi-process, n-step updates, async global network updates).
- ppo.py: PPO training implementation (GAE advantage estimation, clipped surrogate objective, mini-batch multi-epoch iteration).
- models.py: Actor-Critic network. Actor output mapped to the action space [-2, 2] (tanh + scaling), Critic outputs V(s).
- utils.py: Logging, checkpoint save/load, TensorBoard recording.
- evaluate.py: Load a model and evaluate it, with rendering support.
- README.md: Describe dependency installation, run commands, and TensorBoard usage.

Training objective:
- Within 500-1000 episodes, average reward should converge to -300 or higher.
- Use reward normalization or gradient clipping to ensure stability.

Notes:
- All code and output files should be written directly into the current working directory.
- You may use context/A3C+PPO.pdf as a reference, but do not copy reference answers or scoring criteria into this file.
- The evaluation script will call eval/rubric.py after each attempt to score and generate feedback.

---

### en_ai_science_report

Query:
---

[Query Description]
Write a technical, industry, or policy research analysis report on "Applications of Artificial Intelligence Technology in Scientific Research."

**Task Objective**: Independently complete an academically rigorous research analysis report that examines the applications, trends, challenges, and industry or policy implications of AI technology in scientific research.

**Process and Requirements**:

1. **Format**: Write the report in **LaTeX**.
2. **Length**: The body text must be in English, with the main text spanning **4-6 pages** (strict page/word count control).
3. **References**: At least **10** references from reliable sources. Blog-type non-professional sources such as CSDN, Zhihu, etc. are strictly prohibited.
4. **Originality and Standards**: Ensure low duplication rate/originality; large-scale plagiarism or content clearly unrelated to the topic is prohibited.
5. **Content Requirements**: The report should analyze from the dimensions of technical applications, scientific impact, industry trends, challenges, and policy/ethics.

**Suggested Steps**: First read `context/operation_list.md` for writing steps and constraints, then read the background and reference material guidelines in `context/problem_context.md`, and write the LaTeX report following an academic report structure, saving it to the current directory.

**Output Format**: Save the final report as a **LaTeX source file** (e.g., `report.tex`) or also provide the compiled PDF (e.g., `report.pdf`) in the current directory.

[Context]
File list:
- `context/operation_list.md`: Writing steps and instructions
- `context/problem_context.md`: Task background and reference material guidelines

---

### en_bibtex_reference_gen

Query:
---

**Task Description**

Task: You are a researcher writing the references section of your paper. You need to look up and compile BibTeX entries for all 41 papers listed in `paper_title.md`, and consolidate them into a single file `ref.bib` for LaTeX citation. Specifically:
    - Use academic search engines (e.g., Google Scholar, Semantic Scholar, ResearchGate, IEEE Xplore, ACM Digital Library) or visit the original paper pages / conference/journal websites to find the BibTeX entry for each paper.
    - Ensure each BibTeX entry contains complete and accurate information, including authors, title, publication name, volume, issue, pages, year, DOI, etc. Each paper should correspond to exactly one BibTeX entry to avoid duplicates.

Expected output: A complete `ref.bib` file containing accurate BibTeX entries for all 41 papers listed in `paper_title.md` (authors, title, journal/conference, volume/issue, pages, year, DOI, etc.), ready for direct use in LaTeX bibliography.

**Context**

Paper titles:
`paper_title.md`

Academic search engine reference URLs:
- Google Scholar: https://scholar.google.com/
- Semantic Scholar: https://www.semanticscholar.org/
- ResearchGate: https://www.researchgate.net/
- IEEE Xplore: https://ieeexplore.ieee.org/
- ACM Digital Library: https://dl.acm.org/

---

### en_blackhole_visualization

```markdown
# Query 1:

## [Query Description]

I need to create a web-based "Interstellar"-style black hole visualization using Three.js. Core requirements are as follows:
1. Visual effects:
    - Recreate the movie's black hole with an accretion disk and gravitational lensing effect (appearing as a light ring surrounding the black hole).
    - Implement a "Backward Ray Tracing" algorithm; do not use ordinary geometric spheres.
    - The accretion disk should exhibit the "brighter on the left, darker on the right" Doppler effect.
    - The background should have a dynamic starfield with a breathing light effect, featuring blue supergiants, red dwarfs, and other colored stars. Density should be high but not distracting.
    - Do not cheat by pasting the original image as the background!

2. UI Interaction:
    - Add a "frosted glass" style card in the bottom-left corner, titled "GARGANTUA" (with gradient sci-fi font).
    - The card should clearly state the controls: left-click to rotate, right-click to pan, scroll wheel to zoom.
    - Add an animation control toggle switch (Toggle Switch), ensuring the HTML element ID is anim-toggle, and the corresponding `<input>` tag is actionable in the DOM tree (do not set display: none; you may use minimal opacity or absolute positioning offset) to facilitate automated testing capture.

3. Code requirements:
    - Output as a **single HTML file**, and the file must contain **complete, runnable black hole rendering code** (Three.js scene, ray tracing/shaders, accretion disk, starfield, etc.) that displays the black hole when opened in a browser.
    - Do not just generate a "task description + placeholder comments" page; also do not simply run generate_visualization.py and consider it done - that script generates a placeholder page, and you must replace it with a real visualization implementation.
    - Key visual adjustment parameter locations must have comments for easy modification.

## [Context]
1. Reference image: `context/query1_Reference_Image.jpg`: (Description: a glowing accretion disk surrounding a central dark body, with light bending into curved rings above and below the black hole, brighter on the left side, darker on the right side)

2. Dependency libraries (CDN):
    - Three.js: https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js
    - OrbitControls: https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/

3. Design constraints (based on historical conversations):
    - Physical parameters: black hole radius $\approx 1.0$, accretion disk inner edge $\approx 3.0$, outer edge $\approx 10.0$.
    - Interaction limits: zoom distance limited between 1.5 and 60.0.
    - Performance requirements: Ray Marching steps limited to 150 or fewer.
    - Pasting original images as background is not allowed.

## [Implementation Key Points] Must be implemented, otherwise the screen will be completely black or fail automated evaluation

1. **Ray construction (most critical for preventing black screen)**: **Do not** use `invViewMatrix`/`invProjectionMatrix` in the shader to reverse-project rays from NDC (error-prone, causing black screen). Instead, pass `iCameraPos`, `iCameraDir` (using `camera.getWorldDirection()`), `iCameraUp`, `iFov`, `iResolution`, and calculate `rayOrigin` and `rayDir` directly in the fragment shader using the formulas in the "Correct Implementation Guide."
2. **Fragment shader final color**: `outColor` must be composed of "starfield color + accretion disk/photon ring glow"; it cannot be unassigned or only output vec4(0,0,0,1). First accumulate accretion disk and lens glow along the ray via Ray Marching, add procedural starfield for escaped rays, then apply exposure/tone mapping before writing to outColor.
3. **Uniform updates every frame**: In animate(), you must update and pass: `iTime`, `iResolution`, `iCameraPos`, `iCameraDir`, `iCameraUp`, `iFov`, as well as `diskInner`/`diskOuter`/black hole radius, etc. `iCameraDir` must be updated every frame using `camera.getWorldDirection(vec)`.
4. **Exposure and brightness**: `exposure` or `toneMappingExposure` should be 1.0-2.0; accretion disk glow intensity must not be 0.
5. **OrbitControls**: Call `controls.update()` every frame, use the **same** PerspectiveCamera to render the full-screen quad and pass its position/getWorldDirection/up/fov into the shader.
6. **Animation toggle**: Must have `<input type="checkbox" id="anim-toggle" />` (may be inside a label), and in animate, determine whether to increment `iTime` based on the checked state.

## [Common Mistakes and Avoidance]

- **Completely black screen**: (1) **Do not** attach the full-screen quad to the camera (`camera.add(quad)` + `scene.add(camera)`), otherwise the quad may not be rendered -> black screen; the quad must use `scene.add(quad)`, with vertex shader using `gl_Position = vec4(position, 1.0)`. (2) **iResolution must not be (0,0)**, otherwise the fragment will produce NaN -> black screen; protect with `Math.max(..., 1)` before passing from JS, and also use `max(iResolution.x, 1.0)/max(iResolution.y, 1.0)` in the fragment for aspect ratio to prevent 0. (3) The fragment must write starfield + accretion disk/glow (including glow when absorbed or a minimum brightness) to outColor, with exposure >= 1.0. (4) The fragment shader must begin with `precision highp float;`, otherwise it may fail to compile or behave abnormally in some environments; Ray Marching loop upper bound should use a constant `#define MAX_STEPS 150`, avoid using uniform int as the for loop upper bound.
- **Rotation has no effect**: Ensure `controls.update()` is called every frame and camera position/getWorldDirection/up/fov are passed to the shader.
- **Black hole/disk suddenly disappears when zooming**: When the camera zooms out, the accretion disk disappears, likely because the step size is too large and skips y=0 in one step, or runs out of steps before reaching the disk. Use explicit ray-plane intersection with y=0 each step (see 4.1) to sample the disk surface, and/or use smaller step size in the disk region and larger step size in far regions, ensuring MAX_STEPS is sufficient.
- **Evaluation cannot find anim-toggle**: Use `<input type="checkbox" id="anim-toggle">`, do not hide with display:none; you may use opacity or positioning to place it inside the card.
- **Tech stack not scoring**: Must use THREE.ShaderMaterial (or RawShaderMaterial) and OrbitControls, and they must be visible in the code (e.g., THREE.ShaderMaterial, controls.update), otherwise automated evaluation will deduct points.

## [Correct Implementation Guide] Common causes of black screen and required implementation details

The following are typical issues that cause black screens and the correct approaches. Please implement strictly according to these guidelines to avoid black screens.

### 1. Ray Construction: Do not use inverse matrices; use "camera position + forward + FOV" to calculate directly (critical)

- **Wrong approach (easily causes black screen)**: Using `invProjectionMatrix * vec4(ndc, ...)` and `invViewMatrix` in the fragment shader to reverse-project rays from NDC. Common bugs: using NDC depth `1.0` instead of `-1.0`, doing `view /= view.w` without normalizing the direction, or passing wrong/not-updated-per-frame matrices - any of these will cause incorrect rays and thus black screen.
- **Correct approach**: Do not pass inverse matrices; instead pass **camera position, camera forward direction, camera up vector, vertical FOV**, and construct the ray directly from these in the fragment.

**Fragment shader ray construction (must follow this approach with zero-protection):**

```glsl
// Input uniforms: iCameraPos, iCameraDir, iCameraUp, iFov, iResolution
vec2 uv = vUv * 2.0 - 1.0;
float aspect = max(iResolution.x, 1.0) / max(iResolution.y, 1.0);  // Prevent 0 to avoid NaN causing black screen
uv.x *= aspect;
vec3 camDir = normalize(iCameraDir);
vec3 camRight = normalize(cross(camDir, iCameraUp));
vec3 camUp = cross(camRight, camDir);
float fovRad = iFov * 3.14159265 / 180.0;
float focalLength = 1.0 / max(tan(fovRad * 0.5), 1e-4);  // Prevent tan being 0 causing division by zero
vec3 rayDir = normalize(camRight * uv.x + camUp * uv.y + camDir * focalLength);
vec3 rayOrigin = iCameraPos;
```

**JavaScript uniforms that must be updated every frame in animate():**

- `iTime`: animation time (incremented by delta when toggle is on).
- `iResolution`: **Must be updated every frame in animate()** (not just once in init or resize), otherwise headless/automation environments may get (0,0) on the first frame or incorrect layout -> black screen. **Must** use `renderer.getDrawingBufferSize(vec)` to get the size and apply `Math.max(..., 1)` to x and y; **do not** use only `renderer.domElement.width`/`height` (often 0 or out of sync in headless/Docker, causing incorrect aspect ratio, ray errors, black screen).
- `iCameraPos`: `camera.position`.
- `iCameraDir`: **Must** use `camera.getWorldDirection(tempVector)` to get the forward vector; cannot be omitted or incorrect.
- `iCameraUp`: `camera.up`.
- `iFov`: `camera.fov` (in degrees).
- Accretion disk/black hole parameters: such as `uDiskInner`, `uDiskOuter`, `uBhRadius`, etc., consistent with config (inner edge approx 3.0, outer edge approx 10.0, black hole radius approx 1.0).

### 2. Rendering Pipeline and Quad Ownership (extremely likely to cause black screen)

- **Quad must be in the scene, not attached to the camera**: Must use `scene.add(mesh)` (mesh = full-screen PlaneGeometry(2,2) + ShaderMaterial). **Do not** use `camera.add(fullQuad)` then `scene.add(camera)`: in Three.js, when added as the "current rendering camera" to the scene, the renderer typically skips the Camera node and does not render it, causing the camera's children (your full-screen quad) to **not be drawn at all**, resulting in black screen.
- Use the **same** PerspectiveCamera (with OrbitControls) for rendering: `renderer.render(scene, camera)`, where `scene` contains only the full-screen quad, and `camera` serves only as render's second argument; **do not** add camera to scene to "carry" the quad for drawing.
- **Canvas mounting**: Use `document.body.appendChild(renderer.domElement)` to avoid first-frame layout issues in some environments when canvas is only placed inside div#app.
- Vertex shader must: `gl_Position = vec4(position, 1.0);` (directly in clip space, full-screen -1 to 1), so the quad does not need to follow camera position and is always full-screen.
- Do not use "one orthographic camera to render quad, another perspective camera only providing matrices": use the same perspective camera for both interaction and rendering; the shader only uses that camera's position + getWorldDirection + up + fov.

### 3. Final Color Must Include Starfield + Accretion Disk/Glow (Including Absorbed Paths)

- The fragment shader must ultimately: first Ray March along the ray (geodesic bending, accretion disk y=0 plane intersection, Doppler brightness), accumulating glow; **if the ray escapes to the far field**, add procedural starfield color (e.g., direction-based noise/hash star points + breathing effect).
- **If the ray is absorbed (falls into the event horizon)**: cannot only output `colorAccum * 0.25` where colorAccum may be near 0, otherwise the entire screen will still be black. Must ensure visible output even when absorbed, e.g.: accumulate a distance-dependent glow during ray marching (such as `glow += 0.01 / (pow(r,4.0) + 0.1)`), and when writing finalColor, **whether escaped or absorbed**, add the glow contribution (or at least a minimum brightness), then apply exposure/tone mapping, so that the final `gl_FragColor` is never constantly black.
- Final `gl_FragColor` = above color with exposure and tone mapping (exposure >= 1.0), **must not** be unassigned or constantly `vec4(0,0,0,1)`.
- Starfield suggestion: use hash/noise to generate star points based on "direction", combine with `iTime` for twinkling; can differentiate blue/white/red colors, high density but not distracting.

### 3.1 Shader Compilation and Compatibility (Avoid compilation failure or NaN causing black screen)

- **Precision declaration**: The fragment shader **must** begin with `precision highp float;` (WebGL 1 requires fragment shaders to specify float precision, otherwise some environments will fail to compile or have undefined behavior). Vertex shader should also add `precision highp float;` if using float.
- **Zero protection and division by zero**: When computing aspect ratio with `iResolution` in the fragment, must prevent zero, e.g., `aspect = max(iResolution.x, 1.0) / max(iResolution.y, 1.0)`; when computing focal length, must prevent `tan(fovRad*0.5)` from being 0, e.g., `focalLength = 1.0 / max(tan(fovRad * 0.5), 1e-4)`. Otherwise NaN/Inf will be produced causing black screen.
- **Loop upper bound**: Ray Marching for loop upper bound should use a **constant** (e.g., `#define MAX_STEPS 150`), and use `if (i >= someConstant) break` inside the loop to control step count. **Avoid** using `uniform int uMaxSteps` directly as the for upper bound (e.g., `for(int i=0; i<uMaxSteps; i++)`), as some WebGL implementations have poor support for non-constant loop bounds, potentially causing compilation failure or anomalies.
- **Uniforms and varyings**: Ensure all uniforms used in the fragment are defined in ShaderMaterial.uniforms; varyings must have consistent types between vertex and fragment (e.g., vec2 vUv).

### 4. Accretion Disk and Gravitational Bending

- The accretion disk is at the y=0 plane (or near-plane thin disk), with inner radius approx 3, outer radius approx 10; during ray marching, sample disk surface color when crossing y=0, and apply Doppler effect (tangential velocity dot product with line of sight, brighter left darker right).
- Gravitational bending: each step applies a force toward the center on the ray direction (e.g., `force = -normalize(pos) * (k/(r*r))`), then normalize and step, with step count <= 150.

### 4.1 Black Hole Does Not Disappear When Zooming/Pulling Back (Must ensure disk is visible from any angle)

- **Symptom**: When the camera zooms out to a certain distance, the accretion disk/black hole suddenly disappears, only reappearing when zooming in significantly. The cause is that the step size grows with distance (e.g., `step = r * 0.08`), and at medium distances **one step crosses y=0 accretion disk** without detecting the crossing, or runs out of steps before reaching the disk surface.
- **Recommended approach (choose one or both)**:
  1. **Explicit ray-plane intersection each step**: Before or after stepping, use explicit intersection of the ray with the y=0 plane to determine if the accretion disk is hit, avoiding reliance on "whether this step crossed y=0." That is: if `dir.y != 0`, let `t_plane = -pos.y / dir.y`; if `t_plane > 0` and `t_plane` does not exceed the current step size (or a reasonable upper limit), then `hit = pos + dir * t_plane`; if `length(hit.xz)` is within `[diskInner, diskOuter]`, sample the disk surface and accumulate color. This way, regardless of step size, the disk will not be missed as long as the ray crosses the disk surface.
  2. **Smaller step size in disk region**: When the ray's current distance to origin r is near the accretion disk (e.g., r between `diskInner-2` and `diskOuter+3`), use a smaller step size (e.g., 0.05-0.15) to avoid crossing the thin y=0 disk in one step; use larger step sizes at far distances to save steps.
- **Step count**: At far distances, the ray needs many steps to reach the disk surface. If `MAX_STEPS` is only 150 with a small step size, it may exhaust steps before reaching the disk. Consider increasing `MAX_STEPS` (e.g., 200-256), or using larger step sizes at far distances and smaller ones when entering the disk region, to ensure reaching the disk or escaping within the step limit.

**Ray-plane y=0 intersection example (called each step to avoid missing the disk):**
```glsl
// Inside the stepping loop: if disk not yet hit, and dir.y is non-zero, first compute intersection with y=0
if (!hitDisk && abs(dir.y) > 1e-5) {
  float t_plane = -pos.y / dir.y;
  if (t_plane > 0.0 && t_plane <= stepLen * 1.01) {  // Intersection within this step's range
    vec3 hit = pos + dir * t_plane;
    float rad = length(hit.xz);
    if (rad >= uDiskInner && rad <= uDiskOuter) {
      // Hit accretion disk, sample disk surface color and accumulate, hitDisk = true
    }
  }
}
// Then apply gravitational bending and pos += dir * stepLen
```

### 5. Tech Stack and UI (consistent with previous requirements)

- THREE.ShaderMaterial (or RawShaderMaterial) + OrbitControls must be visible and functional in the code.
- Bottom-left frosted glass card titled "GARGANTUA", interaction instructions: left-click to rotate, right-click to pan, scroll wheel to zoom; `<input type="checkbox" id="anim-toggle">` must exist and be clickable (do not use display:none), and in animate determine whether to increment `iTime` based on its checked state.

After implementing according to the above points, opening the HTML should immediately show the black hole (accretion disk + lens ring + starfield), not a black screen. If still black, check each item: whether rays are constructed using iCameraPos + iCameraDir + iFov, whether getWorldDirection is passed every frame, whether the final color includes starfield and disk glow.

---

## [Anti-Black-Screen Checklist] Must check off each item after implementation, otherwise evaluation screenshots will be completely black

The following are required implementation conditions; missing any one may cause a black screen. Please **strictly follow**:

- [ ] **Full-screen quad**: Use `THREE.PlaneGeometry(2, 2)` + `THREE.ShaderMaterial`, get `mesh` then **must** write `mesh.frustumCulled = false`, then `scene.add(mesh)`. **Do not** use `camera.add(mesh)` or `scene.add(camera)` to "carry the quad for drawing."
- [ ] **Canvas mounting**: `document.body.appendChild(renderer.domElement)`, and `renderer.setSize(window.innerWidth, window.innerHeight)` (or at least non-zero width/height).
- [ ] **animate() per-frame updates** (suggested order):
  1. `iTime`: increment or hold based on `#anim-toggle` checked state.
  2. **iResolution**: In animate(), **must** use `renderer.getDrawingBufferSize(vec)` to get size, then apply `Math.max(..., 1)` to x and y; **do not** use only `renderer.domElement.width`/`height` (often 0 or incorrect in headless environments, causing black screen).
  3. `iCameraPos.value.copy(camera.position)`.
  4. `camera.getWorldDirection(tempVec)` then `iCameraDir.value.copy(tempVec)`.
  5. `iCameraUp.value.copy(camera.up)`, `iFov.value = camera.fov`.
  6. `controls.update()`.
  7. `renderer.render(scene, camera)`.
- [ ] **Vertex shader**: `gl_Position = vec4(position, 1.0);` (direct NDC, full-screen -1 to 1).
- [ ] **Fragment shader**: (1) Must begin with `precision highp float;`. (2) Rays are constructed in the fragment using uniforms `iCameraPos, iCameraDir, iCameraUp, iFov, iResolution` per the formula above, with aspect ratio using `max(iResolution.x,1.0)/max(iResolution.y,1.0)` and focal length using `1.0/max(tan(...),1e-4)` for zero protection. (3) Ray March loop upper bound uses a constant (e.g., `#define MAX_STEPS 150`), avoiding `for(i=0; i<uMaxSteps; i++)`. (4) Add procedural starfield when escaped; **when absorbed** must also have visible output (e.g., accumulate glow during stepping and add to final color), not just output near-zero colorAccum. (5) Final `gl_FragColor` is composed of "accretion disk/photon ring + starfield or glow + exposure/tone mapping", **must not** be constantly `vec4(0,0,0,1)`; exposure >= 1.0.
- [ ] **#anim-toggle**: `<input type="checkbox" id="anim-toggle" checked>` must exist in the DOM and be clickable (do not use display:none), and in animate determine whether to increment iTime based on its checked state.
- [ ] **Disk does not disappear when zooming**: Accretion disk remains visible when pulling back the camera. Implementation must avoid "large step crossing y=0": each step uses explicit ray-plane y=0 intersection (`t_plane = -pos.y/dir.y`, then check if hit radius is within diskInner to diskOuter) to sample disk surface, and/or use smaller step size in disk region (r approx 2-15); MAX_STEPS or step size strategy must ensure reaching the disk or escaping even at far distances.

### Recommended Implementation Structure (following this structure avoids black screen)

```javascript
// 1. Create full-screen quad and add to scene (do not attach to camera)
const geometry = new THREE.PlaneGeometry(2, 2);
const mesh = new THREE.Mesh(geometry, blackHoleMaterial);
mesh.frustumCulled = false;   // Required, otherwise may be frustum culled causing black screen
scene.add(mesh);

// 2. In animate(), must update uniforms in order every frame before rendering
function animate() {
    requestAnimationFrame(animate);
    if (document.getElementById('anim-toggle').checked) shaderTime += clock.getDelta();
    blackHoleMaterial.uniforms.iTime.value = shaderTime;
    const resVec = new THREE.Vector2();
    renderer.getDrawingBufferSize(resVec);
    blackHoleMaterial.uniforms.iResolution.value.set(Math.max(resVec.x, 1), Math.max(resVec.y, 1));
    blackHoleMaterial.uniforms.iCameraPos.value.copy(camera.position);
    const camDir = new THREE.Vector3();
    camera.getWorldDirection(camDir);
    blackHoleMaterial.uniforms.iCameraDir.value.copy(camDir);
    blackHoleMaterial.uniforms.iCameraUp.value.copy(camera.up);
    blackHoleMaterial.uniforms.iFov.value = camera.fov;
    controls.update();
    renderer.render(scene, camera);
}
animate();
```

Three.js import method (choose one):
- **Method A**: In `<head>` first place `<script type="importmap">` specifying `"three"` and `"three/addons/"` CDN URLs, then `<script type="module">` with `import * as THREE from 'three'; import { OrbitControls } from 'three/addons/controls/OrbitControls.js';`
- **Method B**: Directly `import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';` etc., ensure CDN is accessible.

## [Evaluation Dimensions Summary] Your implementation will be automatically scored on the following aspects

- **Technical Architecture (20)**: THREE.ShaderMaterial (or RawShaderMaterial) + OrbitControls appear and function in the code.
- **Physics/Visual Logic (30)**: Code shows implementation or comments for geodesic/ray bending, Doppler brightness, procedural starfield (e.g., noise/hash functions).
- **Interaction (30)**: Left-click rotation, right-click pan, scroll wheel zoom work (OrbitControls), and a clickable #anim-toggle controlling the animation toggle exists.
- **Visual Similarity (20)**: Screenshots are geometrically similar to the reference image (accretion disk, lens ring, central dark area); completely black screenshots score 0 for this dimension.

Please strictly implement according to the above points to ensure the HTML displays the black hole visualization (not a black screen) when opened, and passes automated evaluation.

---

### en_breach_forensics

[Query Description]

**Title:** Incident Response: Proprietary App Breach Investigation

**Role:** Senior Security Analyst.

**Scenario:**
Our SIEM system detected a suspicious outbound connection from our internal file server (`103.45.12.99`) at 03:00 AM. 
Management believes the **File Upload** feature was exploited, but we don't know how.

**Resources:**
You have access to the server logs (`nginx_access.log`), the complete application source code (`.py` files), and the storage directory (`uploads/`).

**Mission:**
Perform a "Black Box" investigation to determine the extent of the breach and secure the system.

**Objectives:**

1.  **Forensic Decryption (The "What"):**
    *   Locate the attacker's entry point in `nginx_access.log`.
    *   The User-Agent string contains an obfuscated payload. **Reverse-engineer the obfuscation logic** by analyzing the application source code configuration to find the decryption method/keys.
    *   Report the **exact cleartext command** the attacker executed.

2.  **Threat Hunting (The "Where"):**
    *   Audit the `uploads/` directory. Identify any file that poses a security threat.
    *   Explain *technically* why this file is dangerous despite having a safe extension.

3.  **Vulnerability Patching (The "Fix"):**
    *   Modify `upload_server.py` to prevent this attack vector.
    *   **Constraint:** You must encapsulate your fix in a function named **`validate_image_header(file_stream)`**.
    *   *Requirement:* The fix must be robust enough to reject "spoofed" files (like the one you found) while allowing legitimate images.

4.  **Containment:**
    *   Write a script `cleanup.sh` to remove the identified malware and block the attacker's IP.

**Deliverables:**

1.  `Incident_Report.md`: Analysis of the attack vector and the decrypted payload.
2.  `secure_upload.py`: The patched server code.
3.  `cleanup.sh`: The containment script.

[Context]:

The following files are available in the `context/` directory:

- `context/uploads/` — the storage directory containing uploaded files
- `context/nginx_access.log` — the server access logs
- `context/upload_server.py` — the application source code
- `context/config.py` — the application configuration

---

### en_bvh_path_tracing

Query:
---

[Query Description]
You need to complete a BVH path tracing renderer. Fix/complete the following core logic in the workspace/submission directory so that the program compiles successfully and generates output.png:

1. BVH intersection calculation (BVH.cpp)
2. Ray-bounding box intersection (Bounds3.hpp)
3. Rendering main loop (Renderer.cpp)

[Requirements]
- Compile successfully using CMake + Make
- Generate output.png after running ./renderer
- Keep the code structure and interfaces unchanged

[Deliverables]
- workspace/submission/BVH.cpp
- workspace/submission/Bounds3.hpp
- workspace/submission/Renderer.cpp
- workspace/submission/README.md

[Evaluation]
- Run eval/grade.py (automatically performs build, output checking, code similarity, and image quality evaluation)

[Context]
- context/PA6.pdf (task description)
- context/operation_list.md (build and run operation reference)
- context/models/ (rendering model resources)

---

### en_checkers_alphabeta_pruning

## Reinforcement Learning and Game Theory Assignment 4: Alpha-Beta Pruning Search Implementation in Checkers Environment

### 1. Query (Task Description)

**Task Background**:
In a simplified checkers environment (`triangle_size = 2`), the traditional greedy strategy (Greedy) only considers the immediate reward of the current step and easily falls into local optima. This task requires implementing a **Minimax algorithm with Alpha-Beta pruning** in `agents.py` to predict opponent actions through game tree search and formulate better strategies.

**Task Requirements**:

1. **Algorithm Implementation**: Implement the Minimax algorithm in the designated interface in `agents.py`.
* Must include **Alpha-Beta pruning** logic to improve search efficiency.
* Design a custom heuristic evaluation function (Heuristic Function), for example considering the total distance of pieces to the target area.


2. **Search Depth**: Set a reasonable search depth based on computational resources (recommended depth >= 3).
3. **Runtime Environment**: Code must run under the `triangle_size 2` configuration.
4. **Performance Requirement**:
* Submit `agents.py` code.
* **Win rate requirement**: In test matches against the built-in `Greedy` strategy, the **win rate must exceed 80%** after 20 games.


### 2. Context (Context Files)

* **Environment code**: `ChineseChecker/env/` directory, defining board layout, legal action generation (including consecutive jump rules), and win/loss determination.
* **Baseline code**: `RandomAgent` and `GreedyAgent` format references already present in `agents.py`.
* **Rule logic**:
* Movement: Move one cell or jump over adjacent pieces (consecutive jumps allowed).
* Victory: The first player to fully occupy the opponent's initial triangle area wins.


* **Execution command reference**: `python play.py --triangle_size 2`.

---

### en_chip_edge_detection

# Query 4: Chip Ring Inner Edge Detection Algorithm Implementation

## Task Description

Based on the requirements below, implement a complete chip ring inner edge detection algorithm. The algorithm must handle high-resolution grayscale images (up to 30,000 x 30,000 pixels), precisely detect the circle center coordinates and radius of the chip's inner edge, and generate high-quality mask images.

Specific task requirements:
1. Implement an image preprocessing module, including downsampling, Gaussian blur, and background subtraction
2. Implement a coarse localization algorithm using maximum contour detection to obtain the initial center and radius
3. Implement a fine localization algorithm using radial gradient scanning and a dual-edge detection strategy
4. Implement a robust statistics module using MAD (Median Absolute Deviation) technique and the 3-sigma rule to filter out outliers
5. Implement feature point detection to identify chord midpoints, high-intensity points, and outlier points
6. Generate a high-quality circular mask with chord-adaptive horizontal cropping support
7. Provide comprehensive processing visualization and debugging capabilities

Performance requirements:
- For 30,000 x 30,000 pixel images, processing time should not exceed 5 seconds (target: under 1 second)
- Circle center coordinate error within +/-40 pixels
- Radius error inward should not exceed 40 pixels

## Context

File list (see context/ directory):
- `ground_truth_data.json` - Contains ground truth circle center coordinates and radius values for 5 test images

```
Note: Due to actual project requirements, raw data and actual images are not provided here; only the file framework needed for the Query is given.
```

## Expected Output

Complete Python implementation code, including the following main modules:
- `preprocess.py` - Image preprocessing module (downsampling, Gaussian blur, background subtraction)
- `coarse_detection.py` - Coarse localization implementation (maximum contour detection, initial center and radius estimation)
- `fine_detection.py` - Fine localization implementation (radial gradient scanning, dual-edge detection strategy)
- `statistical_analysis.py` - Robust statistical analysis (MAD technique, 3-sigma rule outlier filtering)
- `mask_generation.py` - Mask generation module (circular mask, chord-adaptive horizontal cropping)
- `main.py` - Main program entry point (command-line argument configuration, logging, visualization output)
- `test.py` - Testing and evaluation module (load ground truth, compute errors, evaluate performance)

The code uses a modular design, supports command-line argument configuration, and provides comprehensive logging and visualization output.

---

### en_cmo_proof

# CMO 2024 Problem 6 - Mathematical Competition Solution

## Task Description

Please solve Problem 6 from the Chinese Mathematical Olympiad (CMO) 2024 competition. This is a mathematical proof problem consisting of two parts:

## Problem Content

Given real numbers $a_1, a_2, \ldots, a_n$ satisfying:
$$\sum_{i=1}^{n} a_i = n, \quad \sum_{i=1}^{n} a_i^2 = 2n, \quad \sum_{i=1}^{n} a_i^3 = 3n.$$

Define the **width** $\Delta = \max\{a_1, a_2, \ldots, a_n\} - \min\{a_1, a_2, \ldots, a_n\}$.

### Part 1: Prove C = sqrt(5)

**(1)** Find the largest constant $C$ such that for all $n \geq 4$, we have $\Delta \geq C$.

Required:
- Provide a concrete example showing the width can approach arbitrarily close to C = sqrt(5)
- Prove the lower bound of the width: i.e., $\Delta \geq \sqrt{5}$ holds for all sequences satisfying the conditions

### Part 2: Higher-Order Exact Lower Bound

**(2)** Prove there exists a constant $C_2 > 0$ such that $\Delta \geq C + C_2 n^{-3/2}$, where $C$ is the constant from part (1).

## Submission Requirements

Please write your complete mathematical proof in an `answer.md` file and save it in the current working directory.

Format requirements:
- Use Markdown format
- Use mathematical notation clearly
- The proof process must be logically rigorous with no critical steps omitted
- Divide into "## Part 1" and "## Part 2" sections

## Hints

- Non-negative polynomial methods may be used
- Construct auxiliary functions
- Analyze discrete obstructions
- Use lower bounds on irrational number approximation errors

---

### en_data_analysis_study_plan

# Query 5: Personalized 30-Day Data Analysis Interview Study Plan

## [Task Description]

Design a **30-day personalized study plan** targeting **data analysis job interviews** for an **intermediate Python learner**. The plan should comprehensively consider the user's current skill level, target job requirements, daily available study time, and learning style preferences, generating a structured daily learning task schedule to help the user systematically prepare for interviews.

## [Task Background]

Data analysis is a popular career direction today, with job requirements spanning SQL data querying, Python data processing (Pandas/NumPy), data visualization, statistics fundamentals, machine learning introduction, and other skills. For learners preparing to switch careers or job hunt, systematically mastering these skills within limited time is a major challenge.

Traditional study plans often lack personalization and struggle to adapt to different learners' foundation levels and schedules. This task requires designing an intelligent study plan generation system that automatically generates a customized 30-day learning path based on user profiles (current level, target position, available time, learning preferences), with optional calendar file output for reminders.

## [User Profile]

- **Current Skill Level**: Intermediate Python learner
  - Already mastered: Python basic syntax, basic data structures (list/dict/tuple), function definitions, file I/O
  - To improve: Data processing libraries (Pandas/NumPy), SQL, data visualization, statistics, machine learning
- **Target Position**: Data Analyst / Data Analysis role
  - Job requirements: SQL proficiency, Python data processing, data visualization, statistics fundamentals, basic machine learning knowledge
- **Daily Available Study Time**: 2-3 hours (adjustable based on actual availability)
- **Learning Style Preference**: Video instruction + hands-on practice + reading documentation (comprehensive learner)

## [Objectives]

1. **Generate daily learning task schedule**: Including learning topics, recommended resource links, and practice exercises
2. **Dynamically adjust difficulty and pace**: From basics to advanced, step by step
3. **Output in interactive calendar format (.ics file)**: Importable into Google Calendar/Outlook for reminder setup

## [Output Requirements]

### 1. **Markdown Study Plan** (Required)

Suggested filename: `data_analysis_interview_30day_study_plan.md`

**Structure Requirements:**

```markdown
# Data Analysis Interview 30-Day Study Plan

## User Profile
- Current skills: Intermediate Python
- Target position: Data Analyst
- Daily study time: 2-3 hours
- Learning preference: Video + hands-on + reading

---

## Week 1: SQL Fundamentals & Data Querying (Day 1-7)

### Weekly Objective
Master basic SQL syntax, able to perform single-table queries, multi-table joins, aggregate statistics

### Day 1: SQL Introduction - SELECT Basic Queries
**Learning Topics:**
- SQL basic concepts: database, table, row, column
- SELECT statement: querying single table data
- WHERE clause: conditional filtering
- ORDER BY: sorting

**Learning Resources:**
1. [Video] SQL Tutorial for Beginners - freeCodeCamp (YouTube, first 1 hour)
   Link: https://www.youtube.com/watch?v=HXV3zeQKqGY
2. [Reading] W3Schools SQL Tutorial - SELECT Statement
   Link: https://www.w3schools.com/sql/sql_select.asp
3. [Practice] SQLBolt - Interactive SQL Lessons (Lesson 1-3)
   Link: https://sqlbolt.com/

**Practice Tasks:**
- Complete all exercises in SQLBolt Lessons 1-3
- Exercise: Query specific conditions in a sample database (e.g., "find all orders with sales > 1000")

**Estimated Time:** 2.5 hours

---

### Day 2: SQL Advanced - JOIN Multi-table Connections
**Learning Topics:**
- INNER JOIN
- LEFT JOIN / RIGHT JOIN
- Multi-table join practice

**Learning Resources:**
1. [Video] SQL Joins Explained - Programming with Mosh (YouTube, 15 min)
2. [Practice] SQLBolt - Lesson 6-7 (Joins)
3. [Reading] Mode Analytics SQL Tutorial - Joins
   Link: https://mode.com/sql-tutorial/sql-joins/

**Practice Tasks:**
- Complete SQLBolt JOIN exercises
- Hands-on: Join orders table and customers table, calculate total order amount per customer

**Estimated Time:** 2.5 hours

---

(Day 3-7 continued...)

---

## Week 2: Python Data Processing - Pandas & NumPy (Day 8-14)

### Weekly Objective
Proficiently use Pandas for data cleaning, transformation, aggregation; master NumPy array operations

### Day 8: Pandas Introduction - DataFrame Basics
...

---

## Week 3: Data Visualization & Statistics (Day 15-21)

### Weekly Objective
Master Matplotlib/Seaborn charting; understand descriptive statistics, probability distributions, hypothesis testing

### Day 15: Matplotlib Basic Charting
...

---

## Week 4: Machine Learning Introduction & Comprehensive Projects (Day 22-30)

### Weekly Objective
Understand basic machine learning concepts; complete 1-2 end-to-end data analysis projects

### Day 22: Machine Learning Overview & sklearn Introduction
...

### Day 28-30: Comprehensive Project Practice
**Project 1: E-commerce User Behavior Analysis**
- Dataset: Kaggle - E-commerce Data
- Tasks: User profiling, purchase behavior prediction, visualization report
- Skills integration: SQL data extraction + Pandas cleaning + visualization + simple modeling

**Project 2: Financial Data Analysis (Optional)**
- Dataset: Yahoo Finance stock data
- Tasks: Trend analysis, correlation analysis, risk assessment

---

## Appendix: Recommended Learning Resources Summary

### Online Courses
- Coursera: "Data Analysis with Python" (IBM)
- DataCamp: "Data Analyst with Python Career Track"
- Kaggle Learn: Free Pandas/SQL/visualization tutorials

### Recommended Books
- "Python for Data Analysis" - Wes McKinney
- "SQL in 10 Minutes" - Ben Forta

### Practice Platforms
- LeetCode Database problems (SQL practice)
- Kaggle Datasets (real dataset practice)
- HackerRank SQL/Python challenges

---

## Study Tips

1. **Daily review**: Review previous day's key points before starting each day (15 min)
2. **Practice-focused**: 70% time on hands-on practice, 30% on theory
3. **Project-driven**: From Week 3, try small projects on Kaggle
4. **Interview prep**: Last week, organize common interview questions, simulate interview scenarios
5. **Take notes**: Use Notion/GitHub to record daily study notes and code

```

**Content Key Points:**
- Organized by week/day, 30 days total
- Each day includes: Learning topics, resources (video/article/book links), practice tasks, estimated time
- Each week sets a theme objective
- Last week includes comprehensive practice project(s)

### 2. **.ics Calendar File** (Optional)

Suggested filename: `study_plan_calendar.ics`

**Requirements:**
- Importable into Google Calendar, Outlook, Apple Calendar and other major calendar applications
- Create one calendar event per day, titled with the day's learning topic
- Event description includes learning task summary and resource links
- Set reminders (e.g., every day at 9:00 AM or 7:00 PM)

**Example .ics format:**
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Data Analysis Study Plan//EN
BEGIN:VEVENT
DTSTART:20260207T090000Z
DTEND:20260207T110000Z
SUMMARY:Day 1: SQL Introduction - SELECT Basic Queries
DESCRIPTION:Learn SQL basic syntax\nResources: SQLBolt Lesson 1-3\nExercise: Complete basic query exercises
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:SQL study starts in 15 minutes
END:VALARM
END:VEVENT
...
END:VCALENDAR
```

### 3. **Content Requirements**

1. **Fit within 30-day time limit**: Arrange 2-3 hours of learning content per day, moderate content volume
2. **Reasonable difficulty progression**: From SQL basics -> Python data processing -> visualization & statistics -> ML introduction
3. **Cover core skills**:
   - SQL: Queries, joins, aggregation, subqueries
   - Python: Pandas (data cleaning/transformation/aggregation), NumPy (array operations)
   - Visualization: Matplotlib, Seaborn
   - Statistics: Descriptive statistics, probability distributions, hypothesis testing
   - Machine Learning: Linear regression, logistic regression, decision trees (introductory level)
4. **Real, usable learning resources**: Recommended videos, articles, and book links must actually exist and be high quality
5. **Include practice projects**: Last week arrange 1-2 comprehensive projects integrating learned skills
6. **Strong executability**: Clear task descriptions, easily accessible resources, reasonable time arrangements


## [Hints]

### Skill System Planning
- **Week 1**: SQL data query fundamentals (single table, multi-table, aggregation)
- **Week 2**: Python data processing (Pandas, NumPy)
- **Week 3**: Data visualization (Matplotlib, Seaborn) + statistics fundamentals
- **Week 4**: Machine learning introduction + comprehensive project practice

### Learning Resource Recommendations
- **SQL**: SQLBolt (interactive exercises), Mode Analytics Tutorial, LeetCode Database
- **Python/Pandas**: Kaggle Learn, DataCamp, "Python for Data Analysis"
- **Visualization**: Matplotlib official tutorials, Seaborn Gallery
- **Statistics**: Khan Academy Statistics, "Statistical Learning Methods"
- **Machine Learning**: Coursera Machine Learning, Scikit-learn documentation

### Practice Project Suggestions
- Data analysis projects from Kaggle Datasets (e.g., Titanic, House Prices)
- Real business scenario simulations (e-commerce user analysis, financial data analysis)

### .ics File Generation
- Python library: `icalendar`
- Online tools: iCalendar.org, ICS File Generator

### Personalization Adjustment Suggestions
- Adjust task volume based on user's daily available time
- Adjust resource type ratio based on learning preference (video/reading/hands-on)
- Adjust focus based on target position specific requirements (e.g., emphasis on business analytics or technical analytics)

---

### en_ddqn_mountaincar

## Experiment Task: Double DQN-Based MountainCar Energy Hill-Climbing Optimization

### 1. Query (Task Description)

**Task Objective**:
Train an agent in the `MountainCar-v0` environment using the **Double DQN (DDQN)** algorithm. Due to extremely sparse rewards in this environment (-1 per step until reaching the goal), standard DQN tends to produce severe overestimation problems. You need to implement the core DDQN logic to improve training stability.

**Specific Requirements**:

1. **Algorithm Logic**: Modify the standard DQN target value computation. Use the **policy network** (Policy Net) to select the optimal action, and use the **target network** (Target Net) to compute the Q-value for that action.
2. **Network Architecture**: Since the state space is only 2-dimensional, simple fully connected layers (MLP) are sufficient; no convolutional layers needed.
3. **Output Requirements**:
* Submit a `ddqn_main.py` script containing model training and testing code.
* Record and save `loss` and `reward` data during training.
* **Performance Target**: The trained model must be able to reach the hilltop from the car's starting position within **200 steps** (i.e., single test reward > -200).

* **Environment Documentation**: [Gymnasium MountainCar-v0 Official Docs](https://gymnasium.farama.org/environments/classic_control/mountain_car/).
* **Algorithm Reference**: Paper "Deep Reinforcement Learning with Double Q-learning (Hasselt et al., 2015)".

---

### en_dijkstra_optimize

# Code Refactoring and Performance Optimization

## Query
You are a software engineer tasked with refactoring and optimizing a Python implementation of Dijkstra's algorithm for finding the shortest path in a graph. The current implementation has performance issues and doesn't handle large graphs efficiently. Your task is to:
1. Analyze the current implementation to identify bottlenecks
2. Refactor the code to improve readability and maintainability
3. Optimize the algorithm to handle large graphs efficiently
4. Add comprehensive unit tests to verify correctness
5. Measure and report performance improvements

## Context
File list:
- context.md - Project overview, file structure description, original implementation analysis, and other background information
- dijkstra_original.py - Original Dijkstra algorithm implementation
- test_dijkstra.py - Performance test script
- requirements.txt - Python dependency configuration

## Deliverables
Create the following files in the working directory:
- dijkstra_optimized.py - Optimized Dijkstra algorithm implementation (must include a Graph class with the same interface as the original implementation)
- performance_report.md - Performance test report (including optimization approach, test results, speedup analysis)
- comparison.csv - Performance comparison data (including test time comparisons for graphs of different scales)

---

### en_distributed_consistency_design

Query:
---

[Query Description]
Design a data consistency solution for a distributed e-commerce system. The current system uses a microservices architecture and suffers from problems such as inventory overselling, order status inconsistency, and duplicate payment processing.

**Goals:**
1. Analyze consistency issues in distributed transactions (inventory, orders, payments, etc.)
2. Design appropriate solutions to ensure high availability and performance
3. Provide concrete technical implementation ideas or pseudocode/code for key components

**Process:**
1. Read `context/current_order_flow.py` to understand the current order flow and its problems
2. Write a data consistency design document: problem analysis, solution selection, architecture and flow
3. Explain key technical points: distributed locks, TCC/Saga, message queues, idempotency, compensation and reconciliation, etc.
4. Provide implementation examples or pseudocode for key components (inventory deduction, order service, payment service, event handling, monitoring and compensation, etc.)
5. Briefly assess performance impact, high availability, fault tolerance, and scalability
6. Save all deliverables to the current directory

**Deliverable Requirements:**
- Data consistency design document (e.g., `consistency_design.md` or `analysis_report.md`)
- Architecture design and flowchart description (may be merged into the design document or as a separate file)
- Implementation examples or pseudocode for key components (may be merged into the document or as separate .py files)
- Performance impact assessment (may be merged into the design document)

[Context]
File list:
- `context/current_order_flow.py` - Current order flow (with consistency issues)
- `context/operation_list.md` - Operational steps reference

---

### en_docker_env_config

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

---

### en_document_qa_citation

Document QA Task (Based on Provided Report)

Task Instructions
- Use ONLY the documents provided in the context/ directory as information sources:
  - context/the-state-of-ai-in-2025.pdf
  - context/q.md (contains the questions to answer)
- Answer each of the 4 questions in context/q.md sequentially. Do not use external knowledge or fabricate information.
- If the document does not mention the answer to a question, you must explicitly answer: "Context mentions nothing about this".
- Each factual statement must be annotated with the source page number, format example: [Page 5].

Deliverables
- Create answers.md in the current working directory, organized in the following format:

1. (Answer to Question 1. Include necessary facts and [Page X] citations)
2. (Answer to Question 2. Include necessary facts and [Page X] citations)
3. (Answer to Question 3. Include necessary facts and [Page X] citations)
4. (Answer to Question 4. Include necessary facts and [Page X] citations)

Important Notes
- Absolutely no speculation; answer only based on the PDF source text.
- Evaluation strictly requires every answer to include page citations [Page N]. Even if you are not completely certain of the page number, provide the closest evidence page. Whether a citation is provided takes priority over whether the citation is perfectly accurate.
- Citation page numbers must match the actual PDF page numbers, annotated with [Page N].
- It is recommended to first read through the questions in context/q.md, then locate relevant evidence in the PDF before answering.

---

### en_dqn_implementation

# Task: DQN and Double DQN Algorithm Implementation

## 1. Task Objective
In this experiment, you need to implement and compare **DQN** and **Double DQN** algorithms in the `MountainCar-v0` environment. The core of the task is to fill in the missing logic and demonstrate that your implementation achieves significant convergence.

## 2. Context Files
All necessary files are in the `context/` folder within the working directory:
- `context/dqn_task.py`: Contains the task skeleton with `TODO` markers for code to be completed.

## 3. Standardized Development Workflow (TODO List)
Please modify `dqn_task.py` according to the following stages:

### TODO 1: Network Architecture (`QNetwork`)
- Build a feedforward neural network.
- **Requirements**: Input layer adapted to the environment state space (2-dimensional), output layer adapted to the action space (3-dimensional). Two hidden layers with 64 units each and ReLU activation are recommended.

### TODO 2: Experience Replay (`ReplayBuffer`)
- Maintain a circular queue.
- **Requirements**: Implement `push` to store transition tuples, implement `sample` to randomly return batch data (must convert to Numpy arrays to facilitate Tensor conversion).

### TODO 3: Training Logic (`train_dqn`)
- **Exploration strategy**: Implement $\epsilon$-greedy decay logic.
- **Target computation**:
  - `double_dqn=False`: $y_j = r_j + \gamma \max_{a'} \hat{Q}(s_{j+1}, a')$
  - `double_dqn=True`: $y_j = r_j + \gamma \hat{Q}(s_{j+1}, \text{argmax}_{a'} Q(s_{j+1}, a'))$
- **Data return**: Must return the `all_rewards` list for later performance evaluation.

## 4. Submission
Please save the completed **`dqn_task.py`** file in the current working directory.

---

### en_dqn_migration

### [Query: Code Migration - DQN Reinforcement Learning]

You are a reinforcement learning researcher who needs to migrate an existing DQN (Deep Q-Network) reinforcement learning algorithm implemented in TensorFlow to the PyTorch framework, and replace the deprecated Gym library with Gymnasium.

**Requirements:**
1. Maintain the core structure of the DQN algorithm (including the neural network model, experience replay buffer, target network updates, etc.) and configuration (including model parameters, loss function, optimizer, etc.) unchanged.
2. Ensure it can run properly in a PyTorch environment, including model training, inference, and interaction with the Gymnasium environment.
3. Add a hyperparameter tuning module to tune some key parameters, record and visualize the performance under different hyperparameter combinations.
4. Visualize the training process, including reward curves, loss function values, etc., to facilitate model performance analysis.
5. Implement all functionality in a single Python file, ensure clear code structure, provide comments at key sections, and add necessary instructions at the beginning of the code (required libraries, how to run, etc.).

**Expected Output:**
- `dqn_torch.py` - A runnable single-file implementation containing:
  - DQN implementation using PyTorch
  - Experience Replay (ReplayBuffer)
  - Target network updates
  - Hyperparameter tuning module
  - Training visualization (reward curves, loss curves, etc.)
  - Able to train and evaluate in a Gymnasium environment (MountainCar-v0)
  - Output training logs and image files

**Context:**
Original TensorFlow code files:
- `context/agent.py` - TensorFlow version DQN agent
- `context/replay_buffer.py` - Experience replay buffer
- `context/main.py` - Main program entry point
- `context/ReadMe.txt` - Original configuration description
- `context/requirements.txt` - Original dependency list

---

### en_emotion_recognition

### [Query Image Classification - Facial Emotion Recognition]
You will be provided with a baseline TensorFlow/Keras implementation for a 5-class facial emotion recognition task using the samithsachidanandan/human-face-emotions Kaggle dataset. The current model is a simple CNN with three convolutional layers, dropout, and a small fully connected layer, trained on 128x128 RGB images with early stopping based on validation loss.

Your goal is to redesign and improve the training pipeline and/or model architecture to significantly enhance validation performance, focusing on model quality and generalization capability.

**Implementation Requirements:**
1. Create a Python script named `train_improved_model.py`
2. The script must train the model and save two files:
   - `emotion_model.h5`: The final trained Keras model
   - `metrics.json`: A JSON file containing the following keys:
     {
       "val_acc": float (validation accuracy, e.g., 0.8955),
       "train_acc": float (training accuracy, e.g., 0.9200),
       "macro_f1": float (macro-average F1 score, e.g., 0.8800),
       "per_class_f1": list (per-class F1 scores, e.g., [0.85, 0.90, 0.88, 0.82, 0.91])
     }

**Training Requirements:**
1. Use the same data loading protocol:
   - Image size: 128x128 RGB
   - Validation split: 0.2 (20% validation)
   - Seed: 281 (for reproducibility)
   - Batch size: 64 (recommended)
   - Label mode: 'categorical'

2. Dataset directory structure:
   - Load from kagglehub: `kagglehub.dataset_download('samithsachidanandan/human-face-emotions')`
   - Or use the provided local path
   - Dataset contains 5 emotion classes

**Improvement Strategies (choose one or more):**
1. **Transfer Learning**: Use a pretrained backbone (MobileNetV2, EfficientNetB0, ResNet50V2)
2. **Data Augmentation**: RandomFlip, RandomRotation, RandomZoom, RandomContrast
3. **Advanced Architecture**: Deeper CNN, residual connections, attention mechanisms
4. **Regularization**: Dropout, L2 regularization, batch normalization
5. **Optimization**: Learning rate scheduling, tuned Adam parameters
6. **Callbacks**: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint


### [Context]
- 0-8955-human-face-emotions-with-simple-conv2d.ipynb (baseline implementation)
- Dataset: samithsachidanandan/human-face-emotions (via Kaggle)

---

### en_f1_driver_advantage

# Benchmark 2 (Revised): Driver "Environment-Stripped" Stable Advantage Index

Description
- **Scoring is based solely on submitted result files (numerical values, structure, consistency, verifiable prediction performance)**; no specific model type is required or checked.
- Participants may use any modeling/inference/machine learning method; the scorer only reads output files and performs automated calculations.

Objective
- Estimate the "driver stable advantage" metric from multi-session lap time data (unit: seconds/lap, higher is better), and provide uncertainty intervals.
- Additionally provide: teammate comparison (within-team differences and significance/confidence intervals), and cross-circuit or cross-session prediction generalization evaluation results (measured by error and interval coverage).

Allowed Data Resources
- Session data (CSV): lap times, pit stop markers, etc.
- Tire data (CSV): compound, tire_age_laps, etc.
- Weather data (CSV): air_temp, track_temp, humidity, wind_speed, rain_intensity, etc.
- Circuit data (CSV): circuit characteristics
- Driver/team data (CSV): driver_id, team_id, etc.
- Data dictionary, version log (Markdown)
- Prohibited: external data sources (race penalties, radio communications, dedicated telemetry signals, or other unprovided resources)

Unified Primary Key & Filtering (Reference; not scored but recommended)
- Primary key: {season, round, session_type, circuit_id, driver_id, stint_id, lap_number}
- Recommended filtering:
  - Exclude laps with is_pit_in==True or is_pit_out==True
  - Exclude laps with lap_time<=0 or extreme outliers (must be reflected in the anomaly list)
  - Wet condition identification: rain_intensity>0 or compound in {Inter, Wet}

---

## Required Output Files and Format (scoring is strictly based on the following files)

1) stable_advantage.csv
- Purpose: Submit the final "stable advantage" metric (method-agnostic).
- Columns:
  - driver_id
  - driver_name (optional but recommended)
  - StableAdv_mean_s_per_lap (stable advantage mean, in seconds/lap, higher is better)
  - StableAdv_low_s_per_lap (interval lower bound, e.g. 95%)
  - StableAdv_high_s_per_lap (interval upper bound, e.g. 95%)
  - sample_laps_used (number of laps used for estimation; used for scoring weight and quality checks)
- Row granularity: one row per driver_id

2) teammate_comparison.csv
- Purpose: Provide within-team comparison output (only numerical values and consistency are scored).
- Columns:
  - season (can be extended for multi-season; recommended even for single season)
  - team_id
  - team_name (optional)
  - driver_id_a, driver_id_b (two teammates, deduplicated by lexicographic order)
  - adv_diff_mean_s_per_lap = StableAdv_mean(a) - StableAdv_mean(b)
  - adv_diff_low_s_per_lap
  - adv_diff_high_s_per_lap
  - laps_used_a, laps_used_b
- Row granularity: one row per (team_id, driver_id_a, driver_id_b)

3) generalization_report.csv
- Purpose: Submit "generalization evaluation" results (method-agnostic; only checks whether results are reasonable and measurable).
- Evaluation protocol (fixed for automated scoring):
  - Submit at least one of two holdout protocols; submitting both yields a higher score ceiling:
    1) Leave-One-Circuit-Out (LOCO): hold out by circuit_id
    2) Leave-One-SessionType-Out (LOSO): hold out by session_type
- Columns:
  - protocol in {LOCO, LOSO}
  - fold_id (e.g. the held-out circuit_id or session_type)
  - n_laps_test
  - error_mae_s (MAE on test set for lap_time, in seconds)
  - error_rmse_s (optional)
  - interval_coverage (proportion of true lap_time falling within prediction interval; leave blank if no prediction interval is provided, but this affects the score)
  - median_interval_width_s (median interval width on test set; leave blank if not provided but affects score)
- Row granularity: one row per fold (must cover at least 80% of all circuits or all session types)

4) lap_level_predictions.parquet (or .csv; parquet recommended)
- Purpose: Used by the scorer to "recompute" generalization error and coverage, preventing submission of summary-only numbers.
- Content: For each test sample lap, output its prediction and interval (no specific model required).
- Columns:
  - season, round, session_type, circuit_id, driver_id, lap_number
  - lap_time_s_true
  - lap_time_s_pred_mean
  - lap_time_s_pred_low
  - lap_time_s_pred_high
  - split_tag (e.g. train/test, used to identify test set samples in generalization evaluation; if the same lap appears in multiple folds, include fold_id)
  - fold_id (aligned with generalization_report; optional but strongly recommended)
- Row granularity: one row per lap (must include at least all test sample laps; recommended to include all laps with labels)

5) anomalies.csv
- Purpose: List of anomalous/excluded laps (only checked for completeness and reasonableness; the detection method is not evaluated).
- Columns:
  - season, round, session_type, circuit_id, driver_id, lap_number
  - reason in {pit_in, pit_out, invalid_time, outlier, missing_feature, wet_excluded, other}
- Row granularity: one row per excluded lap

6) manifest.json
- Purpose: Metadata (not scored for methodology, but used by the scorer to interpret interval semantics and protocol).
- Recommended fields:
  - dataset_version (reference version number or date from the version log)
  - season_range
  - interval_level (e.g. 0.95)
  - wet_handling in {excluded, modeled_together, modeled_separately}
  - protocols_included (LOCO/LOSO)
  - units declaration (time in seconds, temperature in Celsius)

---


**[Deliverable File Requirements]**
- `lap_level_predictions.csv` — Per-lap prediction data
- `schedule.csv` — Schedule data
- `circuits.csv` — Circuit data
- `laps.csv` — Lap time data
Please save the above files in the current directory.

---

### en_fullstack_debug


# Query 3:
## Task Description

```
This task provides a pre-implemented pure frontend React app and a pure backend FastAPI service. Both can run independently, but the frontend-backend integration has not been completed yet, and some features do not work properly.

The application is a "Custom German Vocabulary Notebook" with only the "Verbs" module currently implemented. Key features include:
- Home page displays multiple word category entries (Verbs, Nouns, Adjectives, Prepositions, Adverbs), with only the "Verbs" entry functional
- Verb list page displays all saved German verbs, sorted alphabetically
- Each verb entry shows "German word + Chinese translation"
- Clicking the "View Conjugation" button expands the German verb conjugation table on the current page (no page navigation)
- Users can add new verb entries through the "Add Verb" form

Currently, the frontend and backend have not completed integration regarding API calls, data structures, or state updates.

Your task is:
1. Read and understand the provided frontend and backend code structure and implementation
2. Complete the frontend-backend integration so the frontend can correctly call the backend API
3. Fix issues caused by inconsistent interfaces or data structures
4. Modify the frontend and/or backend code with minimal necessary changes
5. Ensure the application's core functionality works correctly

Expected final results:
- Frontend can correctly load and display the verb list
- Verb list is sorted alphabetically
- Clicking "View Conjugation" correctly renders the verb conjugation table
- After adding a new verb, the list correctly updates and displays the new content
- Frontend-backend communication works without runtime errors

--------------------------------------------------
[Backend Code Structure (FastAPI)]

backend/
├── main.py
│   - FastAPI application entry point
│   - Defines REST API routes
│   - Provides the following endpoints:
│       GET  /verbs        Get all verbs (alphabetically sorted)
│       GET  /verbs/{id}   Get a single verb's details
│       POST /verbs        Add a new verb
│
├── models.py
│   - Defines data models (Pydantic)
│   - Includes:
│       Verb               Verb entity (id, word, meaning, conjugations)
│       Conjugations       Verb conjugation structure
│       Indikativ          Indicative mood (present, past, perfect)
│       Tense              Person conjugation (ich/du/er/wir/ihr/sie)
│
├── data.py
│   - Uses in-memory data storage for the initial verb list
│   - Provides sample verbs with their complete conjugations
│
└── README.md
    - Backend startup instructions (run with uvicorn)

--------------------------------------------------
[Frontend Code Structure (React + TypeScript)]

frontend/src/
├── api/
│   └── verbs.ts
│       - Encapsulates frontend HTTP requests to the backend
│       - Contains methods for fetching the verb list and adding new verbs
│
├── pages/
│   ├── Home.tsx
│   │   - Application home page
│   │   - Displays multiple word category entries (only Verbs is clickable)
│   │
│   └── VerbList.tsx
│       - Verb list page
│       - Responsible for loading verb data and rendering the list
│       - Contains "Back to Home" and "Add Verb" entry points
│
├── components/
│   ├── VerbItem.tsx
│   │   - Single verb entry component
│   │   - Displays word and Chinese translation
│   │   - Controls conjugation table expand/collapse
│   │
│   ├── ConjugationTable.tsx
│   │   - Verb conjugation table component
│   │   - Displays present, past, and perfect tense conjugations for 6 persons in table format
│   │
│   └── AddVerbModal.tsx
│       - Add verb form component
│       - Used to submit new verb data
│
├── types/
│   └── verb.ts
│       - Frontend TypeScript type definitions
│       - Defines Verb, Conjugations, and other interfaces
│
├── App.tsx
│   - Application entry component
│   - Controls switching between home page and verb list page
│
└── main.tsx
    - React application startup entry point
```

## Context

File list:
- All files in ./backend/
- All files in ./frontend/


**[Key Deliverable Files]**
- `frontend/package.json` — Frontend project dependency configuration (required)
- `backend/` — Backend code directory
- `frontend/` — Frontend code directory

---

### en_geometry_circles

## Query

The geometry diagram for the problem is as follows (see attached figure):

* There are two circles:

  * Large circle circle_A
  * Small circle circle_B
* Line CD is the common chord of the two circles
* Point relationships:

  * C, D are the intersection points of the two circles
  * E, H are on the large circle
  * M, N are on the small circle
* Segment relationships:

  * EH is a common tangent line
  * CH perpendicular to CD
  * F is the intersection point of EH and CD
* Given conditions:

  * \( EF = \sqrt{2} \)
* Objective:

  * Find the maximum value of segment \(MN\)

### Expected Output

1. The maximum value of MN
2. The relationship between the maximum value of MN and the radii of the two circles

---

## Context

See the attached figure for the problem (context/asset.jpg)

* The two circles intersect at C and D
* CD is the common chord
* Through C draw perpendicular line CH
* EH is the common tangent line of the two circles
* F = EH intersection CD
* EF = sqrt(2)
* Points M, N are the intersection points of the small circle with a certain secant line
* Find the maximum value of |MN|

---

### en_graph_algorithms

**Task: Implement graph algorithms for network analysis**

You are tasked with implementing several graph algorithms to analyze network topology and find optimal paths. The implementation should be efficient and well-documented.

**Context:**
- A graph representation module is provided in `context/graph.py`
- You need to implement the algorithms in `algorithms.py`

**Requirements:**
1. Implement the following algorithms in `algorithms.py`:
   - Dijkstra's shortest path algorithm
   - Bellman-Ford algorithm (for graphs with negative edges)
   - Floyd-Warshall all-pairs shortest paths
   - Kruskal's minimum spanning tree
   - Topological sort for directed acyclic graphs
2. Each algorithm should:
   - Handle edge cases (empty graph, disconnected components, etc.)
   - Return appropriate data structures (paths, distances, trees)
   - Include time complexity analysis in comments
3. Create a performance comparison report `performance_report.txt` that compares the algorithms on different graph sizes

**Important - Deliverable Location:**
- **Put all deliverables directly in this directory (outside of `context/`)**
- Do NOT put deliverables inside `context/` - they will not be evaluated

**Deliverable:**
- `algorithms.py` - Implemented algorithms (in this directory, not in context/)
- `performance_report.txt` - Performance comparison report (in this directory, not in context/)

**Evaluation:**
The implementation will be evaluated based on correctness, efficiency, and documentation quality.

Note: the spec is in `algorithms.py`.

---

### en_ksat_random_walk

## Query Description
You are acting as a teaching assistant for a theoretical computer science course. Please read the course lecture notes provided in the Context about the "2-SAT Random Walk Algorithm" (including algorithm description, correctness proof, and summary), as well as a problem set `questions.md` about extending this approach to the "k-SAT" ($k \ge 3$) problem.

Please provide detailed solutions for all problems (Problem 1 through Problem 6) in `questions.md`.

**Solution Requirements:**
1.  **Format Standards**: All mathematical formulas must use standard Markdown LaTeX format (e.g., `$\mathbb{P}[X_t = n]$` or `$$ ... $$`).
2.  **Logical Rigor**: For proof problems (especially Q2, Q3, Q4), complete derivation steps must be written out without skipping steps.
3.  **Knowledge Transfer**: You need to refer to the proof approach for 2-SAT in the Context (such as constructing a one-dimensional random walk, coupling methods, Markov's inequality, etc.) and generalize it to the k-SAT case (note the parameter changes when $k \ge 3$).
4.  **Final Conclusion**: In Problem 6, please explicitly give the expression for the constant $c$ in terms of $k$.


## Context
File list:
- 2sat.md
- 2sat_summary.md
- questions.md

---

### en_lc3_calculator

# Query: LC-3 Stack-Based Calculator

## Task Description

Implement a stack-based calculator program using **LC-3 assembly**. The program reads commands and operands from user input and supports the following features:

- **X**: Exit.
- **C**: Clear the stack.
- **+**, **\***, **%**, **@** (XOR), **neg** (negate): Pop operand(s) from the stack top, perform the operation, and push the result; the result must be within [-999, 999], otherwise report an error and restore the stack.
- **D**: Display the stack top (without popping).
- **Digits**: Push a valid integer onto the stack.

The stack grows from high address to low address. The stack region can be a fixed range (e.g., x3FFF to x3FFB). **R6** is the stack pointer. You must implement **PUSH** and **POP** subroutines, with the convention that **R5=0** indicates success and **R5=1** indicates failure (stack empty/full, etc.).

## Workflow

1. **Read context**
   - Read `context/problem_context.md` for LC-3 conventions, stack, and instruction set details.
   - Read `context/operation_list.md` for recommended implementation steps and correspondence with reference code in context.

2. **Implement PUSH / POP**
   - Refer to the stack implementations in context (e.g., 10.push.asm, 10.pop.asm), implement PUSH and POP that follow the task conventions, and correctly maintain R6 and R5.

3. **Implement operations and main loop**
   - Implement OpAdd, OpMult, Opmod, OpXOR, Opneg, OpClear, OpDisplay, etc. The main loop dispatches to the corresponding handler based on the input character, or pushes a number.
   - Pay attention to range checking (e.g., -999 to 999) and restoring the stack on error.

4. **Output**
   - Save the complete LC-3 assembly program to **lab2.asm** (or **answer.asm** / **solution.asm**) in the current directory. The program should begin with `.ORIG x3000` and include all subroutines and the data section.

## Constraints and Assumptions (from Context)

- Use the LC-3 instruction set; stack region and register conventions are specified in context.
- Do not depend on external tools or files other than those in context.
- The .asm files in context are reference snippets (corresponding to textbook figures); you may reference their logic and interfaces, but must independently produce a complete, assembleable, runnable program.

## Deliverables

- **lab2.asm** (or answer.asm / solution.asm): Complete LC-3 assembly source program, including main program, PUSH/POP, all operation subroutines, and data definitions.

## Notes

- Ensure POP returns failure when the stack is empty and PUSH returns failure when the stack is full; when operation results are out of range, report an error and restore the stack as required.
- Evaluation is performed by eval_task calling eval/rubric.py; context only contains background material and reference code, not the evaluation script.

---

### en_locking_dance_choreo

Query:
---

[Query Description]
You are a professional Locking dance choreographer. You need to design a Locking choreography for an 8x8 counts Funk track "Funky Master Lock." Key areas of focus:
1. Deep musical correspondence: movements matching rhythm, instruments, and emotion
2. Technical presentation quality: accurately presenting Locking techniques while maintaining style purity
3. Creative choreographic expression: creative combinations and variations within the Locking framework
4. Performance artistry: energy variation, spatial usage, focus management

[Context]
Please read `context/`:
- `music_specification.md`
- `student_profile.md`
- `style_constraints.md`
- `task_requirements.md`
- `output_format.md`
- `locking_fundamentals.md`

[Output Requirements]
1. Strictly follow the format requirements in `context/output_format.md`
2. Save the final answer as `answer.txt` in the current directory

---

### en_log_security_analysis

**Task: Analyze web server logs to identify security threats**

You are given Apache web server log files. Your task is to analyze these logs to identify potential security threats and generate a security report.

**Context:**
- Log files are in the `context/logs/` directory
- Logs follow Apache Common Log Format
- You should look for:
  - Suspicious IP addresses with unusual activity patterns
  - Potential SQL injection attempts
  - Directory traversal attempts
  - Unusual user agent strings
  - High-frequency requests from single IPs

**Requirements:**
1. Create a Python script `analyze_logs.py` that:
   - Parses all log files in the `context/logs/` directory
   - Identifies suspicious activities based on predefined patterns
   - Generates a security report `security_report.txt`
2. The security report should include:
   - Top 10 suspicious IP addresses with request counts
   - Detected attack patterns with examples
   - Timeline of suspicious activities
   - Recommendations for blocking/mitigation

**Important - Deliverable Location:**
- **Put all deliverables directly in this directory (outside of `context/`)**
- Do NOT put deliverables inside `context/` - they will not be evaluated

**Deliverable:**
- `analyze_logs.py` - Analysis script (in this directory, not in context/)
- `security_report.txt` - Generated security report (in this directory, not in context/)

**Evaluation:**
The analysis will be evaluated based on the accuracy of threat detection and completeness of the security report.

---

### en_mahjong_rl_agent

# Query 1: Reinforcement Learning-Based Mahjong Agent

## [Query Description]

Design a reinforcement learning-based Mahjong agent that can learn reasonable tile-discarding strategies given a hand of tiles and rule constraints, achieving a high win rate across multiple rounds of play. This task aims to apply deep reinforcement learning theory to a complex multi-player game environment, evaluating core abilities in state space modeling, action selection strategy, and reward function design.

## [Background]

Mahjong is a highly complex multi-player imperfect information game involving multiple factors: randomness (drawing tiles), strategy (tile selection), and competition (multi-player rivalry). Designing Mahjong AI requires handling:
- **Large-scale state space**: Hand tile combinations, discard history, inference about other players' possible hands
- **Partial observability**: Cannot directly observe other players' hands
- **Long-term rewards**: The value of a single discard must consider the impact of subsequent multiple steps
- **Multi-agent interaction**: Must respond to strategy changes by other players

Reinforcement learning provides a powerful tool for solving such problems. Through interaction with the environment and receiving reward feedback, the agent can gradually learn effective strategies.

## [Context]

### 1. Mahjong Rules:

**Basic Information:**
- Players: 4
- Total tiles: 136
- Tile types:
  - Characters (1-9), 4 of each, 36 total
  - Bamboo (1-9), 4 of each, 36 total
  - Dots (1-9), 4 of each, 36 total
  - Winds (East, South, West, North), 4 of each, 16 total
  - Dragons (Red, Green, White), 4 of each, 12 total

**Basic Flow:**
1. **Dice Roll to Determine Dealer**: Randomly determine the dealer position
2. **Drawing Tiles**: The dealer draws 14 tiles, the other three players each draw 13 tiles
3. **Taking Turns**: The dealer plays first, then turns proceed clockwise. Each turn, a player draws one tile and then discards one tile
4. **Chow/Pung/Kong Operations**:
   - **Pung**: When you have two identical tiles and someone discards a third identical tile, you may "Pung" to claim it, then discard one tile from your hand. The three tiles are placed face-up on the table
   - **Kong**:
     - **Exposed Kong**: When you have three identical tiles and someone discards the fourth, you may "Kong"
     - **Concealed Kong**: When you have four identical tiles in hand, you may declare a "Concealed Kong"
     - **Added Kong**: After a Pung, when you draw the fourth identical tile, you may "Added Kong"
   - After a Kong, draw one tile from the end of the wall (Kong replacement draw), then discard one tile
5. **Riichi (Optional Rule)**: When in Tenpai (one tile away from winning), you may declare "Riichi", announcing your ready state. After this, you cannot change your waiting pattern, but you receive extra points upon winning
6. **Winning Settlement**: When the winning condition is met (generally 4 sets of sequences/triplets + 1 pair, or special hands like Seven Pairs, Full Flush, etc.), you may declare a win. Points are calculated based on the hand and scores are settled
7. **Draw Game**: If the wall is exhausted and no one wins, it is a draw, with no settlement or special rules applied

**Points:**

| Type | Points | Description |
|------|--------|-------------|
| Basic Win | 1 pt | Basic winning hand, composed of sequences and triplets |
| All Triplets | 2 pts | Entirely composed of triplets (three identical tiles) |
| Full Flush | 4 pts | All tiles are of the same suit (Characters/Bamboo/Dots) |
| Seven Pairs | 4 pts | Composed of seven pairs |
| Win After Kong | +1 pt | Winning immediately with the tile drawn after a Kong |
| Self-Draw | x2 | Winning by drawing your own tile (not from another's discard), score doubled |

Final Score = Base Points x Tile Value Bonus + Kong Points

**Kong Rules and Points:**
- **Exposed Kong** (Kong from another's discard): Each of the other three players pays 1 point
- **Concealed Kong** (Four identical tiles in hand): Each of the other three players pays 2 points
- **Added Kong** (Drawing the fourth tile after a Pung): 1 point

### 2. Agent Interface Requirements

You need to implement the following Agent interface so your agent can interact with the Mahjong game environment:

**Important: Please strictly follow the interface specification below to ensure data formats match exactly, otherwise evaluation will fail!**

```python
# =========================================================
# Agent Interface
# =========================================================

class MahjongAgent:
    """Mahjong agent base class"""

    def act(self, obs: Dict) -> Dict:
        """
        Select an action based on the observation

        Parameters:
        -----------
        obs: Dict
            Observation information (note: this is the actual format passed by the evaluation environment):
            {
                "hand": List[str],          # Current hand tiles, format e.g. ["B1", "B2", "T3", "M5", "E", "S"]
                                            # Characters=B, Bamboo=T, Dots=M; Winds=E/S/W/N; Dragons=P/F/D
                "melds": List[List[str]],   # Punged/Konged tile groups, e.g. [["B1", "B1", "B1"]]
                "riichi": bool,             # Whether currently in Riichi state
                "last_draw": str or None,   # Last drawn tile, e.g. "B5"
                "can_riichi": bool,         # Whether Riichi is currently available
                "other_players": List[Dict] # Other players' information, format:
                    [
                        {
                            "pid": int,            # Player ID
                            "discards": List[str], # Discarded tiles
                            "melds": List[List[str]], # Punged/Konged tile groups
                            "riichi": bool         # Whether in Riichi state
                        },
                        ...
                    ]
            }

        Tile representation format (must be strictly followed):
        - Character tiles: "B1" ~ "B9"  (B = Characters)
        - Bamboo tiles: "T1" ~ "T9"  (T = Bamboo)
        - Dot tiles: "M1" ~ "M9"  (M = Dots)
        - Wind tiles: "E" (East), "S" (South), "W" (West), "N" (North)
        - Dragon tiles: "P" (Red), "F" (Green), "D" (White)

        Returns:
        --------
        action: Dict
            Action dictionary, must contain:
            {
                "type": str,  # Action type, must be "discard" or "riichi_discard"
                "tile": str   # Tile to discard, must be in obs["hand"], format e.g. "B3"
            }

        Notes:
        1. The returned tile must exist in obs["hand"], otherwise it is treated as an illegal action
        2. type only supports "discard" and "riichi_discard"
        3. Tile format must match the input format (e.g. "B1" not "1-Character")

        Example:
        --------
        >>> obs = {
        ...     "hand": ["B1", "B2", "B3", "T1", "T2", "T3", "E", "E"],
        ...     "melds": [],
        ...     "riichi": False,
        ...     "last_draw": "E",
        ...     "can_riichi": False,
        ...     "other_players": [...]
        ... }
        >>> action = agent.act(obs)
        >>> print(action)  # {"type": "discard", "tile": "E"}
        """
        raise NotImplementedError("Subclass must implement the act method")


class RandomAgent(MahjongAgent):
    """Random strategy agent (baseline)"""

    def act(self, obs):
        import random
        hand = obs.get("hand", [])
        if not hand:
            # Edge case: if hand is empty, return a safe action
            return {"type": "discard", "tile": ""}

        tile = random.choice(hand)

        # 10% chance of Riichi (if available)
        if obs.get("can_riichi", False) and random.random() < 0.1:
            return {"type": "riichi_discard", "tile": tile}

        return {"type": "discard", "tile": tile}
```

### 3. Reference Files

- `context/before.py`: Basic implementation code for the Mahjong game environment, including game logic, state management, action execution, etc. You can reference this file to understand the environment interface, but you do not need to modify it.

## [Deliverable Requirements]

### 1. **Python Code Files** (Required)

Implement a reinforcement learning-based Mahjong agent. Suggested file name: `rl_mahjong_agent.py` or similar.

**Core Requirements:**
- **Must implement the `MahjongAgent` interface**, overriding the `act(obs)` method
- **Must correctly handle data formats in obs** (see interface description above), ensure tile representation format is consistent
- Suggested agent class name: `RLMahjongAgent` or `DQNMahjongAgent`, etc.
- Any reinforcement learning algorithm may be used:
  - Value function methods: Q-Learning, Deep Q-Network (DQN), Double DQN, Dueling DQN
  - Policy gradient methods: REINFORCE, Actor-Critic, A3C, A2C
  - Combined methods: Proximal Policy Optimization (PPO), Soft Actor-Critic (SAC)
- Code structure should be clear with necessary comments

**Key Design Points:**
- **State Representation**: How to encode current hand, discards, possible actions, etc. as neural network input
  - Suggested: 34-dimensional tile count vector (Characters 1-9, Bamboo 1-9, Dots 1-9, East/South/West/North, Red/Green/White)
  - Handle tile format conversion ("B1" -> Character 1)
- **Action Space**: Define all possible discard actions
  - Suggested: 34-dimensional action space, each action corresponds to discarding one type of tile
  - Must filter illegal actions (tiles not in hand)
- **Reward Function**: How to design reward signals to guide agent learning
  - Sparse reward: Win +100, Draw 0, Deal-in -50
  - Dense reward (optional): Small reward each step based on changes in Shanten number
  - Combined reward: Incorporate final score, winning hand type, etc.
- **Neural Network Architecture**: What network structure to use (FC, CNN, RNN, etc.)

**Special Note (Regarding Training):**
- Warning: **RL models need training to be effective**; untrained or undertrained models may perform poorly
- Warning: **The evaluation environment will NOT perform training**, it will only call the `act()` method
- Two recommended approaches:
  1. **Pre-trained model**: Provide trained model weight files (e.g., `model.pth`), auto-loaded in `__init__`
  2. **Rule-assisted strategy**: Use heuristic rules as fallback when training is insufficient (e.g., prioritize discarding isolated tiles, preserve sequence/triplet structures, etc.)
- If using a pre-trained model, describe the training process and hyperparameters in the README

### 2. **Training Code** (Optional)

If the agent requires training, provide a training script. Suggested file name: `train.py`.

**Contents should include:**
- Training loop code
- Hyperparameter settings (learning rate, batch size, exploration rate, etc.)
- Training log recording (loss, reward, win rate curves, etc.)
- Model save and load logic

If the model is already trained, provide the **model weight file** (`model.pth`, `model.h5`, etc.) and explain how to load and use it in the README.

### 3. **README.md** (Required)

Detailed documentation that includes at least the following:

```markdown
# Reinforcement Learning-Based Mahjong Agent

## Algorithm Description
- RL algorithm used (e.g., DQN / PPO / A3C)
- State space design: how observation information is represented
- Action space design: how actions are defined
- Reward function design: how reward signals are designed
- Neural network architecture: network structure diagram or description

## Dependency List
```
python >= 3.8
torch >= 1.10  (or tensorflow >= 2.6)
numpy >= 1.20
...
```

## Installation and Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent (load pre-trained model)
python run_agent.py

# Train the agent (optional)
python train.py
```

## Performance
- Game testing: Win rate statistics from 100 game tests
- Comparison with random strategy: Win rate improvement
- Training curves (optional): Reward/win rate changes over training episodes

## References (Optional)
List referenced papers, blog posts, open-source projects, etc.
```

### 4. **Performance Test Report** (Optional)

Provide agent performance test results. Suggested file name: `test_results.txt` or `performance_report.md`.

**Suggested contents:**
- Win rate statistics from at least 100 games
- Comparative experiments with RandomAgent
- Average score per game
- Training curve plots (if available)

## [Performance Requirements]

1. **Functionality**: The agent must run normally and be able to receive observations and output legal actions
2. **Effectiveness**: The agent's strategy should significantly outperform the random strategy (win rate improvement of at least 10% recommended)
3. **Reproducibility**: Provide clear instructions for others to reproduce results

## [Hints]

### Data Format Conversion (Important!)

The evaluation environment uses a tile representation format different from common representations. **Format conversion must be handled correctly**:

| Common Representation | Evaluation Format | Description |
|----------------------|-------------------|-------------|
| 1-Character ~ 9-Character | B1 ~ B9 | B = Characters |
| 1-Bamboo ~ 9-Bamboo | T1 ~ T9 | T = Bamboo |
| 1-Dot ~ 9-Dot | M1 ~ M9 | M = Dots |
| East/South/West/North | E, S, W, N | Wind tiles |
| Red/Green/White | P, F, D | Dragon tiles (Red=P, Green=F, White=D) |

**Example conversion code:**
```python
# Tile mapping table (34 tile types)
TILES_34 = [
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",  # Characters
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9",  # Bamboo
    "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9",  # Dots
    "E", "S", "W", "N",  # East, South, West, North
    "P", "F", "D"        # Red, Green, White
]

TILE_TO_ID = {tile: i for i, tile in enumerate(TILES_34)}
ID_TO_TILE = {i: tile for i, tile in enumerate(TILES_34)}

def hand_to_counts(hand: List[str]) -> np.ndarray:
    """Convert hand tile list to count vector (34-dimensional)"""
    counts = np.zeros(34, dtype=np.int32)
    for tile in hand:
        if tile in TILE_TO_ID:
            counts[TILE_TO_ID[tile]] += 1
    return counts
```

### Algorithm Selection Suggestions
- **DQN series** (Recommended for beginners): Deep Q-Network and variants (Double DQN, Dueling DQN), suitable for discrete action spaces
- **PPO** (Recommended for intermediate): Proximal Policy Optimization, good training stability, suitable for complex environments
- **A3C/A2C**: Asynchronous Advantage Actor-Critic, suitable for parallel training
- **Rule-assisted methods** (Recommended for quick implementation): Heuristic rules + minimal learning, can quickly achieve reasonable performance
- **Others**: REINFORCE, SAC, Rainbow DQN, etc.

### State Representation Suggestions
- **Hand encoding**: 34-dimensional count vector (quantity of each tile 0-4)
- **Seen tile statistics**: Count remaining tiles of each type (inferred from discards)
- **Game state**: Whether Riichi is available, last drawn tile (one-hot encoding), other players' Riichi status
- **Feature engineering**: May add advanced features like Shanten number, effective tile count

### Reward Function Design Suggestions
- **Sparse reward**: Win +100, Draw 0, Deal-in -50
- **Dense reward**: Small reward each step based on hand value changes (e.g., Shanten decrease +5)
- **Combined reward**: Incorporate final score, winning hand type, Kong rewards, etc.
- **Risk penalty**: Negative reward for discarding dangerous tiles (when other players are in Riichi)

### Training Tips
- Use **Experience Replay** to improve sample efficiency
- Use **Target Network** to stabilize training
- Gradually decay **Exploration Rate**: from 1.0 to 0.05
- Consider **Self-play** to improve strategy robustness
- **Training duration**: DQN typically needs 10,000 ~ 100,000 games to converge
- **Pre-training strategy**: Can use imitation learning for pre-training, then fine-tune with RL

### Quick Implementation Suggestions (For Limited Time)

Since RL training takes a long time, consider one of the following strategies:

**Option 1: Rules + Minimal Learning (Recommended)**
```python
class HybridAgent(MahjongAgent):
    def act(self, obs):
        hand = obs["hand"]

        # Use simple rules to select candidate actions
        candidates = self.get_rule_based_candidates(hand)

        # If a trained model is available, use the model to select among candidates
        if self.model and self.is_trained:
            tile = self.model_select(candidates, obs)
        else:
            # Fall back to rule-based strategy
            tile = self.rule_select(candidates, obs)

        return {"type": "discard", "tile": tile}

    def get_rule_based_candidates(self, hand):
        # Rules: prioritize discarding isolated tiles, honor tiles, edge tiles
        # ...
        pass
```

**Option 2: Use a Pre-trained Model**
- Train the model locally and save weight files (e.g., `model.pth`)
- Load the model during Agent initialization
- Note: Training requires at least several hours (GPU recommended)

**Option 3: Pure Rule-Based Strategy (Baseline)**
- Implement heuristic rules, such as:
  - Discard the tile that increases Shanten number the least
  - Prioritize preserving sequence/triplet structures
  - Discard isolated and edge tiles
  - Avoid discarding dangerous tiles (when other players are in Riichi)
- While not RL, this serves as a Baseline reference

### Tools and Frameworks
- **Deep learning frameworks**: PyTorch (recommended), TensorFlow, JAX
- **Reinforcement learning libraries**: Stable-Baselines3 (recommended), RLlib, TF-Agents
- **Environment interface**: Reference context/before.py for environment interaction
- **Shanten calculation**: Can reference open-source implementations (e.g., mahjong-python)

---

### en_meeting_task_extraction

# Extract Task List from Meeting Minutes

Please read the dataset.py file in the workspace directory to understand the dataset preparation method. Your task is to extract action items from meeting transcription text (transcript) and model task dependency relationships.

## Task Requirements

### 1. Action Item Extraction and Normalization

Each action item must include:
- `task_id`: Task ID
- `assignee`: Person responsible
- `action`: Action description
- `object`: Action object (may be empty)
- `deadline`: Due date (if present)
- `source_span`: Position in original text

Output format: `action_items.json` (JSON format task list)

### 2. Task Dependency Modeling

- Automatically infer dependencies between tasks (semantic, temporal, logical dependencies)
- Build an acyclic dependency graph (DAG)
- Output format: `dependency_graph.json` (JSON object containing an edges list)

### 3. Provide Meeting Transcription Text

- Save the meeting transcription text used for extraction as `transcript.txt`

## Deliverables

After completing the task, save all deliverables in the current directory:

1. `action_items.json` - Structured task list (JSON format)
2. `dependency_graph.json` - Task dependency graph (JSON format, containing edges array)
3. `transcript.txt` - Meeting transcription text (for span grounding verification)

---

### en_omniasr_deployment

## Query

I am trying out a new project, omnilingual-asr, a multilingual speech recognition model open-sourced by Facebook. Project URL: https://github.com/facebookresearch/omnilingual-asr. I need to deploy this model on an Ascend (NPU) server. The lab's Ascend server has domain restrictions and cannot load models via the direct load_model method — it can only load models via checkpoint loading. The checkpoints are omniASR_CTC_300M.pt and omniASR_tokenizer.model, but omnilingual-asr does not provide a checkpoint-based loading method. Furthermore, the project depends on fairseq2, and fairseq2n does not support the Ascend platform (aarch64), nor does it support Windows — no precompiled packages are available for any platform.

Your tasks:
1) Configure omnilingual-asr and solve the fairseq2 installation problem so that `pip install omnilingual-asr` succeeds.
2) Implement checkpoint-based loading of the omniASR_CTC_300M.pt model. (Do this after setting up the environment. You must NOT load the model by downloading it from the network — the checkpoint is already provided in the workspace. The official omnilingual-asr project does not provide a checkpoint loading method; you need to learn how by searching the web, reading the fairseq2 code repository, and reading the original omnilingual-asr paper.) The parameter count must be exactly 325_494_996 (strict), with no missing or unexpected keys.
3) Build a simple speech recognition demo: input an English audio file (provided), output the recognized text (WER will be computed), and decode a text segment with the tokenizer (the result must exactly match the reference output).

## Context

Files:
- context/omniASR-CTC-300M.pt - Model checkpoint file
- context/omniASR_tokenizer.model - Tokenizer model file
- context/common_voice_en_444.wav - Test audio file
- context/context.md - Project URL, network domain whitelist, and other contextual information

---

### en_os_lab3_debug

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

---

### en_os_lab3_report

Query:
---

[Query Description]
Task: You are a student in an operating systems course, working on ChCore Lab3 (Processes and Threads). Please write a complete lab report based on the provided lab assignment document and reference materials.
Specific requirements are as follows:
    - The report must include four main parts: Part 1 Thread Lifecycle Management, Part 2 Exception Management, Part 3 System Calls, Part 4 User Program Development.
    - For each exercise (Exercises 1-3, 5-6, 8-9), show the core code you completed in the corresponding files and briefly explain what the code does.
    - For discussion questions (Questions 4, 7), provide logically clear answers with accurate explanations of the principles.
    - Please use Markdown format. Code blocks should specify the language (e.g., c, assembly).
Expected output: A complete `report.md` lab report containing Parts 1-4, showing completed core code with explanations for the specified exercises, providing clear principle-based answers for discussion questions, with code blocks specifying languages and proper formatting.

[Context]
Lab assignment: `lab3_assignment.docx`
Reference materials: `lab3_reference.docx`

---

### en_paper_presentation

Query:
---

[Query Description]
Based on the provided academic papers, perform a detailed analysis of each paper and generate a professional academic paper analysis PPT.

**Task Requirements:**
1. Read and understand all provided paper PDF files
2. Perform in-depth analysis of each paper, extracting core content
3. **First write a detailed paper analysis summary report** (Markdown format)
4. Based on the analysis summary report, use Python's `python-pptx` library to generate the PPT

**Paper Analysis Summary Report Requirements (papers_summary.md):**
This is the foundation for PPT generation and must be completed first. The report should include:

1. **Overview Section**
   - Research field overview of all papers
   - Relationship analysis between papers (technical evolution, method comparison, complementary relationships, etc.)
   - Overall research trend summary

2. **Detailed Analysis of Each Paper** (in paper order)
   - Paper basic information (title, authors, conference/journal, year)
   - Research background and motivation (field status, existing problems, research objectives)
   - Core contributions (3-5 innovation points, with specific descriptions)
   - Method details (technical approach, model architecture, key algorithms)
   - Experiment analysis (datasets, evaluation metrics, main results, comparison with baselines)
   - Strengths and weaknesses analysis (advantages and limitations of the method)
   - Personal insights (evaluation of the paper, inspirations, potential improvements)

3. **Cross-Paper Comparative Analysis**
   - Method comparison table (horizontal comparison of method characteristics across papers)
   - Performance comparison (if shared datasets exist)
   - Applicable scenario analysis

4. **Summary and Outlook**
   - Key technical points summary
   - Future research direction suggestions

**PPT Content Requirements:**
Based on the paper analysis summary report, each paper's analysis should include the following sections (at least 1 slide per section):
1. **Paper Basic Information**: Title, authors, publication venue/journal, year
2. **Research Background and Motivation**: Field status, existing problems, research motivation
3. **Core Contributions**: Main innovations and contributions of the paper (3-5 points)
4. **Methods/Model Architecture**: Detailed description of core methods or models (may include flowchart illustrations)
5. **Experimental Setup**: Datasets, evaluation metrics, comparison methods
6. **Experimental Results**: Main experimental results (tables recommended for display)
7. **Analysis and Discussion**: Ablation studies, visualization analysis, key findings
8. **Limitations and Future Work**: Paper limitations and future research directions
9. **Summary**: Core takeaways of the paper

**PPT Format Requirements:**
1. **Cover Page**: Include "Multi-Paper Analysis" main title, list of all paper titles, generation date
2. **Table of Contents Page**: Clearly list all papers and their corresponding page ranges
3. **Overview Page**: Cross-paper relationship analysis (based on the summary report's overview section)
4. **Separator Pages**: Add a separator page before each paper's analysis, showing paper title and authors
5. **Comparison Page**: Cross-paper method comparison table (based on the summary report's comparative analysis)
6. **Ending Page**: Include "Thank You" or "Q&A"

**PPT Design Specifications:**
1. Slide dimensions: Widescreen 16:9 (13.333 x 7.5 inches)
2. Color scheme: Use a unified professional color scheme (dark blue theme recommended)
3. Font sizes:
   - Title: 32-40pt, bold
   - Subtitle: 20-24pt
   - Body: 18-20pt
   - Table content: 12-14pt
4. Each page should not have too much content, maintain clarity and readability
5. Appropriate use of bullet points and numbered lists
6. Tables should have clear headers and border styles

**Output Requirements:**
1. **Paper analysis summary report**: `papers_summary.md` (must be completed first)
2. **PPT file**: `papers_analysis.pptx`
3. **Structure file**: `ppt_structure.json`
4. **Code**: `generate_ppt.py`

**ppt_structure.json Format Requirements:**
```json
{
  "title": "PPT main title",
  "total_slides": total_slide_count,
  "total_papers": paper_count,
  "generation_time": "generation time in ISO format",
  "summary_file": "papers_summary.md",
  "papers": [
    {
      "paper_id": 1,
      "title": "paper title",
      "authors": "author list",
      "venue": "publication venue/journal",
      "year": "publication year",
      "start_slide": start_page_number,
      "end_slide": end_page_number,
      "sections": [
        {
          "section_name": "section name",
          "slide_number": page_number,
          "content_summary": "content summary (under 50 words)"
        }
      ]
    }
  ],
  "design_info": {
    "color_scheme": "color scheme description",
    "slide_dimensions": "slide dimensions",
    "font_settings": {
      "title_font_size": "title font size",
      "body_font_size": "body font size"
    }
  }
}
```

[Context]
File list:
- `context/paper1.pdf` (first paper to analyze)
- `context/paper2.pdf` (second paper to analyze)
- `context/paper3.pdf` (third paper to analyze)
- `context/paper4.pdf` (fourth paper to analyze)
- https://python-pptx.readthedocs.io/ (python-pptx official documentation)

---

### en_pokemon_game

# Pokémon Gen 3 Style HTML5 Game (Two Phases)

This task requires you to produce a single-file (HTML/CSS/JS) Pokémon Gen 3 style web game, completed in two phases:

## Phase 1 (Prototype Design)
- Tile-based 2D map engine (grass/roads)
- Characters: Player (keyboard arrow keys for movement, using Gen3 protagonist Sprite), NPC (Rival)
- Interaction: Approach NPC and press "Z" to trigger a dialog box; after dialog ends, trigger battle

## Phase 2 (Optimization & Refactoring)
- Add GBA-style encounter battle transition effects (screen flash/blackout/mosaic, etc.)
- Complete battle engine:
  - Background and battle platform
  - Player displays Back Sprite, enemy displays Front Sprite
  - Bottom action panel (Fight/Bag/Run), classic trapezoidal HP bar frame on top
- Gen 3 mechanics (strict):
  - Physical/Special split by type: Special = Fire, Water, Grass, Electric, Psychic, Ice, Dragon, Dark; all others Physical
  - Core damage formula: ((2*Lv/5+2)*Power*A/D)/50+2 (critical hit multiplier 2x; STAB 1.5; type effectiveness 0.5/1/2)
  - Enemy AI: prioritize moves that are super effective against the player; KO if possible; fallback to avoid softlock
- Asset management: Implement AssetLoader/Preloader, prefer PokeAPI Sprites for dynamic loading; display "Loading..." before loading completes; fallback to placeholder on failure
- Interaction & feel: Text character-by-character printing, hit/critical hit/super effective messages, HP bar Lerp animation, hit feedback (shake/flash), input locked during animations

## Resources & References
- Sprite resources (preferred):
  - Enemy front sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png
  - Player back sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{id}.png
  - Emerald style (optional): https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/{id}.png
- Mechanics reference: See context/Reference.docx

## Output Requirements
- Output only a single HTML file (named game.html)
- Code structure should be clear: MapEngine / BattleEngine / GameLoop / AssetManager
- Handle async image loading: Display "Press Start" after resources finish loading

Please generate game.html directly in the working directory.

---

### en_ppo_pendulum

## Reinforcement Learning Assignment 2: PPO Algorithm Implementation for Pendulum-v1 Continuous Environment

### 1. Task Description

**Background**:
In continuous action space environments such as `Pendulum-v1`, traditional Policy Gradient algorithms often suffer from extremely unstable training due to difficulty in determining the step size. This task requires implementing the **Proximal Policy Optimization (PPO)** algorithm, which introduces a **Clipped Surrogate Objective** to constrain the magnitude of policy updates.

**Requirements**:

1. **Algorithm Implementation**: Implement the PPO algorithm based on an Actor-Critic architecture.
* **Actor**: Outputs the mean (mu) and standard deviation (sigma) of a Gaussian distribution.
* **Critic**: Estimates the state value function.


2. **Core Mechanism**: Must include PPO's Clipping mechanism, ensuring the probability ratio between new and old policies stays within a safe interval.
3. **Output Requirements**:
* Submit the `ppo_pendulum.py` code.
* **Performance Target**: After training is complete, perform 5 independent evaluation episodes. **The average return must be greater than -350**.

---

### en_privacy_audit

````markdown
### 1. Query (Task Description)

**Task Name**: Build an LLM-based automated Reddit privacy information identification and audit system.

**Detailed Description**:
You need to develop an end-to-end automation script that accomplishes the following tasks:

1. **Data Cleaning**: Parse the provided Reddit RSS XML data, extract post bodies, and remove HTML tags, escape characters, and Reddit-specific redundant suffixes such as "submitted by".
2. **Privacy Classification**: Use a large language model to classify and label the cleaned text according to 12 predefined privacy categories.
3. **Closed-loop Audit**: Call a higher-tier model as an "auditor" to verify the classification results, outputting JSON-format results of `Confirmed`, `False Positive`, or `Missing`.
4. **Visual Report**: Compute privacy distribution statistics and calculate system accuracy, false positive rate (FPR), and false negative rate (FNR), then generate distribution charts (e.g., Bar Chart).

**Expected Output**:

- A complete, runnable Python script.
- A structured CSV dataset containing at least 50 records (including original text, classification labels, and audit results).
- Two analysis charts (privacy distribution chart and confusion matrix/error rate chart).

```

---

### en_qwen_quantization_deploy

# Query 2

[Task Description]
You are an edge-side AI deployment engineer tasked with completing the full pipeline for mixed-precision quantization deployment of `Qwen2.5-1.5B-Instruct` in a MacBook environment. You need to handle environment setup (create a virtual environment and submit `requirements.txt`), resource preparation (download the original model yourself and manually convert the provided Parquet-format validation set `context/validation-00000-of-00001.parquet` to `validation.jsonl` format), and write a script to generate the mixed-precision `qwen_quantized.pth`.

[Context]
File list:
- `context/validation-00000-of-00001.parquet`: Raw validation data (needs conversion).
- `Qwen2.5-1.5B-Instruct`: Must be downloaded by the user.

---

### en_rag_course_assistant

### [Query System Implementation - RAG Course Assistant]

You need to implement a RAG-based course assistant system.

**Functional Requirements:**
- Document parsing: Support PDF, PPTX, DOCX, TXT, preserving metadata such as page numbers/slides/paragraphs.
- Text splitting: Support chunk_size and chunk_overlap.
- Vector database: Generate embeddings and write to ChromaDB, support Top-K retrieval.
- RAG Agent:
  - Define a system prompt (course assistant role, no fabrication allowed)
  - Retrieve and format context (including filename + page number/slide)
  - Answers must be evidence-based with citations

**Runtime Requirements:**
- Running `python process_data.py` should complete database building
- Running `python main.py` should enable interactive Q&A
- Regardless of whether data/ contains files of a certain format, all four loaders must be implemented

**Deliverables:**
- `process_data.py` — Completes data processing and database building
- `main.py` — Supports interactive Q&A with citations
- `vector_store.py` — Vector storage module
- `rag_agent.py` — RAG Agent core logic
- `config.py` — Configuration file
- `vector_db/` — Built vector database

---

### en_robocasa_camera_move

# Robocasa Camera Movement Implementation

## Task Objective

Implement camera movement functionality in the Robocasa simulation environment, supporting setting different poses for the same camera at each timestep, in order to collect training data for next best view selection models in robot manipulation.

Please work on the current main branch of Robocasa and provide a method for setting camera poses using absolute coordinates in the robot base frame within the Robomimic framework.

## Background

Robocasa is a robot simulation environment based on Robosuite / MuJoCo, designed for robot manipulation tasks in kitchen scenes. This task requires you to understand the camera system in Robocasa/Robosuite and implement the ability to dynamically control camera poses through code.

Camera poses need to be set using absolute coordinates in the robot base frame, rather than the world frame, to facilitate alignment with robot manipulation data.

## Deliverables

Please complete the following three deliverables and save them in the current directory:

1. **Python example script (*.py)** -- A minimal portable solution that can be easily integrated into existing data collection pipelines. The script should demonstrate how to dynamically set camera poses at each timestep and perform offscreen rendering.

2. **Functionality documentation (*.md)** -- A concise document describing the key interfaces needed to implement this feature, including:
   - How to set camera poses (position + orientation)
   - How to perform offscreen rendering
   - Usage examples within the Robomimic framework
   - Notes (coordinate frame conventions, quaternion format, etc.)

3. **Camera trajectory video (*.mp4)** -- Continuous smooth camera trajectory movement in a kitchen scene (e.g., PnPCounterToSink), rendered offscreen as a human-readable video.

## Technical Requirements

- Use Robocasa / Robosuite MuJoCo simulation interfaces
- Camera poses expressed in absolute coordinates of the robot base frame
- Support setting different poses for the same camera at each timestep
- Use offscreen rendering to generate video
- Code should be a minimal portable solution with clear structure

---

### en_sift_algorithm_report

Query:
---

Based on the materials in `context/`, complete a rigorously structured SIFT Algorithm Research Report that combines theoretical depth with practical guidance.

**Materials**
- `context/query3.txt` (task description and output requirements)
- `context/reference1.txt`
- `context/reference2.txt`
- `context/reference3.txt` (if available)
- `context/query3.docx` (may be used as reference if needed)

**The report must include the following five sections:**
1. Core Algorithm Principles and Mathematical Foundations: scale space, DoG approximation, extrema detection, Hessian/curvature, etc.
2. Key Implementation Details: scale-space construction, keypoint detection and localization, orientation assignment, descriptor generation
3. Feature Matching and Robust Estimation: matching criteria, ratio test (Lowe ratio test), RANSAC, etc.
4. Algorithm Performance Evaluation: scale/rotation invariance, illumination robustness, noise/blur impact; provide experimental design and reproducible verification plans
5. Improved/Alternative Algorithm Comparison: compare at least SIFT vs. SURF and ORB in terms of advantages, disadvantages, and applicable scenarios

**Output**
- Save the final version as `answer.md` in the current directory

---

### en_sift_homework_report

# SIFT Homework Report Writing Task (Query 4)

Please complete a high-quality course homework report `report.md` based on the following context:

- context/hw_sift.pdf: Homework requirements (theoretical and programming problems)
- context/sift.py: Your completed SIFT algorithm implementation (for reference)

The report should contain two parts:

## 1. Theoretical Proof (Written Assignment)
- Perspective Projection:
  - (a) Rigorously establish the projection model. From a 3D point $(X,Y,Z)$ through perspective projection to the image plane $(x,y,-f)$, prove that a circle parallel to the image plane still projects as a circle, and derive the standard equation $(x - x_c)^2 + (y - y_c)^2 = r^2$.
  - (b) Derive the vanishing point $(x_v, y_v)$ of a set of parallel lines on the plane $Ax + By + Cz + D = 0$ in the image.
  - (c) Prove that these vanishing points are collinear, and derive the vanishing line equation $Ax_v + By_v + Cf = 0$.
- Verification: Use special cases (e.g., lines on the $y=0$ or $x=0$ plane) to check formula correctness.

It is recommended to include formula blocks (LaTeX), step-by-step derivations, and necessary geometric diagrams.

## 2. Programming Experiment Report (Programming Assignment)
- Core Algorithm Analysis:
  - Explain why DoG is used to approximate LoG and its efficiency advantage in scale space.
  - Describe 3x3x3 extrema detection, contrast threshold, and Hessian edge response suppression.
  - Describe the role of histogram smoothing and parabolic interpolation in orientation assignment.
  - Provide a detailed description of the 128-D descriptor construction process (16x16 region, rotation alignment, trilinear interpolation, normalization-truncation-renormalization).
- Results Presentation:
  - You may insert generated visualizations (e.g., `sift_keypoints_vis.png`) into the report:
    - `![SIFT Keypoints](sift_keypoints_vis.png)`

Please save the completed `report.md` in the root of the current working directory (the workspace root at the same level as this file), and ensure the Markdown structure is well-formatted with LaTeX syntax for formulas.

---

### en_sleep_screen_stats

# Query: Statistical Analysis of Sleep and Screen Time

Based on the 28-day personal data in context/data.csv, complete the following tasks and save all outputs to the current working directory:

1. Data Visualization
   - Must generate a scatter plot of sleep duration vs. screen time (save as `scatter.png`).
   - Choose at least one of: histogram (`hist_sleep.png`/`hist_screen.png`) or box plot (`boxplot.png`) for distribution display.

2. Statistical Analysis and Parameter Estimation
   - Calculate for both datasets: mean, standard deviation, quartiles.
   - Perform normal distribution parameter estimation (mu, sigma) for both sleep duration and screen time, and provide 95% confidence intervals.

3. Correlation Analysis
   - Calculate the Pearson correlation coefficient r and its significance test p-value.

4. Structured Output and Report
   - Write key metrics to `metrics.json` (include fields: `sleep_mu`, `sleep_sigma`, `sleep_ci95`, `screen_mu`, `screen_sigma`, `screen_ci95`, `pearson_r`, `pearson_p`).
   - Generate a report `report.md` or `report.pdf` briefly describing methods, results, and conclusions, with necessary charts included.

Constraints and Tips:
- Use only the local file `context/data.csv`, do not depend on external network.
- Name the code file `analysis.py`; running it directly should generate all the above files.

---

### en_speculative_decoding

# Background

Your large model inference team is maintaining a high-frequency generative text service. The business scenario requires the model to have a certain level of **creativity (Temperature > 0)**. The current online flagship model (Target Model) is constrained by GPU memory bandwidth, and its response latency cannot meet real-time interaction requirements.

The team has decided to introduce a **Speculative Decoding** architecture. You have already obtained a Draft Model whose vocabulary is aligned with the main model.

---

# Task Objective

You need to refactor the existing serial inference pipeline (`inference.py`) to implement a high-performance speculative inference engine that **supports Stochastic Sampling**.

## Core Challenges (Hard Mode)

### 1. Implement Rejection Sampling
   - **Algorithm difficulty upgrade**: The business requires `temperature > 0`. You cannot simply do token comparison.
   - You must implement standard **Rejection Sampling** logic:
     - When $p_{draft}(x) \le p_{target}(x)$, accept unconditionally.
     - When $p_{draft}(x) > p_{target}(x)$, accept with probability $p_{target}(x) / p_{draft}(x)$.
     - **Key constraint**: Upon rejection, you must resample from the **corrected distribution** (Normed Difference Distribution), strictly ensuring the final output distribution $P(x)$ is completely identical to sampling from the Target Model alone (mathematically lossless).

### 2. Zero-Copy KV-Cache Rollback
   - **Engineering difficulty upgrade**: Under extremely high concurrency, frequent `torch.cat` or Tensor reallocation leads to GPU memory fragmentation.
   - You need to implement **efficient rollback**:
     - When speculation is rejected, only modify the "valid length pointer" or perform slice view operations on the KV Cache, **avoiding creation of new KV Tensors as much as possible**.

### 3. Performance Optimization and Verification
   - Analyze the Baseline bottleneck and prove that your parallel verification mechanism can break through that bottleneck.

---

# Key Operation Instructions (Must Read)

To accurately test the acceleration effect of speculative decoding, you need to simulate the ideal case where "Draft Model predictions are very accurate" (i.e., high acceptance rate scenario), otherwise the speedup ratio will not be apparent.

**Please be sure to follow these steps:**
1.  **Run `setup_benchmark.py`**: This script generates vocabulary-aligned `target_model.pt` and `draft_model.pt` (by applying Identity Patch to the last few layers of the Target, making the two distributions converge).
2.  **Write `inference.py`**: Load the generated model weights in the code for testing.

---

# Performance Verification

You need to build test scripts to verify the refactored inference engine:

- **Distribution Consistency (Distribution Match)**:
  - Since randomness is involved, token-by-token comparison is not possible. You need to prove under a fixed Random Seed that the Speculative Decoding output is **bitwise identical** to the Baseline, thereby proving the mathematical correctness of your Rejection Sampling logic.
- **Speedup**:
  - Under conditions of `gamma=4` and `temperature=0.8`, end-to-end throughput (Tokens/Sec) should improve by **1.3x or more** compared to the baseline.

---

# Expected Output

1. **`inference.py`**: Complete implementation containing Baseline and Rejection Sampling Speculative Decoding.
2. **`benchmark_report.md`**: Performance comparison report, must include analysis of speedup ratio changes under different Temperature values.

---

# Technical Requirements

- **Environment constraint**: Do not modify `gpt_lite.py`.
- **Verification mechanism**: The Target Model must compute probability distributions for all Draft Tokens in parallel.
- **Robustness**: The algorithm must handle both `temperature=0` (degenerates to Greedy) and `temperature > 0` cases.
- **Memory safety**: GPU memory peak fluctuations during the Rollback phase are strictly prohibited.

---

# Success Criteria

- [Math] Under stochastic sampling mode, output results are completely identical to Baseline under a fixed seed.
- [Perf] Inference speed is significantly improved (>1.3x).
- [Code] Memory operations are efficient, with no redundant Tensor allocations.

---

### en_speech_model_report

## Query

You are a researcher specializing in Speech Foundation Models. You need to write a comprehensive research report on speech foundation model technology. This report will be used to introduce the latest advances, core challenges, and future development directions in the speech foundation model field to a technical team and management.

Task objective: Based on the provided reference papers and related technical materials, write a professional, comprehensive, and insightful research report covering the following core aspects:

 - Speech foundation model technology evolution: The progression from traditional speech processing to large-scale pre-trained speech models

 - Frontier technical architectures: Detailed analysis of current mainstream speech foundation model architectures, including but not limited to self-supervised learning models, multimodal speech models, speech language models, speech generation models, etc.

 - Key technical challenges: In-depth discussion of core technical challenges in the speech foundation model field, such as data efficiency, computational efficiency, multilingual support, zero-shot learning capability, ethical safety, etc.

 - Evaluation framework analysis: Systematic review of evaluation methods and metrics for speech foundation models, including multi-task evaluation across speech understanding, speech generation, speech recognition, speech synthesis, etc.

 - Application scenario analysis: Analysis of practical applications of speech foundation models in intelligent assistants, education, healthcare, entertainment, accessibility technology, and other domains

 - Future development directions: Predictions of future development directions and potential breakthroughs for speech foundation models based on current research trends

Expected output:

 - A well-structured, in-depth research report (2000-3000 words)

 - The report should include an abstract, introduction, main body chapters, conclusion, and references

 - Use professional academic language while ensuring technical concepts are clearly explained

 - Cite at least 10 important research papers from recent years (post-2020)

 - Include discussion of practical application scenarios

## Context

File list:
- context.md - Detailed abstracts and references of important research papers (2020-2025) in the speech foundation model field

---

### en_sphere_uformer_export

# task1
In this task, you need to read data_rgb.png and data_depth.png, and save them as two .npy point cloud files following the Sphere UFormer input format.
Before starting the coding task, please set up the environment first. If conda is not available, use .venv instead.
For data_rgb.png, save it as rgb.npy, which is a 2D array with n rows and 6 columns. Each row has the first three dimensions as unit sphere xyz coordinates, and the last three dimensions as rgb values conforming to the model input standard.
For data_depth.png, save it as depth.npy, which is a 2D array with n rows and 4 columns. Each row has the first three dimensions as unit sphere xyz coordinates, followed by the depth value conforming to the model input standard.
Note: You need to ensure the data format and applied processing are identical to the original model's default processing method. Required files such as valid_mask can be found under sphere_uformer; please locate them by examining the code yourself. You may need to use trimesh_utils.py.
The final required files for this task are: rgb.npy, depth.npy, and your export script. Please place the script under sphere_uformer/export/. When running, execute `python export/export.py` from within task1/sphere_uformer/src.

---

### en_stock_greedy_algo

# Task: Stock Trading Maximum Profit (Regret-Based Greedy)

## 1. Problem Description
Buy and sell stocks over $n$ days, with a transaction fee $C$ charged for each sale. At most one share can be traded per day. Find the maximum profit.

### Input Format
- First line: $n$ and $C$ ($1 \le n \le 10^5$, $0 \le C \le 10^6$)
- Second line: $n$ integers $a_i$ ($1 \le a_i \le 10^6$)

### Output Format
- A single integer on one line representing the maximum profit.

## 2. Core Approach Guide
- **Context reference**: `./context/Logic_hint.txt` contains the basic idea behind the regret-based greedy approach.
- **Key questions**:
    1. If you buy today and sell at a higher price in the future, the profit is `sell_price - buy_price - C`.
    2. If we buy on day `i`, sell on day `j`, and later discover that day `k` has a higher price (`k > j`), how should we "undo" (regret)?
        - Ideally: buy on day `i`, sell on day `k`.
        - This is equivalent to executing the `(i, j)` transaction, then undoing it and executing the `(i, k)` transaction.
        - **Think**: On day `j`, how can we both settle the `(i, j)` profit and reserve a "virtual buy point" for a future day `k`? What is the cost of this virtual buy point?

- **Algorithm hints**:
    - Use a **min-heap (priority_queue)** to maintain all **potential buy costs**.
    - Iterate through each day's `price`:
        - If `price - C` is greater than the minimum cost at the top of the heap, there is a profit opportunity.
        - At this point, execute the trade and think about how to update the heap to support future "regret" operations.

## 3. Output Requirements
- Provide a complete **C++ code** implementation, saved as **`solution.cpp`**.
- **Note**: All profit and price calculations should use `long long`.

---

### en_svd_model_merging

## Query Description

**Task Background**:
You are an AI researcher reproducing the core algorithms from the paper "No Task Left Behind: Isotropic Model Merging". This paper proposes a merging method that smooths the singular value spectrum of model parameters via SVD (Singular Value Decomposition) to address interference problems in multi-task model merging.

**Task Objective**:
The context provides a code template `merging_interface.py` and a paper summary. Based on the function signatures in `merging_interface.py`, **fill in the missing code** to implement the two core algorithms from the paper:

1.  **Iso-C (Algorithm 1)**: Isotropic Merging in Common Subspace.
2.  **Iso-CTS (Algorithm 2)**: Isotropic Merging with Common and Task-Specific Subspaces.

**Core Implementation Requirements**:
1.  **Interface-based Programming**:
    *   Please strictly follow the input/output definitions of `iso_c_merging` and `iso_cts_merging`.
    *   Do not modify the function signatures.
    *   Do not include file read/save logic (File I/O); focus only on tensor computation.

2.  **Dimension Handling Strategy (Important)**:
    *   **2D Weight Matrices (Weight Matrix)**: Apply the SVD merging algorithm from the paper.
    *   **0D/1D Tensors (Bias, LayerNorm)**: Do not apply SVD. Directly use **Task Arithmetic (Mean)**, i.e., compute the mean of all task vectors, then multiply by scaling coefficient $\alpha$ and add back to the pre-trained weights.

3.  **Algorithm Details**:
    *   **Iso-C**:
        *   Compute the SVD of the Task Matrix sum ($\Delta_{TA}$).
        *   Compute the mean of the singular values $\bar{\sigma}$.
        *   Reconstruct the update matrix using $\bar{\sigma}$: $\Delta_{new} = \alpha \cdot \bar{\sigma} \cdot (U V^\top)$.
        *   Recommended Scaling Coefficient $\alpha = 1.3$ (default parameter).
    *   **Iso-CTS**:
        *   Extract the Common Subspace.
        *   Project each task onto the Orthogonal Complement of the common subspace to extract task-specific directions.
        *   Concatenate the common basis and all task-specific bases.
        *   **Key Step**: Apply **Whitening (Orthogonalization)** to the concatenated basis to ensure orthogonality.
        *   Compute the isotropic factor and reconstruct.
        *   Recommended Scaling Coefficient $\alpha = 1.4$ (default parameter).

**Output Format**:
Please save the completed code as `merging_interface.py`.

---

### en_time_tracking_dashboard


## Query3:
### [Query Page Design]
You are given a "Time Tracking Dashboard" frontend starter project based on a Frontend Mentor challenge. The context includes: an initial index.html with pre-written semantic content, a basic styles.css file, an optional starter script.js, a style-guide.md containing design tokens (colors, fonts, spacing, etc.), JPEG design mockups for mobile and desktop in the /design folder, and an optional data.json file containing time tracking activities with their daily/weekly/monthly statistics.

Your task is to implement and refine this dashboard so it matches the provided designs as closely as possible, using the JSON data file as the sole data source for the activity cards. The dashboard must allow users to switch between Daily, Weekly, and Monthly views via a switcher (such as three buttons or tabs), updating all activity current/previous time statistics accordingly using data from data.json (not hardcoded values in HTML). The layout should be built using modern CSS (preferably CSS Grid) and be fully responsive from mobile to desktop, following the given style guide and design previews. All interactive elements (view switcher, any clickable cards or controls) must have clear hover and focus states.

Your implementation will be evaluated by an AI that loads your page in a headless browser, inspects the DOM structure and CSS classes, simulates user interactions (switching views), validates that data is correctly rendered from the JSON file, and generates a JSON report describing which features passed; that report is then fed into a scoring script to produce a final numerical score for your solution.

### [Context]
time-tracking-dashboard-main.zip

### [Deliverables]
- index.html - Page structure
- styles.css - Styles and layout
- script.js - Interaction logic (render from data.json)
- dashboard_report.json - Test report (generated by test_dashboard.js)

---

### en_tts_research_report

## Query

You are a researcher specializing in the Text-to-Speech (TTS) field and need to write a comprehensive research report on cutting-edge TTS technologies. This report will be used to introduce the latest advances, core challenges, and future development directions in the TTS field to the technical team and management.

Task objective: Based on the provided references and related technical materials, write a professional, comprehensive, and insightful research report covering the following core aspects:

 - TTS technology evolution: The progression from traditional methods to modern deep learning approaches

 - Cutting-edge technical architectures: Detailed analysis of current mainstream cutting-edge TTS architectures, including but not limited to autoregressive models, non-autoregressive models, diffusion models, and flow models

 - Key technical challenges: In-depth exploration of core technical challenges facing the TTS field, such as the balance between generation speed and quality, expressive diversity, cross-lingual/cross-speaker capabilities, etc.

 - Evaluation framework analysis: Systematic review of TTS evaluation methods and metrics, including both subjective and objective evaluation

 - Future development directions: Based on current research trends, predict future development directions and potential breakthrough points for TTS technology

Expected output:

 - A well-structured, in-depth research report (2000-3000 words)

 - The report should include an abstract, introduction, main chapters, conclusion, and references

 - Use professional academic language while ensuring technical concepts are clearly explained

 - Cite at least 10 important research papers from recent years (after 2020)

 - Include discussion of practical application scenarios

## Context

File list:
- context.md - Detailed summaries and references of important TTS research papers (2020-2025)

---

### en_web_automation_scraping

## Query Description

You are a Web automation testing expert. Your task is to write a Python script using **Playwright (Sync API)** to perform specific filtering operations on the `csrankings.org` website and extract data related to Shanghai Jiao Tong University (SJTU).

**Core Task Objective:**
Visit `https://csrankings.org/`, analyze the page DOM structure and interaction logic, filter ranking data for the **2020-2025** period, **World** scope, and **Artificial Intelligence (AI)** field, and extract SJTU's metrics.

**Specific Execution Steps:**

1.  **DOM Analysis (Reasoning)**:
    *   Analyze the HTML structure and infer the locators for "year dropdown", "region dropdown", "field checkboxes", and "data table rows".

2.  **Interaction Logic (Interaction)**:
    *   **Region Setting**: Switch Region to "World" (note the default value may differ).
    *   **Year Setting**: Lock the time range to [2020, 2025].
    *   **Field Filtering**:
        *   Select only **AI and its sub-fields** (Artificial intelligence, Computer vision, Machine learning, NLP, The Web & Information retrieval).
    *   *Note*: This website uses Client-side Rendering. After clicking controls, the URL Hash updates and the DOM table refreshes. The script must include appropriate **wait mechanisms** to ensure data loading is complete.

3.  **Data Extraction (Extraction)**:
    *   Locate "Shanghai Jiao Tong University" in the filtered table.
    *   Extract the following three fields:
        *   **Rank** (ranking)
        *   **Count** (geometric mean paper count)
        *   **Faculty** (faculty count)

**Output Requirements:**
After script execution, it must **only** print a valid JSON object to standard output (`stdout`) in the following format (do not output other debug logs):

```json
{
  "final_url": "Complete page URL at script end (including parameters)",
  "data": {
    "institution": "Shanghai Jiao Tong University",
    "rank": 4,
    "count": 10.5,
    "faculty": 45
  }
}
```

---

## Context
[dom_snippets.html](../context/dom_snippets.html)
This contains key HTML structure snippets of the target webpage. The model should read this content to infer interaction logic. This was obtained by directly previewing the source code in a browser.

---

## 中文 Tasks

### zh_alc_zhishiku

# 1. Query（任务描述）

给定 `context/context.txt` 的中文自然语言文本，构造一个 ALC 知识库 $K=\langle T,A\rangle$。

## 核心任务：抽取为 ALC
请输出以下内容，并**保存到当前目录下的 `alc_kb.txt` 文件中**：

- **TBox**：概念包含公理，形如 `C ⊑ D`
- **ABox**：断言，形如 `C(a)` 或 `R(a,b)`

**要求：**
1. 个体（individual）直接使用原文出现的命名（例如 `霍·阿·布恩蒂亚`、`马孔多`、`梅尔加德斯`、`吉卜赛人` 等），不使用额外命名规范。
2. **每一条** TBox/ABox 语句行末追加原文证据，便于核查：
   - `ALC语句  // evidence: "原文片段"`
   其中注释仅作为核查材料，不属于 ALC 语句本体。
3. 尽可能完整抽取 `context.txt` 中“显式可确定”的信息。

## 追加任务：理解 ALC 的表达边界
在 `alc_kb.txt` 的最后部分（标记为 `Non-ALC Statements`），列举出 `context.txt` 叙事部分中 **至少五条**“无法用标准 ALC（仅 TBox/ABox，且断言只允许 `C(a)` 与 `R(a,b)`）直接表达”的语句或信息点，并逐条解释为什么。

## 输出文件格式示例 (alc_kb.txt)

```text
=== TBOX ===
人物 ⊑ ⊤ // evidence: "..."
...

=== ABOX ===
人物(霍·阿·布恩蒂亚) // evidence: "..."
...

=== Non-ALC Statements ===
1. 原文: "..."
   原因: ...
...
```

## 参考文件
请阅读目录下的 context/context.txt。

### 5. context/context.txt
（内容为提供的 Context.txt 原文，此处省略具体文本以节省篇幅，实际生成时会包含完整内容）

---

### zh_bisai_tongji

# Query 5: 比赛数据统计分析与实力预测

## 任务描述

任务目标：基于给定的比赛数据文件，生成详细的队伍统计报告，并进行实力预测分析。

具体任务要求：
1. 统计分析：对输入的.csv格式比赛数据进行解析，计算每个队伍的以下统计指标：
   - 地图胜率：每张地图的胜负统计和胜率计算
   - 比赛场胜率：BO1/BO3/BO5等不同赛制的胜率统计
   - 连胜连败情况：记录每个队伍的连胜场次和连败情况
   - 对阵历史：分析队伍之间的对战记录和胜负关系
   - 特殊事件统计：迟到、弃赛、判负等情况的统计

2. 实力预测：基于统计结果，对队伍实力进行综合评估和预测，包括：
   - 当前实力排名预测
   - 未来表现趋势分析
   - 关键优势和改进建议

3. 报告生成：生成结构化的分析报告，包含表格、图表和文字分析。

## Context

文件列表（见 context/ 目录）：
- `match_data/`（包含完整的比赛数据，格式符合stats_calculator.py的输入规范）
- `stats_calculator.py`（提供的统计程序，用于对比验证）

数据说明：
```python
# .csv文件采用gbk编码。
# 第一行第一列如果是数字6657，则开始读入后面的内容。
# 第二行填入3个数，依次代表比赛进行的年，月，日。
# 第三行填入一个数n，表示队伍的总数，一个数x，手动设置，调控用
# 接着n行每行填入了五列，第一列代表队伍名；第二列一个数字代表队伍在打这次比赛前的已有排名，如果没有的话则为"*"；第三列一个数字代表队伍在这次比赛的排名。第四列有-1代表弃赛，第五列为手动设置的调分参数
# 接下来若干行代表每一场的记录。
# 对其中的任意一行，第一列一个数字代表该场比赛的性质：如果是1则为BO1，3则为BO3，5则为BO5。
# 第二列一个数字代表该场比赛的重要程度，第三列和第四列代表该场比赛的两个参赛队伍。
# 从第五列起，对每三列有以下的规律：其中的第一列代表第一个队伍的单局比分，第二列代表第二个队伍的单局比分，第三列代表该局所用地图，如果没有则为"*"。
# 对第一局比赛，（如果有的话）-1是迟到，-2是弃赛，-3是判负，另一个填0.
# 读到某一行的第一列为数字123321时，终止读入。
```

## 预期输出

一份完整的统计分析报告（Markdown格式），包含：
1. 总体统计（比赛日期、参赛队伍数量、总比赛场次等）
2. 队伍详细统计（地图胜率、赛制胜率、连胜连败、对阵历史、特殊事件等）
3. 实力预测分析（实力排名预测、趋势分析、关键优势和改进建议）

---

### zh_chepai_shibie

# Query 3：中国车牌识别系统

## 【Query描述】

请写一个 Python 程序，用于对静态图像中的中国车牌信息进行识别。你需要生成一个可交互的 GUI 界面，用户可以在界面中选择车牌图像。程序需要展示：
1. 用户所选图像
2. 车牌部分图像的提取
3. 车牌颜色的识别
4. 车牌文字信息的提取

你需要完成仅针对中国车牌的识别。

**测试集包含378张绿色车牌图片，建议使用HyperLPR3进行车牌识别以获得最佳效果。**

## 【车牌信息说明】

中国车牌包含以下信息：
- **车牌颜色**：绿色
- **省份汉字**：车牌的第一个字符代表省份（如：京、沪、粤等）
- **城市字母**：车牌的第二个字符（A-Z，无 I 和 O）
- **其余字符**：数字和字母的组合（5-6 位）

车牌格式示例：`京A12345`、`沪B·12345`（新能源绿牌）

## 【测试数据】

测试数据位于以下目录：
- `test_images/ccpd_green/` - 绿色车牌（新能源车）

图像文件名包含编码的车牌信息，可用于验证识别准确性。

## 【交付要求】

1. **Python 程序**（建议使用 Tkinter 或其他 GUI 库）
2. **功能要求**：
   - GUI 界面，支持图像选择
   - 显示原始图像
   - 车牌区域定位和提取
   - 车牌颜色识别（绿）
   - 车牌文字识别（省份汉字 + 城市字母 + 其余字符）
3. **输出格式**：
   - 车牌颜色：`绿色` / `蓝色` / `黄色`
   - 车牌号码：完整的车牌字符串（如 `京A12345`）
4. **性能要求**：
   - **识别准确率应达到 85% 以上**（在378张测试图片上）
5. **批量评测输出**：
   - 生成 `recognition_results.json` 文件
   - 包含每张图片的识别结果和准确率统计

## 【重要提示】

⚠️ **避免常见错误：**

1. **OCR选择**: 建议使用HyperLPR3
2. **准确率要求**: 识别准确率应达到 85% 以上（在378张测试图片上）
3. **批量模式**: 程序需要支持 `--batch` 参数进行批量识别，并输出 `recognition_results.json`

## 【技术建议】

**强烈建议使用以下技术栈以确保高准确率：**

### 推荐方案
- **OCR识别**: **HyperLPR3** （专为中文车牌设计，pip install hyperlpr3）
  - 优势：端到端识别，对中文汉字识别准确率高
  - 可直接对完整图像进行识别
  
### 备用方案
- **OCR识别**: EasyOCR, PaddleOCR, Tesseract
  - 注意：EasyOCR单独使用时对中文车牌识别效果较差（准确率约10%）

### 其他依赖
- 图像处理：OpenCV, PIL/Pillow
- GUI开发：Tkinter, PyQt, Gradio

## 【文件名解码说明】

测试图像的文件名包含编码信息，可使用以下函数解码：

```python
def decode_plate(filename):
    """
    从 CCPD 数据集文件名中解码车牌信息
    文件名格式示例：0078125-88_270-267&518_412&567-...
    """
    provinces = "皖沪津渝冀晋蒙辽吉黑苏浙京闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新"
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # 无I和O
    chars = letters + "0123456789"

    parts = filename.split('-')
    codes = list(map(int, parts[4].split('_')))

    plate = provinces[codes[0]]  # 省份
    plate += letters[codes[1]]    # 城市字母
    for c in codes[2:]:
        plate += chars[c]
    return plate
```

此函数可用于验证你的识别结果，但**不要直接使用它作为识别方法**。

请将最终程序保存为 `license_plate_recognition.py`。

---

### zh_chuanxi_diaoyan

# 背景

“你现在是一支 8 人大学生社会实践考察团的领队，负责 2026 年 7 月为期 7 天的川西学术调研。

你的核心目标是： 在 20,000 元 的预算红线内，带领团队完成从立项、执行到安全返程的全过程，并提交最终的成果报告。”

## 任务逻辑时间点

“请注意，你的任务包含两个逻辑时间点：

规划时点（模拟出发前）：请忽略 System_Config 和 Dynamic_Updates 中的实时状态，仅基于 Initial_Data 设计一份完美的 7 天理塘-稻城方案。

执行时点（模拟 7 月 4 日）：此时请将自己代入到 System_Config 指定的时间和位置，审视 Dynamic_Updates。你必须像真实领队一样，基于当前情况动态调整方案，在保留前 3 天已发生事实的基础上，重构后 4 天的方案。”

## 执行要求

### 环境感知

你必须实时调取 Context/ 文件夹下的所有数据（包含 System_Config.json、Initial_Data/ 和 Dynamic_Updates/）。

### 动态决策

#### 立项阶段

根据背景资料自主确定调研主题，并设计一套满足海拔安全规律与财务报销红线的初始方案。

#### 执行阶段

请根据 System_Config.json 确定的‘当前系统时间’，自行判断当前环境下是否存在影响任务的突发变量。

#### 响应与重构

若感知到外部环境（路况、政策等）发生不可抗力变化，你必须立即自主启动预案，调整调研主题、重构路线并重新配平预算。

## 预期输出

- 《社会实践全流程执行档案》：包含初始方案、执行过程记录、以及针对突发事件的决策分析。
- 《财务审计报告》：最终的开支明细（含损失核算），需证明未超支。
- 《学术调研成果》：基于实际抵达地点的调研产出。

## 注意

评价你表现的最高准则是：在极端环境下，能否在不超支、不违规的前提下，实现学术价值最大化并确保全员安全。

---

### zh_datika_yueju

# 任务：高中物理答题卡自动化阅卷

## 1. 任务背景
你现在是一名高中物理老师的助教。你需要利用计算机视觉和逻辑处理能力，批量识别学生的答题卡扫描件，并计算最终得分。

## 2. Context 上下文文件信息
所有必要文件存放在当前目录的 `context/` 文件夹中：

| 文件/文件夹 | 路径 | 说明 |
| :--- | :--- | :--- |
| **pictures/** | `context/pictures/` | 包含 46 张学生答题卡扫描件（jpg/png）。 |
| **answer.txt** | `context/answer.txt` | 包含客观题（1-30题）的标准答案及主观题的评分细则。 |

## 3. 任务要求
1. **客观题识别**：自动识别答题卡中第 1-30 题的填涂结果。
2. **分值计算**：
   - 对比 `answer.txt` 计算客观题得分。
   - 识别或提取扫描件中的主观题得分（如果图片上有标记）或按细则汇总。
3. **最终汇总**：输出每位学生的客观题得分、主观题得分以及总分。

## 4. 输出格式
请将 46 位学生的阅卷结果汇总，并以 **JSON 列表** 格式保存为 **`grading_results.json`**。
列表中的每个对象必须包含 `total_score` 字段。
示例格式：
```json
[
  {"student_id": "01", "objective_score": 40, "subjective_score": 34, "total_score": 74},
  ...
]

---

### zh_esp32_fenxi

Query3: 代码功能识别与分析报告生成

---
### [Query 描述]

你是一个技术文档工程师，需要分析给定的嵌入式系统代码项目，识别其中的核心功能模块和技术实现，并生成一份详细的技术分析报告。

任务目标：
1. 分析提供的Arduino ESP32代码文件，识别代码实现的主要功能和技术特性
2. 理解硬件接口配置、通信协议和外设驱动实现
3. 分析音频处理流程、显示控制逻辑和传感器数据采集机制
4. 识别代码中的潜在问题和优化建议
5. 生成结构完整、技术准确的分析报告

预期输出：
- 完整的项目技术分析报告（Markdown格式）
- 针对每个功能模块的详细技术说明
- 代码质量评估和改进建议

### [Context]

文件列表：
- Code/（项目根目录）
- ESP32手势控制小车实验报告.docx（测试用实验报告样例）

硬件规格说明：
- 主控芯片：ESP32-S3
- 音频编解码器：ES8311
- 运动传感器：QMI8658 IMU
- 显示屏：ST7735S TFT屏幕
- 通信接口：I2C、I2S、SPI、蓝牙

报告样例结构：

```docx
# 项目技术分析报告
## 1. 系统概述
## 2. 硬件架构分析
## 3. 软件模块设计
## 4. 核心算法实现
## 5. 性能评估
## 6. 优化建议
## 7. 总结
```

---

### zh_excel_zhengli

Query 3:
---
【Query 描述】
任务：EXCEL汇总表整理

你需要基于提供的原始 Excel 文件 `EXCEL汇总表整理.xlsx`，对学生奖学金信息汇总表进行数据清洗、去重、排序与排版美化，并最终另存为 `EXCEL 汇总表整理_完成.xlsx`。

强约束：
- 不得查看或使用参考答案文件 `EXCEL 汇总表整理_完成.xlsx` 的任何内容（该文件仅用于评分对照）。
- 允许使用 Excel 手工操作，或使用 Python + openpyxl 自动化处理。

Sheet1（完成后命名为“汇总表”）要求：
1、字体与版式
- 所有普通单元格：横排文字、宋体、黑色、11号；不加粗/不倾斜/无下划线/无删除线/无填充色（规则要求的黄色/红色标注除外）。
- 第1行标题：合并后居中，黑体 18号 加粗，黑色；标题行不加边框。
- 第2行表头：宋体 12号 加粗，黑色，居中。
- 行高：全表统一 25。
- 适当调整列宽以保证内容可读；内容整体水平居中。
- 取消所有超链接。

2、表头顺序（可见列必须严格一致）
可见列的表头顺序必须为：
序号、奖励/资助年度、学号、姓名、班级、学院、奖学金名称、金额、性别、在读学位、生源地、民族、成绩、专业排名、联系电话、E-mail、基本情况、评审类型。

同时需要按要求插入并隐藏两列辅助列：
- 在“学号”后插入“学号长度”（用于 LEN 计算，最终需隐藏）。
- 为实现姓名对齐与查重：保留“原姓名”列（最终需隐藏），并在其后生成“姓名”列作为最终显示姓名（最终保留）。

3、去重（同一位同学）
- “重复项”指同一位同学重复出现；以“学号”为主键进行去重（若学号为空，可退化为“原姓名+联系电话”）。
- 对于重复记录：删除后出现的记录（行号更靠后的优先删除），保留最先出现的那一行。
- 对“被保留的重复学生记录”进行红色背景标注（整行或至少“姓名”单元格均可接受，以能明显标识为准）。

4、各列数据清洗与规范
- 学号、联系电话：单元格格式设为文本（@）。
- 学号长度：
  - 在“学号长度”列用 LEN 公式统计（如 学号长度=LEN(学号)）。
  - 学号长度不足 12 位判为错误，并用黄色背景标注（标注位置可为“学号”或“学号长度”单元格，但需明显）。
  - 最后隐藏“学号长度”列。
- 姓名：
  - 最终显示姓名在“姓名”列。
  - 二字姓名需在中间加空格以与三字姓名对齐，必须使用公式实现（允许等价公式写法；只要实现“二字名中间插入空格、三字名不变”的逻辑即可）。
    示例（仅示例，不要求完全一致）：姓名=IF(LEN(原姓名)=2, MID(原姓名,1,1)&" "&MID(原姓名,2,1), 原姓名)。
  - 若存在姓名重复（以“原姓名”列判断），则对这些同学在“姓名”列进行红色背景标注；最后隐藏“原姓名”列。
- 学院：统一为全称（全称与排序顺序以 Sheet4 为准）。
  - 说明：Sheet4 给出的“学院顺序”可能按一列（自上而下）或按一行（自左向右）呈现；以出现顺序作为学院排序顺序。
- 金额：删除“元”，且为整数（例如 5000），不保留小数。
- 在读学位：统一为“本科 / 硕士 / 博士”。
- 生源地：删除“省/市/自治区”等后缀（如“云南省”→“云南”，“北京市”→“北京”）。
- 民族：删除“族”（如“汉族”→“汉”）。
- 基本情况：垂直对齐靠上、自动换行。

5、排序与重新编号
按以下优先级多级排序：
- 学院（按 Sheet4 的学院顺序）
- 在读学位（本科→硕士→博士）
- 评审类型（新→续→补）
- 金额（从小到大）
排序完成后，按当前顺序重新编号（序号从 1 开始连续）。

6、边框
- 标题行无边框。
- 表头+内容区域有细边框；表格外侧边框加粗。

7、冻结窗格
- 冻结前两行、前四列。
- 说明：评分以“冻结效果”为准（即前两行与前四列在滚动时保持可见），不强制要求 freeze_panes 的具体坐标必须为某一个单元格。

Sheet2（完成后命名为“打印版”）要求：
- 将“汇总表”复制到 Sheet2。
- 仅保留并展示以下列：序号、学号、姓名、学院、金额、在读学位、民族、评审类型。
  - 说明：允许通过“删除多余列”或“隐藏多余列”实现；评分时以“未隐藏列（可见列）”为准进行检查。
- 设置打印格式：
  - 纸张方向横向；
  - 页面水平居中；
  - 所有可见列在一页内打印；
  - 适当调整页边距。
  - （可选加分/建议设置）打印标题为前两行。

Sheet3 要求：
- 用公式统计“汇总表”中汉族同学人数与奖学金总金额，并填写在对应单元格右侧：
  - A1=“汉族同学人数”，B1 使用 COUNTIF 统计“民族”列中等于“汉”的数量。
  - A2=“奖学金总金额”，B2 使用 SUM 对“金额”列求和。
- 统计范围要求：
  - 从第 3 行数据开始，覆盖到最后一行数据（允许使用整列引用，如 民族列:民族列、金额列:金额列；或使用明确的 3:末行范围）。
  - 不要求固定列字母（应以“汇总表”表头定位“民族/金额”所在列）。

最后：将文件另存并重命名为 `EXCEL 汇总表整理_完成.xlsx`。

【Context】
CONTEXT
└─Excel_Organization
        EXCEL 汇总表整理_完成.xlsx
        EXCEL汇总表整理.xlsx
        rubric.py

【参考答案】
参考答案文件：`EXCEL 汇总表整理_完成.xlsx`

【Rubric】
采用自动评分脚本 `rubric.py`，使用其中的 `evaluate(answer, query, context_dir)` 对提交的 `EXCEL 汇总表整理_完成.xlsx` 进行评分。
评分总分 100 分，分项如下：
- A. 去重与排序（25 分）：去重正确性、重复项标红、排序规则、序号重编。
- B. 数据规范化（20 分）：学号/电话文本、金额整数化、学位/生源地/民族清洗、学院全称。
- C. 格式与表格设置（30 分）：字体字号、标题/表头格式、行高、边框、隐藏列、冻结窗格。
- D. 公式与函数（15 分）：LEN、IF 公式存在且引用正确；Sheet3 的 COUNTIF 与 SUM。
- E. Sheet2/Sheet3（10 分）：打印版列选择与基本打印设置；统计表结构与公式。
- F. 文件完整性（5 分）：文件名正确、关键工作表齐全且可打开。

---

### zh_gailv_daan

Query:
---

【Query 描述】
任务：你是一名概率统计课程的老师，你需要为学生提供一份往年考试题目的参考答案，以帮助他们更好地理解考试内容和题型要求并检验自己的知识掌握程度。你需要对给定的考试题目进行细致的分析解答，编写一份详细、准确的参考答案文档。具体要求如下：
    - 请确保参考答案涵盖对所有题目的解答。
    - 所有解答需要保证准确性，概念定义使用正确，计算清晰无误。
    - 参考答案文档请使用 Markdown 格式进行编写，并在每道题目后面附上考察的知识点说明，具体格式参考如下：
1. 对于选择题：
```markdown
题号. 题目内容
选项：A. 选项1 B. 选项2 C. 选项3 D. 选项4
<正确答案>
解题思路：
   分析过程
   ...

知识点说明：简要说明该题目考察的概率统计知识点


eg: 
1. 这是一道用于示例的选择题目：
A. 正确选项 B. 错误选项1 C. 错误选项2 D. 错误选项3
正确答案：A
解题思路：
   这是一段测试解题思路的内容
   ...
知识点说明：这是一段测试知识点说明的内容
```
2. 对于简答题：
```markdown
题号. 题目内容
解：
   详细解答过程
   ...
<最终结果>（一般为数字或表达式)

知识点说明：简要说明该题目考察的概率统计知识点


eg:
2. 这是一道用于示例的简答题目：
解：
    这是一段测试解答过程的内容
    ...
正确答案：1

知识点说明：这是一段测试知识点说明的内容
```
预期输出：一份完整的 Markdown 参考答案文档，对 `卷1.pdf` 中的所有题目提供准确解答，包含选择题答案与解题思路、简答/计算题的详细推导与最终结果，并在每题后标注“知识点说明”。

【Context】
考试题目文件：`卷1.pdf`

---

### zh_geci_chuangzuo

Query:
---

【Query 描述】
从唐诗宋词元散曲中选择一篇或几篇作品作为素材，以自己喜欢的某首现代歌曲为结构模板，创作一首意象丰富、具有意境的现代歌词。可以借用原作意境，并将主题适当现代化。

【输入】
素材位于：
- `context/`（PDF：古典文学作品选集、歌词选等）

【要求】
1. 选择古典文本与现代歌曲各一份（可在 lyrics.md 开头注明）
2. 体现 verse / chorus 等现代歌曲结构（可用小标题标注）
3. 突出意象融合（造境、借境），并保持语言可唱性与现代表达

【预期输出（保存到 workspace 目录）】
- `lyrics.md`（最终歌词正文）

---

### zh_hangzhou_lvyou

# 杭州旅行规划任务

你需要为用户规划一次杭州旅行。

## 用户需求
用户描述：我计划 6 月去杭州旅游 3 天，第一次去，偏好自然风景和历史文化，不想太累，希望行程合理一些。

## 任务要求
1. 将用户的总体需求拆解为若干明确的子问题
2. 基于 workspace 目录下提供的信息源检索相关信息：
   - official_attractions.md：官方旅游局发布的景点介绍与开放信息
   - travel_guides.md：来自主流旅游平台的多篇攻略摘要
   - evaluation_criteria.md：信息可靠性与时效性评估标准
3. 评估信息的可靠性、时效性和相关性
4. 生成一份结构清晰、可执行的旅游攻略

## 输出要求
生成的 travel_plan.md 应包含：
- 完整的 3 天行程安排（每天包含上午、下午、晚上的活动）
- 符合用户偏好（自然风景 + 历史文化）
- 体现轻松节奏（不想太累）
- 包含实用信息（交通、开放时间、用餐建议等）
- 提供实用贴士和建议

完成任务后，将 travel_plan.md 保存在当前目录下。

---

### zh_huaxue_jingsai

## Query：化学竞赛试题解答
**角色设定**：你是一名资深计算化学专家。
**任务目标**：针对附件中提供的第 36 届中国化学奥林匹克（初赛）试题（包含手写扫描图），给出完整的解析步骤和最终结论，保存为 `answers.md`。
**核心要求**：
1. **多模态识别**：
    - 调用 OCR/VLM 能力精准提取手写实验参数及复杂化学方程式。
    - 使用 VLM 识别并描述晶体空间群结构（如：指出配位原子环境、晶胞参数 $a, b, c$ 之间的几何关系）。
    - 识别有机分子结构简式，特别是涉及到旋光性、构型（R/S）或顺反异构的部分。
2. **逻辑推理与计算**：
    - **热力学计算**：必须调用计算工具计算反应的标准摩尔焓变 $\Delta_r H_m^\theta$ 或吉布斯自由能。
    - **晶体密度**：根据 VLM 提取的晶胞体积及 OCR 提取的原子种类，精确计算该物质的理论密度 $\rho$。
    - **有机合成**：推导目标产物的合成路径，需指出每一步的反应类型。
3. **Context 遵循**：
    - 在解析过程中，必须引用 Context 提供的"实验室特殊标准规范"（例如：特定的有效数字保留要求、特定的热力学常数取值）。
4. **输出要求**：
    - 解析过程需严谨，所有化学式及数学公式必须使用 LaTeX 渲染。
    - 最终结论需单列。

**输出示例格式**：
```
## 第 1 题
**1-1** 解答内容...
**1-2** 解答内容...

## 第 2 题
**2-1** 解答内容...
...
```

---

## Context
试题详见 context 文件夹，共 10 道题目。图片文件为手写扫描图，请使用 VLM 进行识别。

---

## Multimodal File Analysis

For analyzing image contents, an OpenAI-compatible API is available via environment variables:
- `OPENAI_API_KEY` - API key
- `OPENAI_API_BASE` - API endpoint

To list all available models, curl the `/v1/models` endpoint:
```bash
curl -H "Authorization: Bearer $OPENAI_API_KEY" $OPENAI_API_BASE/models
```

Example usage:
```python
import os
from openai import OpenAI
client = OpenAI(base_url=os.environ["OPENAI_API_BASE"], api_key=os.environ["OPENAI_API_KEY"])

# For vision tasks, use a vision-capable model
response = client.chat.completions.create(
    model="gemini-2.5-flash",  # or other vision-capable model
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this chemistry problem..."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
    }]
)
```

---

**Important - Deliverable Location:**
- **Put all deliverables directly in this directory (outside of `context/`)**
- Do NOT put deliverables inside `context/` - they will not be evaluated

---

### zh_jiazu_tupu

# 任务：《百年孤独》布恩迪亚家族图谱构建

## 1. 任务背景
你需要从《百年孤独》的原始文本 `context/raw_text.txt` 中，构建一个精确的、结构化的布恩迪亚家族知识库。

## 2. 核心任务要求
1. **实体消歧（关键）**：
   - 家族中存在大量的同名者。请务必根据其**代际**、**配偶**、**职业（如上校、神父、研究者）**或**结局**来区分不同的“奥雷里亚诺”和“何塞·阿尔卡蒂奥”。
2. **关系抽取**：
   - 提取姓名、代际、父母、伴侣及性格命运特征（traits）。
3. **输出格式**：
   - 必须保存为 **`solution.json`**，且包含一个 `characters` 列表。

## 3. 结果 Schema 规范
为了确保阅卷系统能正确读取你的结果，请在 `relations` 字典中使用以下 **标准 Key**：
- `parents`: 列表格式，包含父母姓名。
- `spouse`: 字符串，指受法律认可或主要的配偶。
- `mistress`: 字符串或列表，指情妇或非正式伴侣。
- `children`: 列表格式，包含所有子女人名。

## 4. 深度实现提示
请在分析文本时，重点核实并体现以下细节：

- **家族早期纽带**：有一位女性，她分别与布恩迪亚家族**第二代**的两兄弟都有过私生子，请准确记录她在两兄弟关系中的角色。
- **美貌与飞升**：注意家族中一位被冠以“美人儿”称号的女性，应包含她最终脱离尘世的特殊结局。
- **生活在别处的双胞胎**：区分第四代的双胞胎。其中一人生活极度放荡，请同时记录他的**正式妻子**和**情妇**。
- **末代血缘与宿命**：重点分析**第七代**婴儿的生理特征。该婴儿是第六代的奥雷里亚诺·巴比伦与他的**姨妈**之间产生的后代，请在关系中准确反映这一特殊的伦理逻辑。

## 5. 输出示例
```json
{
  "characters": [
    {
      "name": "何塞·阿尔卡蒂奥·布恩迪亚",
      "generation": 1,
      "traits": "家族创建者，沉迷科学，最终在栗树下发疯。",
      "relations": {
        "spouse": "乌尔苏拉",
        "children": ["何塞·阿尔卡蒂奥", "奥雷里亚诺", "阿玛兰妲"]
      }
    }
  ]
}

---

### zh_jidi_fuxi

# Query

你是一名学习助理 Agent，需要帮助我为《走进极地》课程期末考试做系统复习。
我提供了该课程的所有课件 PDF（共 13 份或以上，文件名见 Context 列表）。请你完成以下任务，并严格按照 output_format.md 中的格式输出：

### 任务要求
#### 课件逐份总结（Lesson Summary）

将所有课件内容整合成一份可用于期末冲刺的复习笔记，要求：
逻辑清晰、分层标题结构完整
必须包含一张"知识结构图"式的文本版思维导图（用缩进 + 编号表示即可）
必须包含一个"高频概念对照表"（如：冰川 vs 冰盖 vs 冰架；FYI vs MYI 等）
生成一份模拟试卷（Mock Exam Paper）

试卷必须覆盖所有课件主要内容，题型包括：
单选题 20 题（每题 4 选 1）
简答题 6 题（每题给参考答案 + 评分点）
论述题 2 题（必须跨至少 2 份课件的知识点，给出高质量参考答案 + 评分 rubric）
试卷需要附上完整答案解析，并标注每题对应的课件来源（文件名 + 页码范围）。

禁止编造课件中不存在的概念；若不确定请明确说明"不在课件中"。
所有关键结论都应能在课件中找到依据，并要标注"课件文件名 + 页码"。
输出内容必须严格符合 output_format.md 中的结构，不得随意更改标题或字段名。
模拟试题的答案解析中必须体现推理链条（而不仅是结论）。

#### 输出文件
- `study_notes.md` — 复习笔记
- `mock_exam.md` — 模拟试卷（含答案解析与引用）

请严格遵循 Context 中的 `output_format.md` 和 `allowed_rules.md`。

## Context
文件列表（PDF 课件）：

第一课.pdf
第二课.pdf
第三课.pdf
第四课.pdf
第五课.pdf
第六课.pdf
第七课-Part1.pdf
第七课-Part2.pdf
第八课.pdf
第十三课-极地资源与治理.pdf
走进极地2025-第10节.pdf
走进极地2025-第11节.pdf
走进极地2025-第12节.pdf

额外规范文件：

output_format.md（规定最终输出的结构模板）
allowed_rules.md（规定禁止事项、引用格式、不得编造等要求）

---

### zh_liaotian_niandu_baogao

# 任务说明：DeepSeek 聊天记录年度总结报告生成

请在当前工作目录中，基于提供的 107 条用户与 DeepSeek 模型的聊天记录（位于 `context/` 目录），生成一份结构化的年度总结报告（Markdown 格式）。

## 具体要求

1. 对话内容分析：
   - 主题分类与频次分布
   - 高频问题与关键对话模式
   - 时间分布特征（如日/周活跃时段）
   - 模型回复类型与特点总结

2. 用户画像分析：
   - 推断用户的专业背景/兴趣领域
   - 使用场景与需求类型
   - 对话风格与交互特征
   - 可能的职业/教育阶段

3. 年终总结与建议：
   - 提炼年度关键对话成果
   - 总结协作模式演变
   - 分析亮点与特殊时刻
   - 提出未来对话优化建议（具体、可操作）

## 输出要求

- `report.md`：Markdown 格式的完整报告，长度约 1000 字，包含明确的章节和要点列表；允许使用文字描述方式给出统计图表（无需生成真实图像）。
- （可选）`analysis.json`：如有进行量化统计，可将主题频次、时间分布等数据要点写入此 JSON 文件，便于评估使用。

## 注意事项

- 请不要在报告中包含参考答案或完整的评分标准。
- 请仅使用 `context/` 目录中的聊天记录作为数据来源，不要引入外部数据。
- 所有生成的文件保存到当前工作目录。

---

### zh_majiang_jisuanqi

# Query 1: 立直麻将晋级条件计算器

## 【Query 描述】
### 背景
在多半庄规则下，由于顺位马点的出现，晋级条件随着不同的胡牌点数，
有很多变化，计算显得很困难。故需要设计一个计算器，对每个人的晋级条件进行总结，
方便选手进行决策。

### 需求：
你需要生成一个可执行文件，用于计算立直麻将的晋级条件。推荐使用java进行编程。
1. 输入信息： 四位选手的id，该半庄前总积分（pt），半庄当前状态（默认此时已到达了南场或者WRC规中已到达牌局最后一局，即如北家下庄即结束本场），选手目前点数，本场数，供托数。
2. 晋级条件：支持前1/2/3位晋级，计算条件。
3. 马点计算：至少需要支持M-League规则、A规、WRC规、最高位规的规则，后续可以增加更多规则。
相关规则请根据补充材料中的网页进行查询。（WRC规默认此时时间已到，本局为终局）
4. 结果生成：需要对每个选手自摸/从剩余三家荣胡/向剩余三家放铳所可以达成晋级的条件进行输出；
对每个选手由于横移动从而失去晋级条件的危险区间进行计算；
对流局的所有16种情况进行计算。
（注：不计算役满包牌、由于违反规则被罚点等过于特殊的情况）

## 【Context】
文件列表：
- 世界立直麻将大赛WRC规则 https://ooyamaneko.net/download/mahjong/riichi/WRC_Rules_2025_en.pdf 
- M-League规则 https://m-league.jp/about
- 日本职业麻将联盟竞技规则（简称A规） https://www.ma-jan.or.jp/guide/game_rule.html
- 最高位战日本立直麻将协会规则 https://saikouisen.com/about/rules/

测试用例详见 context 目录中的 `test_inputs.md`。


## 【交付要求】

1. 完整的Java源代码
2. 编译后的可执行jar文件
3. README.md，包含：
   - 编译和运行指南
   - 输入格式说明
   - 输出格式说明
   - 使用示例


## 样例

### 输入：

    当前亲家：北
    座次： 东 南 西 北
    名字： W1de Lemontruth 浅梦 kagayaki
    开始前总分 -46.5 63.1 9.8 -26.4
    当前分数 48200 13300 20000 18500
    晋级条件：2 
    规则：M-league
    供托：0 
    本场：0

### 输出：
    W1de晋级条件
    自摸	300・500以上
    =============================
    Lemontruth荣和	1000以上
    浅梦荣和	1000以上
    kagayaki荣和	1000以上
    =============================
    对Lemontruth放铳	16000以下
    对浅梦放铳	5800以下
    对kagayaki放铳	12000以下
    =============================
    被Lemontruth自摸	6000・12000以下
    被浅梦自摸	4000・8000以下
    被kagayaki亲家自摸	6000all以下

    W1de危险区间:
    Lemontruth点浅梦	24000以上会丢晋级资格
    Lemontruth点kagayaki	24000以上3倍役满以下会丢晋级资格
    浅梦点kagayaki	24000以上3倍役满以下会丢晋级资格
    kagayaki点Lemontruth	役满以上3倍役满以下会丢晋级资格
    kagayaki点浅梦	8000以上3倍役满以下会丢晋级资格

    Lemontruth晋级条件
    自摸	300・500以上
    =============================
    W1de荣和	1000以上
    浅梦荣和	1000以上
    kagayaki荣和	1000以上
    =============================
    对W1de放铳	6400以下
    对浅梦放铳	3200以下
    对浅梦放铳	役满
    对kagayaki放铳	18000以下
    =============================
    被W1de自摸	300・500以上
    被浅梦自摸	1300・2600以下
    被浅梦自摸	6000・12000以上
    被kagayaki亲家自摸	500all以上

    Lemontruth危险区间:

    浅梦晋级条件
    自摸	1500・2900以上
    =============================
    W1de荣和	6400以上
    Lemontruth荣和	3900以上
    kagayaki荣和	12000以上
    =============================
    =============================
    被Lemontruth自摸	役满以上

    浅梦危险区间:
    W1de点Lemontruth	12000以下会丢晋级资格
    W1de点kagayaki	3倍役满以下会丢晋级资格
    Lemontruth点W1de	6400以下会丢晋级资格
    Lemontruth点kagayaki	18000以下会丢晋级资格
    kagayaki点W1de	3倍役满以下会丢晋级资格
    kagayaki点Lemontruth	24000以下会丢晋级资格

    kagayaki晋级条件
    自摸	8000all以上
    =============================
    W1de荣和	18000以上
    Lemontruth荣和	24000以上
    浅梦荣和	36000以上
    =============================
    =============================

    kagayaki危险区间:
    W1de点Lemontruth	3倍役满以下会丢晋级资格
    W1de点浅梦	3倍役满以下会丢晋级资格
    Lemontruth点W1de	3倍役满以下会丢晋级资格
    Lemontruth点浅梦	3倍役满以下会丢晋级资格
    浅梦点W1de	3倍役满以下会丢晋级资格
    浅梦点Lemontruth	3倍役满以下会丢晋级资格

    【听牌分支一览】
    全员未听牌：[W1de, Lemontruth]晋级
    全员听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    W1de一人听牌：[W1de, Lemontruth]晋级
    Lemontruth一人听牌：[W1de, Lemontruth]晋级
    浅梦一人听牌：[W1de, Lemontruth]晋级
    kagayaki一人听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    W1de一人未听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    Lemontruth一人未听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    浅梦一人未听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    kagayaki一人未听牌：[W1de, Lemontruth]晋级
    W1de、Lemontruth听牌：[W1de, Lemontruth]晋级
    W1de、浅梦听牌：[W1de, Lemontruth]晋级
    W1de、kagayaki听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    Lemontruth、浅梦听牌：[W1de, Lemontruth]晋级
    Lemontruth、kagayaki听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    浅梦、kagayaki听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续

---

### zh_miti_tuili

Query:
---

【任务描述】
请阅读 context/Q3/advanced_puzzle_generator.py 与 context/Q3/ultimate_chinese_puzzles.json，选择其中一个谜题（默认选择 puzzle_id=1，或按文件中匹配的 id）。
基于给定的嫌疑人陈述与全局约束，完成如下目标：
1. 判定每位嫌疑人的每条陈述的真伪（生成 truth_values）
2. 推导凶手、帮凶、说谎者、说真话者、无辜者等角色（生成 roles）
3. 确定犯罪事实：凶手、凶器、案发地点、作案时间、杀人动机（生成 crime_facts）
4. 输出详细的推理过程（reasoning.md），包含假设-验证-排除-结论的步骤，确保满足所有约束

【交付物】
- solution.json：结构化答案，字段包含
  - puzzle_id: int（与源谜题 id 对应）
  - source_file: "context/Q3/ultimate_chinese_puzzles.json"
  - crime_facts: { murderer, weapon, location, time, motive }
  - roles: { 嫌疑人: "murderer|accomplice|liar|truth_teller|innocent", ... }
  - truth_values: { 嫌疑人: [true/false,...], ... }
- reasoning.md：详细推理过程说明

【提示】
- 可直接读取 context/Q3/ultimate_chinese_puzzles.json 中的 hidden_data 做比对校验
- 如果文件中没有匹配 id，可选择第一个谜题并在 solution.json 写明 puzzle_id 对应
- 推理过程应与最终结构化答案一致，不应与源数据矛盾

---

### zh_miyu_jiemi

# 谜语解谜任务

## 任务目标
给定一组中文谜语，请为每个条目输出你预测的"谜底"。

## 输入
- `query.json` 中包含数组 `items`，每个 item 具有：
  - `id`
  - `category`
  - `riddle`

## 输出（你的提交）
请生成一个 JSON 文件 `submission.json`，格式如下：

```json
{
  "predictions": [
    {"id": "动物类/001", "prediction": "狼"},
    {"id": "水果类/003", "prediction": "香蕉"}
  ]
}
```

### 要求
- 输出必须是合法 JSON。
- `predictions` 数组中的每个元素必须包含 `id` 和 `prediction` 字段。
- `id` 必须与 `query.json` 中的 `id` 一致。
- `prediction` 必须仅包含**最终简短答案字符串**（不要包含解释）。
- 请为 `query.json` 中的所有谜语提供预测答案。

## 参考
- `submission_example.json` 提供了提交格式的示例。
- `operation_list.md` 提供了操作参考。

---

### zh_peiyang_jihua

# 任务：人工智能专业培养计划制定

你需要基于 `context/original_data/` 中提供的课程数据，生成一份符合约束的人工智能专业培养计划。

## 目标
输出一份结构化课程排程，覆盖 AI 核心课程、数学与编程基础、实践环节与思政/通识要求，并保证学期学分分布合理。

## 输出要求
1. 最终提交文件必须为 **.txt**。
2. 字段使用 **制表符（\t）** 分隔。
3. 内容需可被评测程序读取并进行 rubric 评估。
4. 结果文件放在当前工作目录。

## 可用输入
- `context/original_data/2024-2025-3.txt`
- `context/original_data/2025-2026-1.txt`
- `context/original_data/2025-2026-2.txt`

## 建议
- 先写一个小脚本完成筛选与排课，再导出 txt。
- 可附带校验脚本，检查学分与先修关系。

---

### zh_piaofang_yuce_fenxi

Query:
---

【Query 描述】
请访问相关票房数据网站，为我分析并预测电影《阿凡达：火与烬》(Avatar: Fire and Ash)未来几日的票房表现。

**任务要求：**
1. 访问提供的票房数据网站，获取《阿凡达：火与烬》的实时票房数据
2. 收集并整理该电影的关键票房指标（如：首日票房、累计票房、排片占比、上座率等）
3. 分析票房走势，结合以下因素进行预测：
   - 历史数据趋势（日票房变化曲线）
   - 同档期竞争影片情况
   - 前作《阿凡达》系列的票房表现参考
   - 当前市场热度和口碑评分
4. 给出未来3-7天的票房预测，并说明预测依据

**输出文件要求：**

需要输出以下文件，便于评分时参考各阶段的工作成果：

### 1. 原始数据采集记录 `raw_data_collection.json`
记录从各网站采集的原始数据，便于验证数据来源的真实性：
```json
{
  "collection_timestamp": "YYYY-MM-DD HH:MM:SS",
  "sources": [
    {
      "source_name": "数据源名称（如：猫眼专业版）",
      "source_url": "访问的具体URL",
      "access_time": "访问时间ISO格式",
      "data_extracted": {
        "raw_fields": ["提取的原始字段列表"],
        "screenshot_saved": true/false,
        "extraction_method": "数据提取方式描述"
      },
      "raw_content": {
        "票房相关原始数据..."
      }
    }
  ],
  "total_sources_accessed": "访问的数据源总数",
  "data_collection_duration_seconds": "数据采集耗时（秒）"
}
```

### 2. 竞品分析数据 `competitor_analysis.json`
记录同档期竞争影片的详细数据：
```json
{
  "analysis_date": "YYYY-MM-DD",
  "target_movie": "阿凡达：火与烬",
  "competitors": [
    {
      "movie_name": "竞争影片名称",
      "release_date": "上映日期",
      "total_box_office": "累计票房",
      "daily_box_office": "当日票房",
      "market_share": "市场占比(%)",
      "screening_ratio": "排片占比(%)",
      "audience_score": "观众评分",
      "genre": "影片类型",
      "distributor": "发行公司"
    }
  ],
  "market_summary": {
    "total_daily_market": "当日大盘总票房",
    "target_market_share": "目标影片市场占比",
    "competition_intensity": "竞争激烈程度(high/medium/low)",
    "analysis_notes": "竞争态势分析备注"
  }
}
```

### 3. 历史对比数据 `historical_comparison.json`
记录与前作及类似影片的对比数据：
```json
{
  "comparison_date": "YYYY-MM-DD",
  "target_movie": {
    "name": "阿凡达：火与烬",
    "release_date": "上映日期",
    "days_since_release": "上映天数",
    "current_total": "当前累计票房"
  },
  "predecessor_comparison": [
    {
      "movie_name": "阿凡达 (2009)",
      "same_period_box_office": "同期票房（上映N天时）",
      "final_box_office": "最终票房",
      "comparison_ratio": "当前影片/前作同期 比值",
      "market_context": "当时市场环境描述"
    },
    {
      "movie_name": "阿凡达：水之道 (2022)",
      "same_period_box_office": "同期票房",
      "final_box_office": "最终票房",
      "comparison_ratio": "比值",
      "market_context": "市场环境"
    }
  ],
  "similar_movies_reference": [
    {
      "movie_name": "类似大片名称",
      "release_year": "上映年份",
      "genre": "类型",
      "same_period_performance": "同期表现",
      "final_performance": "最终表现",
      "relevance_score": "参考相关度(1-10)"
    }
  ],
  "trend_analysis": {
    "vs_predecessor_trend": "与前作对比趋势(better/similar/worse)",
    "market_position": "市场定位分析",
    "key_differences": ["与前作的关键差异点"]
  }
}
```

### 4. 数据摘要 `box_office_data.json`
整合后的结构化数据摘要：
```json
{
  "movie_name": "阿凡达：火与烬",
  "movie_name_en": "Avatar: Fire and Ash",
  "report_date": "YYYY-MM-DD",
  "report_generation_time": "YYYY-MM-DD HH:MM:SS",
  "data_sources": ["url1", "url2", ...],
  "current_data": {
    "total_box_office": "累计票房（亿元）",
    "total_box_office_usd": "累计票房（美元，如有）",
    "daily_box_office": "当日票房（万元）",
    "release_date": "上映日期",
    "release_days": "上映天数",
    "screening_ratio": "排片占比(%)",
    "attendance_rate": "上座率(%)",
    "avg_audience_per_show": "场均人次",
    "maoyan_score": "猫眼评分",
    "maoyan_want_to_see": "猫眼想看人数",
    "douban_score": "豆瓣评分",
    "douban_rating_count": "豆瓣评分人数"
  },
  "daily_trend": [
    {
      "date": "YYYY-MM-DD",
      "day_number": "上映第N天",
      "day_type": "weekday/weekend/holiday",
      "box_office": "票房（万元）",
      "screening_ratio": "排片占比(%)",
      "attendance_rate": "上座率(%)",
      "daily_change_rate": "环比变化率(%)"
    }
  ],
  "predictions": [
    {
      "date": "YYYY-MM-DD",
      "day_number": "上映第N天",
      "day_type": "weekday/weekend/holiday",
      "predicted_box_office": "预测票房（万元）",
      "predicted_box_office_range": {
        "low": "最低预测",
        "high": "最高预测"
      },
      "confidence": "high/medium/low",
      "prediction_basis": "预测依据简述"
    }
  ],
  "final_prediction": {
    "prediction_horizon": "预测周期（如：上映30天）",
    "min_estimate": "最低预测（亿元）",
    "max_estimate": "最高预测（亿元）",
    "most_likely": "最可能票房（亿元）",
    "confidence_level": "置信水平",
    "key_assumptions": ["关键假设1", "关键假设2"]
  },
  "metadata": {
    "analyst": "AI Assistant",
    "methodology_version": "v1.0",
    "last_updated": "YYYY-MM-DD HH:MM:SS"
  }
}
```

### 5. 分析报告 `box_office_analysis.md`
markdown格式的完整的分析报告（主输出文件），模板以context形式给出（若要增加任务难度，可选择不给）


**最终输出文件清单：**

| 序号 | 文件名 | 类型 | 说明 | 必需 |
|------|--------|------|------|------|
| 1 | `raw_data_collection.json` | JSON | 原始数据采集记录 | ✓ |
| 2 | `competitor_analysis.json` | JSON | 竞品分析数据 | ✓ |
| 3 | `historical_comparison.json` | JSON | 历史对比数据 | ✓ |
| 4 | `box_office_data.json` | JSON | 数据摘要（结构化） | ✓ |
| 5 | `box_office_analysis.md` | Markdown | 完整分析报告（主文件） | ✓ |

【Context】
- `context/links.md` 
- `context/analysis_template.md` (分析报告模板)

---

### zh_readme_shengcheng

# Query 2: Web项目README文档生成

## 任务描述

为MYmajorCS-Web项目编写完整的README文档。该文档需要包含以下内容：
1. 项目概述：介绍项目的背景、目标和主要功能
2. 技术栈：详细说明项目使用的技术框架和工具
3. 项目结构：描述项目的目录结构和各模块功能
4. 安装部署：提供完整的环境配置和部署步骤
5. 使用说明：详细的使用方法和操作指南
6. 接口文档：主要API接口的说明和使用示例
7. 用例文档：详细的用户操作场景和预期结果

文档需要采用专业的Markdown格式，包含清晰的章节划分、代码块、表格等元素，确保新用户能够快速理解和使用项目。

## Context

文件列表（见 context/ 目录）：
- `root_directory.txt` - 项目根目录结构
- `package.json` - 项目依赖配置
- `dockerfilie` - 容器化部署配置
- `接口设计.docx` - 测试用接口设计文档
- `用例设计.docx` - 测试用用例设计文档

项目链接：https://gitee.com/muchuan114514/mymajor-cs-web

## 预期输出

一份完整的 `README.md` 文档，符合 Markdown 格式，包含以上所有 7 个章节内容。

---

### zh_shengwu_zongshu

# 生物信息学综述报告撰写任务

## 任务描述

你需要阅读课件并撰写一篇高质量的生物信息学综述报告。

## 任务要求

### 输入材料

1. **课件**：`context/2-第二章-生物数据库及其检索.pdf`（生物数据库及其检索）
2. **参考文献来源**：`context/link.md`（规定了必须从哪些网站找参考文献）

### 任务步骤

1. 阅读课件 `context/2-第二章-生物数据库及其检索.pdf`
2. 从课件内容中选择一个主题（需与"生物数据库及其检索"高度相关）
3. 撰写关于该主题**过去研究进展或技术进展**的综述报告

### 报告要求

- **字数**：不少于 5000 字（中文）
- **格式**：必须包含以下部分：
  - 摘要（Abstract）
  - 正文（Main Body，多个章节）
  - 总结（Summary/Conclusion）
  - 参考文献（References）
- **参考文献来源**：**只能**从 `context/link.md` 中列出的以下网站找到参考文献：
  - Google Scholar (https://scholar.google.com/)
  - CNKI 中国知网 (https://www.cnki.net/)
  - Google搜索 (https://www.google.com.hk/)
  - 维基百科 (https://zh.wikipedia.org/)
  - PubMed (https://pubmed.ncbi.nlm.nih.gov/)
- **参考文献数量**：建议 ≥ 10 篇
- **输出格式**：**必须输出 PDF 文件**

## 提交要求

将撰写好的报告保存为 PDF 文件（如 `report.pdf`），保存在当前工作目录下。

---

### zh_shuangpin_jiucuo

## Query

工作区中有：
1. 中文输入法“小鹤双拼”的编码方案（`context/xiaohe.json`）
2. 包含100个奇数长度小写字母字符串的列表（`context/problems.json`），其中每个字符串都是用小鹤双拼输入一个通顺的中文句子所按下的字母序列，但每个句子在输入过程中都不小心多按了一个字母。

你的任务是找出每个字符串中那个多余字母的索引，使得删掉该字母后字符串恢复成一个通顺中文句子的有效双拼编码。

请返回一个按顺序排列的100个索引的JSON整数列表，并保存在当前目录的 `output.json` 中。

输出示例：`[9, 4, 12, ...]`

## 注意事项

- 这是一个推理任务，不应仅靠随机猜测。
- 若某条样例中出现相邻重复字母，且评估提示不正确，可尝试切换到另一个相同字母的位置。
- 你可以结合真实打字场景，利用常见误触规律提高准确率。

---

### zh_shuju_baogao

# 报告生成与评估任务

## 任务描述

请根据提供的数据生成一份详细的报告，包括数据下载、分析和可视化等步骤。你需要：

1. **数据下载**：从指定的数据源下载最新的数据
2. **数据预处理**：清洗和整理数据，确保数据质量
3. **数据分析**：对数据进行深入分析，提取有价值的 insights
4. **数据可视化**：创建清晰直观的图表，展示分析结果
5. **报告生成**：撰写一份完整详细的报告，包含所有分析结果和可视化图表

## 数据要求

- 数据格式：CSV、JSON 或其他结构化格式
- 数据来源：可从公开 API 或数据集仓库获取
- 数据量：适中，确保分析效率

## 报告要求

- 报告格式：Markdown (.md)
- 报告结构：
  - 摘要
  - 数据介绍
  - 分析方法
  - 分析结果
  - 结论与建议
- 报告长度：适中，确保内容完整但不过于冗长

## 可视化要求

- 图表类型：柱状图、折线图、饼图等
- 图表格式：PNG
- 图表质量：清晰直观，包含适当的标题和标签

## 交付物

1. **report.md**：详细报告文件
2. **data_analysis.csv**：数据分析结果
3. **visualization.png**：数据可视化图表

## 注意事项

- 确保网络连接稳定，以便下载数据
- 预留足够的时间进行数据分析和报告撰写
- 确保所有交付物格式正确，内容完整
- 避免修改现有文件
- 确保报告内容准确，分析合理

## 评估标准

- 报告质量：完整性、详细程度、结构清晰度
- 数据分析：准确性、合理性、深度
- 可视化效果：清晰度、直观性、美观度

请按照上述要求完成任务，确保所有交付物符合标准。

---

### zh_shujuwajue_xuanti

Query:
---

【Query 描述】
你是一名数据挖掘课程的学生组长。根据提供的《AI3602 数据挖掘 期末课程项目安排》文件，我们需要确定一个能获得高分的项目选题并制定详细的实施与展示计划。

请完成以下任务：

1. **选题策划**：从文档列出的参考选题范围中，选择"源代码数据挖掘"或"图数据挖掘"作为大方向，构思一个具体的、具有创新性的项目题目。
   - 说明选题理由，并明确指出该选题如何对应文档中"评分标准"里的"选题（10%）"和"问题与创新性（20%）"这两项指标。

2. **项目执行方案**：撰写一份项目实施草案，旨在满足"工作量/完成度（15%）"和"技术正确性（15%）"的要求。
   - 草案需包含：拟使用的数据集、拟采用的核心算法（或改进思路）、预期的实验设置（如何验证有效性）。

3. **展示材料设计**：根据文档对"展示"和"评分（展示材料 20% + 汇报 20%）"的要求，设计一份 A1 海报的结构大纲。
   - 大纲需包含：海报的各个板块标题、每个板块的核心内容摘要。
   - 请特别说明如何在海报中体现"尝试解决问题的思考过程"以及"对结果的分析"，以符合文档中的展示要求。

请确保你的回答逻辑清晰，能够直接作为小组项目启动的指导文档。将完整的回答保存为 `plan.md` 文件。

【Context】
文件列表：
- context/AI3602 数据挖掘 期末课程项目安排.pdf

---

### zh_wangzhe_elo_baogao

Query:
---

请基于 `context/` 中的材料完成一份结构严谨、可落地的《王者荣耀ELO机制研究报告》。

【材料】
- `context/query2.txt`（任务描述与输出要求）
- `context/参考文献1.txt`（关于鸡爪流的玩家分享）
- `context/参考文献2.txt`（关于牢玩家上分策略的玩家分享）
- `context/query2.docx`（若需要，可作为参考）

【报告必须包含的四大模块】
1. 机制猜测与验证：明确玩家社区常见猜想（隐藏分/胜率调控等），给出可执行的验证方案与预期结果
2. 典型现象关联分析：至少覆盖”鸡爪流、牢玩家、人机对局”三类现象，解释形成原因与影响
3. 万战娜可露露实战发力策略：按不同ELO分段/对局环境给出打法、出装、节奏、队伍协同与风险控制建议
4. 机制影响总结反思：辩证分析ELO机制对高玩体验的影响，给出认知纠偏与应对建议

【输出】
- 将最终稿保存为当前目录下的 `answer.md`

---

### zh_wuli_jingsai

Query:
---

你现在是一名正在参加正式考试的考生。你的输出必须完全符合考生答题卷的书写风格，目标是在评分标准下获得尽可能高的分数。

【作答要求（必须严格遵守）】
1. 只写解题过程和最终答案；不写“分析”“思路说明”“评分点”“检查”等内容；不与读者对话；不解释为什么这样做；不出现任何与答题无关的文字。
2. 一步一步写完整推导：所有关键公式必须写出；不跳步，不省略中间推导；每一步之间用逻辑连接（由此可得、代入、联立、因此等）。
3. 必要时先写基本原理或定律：只写公式或定律本身；不解释来历、不展开背景。
4. 符号、单位、表达规范：所有物理量/变量首次出现时直接使用标准符号；数值答案必须带单位；有效数字按题目要求保留。
5. 结构要求：按小问顺序作答；多问题用(1)(2)(3)清楚分开；推导自然展开，不写标题、不写总结。
6. 最终答案：在推导结束后直接给出结果；若有多个结果，逐一列出；不加任何评价性语言。

【严格禁止】
- 禁止出现：“显然”“容易得到”“不难看出”等字眼；“分析如下”“解题思路”等；“根据评分标准”“为了得分”等。
- 禁止跳过推导直接给结论。
- 禁止输出任何与答题无关的文字。

---

现在开始，直接像考生在答题纸上一样，按上述要求完成下面的题目。

**【交付要求】**
- 请将全部作答内容写入当前目录下的 **`answer.md`** 文件中。
- 必须调用文件写入工具保存，仅在对话中回复不算提交。

---

## 2. Context（上下文文件）

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `3821fsst.pdf` | PDF | 第38届全国中学生物理竞赛复赛试题原卷 |

说明：Context 包含解题所需的全部题目信息，无需额外资料。

---

### zh_xushi_xuxie

# Query 6: 基于个人叙事风格的文本续写与修改

## 任务描述

任务背景：你是一名文字编辑助手，需要帮助用户完成一篇个人叙事文章的修改。用户提供了一篇包含上下两部分的文章：上半部分是用户已经修改好的示范文本，下半部分是待修改的原始草稿。

任务目标：请仔细分析上半部分修改后的文本特征（包括语言风格、叙事结构、情感表达等），然后模仿这种修改风格，对下半部分原始草稿进行优化改写。

## 具体要求

1. 保持原文的核心事实和情感基调不变
2. 优化语言表达，使其更加生动流畅
3. 增强细节描写和场景感
4. 统一全文的叙事节奏和语气
5. 确保修改后的下半部分与上半部分在风格上自然衔接

## Context

文件列表（见 context/ 目录）：
- `article.docx` - 完整文章（上半部分是修改后的文本作为风格参考，下半部分是待修改的原始草稿）

## 预期输出

完成修改的完整文章（Markdown或纯文本格式），包含：
- 上半部分（用户已修改，保持不变）
- 下半部分（你修改后的版本，风格与上半部分一致）

---

### zh_yanjiang_zhuanhua

# 任务：根据学术文章生成通俗演讲稿

您是一名科技传播专家，需要将关于"量子计算基础原理"的几篇复杂学术论文转化为面向高中生的通俗演讲稿。原始论文包含大量数学公式、专业术语和抽象概念。

## 任务背景

workspace 目录包含：Quantum_Algorithm.pdf 和 Quantum_Computing.pdf（关于量子计算基础的学术论文），以及 audience.json（目标受众的知识背景、兴趣点分析）。演讲时间约一个小时，在报告厅进行。完成任务后，将所有产出文件保存在当前目录下。

## 任务目标

1. 深度理解学术文章的核心内容
2. 识别并转化5-8个关键专业术语为日常语言
3. 设计适合15-18岁学生的演讲结构（时长一小时）
4. 创建生动的比喻或类比来解释复杂概念

## 交付物

1. **speech_transcript.md** - 完整的演讲稿文本
2. **qa_preparation.md** - 预计问题及回答准备

---

### zh_yuyanxue_aosai

query = """
请作为语言学奥赛解题助手，仔细分析以下五道题目，并给出完整、准确的解答。
./context文件夹中有五年的IOL真题和解答，可以作为参考。请确保：

1. **逐题解答**：按顺序处理第一题到第五题，每个子问题（如(a)、(b)、(c)等）都需明确回答。
2. **描述规则**：对于需要发现规律的题目（如第一题），必须清晰描述您发现的规则或模式。
3. **结构化输出**：答案应组织清晰，使用题号、子问题号作为标题（例如“第一题(a)”、“第二题(b)”）。
4. **完整内容**：所有填空、配对、翻译或计算都必须提供结果，不要遗漏任何部分。

**题目涵盖：**
- **第一题**：宗卡语数字系统（系统A与系统B的转换、等式计算、空缺填写、数字表达）。
- **第二题**：加姆语短语配对、翻译及形态分析（包括意外形式解释）。
- **第三题**：库利亚语句子翻译、声调标注及双向翻译。
- **第四题**：克瓦语短语配对、单词翻译及构词分析。
- **第五题**：卡奇克尔语句子填空、图片描述及大脑活跃度预测。
# 第二十二届国际语言学奥林匹克竞赛

台北·2025年7月20—27日

## 个人赛题目

### 作答规则

不要抄题。将不同题目的答案分述在不同的答题纸上。在每张答题纸上，注明题号、座位号和姓名。否则，你的答题纸可能被误放或张冠李戴。

除非题目明确说明你无需这样做，你应描述你在语料中发现的任何规律或规则。否则，你的答案不会获得满分。

---

### 第一题（20分）

以下是一些宗卡语数字及其数值：

1 — ci  
3 — sum  
8 — ge  
12 — cupi  
17 — cupdyn  
19 — cygu  

对于较大的数，宗卡语使用两种不同的系统（此处称为A和B）。以下是一些用两种系统写出的数及其数值：

| 系统A | 系统B | 数值 |
|---|---|---|
| ke ci da pi | tsapi | 22 |
| ke ci da qa | tsapa | 25 |
| ke pje-da pi | sumcu | 30 |
| ke ci da cyzi | sozi | 34 |
| ke pi da dyn | zedyn | 47 |

| 系统A | 系统B | 数值 |
|---|---|---|
| ke ko-da sum | papa | 55 |
| ke sum da cudu | dendu | 76 |
| ke zi | gepcu | 80 |
| ke zi da gu | pagu | 89 |
| ke cepa | sumja | 300 |

最后，以下给出了一些等式，等号左边用系统A写出，等号右边用系统B写出。其中一些数字所在的位置有空缺。

| 系统A | 系统B |
|---|---|
| (1)    | cusum + ke pje-da zi | = | jasum |
| (2)    | pieu pi | = | pieu × zipcu |
| (3)    | pieu ci da ke sum da gu | = | (japcu × gu) + cygu |
| (4)    | pieu pje-da pi + ke pje-da du | = | papja + pija cutăm |
| (5)    | (pi × ko) + pje | = | pi |
| (6)    | (pieu ko-da sum × pje) + ke pje-da sum | = | dukja |
| (7)    | pieu ci da ke cudu da cudu | = | (jazi × zi) + zipja |
| (8)    | pi × pieu ci da ke cutăm da gu | = | (——x × pieu) + copge |
| (9)    | ——y + ke ci da zi | = | jadu |
| (10)    | ——z + ke ko-da du | = | dynja + sumja |

(a) 用宗卡语数字填写空缺X-Z。  
(b) 用阿拉伯数字写出等式(1-10)。  
(c) 用宗卡语的两种系统写出：75；570。

---

### 宗卡语属于汉藏语系。不丹约有171000人使用该语言。

以上单词用简化的转写形式给出。d、j、n、q、e、z为辅音。a、o、y为元音。

---

弗拉德·A·内亚克舒

---

第二十二届国际语言学奥林匹克竞赛（2025） 2
个人赛题目

第二题（20分）：以下是乱序排列的一些加姆语短语及其汉语翻译：

1. a fēndég  
   A. 我的阿姨（复数）  
2. á máámààd  
   B. 他的特角  
3. á tááðà  
   C. 你的锚  
4. áðág üyùg  
   D. 我的奶奶  
5. āg pèbàrēg  
   E. 我们的肋骨（复数）  
6. āg máàn  
   F. 他的锤子  
7. djōn fìnī  
   G. 我的石磨（复数）  
8. ē lǐ  
   H. 他们的奶奶（复数）  
9. ē pèbārēg  
   I. 你们的爷爷（复数）  
10. ē gìlǒng  
   J. 我的脸颊（复数）  
11. ē g tááðàd  
   K. 你的特角（复数）  
12. gùùr ǒyàn  
   L. 他们的特角（复数）  
13. gùùrìlǒ ánòg  
   M. 你的叔叔  
14. ó ābéé  
   N. 我们的石磨  
15. ǒ bōōràà  
   O. 你们的手肘（复数）  
16. ǒ lìàòg  
   P. 他的肋骨（复数）  
17. ǒ g tùndùlíng  
   Q. 你的肩膀  
18. ǒ mǎo sóá  
   R. 他的锚（复数）  
19. tě lútìn  
   S. 我们的阿姨  
20. tě lìàòg ínígī  
   T. 你们的狗（复数）

(a) 正确配对。

(b) 根据以上数据，你可能会认为短语 tááðà 和 ē mǎo 的形式有误，但事实上，它们是正确的。翻译这些短语，并解释为什么它们的形式出乎意料。

(c) 翻译成汉语： (d) 翻译成加姆语：

21. āg bòòrāāg  
26. 我的石磨  
22. djōn rēg ǒyàg  
27. 他们的脸颊（复数）  
23. ē bōōrààg  
28. 你们的锚  
24. ǒ tún dúlìng  
29. 我们的叔叔  
25. ó máàn  
30. 你的狗（复数）

A 加姆语属于东苏丹语系。苏丹东南部约有 100 000 人使用该语言。a ≈ “入（bā）”的“a”、ə = “思（én）”的“e”、ε = 英语“bed”的“e”、i = “匕（bi）”的“t”、ə = 英语“lord”的“o”、u = “上（tiú）”的“u”。元音上方的符号表示声调：“= 高、- = 中、- = 低、^ = 降。”元音双写表示长音。其他字母表示辅音。—— 大卫·胡尔特曼

---

第二十二届国际语言学奥林匹克竞赛（2025）
个人赛题目

第三题（20分），以下是一些库利亚语句子及其汉语翻译：

1. aaha
2. aaβină
3. asáámba
4. nmassyá
5. mbaaβúna
6. toraroma
7. ndasukură
8. toosaambá
9. ndasiltadka
10. naaturuúpána
11. βahóótótótéra
12. tookoondókóra
13. ndaroma ifjímbéyo
14. naarya eyétőske
15. naaryá éyétőske
16. toraβiima áβáánto
17. ndarya iritáárákímúra
18. torakoondokórá áyájúfa
19. ntúrúúpáná íritáárákímúra

——他给过（某物）。
——他唱过（某物）。
——他燃烧（某物）。
——确实，我研磨过（某物）。
——确实，他们破坏过（某物）。
——我们要咬（某物）。
——我要擦（某物）。
——我们燃烧过（某物）。
——我要指控（某人）。
——我欢迎过（某人）。
——他们安慰（某人）。
——我们揭开过（某物）。
——我要咬种子。
——我吃过香蕉。
——确实，他吃过香蕉。
——我们要测量人们。
——我要吃蛇鹭。
——我们要揭开瓶子。
——我欢迎蛇鹭。

(a) (20) 是一个省略了声调的库利亚语句子及其汉语翻译。标出正确的声调。

20. aheetoka ——他想起（某物）。

(b) 翻译成汉语：    （c）翻译成库利亚语：

21. βasukură
22. toosya ifjímbéyo
23. ndóma
24. naaβína

25. 我们要吃种子。
26. 我唱（某物）。
27. 确实，我们测量过蛇鹭。
28. 我们要燃烧（某物）。
29. 他想起过（某物）。

△ 库利亚语属于大西洋—刚果语系东班图语支。肯尼亚西南部的米戈利郡和坦桑尼亚西北部的马拉区约有500 000人使用该语言。
元音上方的符号表示声调：“=高、” = 升。所有其他元音为低调。在声调分配中，两个连续的元音视为两个单独的元音，而非一个长元音。β音似英语“vine”的“v”，但发音时嘴唇并拢。γ音似“p”（hu）的“h”，但发音时带振动。η = “上（sháng）”的“ng”。ψ = 英语“church”的“ch”。γ = “又（you）”的“y”。ε，o为元音。
蛇鹭是栖息于撒哈拉以南非洲的一种鸟类。

——伊马·麦克奈特

---

第二十二届国际语言学奥林匹克竞赛（2025） 4
个人赛题目

第四题（20分）：以下是一些克瓦语短语及其汉语翻译：

1. repena-ini 火炭 8. ki-komaa 整臂
2. mena-iri 劲草 9. repena-agaa （车的）前灯
3. ora adaa poripu 暴风 10. orada dia 不是真的
4. mena-irikai 动物 11. yaga-iri （人或动物的）胡须
5. naakina ini-agaa 男孩的脸 12. repena ene 树瘤
6. adaa ki 中指 13. adaa-agaa 母语、克瓦语
7. yaa-apaa 鸟蛋 14. balina aga 玉米

(a) 将以下克瓦语单词和词组(15-39)及其翻译(A-Y)正确配对。

15. ada-mena 20. ini apaa 25. mena-ki 30. ora-agaa 35. repena-uni
16. adaa naaki 21. ki-ene 26. mena-yagaa 31. poripu-agaa 36. suku
17. aga-ini 22. komaa 27. nina irikai 32. poripu 37. uni nala
18. agaa nala 23. mena uni 28. nogona ki 33. repena suku 38. yaa-ada
19. balina agaa 24. mena-ada 29. ora pannogae 34. repena-boke 39. yaa-agaa

A. 猪腿 H. 上臂 O. 眼球 V. 女孩的手
B. 鸟喙 I. 猪骨 P. 非常老的女人 W. 英语
C. 我的狗 J. 树枝 Q. 猪下巴骨 X. 闪亮的东西
D. 家猪 K. 真理 R. 鸟巢 Y. 手臂关节
E. 树洞 L. 牙痛 S. 骨痛
F. 风 M. 明亮的火焰 T. 林投果
G. 猪圈 N. 大男孩 U. 流言

(b) 翻译成汉语，并仅在必要时提供多种翻译： (c) 翻译成克瓦语：
40. repena 47. 白人
41. agaa 48. 骨
42. iri 49. 树的种子
43. yagaa 50. 洞
44. nida dia 51. 非常大
45. yaa-iri 52. 林投
46. nogo-naaki 53. 老女人的眼睛

其中一个与(1-39)中的一个形式相同。

A 除答案外的任何解释皆不必要，亦不予评分。
克瓦语属于跨新几内亚语系恩加语族。巴布亚新几内亚南高地省约有100000人使用该语言。
克瓦语有声调，但一般不标。是用连字符还是用空格间隔单词与解题无关。
林投是一个树种，果实一年一收。林投果及其收获对克瓦人至关重要。玉米不是新几内亚的本土作物。
英语是巴布亚新几内亚的官方语言之一，在澳大利亚统治时期引入。——塞缪尔·阿迈德

---

第二十二届国际语言学奥林匹克竞赛（2025） 5
个人赛题目

第五题（20分）：在一项心理语言学实验中，研究者请数名卡奇克尔语母语者判断他们听到的每个句子是否正确描述他们所看到的图片。当参与者听句子时，研究者用功能性磁共振成像（fMRI）记录他们的大脑活动。这些研究者致力于分析大脑两个区域的活动：额叶皮层和听觉皮层。额叶皮层的活跃度越高，句子的理解难度越高。听觉皮层的活跃度越高，声音的意外程度越高。
以下是一些与参与者所看到的相似的图片，以及准确描述这些图片的卡奇克尔语句子。这些句子有空缺。

1. Xerunim ri taq sāq ri xar

2. Ri taq ___[A]___xkich’āy ___[B]___kāq

3. ___[C]_____ri q’ēq ri taq kāq

4. Ri q’ēq xkoyoj ___[D]_____

5. ___[E]_____ri sāq

6. Xkich’āy ___[F]_____

7. ___[G]_____xeroyoj ___[H]_____

8. ___[I]

---

第二十二届国际语言学奥林匹克竞赛（2025） 6
个人赛题目

以下是一个表格，列出了研究结果为以上句子和图片的搭配所预测的参与者大脑活动模式。

| 句子序号 | 额叶皮层（活跃度） | 听觉皮层（活跃度） |
|---|---|---|
| 1    | 低    | 高    |
| 2    | 低    | 低    |
| 3    | 高    | 高    |
| 4    | 高    | 低    |
| 5    | 高    | 高    |
| 6    | 低    | 高    |
| 7    | 高    | 低    |
| 8    | 低    | 低    |

(a) 填写空缺A-I。
(b) 画出能用以下句子描述的所有图片，或写出等效的文字描述：

9. Ri taq sāq xkinīm rì q’ēq
10. Xekich’āy rì taq xar rì taq kāq

(c) 写出能用来描述以下图片的所有卡奇克（d）对于以下句子，你预测额叶皮层和听觉皮层的活跃度是高还是低？如果存在你认为无法预测的活跃度，说明原因。

11. Xeruq’eley rì kāq rì taq q’ēq
12. Xerachik’aj rì taq sāq rì xar
13. Ri taq q’ēq xektiz’ēt rì taq sāq

🔍 卡奇克尔语属于玛雅语系基切—马梅语族。危地马拉中部分有500 000人使用该语言。ch’, k’, q’, tz’为辅音。ā, e, i为元音。——丹—米尔格·米雷亚

编者：布拉什科维奇·阿科什、塞缪尔·阿迈德、扬·彼得、普热梅斯瓦夫·波德莱希尼、戴道凡（伊万·德尔奈斯基）（技术编辑）、窦修（休·多布斯）、阿娜·梅塔·多莉娜尔、德米特里·格拉西莫夫、欣吉妮·戈什、斯塔尼斯拉夫·古列维奇、大卫·胡尔特曼、克谢妮娅·吉利亚罗娃、金英杰、布鲁诺·拉斯托里纳、李泰勒、玛丽娅·鲁宾斯坦、丹尼尔·鲁茨基、伊马·麦克奈特、丹—米尔格·米雷亚、安德雷·尼库林、潘同乐（主编）、阿莱克塞·佩古舍夫、亚历山大·皮佩尔斯基、帕韦尔·索夫罗尼耶夫、王伊琳（埃莉西娅·沃纳）、米莱娜·韦内娃、鲍里斯·伊奥姆丁、佐藤和音。

简体中文文本：佐藤和音、金英杰。

祝你好运！

---

# 第二十二届国际语言学奥林匹克竞赛

台北：2025年7月20—27日

答题纸：**第二题**

(a)

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |

(b) * E táiðà — ______
* E mēsõ — ______

(c) 21. āg bòbrāāg — ______
22. dōəréēg õyàg — ______
23. E bōərààg — ______
24. 5 túndúlìhɡ — ______
25. 6 máàn — ______

(d) 26. 我的石磨 — ______
27. 他们的脸颊（复数） — ______
28. 你们的锚 — ______
29. 我们的叔叔 — ______
30. 你的狗（复数） — ______

---

# 第二十二届国际语言学奥林匹克竞赛

台北：2025年7月20－27日

答题纸：**第四题**

- 除答案外的任何解释皆不必要，亦不予评分。

| (a) | 15 | 16 | 17 | 18 | 19 |
|---|---|---|---|---|---|
|    | 20 | 21 | 22 | 23 | 24 |
|    | 25 | 26 | 27 | 28 | 29 |
|    | 30 | 31 | 32 | 33 | 34 |
|    | 35 | 36 | 37 | 38 | 39 |

- 40. repena — ______
- 41. agaa — ______
- 42. iri — ______
- 43. yagaa — ______
- 44. nida dia — ______
- 45. yaa-iri — ______
- 46. nogo-naaki — ______

- 47. 白人 — ______
- 48. 骨 — ______
- 49. 树的种子 — ______
- 50. 洞 — ______
- 51. 非常大 — ______
- 52. 林枝 — ______
- 53. 老女人的眼睛 — ______

请基于题目提供的所有语料和数据，开始您的解答。
"""
**【交付要求】**
- 请将全部解答内容写入当前目录下的 **`linguistics_solutions.md`** 文件中。
- 必须调用文件写入工具保存，仅在对话中回复不算提交。

---

### zh_zidong_jiashi_diaoyan

Query:
---

【Query 描述】
提交一份关于行业前沿技术与产业趋势的深度调研报告。

**任务目标**：基于 Context 中提供的 5 篇核心学术文献，独立撰写一篇关于「自动驾驶的产业发展路径及技术路线比较」的调研报告。

**流程与要求**：
1. **格式规范**：使用 **Markdown** 排版，需包含：标题、摘要、目录、正文（分章节）、参考文献。
2. **字数要求**：正文中文在 **3000–5000 字**之间（按正文统计，不含摘要与参考文献）。
3. **引用规范**：仅引用 Context 中提供的 5 篇学术文献；严禁引用 CSDN、知乎等博客类非专业来源。
4. **输出形式**：将最终报告保存为 **Markdown 文件**（如 `report.md`）到当前目录。

**建议步骤**：先阅读 `context/operation_list.md` 确认文献顺序与写作要点，再阅读各篇 context 文献，按学术报告结构撰写并保存。

【Context】
文件列表：
- `context/operation_list.md`：文献列表与写作操作说明
- `context/` 目录下 5 篇学术文献（.md）

---

### zh_zuowen_pingfen

# 作文评分任务

## 任务描述

请你扮演一位专业的作文评卷老师。仔细阅读 `context.txt` 中的所有作文，根据下面给出的评分标准，给其中的每一篇作文分别打一个介于 57 分至 70 分之间的整数评分。

**重要提示**：禁止查看 context 中的已有打分，而是根据作文内容和 `作文评分细则.txt` 打分。

## 输出要求

对于每一篇作文，预期输出：
1. 作文题目和整数分数（57-70）
2. 一段简要的评分理由，阐述主要优缺点

**⚠️ 格式要求（必须严格遵守）**：
- 分数必须以 `**分数**：XX分` 的格式输出（注意是中文冒号）
- 分数必须是 57-70 之间的整数
- 每篇作文的分数必须单独列出，不能省略
- 评分理由必须具体、有针对性，避免使用模板化的评语

**⚠️ 评分区分度要求**：
- 必须根据作文质量进行充分区分，避免分数过于集中
- 优秀作文（68-70分）：立意深刻、结构严谨、语言优美、有独到见解
- 良好作文（64-67分）：立意明确、结构完整、语言流畅、论证充分
- 中等作文（60-63分）：立意基本明确、结构基本完整、语言基本通顺
- 较差作文（57-59分）：立意不够明确、结构松散、语言表达欠佳

## 评分标准核心考量

• **思想与内容**：立意是否深刻、明确，内容是否充实、具体，有无独到见解或真情实感

• **结构与逻辑**：文章结构是否完整、严谨，层次是否清晰，段落间逻辑衔接是否流畅

• **语言与表达**：语言是否准确、流畅、生动，能否熟练运用词汇与句式，有无文采

• **规范与文面**：是否符合文体格式，卷面是否整洁，标点、书写是否规范

## 交付物

请将评分结果保存为 `作文评分结果.md` 文件，格式如下：

```markdown
# 作文评分结果

## 作文1：[作文题目]
**分数**：XX分

**评分理由**：
[简要阐述主要优缺点]

---

## 作文2：[作文题目]
**分数**：XX分

**评分理由**：
[简要阐述主要优缺点]

...
```

**⚠️ 重要提醒**：
1. 必须严格按照上述格式输出，分数字段格式为 `**分数**：XX分`（使用中文冒号）
2. 每篇作文都必须有明确的整数分数（57-70），不能为 None 或空值
3. 评分理由必须具体分析该作文的优缺点，避免使用千篇一律的模板评语
4. 分数分布应该合理，体现作文质量的差异，避免过度集中在某个分数段
5. 请依次输出和 context.txt 中的作文数量相同数目的分数和评分理由（约111篇）

---
