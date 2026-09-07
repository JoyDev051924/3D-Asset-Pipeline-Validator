# BlenderBridge

A UE5 editor plugin for a validated **Blender to Unreal Engine 5** asset pipeline.

Drop your `.glb`/`.fbx` exports in one folder, click **Import**, and BlenderBridge
mirrors them into `/Game` with the right naming, correct normal-map handling, and a
pre-flight validation report. A Blender export becomes game-ready content without
the manual cleanup every Blender-to-UE workflow repeats by hand.

**What it does in one line:** turns the repetitive Blender to UE5 import checklist into
one click: prefix naming, normal-map green-channel flip, lightmap-UV generation, and
scale plus triangle-budget validation. An 82-line throwaway import script, rebuilt as a
validated, reusable editor tool.

> Built for [Survival3D / Island Haven](https://github.com/marko-builds) and extracted
> as a standalone tool. Hybrid design: a C++ editor module hosts the UI; a bundled
> Python package does the asset work.

## Why

Every Blender-to-UE5 import hits the same chores: prefix the assets (`SM_`/`T_`/…),
flip the green channel on normal maps (Blender bakes OpenGL +Y, UE expects DirectX -Y),
generate lightmap UVs, sanity-check scale (a 1 m crate must read as ~100 uu), and wire
material instances from `_BC`/`_N`/`_ORM` texture sets. BlenderBridge does all of it
from one panel.

## Features

- **One-panel import** — scan the drop-zone, see what's pending, import into `/Game`
  mirroring your export subfolders.
- **Smart normals** — green-channel flip applied only to detected normal maps (`_N`),
  not blanket-applied to every texture.
- **Naming enforcement** — auto-prefixes by asset type; flags violations.
- **Pre-flight validation** — scale drift, triangle budget, missing lightmap UVs,
  mis-tagged normal maps.
- **Material auto-wiring** _(v0.2)_ — `_BC`/`_N`/`_ORM` sets become `MI_` instances off
  a master material.

## How it works

A deliberate **hybrid** split keeps each side doing what it's best at:

- **C++ editor module** (`BlenderBridgeEditor`) — a thin Slate panel registered under the
  Tools menu. Kept intentionally minimal so it survives engine-API drift across UE versions.
- **Python core** (`blender_bridge`) — all the asset logic: scan, import, naming,
  validation. Uses Unreal's editor-scripting API, so the rules stay readable and runnable
  without recompiling.

The C++ buttons call the Python entry points via `IPythonScriptPlugin`. Those same entry
points are scriptable from the editor's Python console for headless / CI runs.

## Install

1. Copy this folder into your project's `Plugins/` directory
   (`YourProject/Plugins/BlenderBridge`).
2. Enable **Python Editor Script Plugin** (Edit → Plugins → Scripting).
3. Regenerate project files and build (the editor module is C++).
4. Open the panel: **Tools → BlenderBridge**.

Requires Unreal Engine 5.7+.

## Usage

By default the drop-zone is `<project>/../blender-studio/exports`. Override it from the
editor's Python console:

```python
import blender_bridge
blender_bridge.set_export_dir("/path/to/exports")
blender_bridge.scan()        # dry run
blender_bridge.run_import()  # import into /Game
blender_bridge.validate()    # pre-flight report
```

The panel buttons call these same entry points.

## Status

**v0.1** — the C++ editor module compiles clean against UE 5.7.4; the Python core is
smoke-tested headless (`scan()` maps validated props correctly). In-editor panel
click-through, a `/Game` import, and a walkthrough capture are the next verification pass.
This is the current state, not a finished-v1.0 claim.

## Roadmap

- **v0.1** — import panel, smart normals, naming enforcement, validation report.
- **v0.2** — material-instance auto-wiring + a config DataAsset for folder mapping.
- **v0.3** — selectable per-asset import, captured results in-panel, Fab listing.

## License

MIT. See [LICENSE](LICENSE).
