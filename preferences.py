import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, EnumProperty, BoolProperty


class AlbedolizerPreferences(AddonPreferences):
    bl_idname = __package__

    language: EnumProperty(
        name="Language / Язык",
        items=[
            ("en", "English", ""),
            ("ru", "Русский", ""),
        ],
        default="en",
    )

    cli_path: StringProperty(
        name="Albedolizer CLI Path",
        description="Full path to albedolizer_cli.exe",
        subtype="FILE_PATH",
        default="",
    )

    output_subfolder: StringProperty(
        name="Output Subfolder",
        description="Subfolder next to Albedo texture where PBR maps are saved",
        default="_pbr",
    )

    auto_detect_preset: BoolProperty(
        name="Auto-detect preset from filename",
        description="If filename contains a known preset name (brick, metal, wood...), use it",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "language")
        layout.separator()
        layout.prop(self, "cli_path")
        row = layout.row(align=True)
        row.prop(self, "output_subfolder", text="Output subfolder")
        layout.prop(self, "auto_detect_preset")