# Changelog

## v4

- Added an appearance-tuning note explaining the isolated sample's scope, scene-overlay alignment, layered shadows, edge contrast and size-dependent tuning; the running sample is unchanged.
- Audited all seven pages: fixed the crop aspect ratio, computed exact rounded-boundary ray endpoints, and replaced the fake before/after crop with a formula-derived UV sampling grid.
- Separated per-card texture inputs from copied 2D outputs, and redrew visibility as a reversible lifecycle with an independent dirty flag and explicit disposal trigger.
- Documented the 40 px observation margin, reduced-motion behavior, and one-context-per-engine-instance scope.
- Replaced the illustrative material cards on page 5 with the verified phone-browser capture of the production v5 shader; kept the full source capture and reproducible PDF crops.
- Corrected the material comparison: the two presets share an optical algorithm but also differ in refraction strength, highlight strength, tint and edge parameters.
- Rebuilt the guide diagrams as explicit, numbered input-to-output flows that remain legible on a phone.
- Replaced decorative geometry sketches with annotated crop, distance-field, refraction, material, renderer and lifecycle diagrams.
- Aligned condensed code fragments with production variable names and clarified where the excerpts are intentionally shortened.
- Made the PDF builder self-contained by expanding the bundled Noto Serif SC subset and removing machine-specific font paths.
- Added explicit upstream attribution and bundled the Hyalite MIT notice; flagged the Everett reference's undeclared licence before public release.
- Replaced per-component WebGL contexts with one page-level renderer.
- Added stable 2D snapshots so offscreen chat bubbles survive texture release and context loss.
- Extended refraction from an edge band to a continuous rounded-rectangle field.
- Added luminance-adaptive rim suppression for bright backgrounds.
- Split clear and smoked material recipes while retaining one shader.
- Added a nine-tap Gaussian sample only for selected hero surfaces.
- Added viewport culling, texture disposal, DPR cap, frame cap and reduced-motion behavior.

## v3

- Established the five-layer architecture: scene, sampling, optics, geometry and UI.
- Added rounded-rectangle masking, full-surface refraction and directional glints.
- Documented background-coordinate alignment and basic lifecycle.
