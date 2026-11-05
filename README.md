# Cove Liquid Glass Notes

A compact technical note and a self-contained browser demo for a full-surface liquid-glass material built with CSS, Canvas 2D, WebGL and GLSL.

This repository contains the public, stripped-down version of the optics work used in Cove Home. It does not contain the Home application, private assets, chat logic or personal data.

## Read first

- `docs/liquid-glass-technical-guide-v4.pdf` explains the render chain, equations, material recipes and lifecycle.
- `demo/index.html` is a minimal implementation with clear and smoked glass.
- `demo/liquid-glass.js` contains the shared WebGL renderer and shader.

## Run the demo

Serve the repository with any static server, then open `demo/`.

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080/demo/`.

The demo intentionally samples only the shared background source. Arbitrary DOM content and recursively stacked glass are outside its scope.

## Rebuild the PDF

Install ReportLab, then run:

```bash
python3 tools/build_pdf.py
```

The builder writes `docs/liquid-glass-technical-guide-v4.pdf` and uses the bundled, licensed font subset.

## Current material baseline

```js
{
  refract: 26,
  tint: 0,
  blur: 0,
  edge: 25,
  shine: 13,
  wobble: 15
}
```

These values are tuning controls for this shader, not physical units.

## Public scope

The repository is meant to share the engineering approach: one background coordinate system, rounded-rectangle SDF geometry, full-surface refraction, luminance-adaptive edges, clear/smoked material variants, one shared WebGL context and stable 2D snapshots.

## Credits and publication status

The project was developed after studying two upstream references:

- [`VII-Cae/hyalite--liquid-glass`](https://github.com/VII-Cae/hyalite--liquid-glass), MIT licensed.
- [`everett745/liquid-glass`](https://github.com/everett745/liquid-glass), with no explicit licence detected in the repository when reviewed on 2026-11-05.

The exact lineage and the parts developed during later Cove Home iterations are recorded in `CREDITS.md`. The Hyalite MIT notice is bundled under `third_party/`. A code-level comparison was also made against Everett's published shader and WebGL implementation before this repository was opened; the public Cove demo does not copy those shader bodies, classes or component source.

This repository is public for reading, discussion and linking. No licence is currently granted for the Cove-authored code or documentation; all rights remain reserved unless a later release adds an explicit licence. Third-party material retains its own notices.

## PDF typeface

The PDF build uses an embedded subset of Noto Serif SC. The subset in `assets/noto-serif-sc.ttf` remains under the SIL Open Font License 1.1; see `assets/OFL-1.1.txt`.
