bl_info = {
    "name": "Albedolizer-Blender",
    "author": "INV.LVL",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Albedolizer",
    "description": "Generate PBR maps from Albedo textures via Albedolizer CLI",
    "category": "Material",
}

import os
import bpy
from . import preferences
from . import properties
from . import operators
from . import panels

classes = (
    preferences.AlbedolizerPreferences,
    properties.AlbedolizerProperties,
    operators.ALBEDOLIZER_OT_check_path,
    operators.ALBEDOLIZER_OT_copy_cli_path,
    operators.ALBEDOLIZER_OT_open_cli_folder,
    operators.ALBEDOLIZER_OT_pick_albedo,
    operators.ALBEDOLIZER_OT_clear_albedo,
    operators.ALBEDOLIZER_OT_maps_all,
    operators.ALBEDOLIZER_OT_maps_none,
    operators.ALBEDOLIZER_OT_generate_pbr,
    operators.ALBEDOLIZER_OT_batch_generate,
    operators.ALBEDOLIZER_OT_open_output_folder,
    operators.ALBEDOLIZER_OT_show_donate,
    operators.ALBEDOLIZER_OT_copy_wallet,
    operators.ALBEDOLIZER_OT_open_github,
    operators.ALBEDOLIZER_OT_open_itch,
    panels.ALBEDOLIZER_PT_main_panel,
)


def _find_bundled_cli():
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(addon_dir, "cli", "albedolizer_cli.exe")
    if os.path.isfile(candidate):
        return candidate
    return ""


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.albedolizer = bpy.props.PointerProperty(
        type=properties.AlbedolizerProperties
    )

    prefs = bpy.context.preferences.addons[__package__].preferences
    bundled = _find_bundled_cli()
    if bundled:
        if not prefs.cli_path or not os.path.isfile(prefs.cli_path):
            prefs.cli_path = bundled
            print(f"Albedolizer PBR Bridge: bundled CLI found → {bundled}")
        else:
            print(f"Albedolizer PBR Bridge: using user CLI → {prefs.cli_path}")
    else:
        print("Albedolizer PBR Bridge: bundled CLI not found, set path manually")

    print("Albedolizer PBR Bridge: registered")


def unregister():
    del bpy.types.Scene.albedolizer

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("Albedolizer PBR Bridge: unregistered")