"""Asset import across the Blender -> UE5 bridge.

Built up from the original 82-line `import_from_blender.py`, generalised into a
reusable, configurable importer with a dry-run scan and category mirroring.

The drop-zone defaults to `<project>/../blender-studio/exports` (the bridge
contract), and can be overridden with `set_export_dir()` or the
BLENDER_BRIDGE_EXPORTS environment variable.
"""

import os

try:
    import unreal
except ImportError:  # pragma: no cover - only runs in-editor
    raise SystemExit("blender_bridge must run inside the Unreal editor's Python.")

from . import naming

CONTENT_ROOT = "/Game"
_MESH_EXTS = (".glb", ".fbx")

# Module-level config; resolved lazily so a project can override before importing.
_EXPORT_DIR = None


def _default_export_dir():
    project_dir = unreal.Paths.project_dir()
    return os.path.normpath(os.path.join(project_dir, "..", "blender-studio", "exports"))


def set_export_dir(path):
    """Override the bridge drop-zone directory."""
    global _EXPORT_DIR
    _EXPORT_DIR = os.path.normpath(path)


def get_export_dir():
    """Resolve the drop-zone: explicit override > env var > bridge default."""
    if _EXPORT_DIR:
        return _EXPORT_DIR
    env = os.environ.get("BLENDER_BRIDGE_EXPORTS")
    return os.path.normpath(env) if env else _default_export_dir()


def _category_for(root, export_dir):
    """Map an export subfolder to a PascalCase /Game category (case-sensitive on Linux)."""
    rel_dir = os.path.relpath(root, export_dir)
    if rel_dir == ".":
        return ""
    return "/".join(
        seg[:1].upper() + seg[1:]
        for seg in rel_dir.replace(os.sep, "/").split("/")
    )


def _iter_assets(export_dir):
    """Yield (src_path, dest_package_path) for each importable asset in the drop-zone.

    Staging/hidden folders (names starting with '_' or '.', e.g. the Blender-side
    '_raw' work area) are pruned — only validated category folders cross the bridge.
    """
    for root, dirs, files in os.walk(export_dir):
        dirs[:] = [d for d in dirs if not d.startswith(("_", "."))]
        for fname in files:
            if not fname.lower().endswith(_MESH_EXTS):
                continue
            src = os.path.join(root, fname)
            category = _category_for(root, export_dir)
            dest = f"{CONTENT_ROOT}/{category}".rstrip("/")
            yield src, dest


def scan():
    """Dry run: log every asset that would be imported and where it would land."""
    export_dir = get_export_dir()
    if not os.path.isdir(export_dir):
        unreal.log_warning(f"[bridge] no drop-zone at {export_dir}")
        return []

    found = list(_iter_assets(export_dir))
    if not found:
        unreal.log(f"[bridge] drop-zone empty: {export_dir}")
    for src, dest in found:
        unreal.log(f"[bridge] scan: {os.path.basename(src)} -> {dest}")
    unreal.log(f"[bridge] scan complete — {len(found)} asset(s) pending.")
    return found


def _build_options(src_path):
    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_materials = True
    options.import_textures = True
    options.static_mesh_import_data.set_editor_property("combine_meshes", True)
    options.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
    # Flip the green channel for normal maps only (Blender bakes OpenGL +Y, UE wants
    # DirectX -Y). Blanket-flipping in the old script also touched non-normal textures.
    options.texture_import_data.set_editor_property(
        "invert_normal_maps", naming.is_normal_map(os.path.basename(src_path))
    )
    return options


def _import_one(src_path, dest_package_path):
    task = unreal.AssetImportTask()
    task.filename = src_path
    task.destination_path = dest_package_path
    task.automated = True
    task.replace_existing = True
    task.save = True
    task.options = _build_options(src_path)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.log(f"[bridge] imported {os.path.basename(src_path)} -> {dest_package_path}")


def run_import():
    """Import every pending asset from the drop-zone into /Game."""
    export_dir = get_export_dir()
    if not os.path.isdir(export_dir):
        unreal.log_warning(f"[bridge] no drop-zone at {export_dir}")
        return 0

    count = 0
    for src, dest in _iter_assets(export_dir):
        _import_one(src, dest)
        count += 1

    unreal.log(f"[bridge] import complete — {count} asset(s) from {export_dir}")
    return count
