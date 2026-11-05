# Changelog

## v4

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
