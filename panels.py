import bpy
from bpy.types import Panel

from .translations import tr


class ALBEDOLIZER_PT_main_panel(Panel):
    bl_label = "Albedolizer PBR"
    bl_idname = "ALBEDOLIZER_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Albedolizer"

    def draw(self, context):
        layout = self.layout
        props = context.scene.albedolizer
        prefs = context.preferences.addons[__package__].preferences

        # ═══ CLI ═══
        box = layout.box()
        box.label(text=tr(prefs, "cli_section"), icon="CONSOLE")

        status_row = box.row()
        if prefs.cli_path and __import__("os").path.isfile(prefs.cli_path):
            status_row.label(text=tr(prefs, "cli_status_ok"), icon="CHECKMARK")
        elif prefs.cli_path:
            status_row.label(text=tr(prefs, "cli_status_missing"), icon="ERROR")
        else:
            status_row.label(text=tr(prefs, "cli_status_unknown"), icon="INFO")

        row = box.row(align=True)
        row.prop(prefs, "cli_path", text="")
        row.operator("albedolizer.check_path", text="", icon="FILE_REFRESH")

        row = box.row(align=True)
        row.operator("albedolizer.copy_cli_path", text=tr(prefs, "cli_copy"), icon="COPYDOWN")
        row.operator("albedolizer.open_cli_folder", text=tr(prefs, "cli_open_folder"), icon="FILE_FOLDER")

        # ═══ Albedo ═══
        layout.separator()
        layout.label(text=tr(prefs, "albedo_section"), icon="IMAGE_DATA")
        row = layout.row(align=True)
        row.prop(props, "pending_albedo", text="")
        row.operator("albedolizer.pick_albedo", text="", icon="FILEBROWSER")
        row.operator("albedolizer.clear_albedo", text="", icon="X")

        # ═══ Preset ═══
        layout.separator()
        layout.label(text=tr(prefs, "preset_section"), icon="MATERIAL")
        layout.prop(props, "preset", text="")
        layout.prop(prefs, "auto_detect_preset", text=tr(prefs, "autodetect_preset"))

        # ═══ Correction ═══
        layout.separator()
        layout.label(text=tr(prefs, "correction_section"), icon="SHADERFX")
        layout.prop(props, "correct_mode", text="")
        if props.correct_mode == "ai":
            layout.prop(props, "ai_model", text=tr(prefs, "ai_model"))

        # ═══ Seamless ═══
        layout.separator()
        layout.label(text=tr(prefs, "seamless_section"), icon="MOD_TILE")
        layout.prop(props, "seamless", text=tr(prefs, "seamless_enable"))
        if props.seamless:
            layout.prop(props, "seamless_hipass", text=tr(prefs, "seamless_hipass"))

        # ═══ Maps ═══
        layout.separator()
        row = layout.row()
        row.label(text=tr(prefs, "maps_section"), icon="TEXTURE")
        row.operator("albedolizer.maps_all", text=tr(prefs, "maps_all"))
        row.operator("albedolizer.maps_none", text=tr(prefs, "maps_none"))

        col = layout.column(align=True)
        r = col.row(align=True)
        r.prop(props, "maps_height", toggle=True)
        r.prop(props, "maps_normal", toggle=True)
        r = col.row(align=True)
        r.prop(props, "maps_ao", toggle=True)
        r.prop(props, "maps_roughness", toggle=True)
        r = col.row(align=True)
        r.prop(props, "maps_metallic", toggle=True)
        r.prop(props, "maps_edge", toggle=True)
        col.prop(props, "maps_orm", toggle=True)

        # ═══ Engine ═══
        layout.separator()
        layout.label(text=tr(prefs, "engine_section"), icon="EXPORT")
        layout.prop(props, "engine", text="")

        # ═══ Кнопки ═══
        layout.separator()
        row = layout.row()
        row.scale_y = 1.6
        row.operator("albedolizer.generate_pbr", icon="PLAY", text=tr(prefs, "generate_btn"))

        row = layout.row()
        row.scale_y = 1.2
        row.operator("albedolizer.batch_generate", icon="DUPLICATE", text=tr(prefs, "generate_batch_btn"))

        row = layout.row()
        row.scale_y = 1.1
        row.operator("albedolizer.open_output_folder", icon="FILE_FOLDER", text=tr(prefs, "open_folder_btn"))

        # ═══ Поддержка ═══
        layout.separator()
        row = layout.row(align=True)
        row.operator("albedolizer.open_github", text=tr(prefs, "github_btn"), icon="URL")
        row.operator("albedolizer.open_itch", text=tr(prefs, "itch_btn"), icon="URL")

        row = layout.row()
        row.scale_y = 1.1
        row.operator("albedolizer.show_donate", text=tr(prefs, "support_btn"), icon="FUND")