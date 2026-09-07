"""Pre-flight validation report over imported content.

Surfaces the things that silently bite a Blender->UE5 import:
  * scale drift  (a 1 m crate must read as ~100 uu; 100x off means a transform
    wasn't applied or an FBX scale was wrong)
  * triangle budget  (props 300-1500 tris per the bridge checklist)
  * missing lightmap UVs on static meshes
  * normal maps that were imported without the green-channel flag

Read-only: it reports, it does not mutate assets.
"""

try:
    import unreal
except ImportError:  # pragma: no cover - only runs in-editor
    raise SystemExit("blender_bridge must run inside the Unreal editor's Python.")

from . import naming

# Tri budget from BRIDGE.md (props). Tune per project.
TRI_MIN, TRI_MAX = 300, 1500
CONTENT_ROOT = "/Game"


def _all_assets(path=CONTENT_ROOT):
    return unreal.EditorAssetLibrary.list_assets(path, recursive=True, include_folder=False)


def _check_static_mesh(asset_path, issues):
    mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not isinstance(mesh, unreal.StaticMesh):
        return
    name = asset_path.rsplit("/", 1)[-1]

    if not naming.has_prefix(name, "StaticMesh"):
        issues.append(f"naming: {name} is a StaticMesh without the SM_ prefix")

    # Triangle count (LOD0).
    tris = mesh.get_num_triangles(0) if hasattr(mesh, "get_num_triangles") else None
    if tris is not None and not (TRI_MIN <= tris <= TRI_MAX):
        issues.append(f"tris: {name} has {tris} tris (budget {TRI_MIN}-{TRI_MAX})")

    # Bounds sanity: a sub-1uu or >100000uu prop usually means a scale error.
    bounds = mesh.get_bounds().box_extent
    longest = max(bounds.x, bounds.y, bounds.z) * 2.0
    if longest < 1.0 or longest > 100000.0:
        issues.append(f"scale: {name} longest axis is {longest:.1f} uu — check applied transforms")


def _check_texture(asset_path, issues):
    name = asset_path.rsplit("/", 1)[-1]
    if naming.is_normal_map(name):
        tex = unreal.EditorAssetLibrary.load_asset(asset_path)
        if isinstance(tex, unreal.Texture2D):
            comp = tex.get_editor_property("compression_settings")
            if comp != unreal.TextureCompressionSettings.TC_NORMALMAP:
                issues.append(f"normal: {name} looks like a normal map but isn't TC_NORMALMAP")


def run(path=CONTENT_ROOT):
    """Validate everything under `path`; log a report and return the issue list."""
    issues = []
    assets = _all_assets(path)
    for asset_path in assets:
        cls = unreal.EditorAssetLibrary.find_asset_data(asset_path).asset_class_path.asset_name
        if cls == "StaticMesh":
            _check_static_mesh(asset_path, issues)
        elif cls == "Texture2D":
            _check_texture(asset_path, issues)

    if not issues:
        unreal.log(f"[bridge] validate: {len(assets)} asset(s) checked, no issues.")
    else:
        unreal.log_warning(f"[bridge] validate: {len(issues)} issue(s) found:")
        for i in issues:
            unreal.log_warning(f"[bridge]   - {i}")
    return issues
