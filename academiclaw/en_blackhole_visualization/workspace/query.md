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
