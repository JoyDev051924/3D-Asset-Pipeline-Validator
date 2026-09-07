"""Naming conventions enforced on import.

Mirrors the UE asset-naming standard used across the pipeline:
    SM_ static mesh   SK_ skeletal mesh   T_ texture   M_ material
    MI_ material instance   A_/AS_ animation   BP_ blueprint   DA_ data asset

Texture role suffixes:  _BC base colour   _N normal   _ORM occlusion/rough/metallic
"""

# Asset-type prefixes.
PREFIX = {
    "StaticMesh": "SM_",
    "SkeletalMesh": "SK_",
    "Texture2D": "T_",
    "Material": "M_",
    "MaterialInstanceConstant": "MI_",
    "AnimSequence": "AS_",
    "Blueprint": "BP_",
    "DataAsset": "DA_",
}

# Texture role suffixes we recognise (used by the material auto-wiring in v0.2).
TEXTURE_ROLES = {
    "_BC": "BaseColor",
    "_N": "Normal",
    "_ORM": "ORM",
    "_M": "Metallic",
    "_R": "Roughness",
    "_AO": "AmbientOcclusion",
    "_E": "Emissive",
}


def has_prefix(name, asset_type):
    """True if `name` already carries the correct prefix for `asset_type`."""
    p = PREFIX.get(asset_type)
    return bool(p) and name.startswith(p)


def apply_prefix(name, asset_type):
    """Return `name` with the correct prefix for `asset_type`, idempotently."""
    p = PREFIX.get(asset_type)
    if not p or name.startswith(p):
        return name
    return p + name


def is_normal_map(name):
    """True if the texture name looks like a normal map (carries the _N role suffix)."""
    stem = name.rsplit(".", 1)[0]
    return stem.endswith("_N") or "_N_" in stem


def texture_role(name):
    """Return the recognised texture role for a name, or None."""
    stem = name.rsplit(".", 1)[0]
    for suffix, role in TEXTURE_ROLES.items():
        if stem.endswith(suffix):
            return role
    return None
