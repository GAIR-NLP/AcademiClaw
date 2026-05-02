[Black Hole Visualization Operation Sequence]

This operation sequence guides the Agent to first generate the Three.js black hole visualization page (query1.html), then perform evaluation. Please strictly follow these steps:

1. **Start Task and Prepare Environment**
   - Enter the current working directory.
   - Confirm `workspace/query.md` exists, read the task description and requirements.
   - Confirm `context/query1_Reference_Image.jpg` exists (used for generating answers and subsequent evaluation).

2. **Generate Three.js Visualization Page**
   - Parse `query.md`, understand all visual, interaction, and code requirements.
   - **[REQUIRED]** Implement according to the **[Key Implementation Tips]** in `query.md` to avoid a completely black screen: full-screen quad must use `scene.add(mesh)` with `mesh.frustumCulled = false`; in animate() update iTime, iResolution, iCameraPos, iCameraDir (getWorldDirection), iCameraUp, iFov every frame before rendering; the fragment's final color must include accretion disk/starfield or glow, and must not always be black.
   - Use Three.js (CDN) and OrbitControls (CDN) to implement the black hole visualization:
     - Recreate a movie-style black hole with accretion disk, gravitational lensing, and dynamic starfield.
     - Implement backward ray tracing algorithm, accretion disk Doppler effect, starfield breathing effect, etc.
     - UI card, animation toggle (`<input type="checkbox" id="anim-toggle">` must exist and be clickable), interaction hints, etc. must all be implemented as required.
   - Add comments at key parameter adjustment positions for easy modification.
   - Output a single HTML file named `query1.html`, saved in the workspace/ directory.

3. **Generate Screenshot**
   - Use Playwright or browser automation tool to open `query1.html`.
   - Wait for page rendering to complete, capture the main view, save as PNG (e.g., `screenshot.png`).
   - Save the screenshot file in the workspace/ or output directory.

4. **Generate Operation Sequence Record**
   - Record each key operation in the following JSON format:
     - Parse query.md
     - Design Three.js scene
     - Write HTML/JS code
     - Render and debug
     - Generate final files
   - Each step includes: step, action, timestamp, status, description, error (if any), etc.
   - Output as `operation_sequence.json`, saved in the workspace/ directory.

5. **Deliverable Check and Evaluation Preparation**
   - Confirm workspace/ contains:
     - `query1.html` (main deliverable)
     - `operation_sequence.json` (operation record)
     - (Optional) screenshot file
   - Check file completeness and format.

6. **Enter Evaluation Process**
   - Call the evaluation script (eval_task.py) to automatically evaluate deliverables.
   - Evaluation includes: file existence, page rendering, interaction, visual effects, etc.
   - Evaluation results are written to the gpt-5/ directory.

7. **Multiple Attempts (if not passed)**
   - If evaluation does not pass, fix deliverables based on feedback, repeat steps 2-6, up to 3 attempts.

[Notes]
- All deliverables must be saved in the workspace/ directory.
- Key parameters, algorithms, UI interaction, etc. must strictly follow query.md requirements.
- **Prevent black screen**: Be sure to implement according to the [Anti-Black-Screen Checklist] and [Correct Implementation Guide] (including recommended implementation structure) in query.md, otherwise screenshots will be completely black and evaluation will fail.
- Operation sequences must be detailed and traceable.
- After evaluation passes, the process automatically terminates.
