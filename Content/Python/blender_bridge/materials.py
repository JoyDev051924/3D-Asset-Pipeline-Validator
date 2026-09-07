"""Material-instance auto-wiring (v0.2 — experimental).

Detects texture sets that share a stem (e.g. Rock_BC / Rock_N / Rock_ORM) and
spins up a Material Instance off a master material, hooking each map to its
parameter. This is the tech-artist payoff that turns a raw import into a
ready-to-use material.

Status: scaffolded, not yet wired into the import flow. Enable in run_import()
once the master material + parameter names are finalised (see ROADMAP in README).
"""

try:
    import unreal
except ImportError:  # pragma: no cover - only runs in-editor
    raise SystemExit("blender_bridge must run inside the Unreal editor's Python.")

from . import naming

# Texture role -> Material Instance texture-parameter name on the master material.
# These must match the parameters authored on the master M_BridgeMaster.
PARAM_FOR_ROLE = {
    "BaseColor": "BaseColor",
    "Normal": "Normal",
    "ORM": "ORM",
    "Metallic": "Metallic",
    "Roughness": "Roughness",
    "AmbientOcclusion": "AO",
    "Emissive": "Emissive",
}

DEFAULT_MASTER = "/BlenderBridge/Materials/M_BridgeMaster"


def group_texture_sets(texture_asset_paths):
    """Group texture asset paths by their shared stem (name minus the role suffix)."""
    sets = {}
    for path in texture_asset_paths:
        name = path.rsplit("/", 1)[-1]
        role = naming.texture_role(name)
        if not role:
            continue
        # Strip the role suffix to get the material stem.
        stem = name
        for suffix in naming.TEXTURE_ROLES:
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break
        sets.setdefault(stem.lstrip("T_"), {})[role] = path
    return sets


def create_instance(stem, role_to_path, dest_folder, master_path=DEFAULT_MASTER):
    """Create MI_<stem> in dest_folder, parented to the master, with maps assigned."""
    master = unreal.EditorAssetLibrary.load_asset(master_path)
    if master is None:
        unreal.log_warning(f"[bridge] master material not found: {master_path}")
        return None

    mi_name = naming.apply_prefix(stem, "MaterialInstanceConstant")
    package_path = f"{dest_folder}/{mi_name}"

    factory = unreal.MaterialInstanceConstantFactoryNew()
    factory.set_editor_property("initial_parent", master)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mi = asset_tools.create_asset(mi_name, dest_folder, unreal.MaterialInstanceConstant, factory)

    for role, tex_path in role_to_path.items():
        param = PARAM_FOR_ROLE.get(role)
        tex = unreal.EditorAssetLibrary.load_asset(tex_path)
        if param and tex:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi, param, tex)

    unreal.EditorAssetLibrary.save_asset(package_path)
    unreal.log(f"[bridge] material: created {mi_name} ({len(role_to_path)} maps)")
    return mi
