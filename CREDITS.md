# Credits

This implementation was developed after studying two upstream liquid-glass projects, then reworked through multiple Cove Home iterations for rounded cards, chat bubbles, theme changes and long mobile conversations.

## Upstream references

### VII-Cae / hyalite--liquid-glass

- Author: VII-Cae (VII)
- Source: https://github.com/VII-Cae/hyalite--liquid-glass
- Licence: MIT, copyright (c) 2026 VII-Cae (VII)
- Role in the lineage: rounded-rectangle distance fields, lens/refraction thinking and edge treatment were important prior art.

Hyalite builds SDF lens maps and applies them through SVG displacement and `backdrop-filter`. The public Cove demo uses a separately structured WebGL/Canvas pipeline, but the upstream project and its engineering ideas must remain visibly credited. Its complete MIT notice is preserved at `third_party/VII-Cae-hyalite--liquid-glass-LICENSE.txt`.

### everett745 / liquid-glass

- Author: everett745
- Source: https://github.com/everett745/liquid-glass
- Declared modes: SVG, WebGL and CSS; React and vanilla APIs
- Licence status: no `LICENSE` file or licence field in `package.json` was visible when reviewed on 2026-11-05.

This repository is therefore credited as a technical reference, but its source code must not be copied or redistributed unless the author supplies a licence or grants permission. Before publication, the Cove demo was compared against Everett's `src/core/shaders.ts` and `src/core/effects/webgl.ts`; it does not copy their shader bodies, classes, public API or component implementation. Shared fullscreen-quad setup and WebGL calls are standard platform boilerplate.

## Cove Home iterations

Later Cove work includes the full-surface rounded-rectangle field, local background-coordinate sampling, luminance-adaptive edge treatment, clear/smoked material recipes, one shared WebGL renderer, stable 2D snapshots and the mobile lifecycle documented in the v4 guide.

Public repository: https://github.com/yanceydaisy/liquid-glass-note

## Typeface

The PDF is typeset with a subset of Noto Serif SC, developed by Google and Adobe and distributed under the SIL Open Font License 1.1. The bundled subset is used only by the PDF build and its licence is included at `assets/OFL-1.1.txt`.

- Upstream: https://github.com/notofonts/noto-cjk
- Google Fonts metadata: https://github.com/google/fonts/tree/main/ofl/notoserifsc
