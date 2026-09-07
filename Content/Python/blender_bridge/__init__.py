"""blender_bridge — the Python core of the BlenderBridge UE5 plugin.

Runs INSIDE the Unreal editor's Python (it imports `unreal`). The C++ editor
panel (SBlenderBridgePanel) calls the public entry points below; you can also
drive them from the editor's Python console for headless/CI use.

Public API:
    scan()            list the .glb/.fbx assets waiting in the bridge drop-zone
    run_import()      import them into /Game with naming + smart normal handling
    validate()        pre-flight report (scale, tri budget, missing maps)
    set_export_dir()  override the drop-zone (default: <project>/../blender-studio/exports)

See ../../README.md for the contract this implements.
"""

from . import importer, validate as _validate

__all__ = ["scan", "run_import", "validate", "set_export_dir", "get_export_dir"]

__version__ = "0.1.0"


def scan():
    """Print the assets currently in the drop-zone, with their resolved /Game targets."""
    return importer.scan()


def run_import():
    """Import every asset in the drop-zone into /Game, mirroring export subfolders."""
    return importer.run_import()


def validate():
    """Run the pre-flight validation report over imported content."""
    return _validate.run()


def set_export_dir(path):
    """Override the bridge drop-zone directory."""
    importer.set_export_dir(path)


def get_export_dir():
    """Return the resolved bridge drop-zone directory."""
    return importer.get_export_dir()
