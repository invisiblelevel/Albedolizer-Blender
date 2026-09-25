import os
import subprocess
import threading
import queue
import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from . import cli_bridge
from . import node_builder
from .donate import WALLETS, GITHUB_URL, ITCH_URL
from .translations import tr


def _get_prefs(context):
    return context.preferences.addons[__package__].preferences


def _tag_redraw_all():
    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()
    except Exception:
        pass


def _detect_preset_from_filename(filename, prefs, current):
    if not prefs.auto_detect_preset:
        return current

    name = os.path.splitext(os.path.basename(filename))[0].lower()
    known = [
        "metal", "rust", "oxidized_metal", "patina", "brass", "aluminum", "copper",
        "wood", "leaves", "moss", "organic", "grass", "bark",
        "stone", "concrete", "brick", "ground", "asphalt", "marble", "sand",
        "clay", "granite", "stucco", "gemstone", "tile", "gravel", "coal",
        "roof_tiles", "plastic", "rubber", "glass", "ceramic", "painted_metal",
        "carbon", "cardboard", "cotton", "wool", "silk", "denim", "carpet",
        "velvet", "water", "mud", "snow", "ice", "leather", "fur", "skin",
        "scales", "bone",
    ]
    for key in known:
        if key in name:
            return key
    return current


def _open_in_explorer(path):
    if not path or not os.path.isdir(path):
        return False
    try:
        if os.name == "nt":
            os.startfile(path)
        elif os.name == "posix":
            subprocess.Popen(["xdg-open", path])
        else:
            return False
        return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════
#  БАЗОВЫЕ ОПЕРАТОРЫ
# ═══════════════════════════════════════════════════════════
class ALBEDOLIZER_OT_check_path(Operator):
    bl_idname = "albedolizer.check_path"
    bl_label = "Check CLI"
    bl_description = "Verify that Albedolizer CLI is reachable"

    def execute(self, context):
        prefs = _get_prefs(context)
        ok, msg = cli_bridge.check_cli(prefs.cli_path)
        if ok:
            self.report({"INFO"}, f"CLI OK: {msg}")
        else:
            self.report({"ERROR"}, f"CLI failed: {msg}")
        return {"FINISHED"}


class ALBEDOLIZER_OT_copy_cli_path(Operator):
    bl_idname = "albedolizer.copy_cli_path"
    bl_label = "Copy CLI path"

    def execute(self, context):
        prefs = _get_prefs(context)
        try:
            context.window_manager.clipboard = prefs.cli_path
            self.report({"INFO"}, tr(prefs, "cli_copied"))
        except Exception as e:
            self.report({"ERROR"}, f"Clipboard error: {e}")
        return {"FINISHED"}


class ALBEDOLIZER_OT_open_cli_folder(Operator):
    bl_idname = "albedolizer.open_cli_folder"
    bl_label = "Open CLI folder"

    def execute(self, context):
        prefs = _get_prefs(context)
        if not prefs.cli_path:
            self.report({"ERROR"}, "CLI path is empty")
            return {"CANCELLED"}
        folder = os.path.dirname(prefs.cli_path)
        if _open_in_explorer(folder):
            return {"FINISHED"}
        self.report({"ERROR"}, f"Cannot open: {folder}")
        return {"CANCELLED"}


class ALBEDOLIZER_OT_pick_albedo(Operator):
    bl_idname = "albedolizer.pick_albedo"
    bl_label = "Pick Albedo"
    bl_description = "Pick Albedo texture file"

    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(
        default="*.png;*.jpg;*.jpeg;*.tif;*.tiff;*.bmp",
        options={"HIDDEN"},
    )

    def execute(self, context):
        props = context.scene.albedolizer
        prefs = _get_prefs(context)
        props.pending_albedo = self.filepath
        detected = _detect_preset_from_filename(self.filepath, prefs, props.preset)
        if detected != props.preset:
            props.preset = detected
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class ALBEDOLIZER_OT_clear_albedo(Operator):
    bl_idname = "albedolizer.clear_albedo"
    bl_label = "Clear Albedo"

    def execute(self, context):
        context.scene.albedolizer.pending_albedo = ""
        return {"FINISHED"}


class ALBEDOLIZER_OT_maps_all(Operator):
    bl_idname = "albedolizer.maps_all"
    bl_label = "All maps"

    def execute(self, context):
        p = context.scene.albedolizer
        p.maps_height = True
        p.maps_normal = True
        p.maps_ao = True
        p.maps_roughness = True
        p.maps_metallic = True
        p.maps_edge = True
        p.maps_orm = True
        return {"FINISHED"}


class ALBEDOLIZER_OT_maps_none(Operator):
    bl_idname = "albedolizer.maps_none"
    bl_label = "No maps"

    def execute(self, context):
        p = context.scene.albedolizer
        p.maps_height = False
        p.maps_normal = False
        p.maps_ao = False
        p.maps_roughness = False
        p.maps_metallic = False
        p.maps_edge = False
        p.maps_orm = False
        return {"FINISHED"}


# ═══════════════════════════════════════════════════════════
#  БАЗОВЫЙ КЛАСС С ТАЙМЕРОМ
# ═══════════════════════════════════════════════════════════
class _ModalGenerateBase(Operator):
    bl_options = {'REGISTER'}

    _timer = None
    _thread = None
    _queue = None
    _cancel_flag = None
    _done = False

    def execute(self, context):
        return {'CANCELLED'}

    def _start_progress(self, context, label):
        props = context.scene.albedolizer
        props.progress = 0.0
        props.progress_label = label
        props.is_generating = True
        _tag_redraw_all()

    def _stop_progress(self, context):
        props = context.scene.albedolizer
        props.is_generating = False
        props.progress = 0.0
        props.progress_label = ""
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        _tag_redraw_all()

    def modal(self, context, event):
        if event.type != 'TIMER':
            return {'PASS_THROUGH'}

        if self._done:
            return {'PASS_THROUGH'}

        props = context.scene.albedolizer

        try:
            while True:
                msg = self._queue.get_nowait()
                if msg[0] == "progress":
                    _, pct, stage = msg
                    props.progress = pct / 100.0
                    props.progress_label = f"Albedolizer: {stage} ({pct}%)"
                    _tag_redraw_all()
                elif msg[0] == "done":
                    _, ok, result = msg
                    self._done = True
                    self._stop_progress(context)
                    self._on_done(context, ok, result)
                    return {'FINISHED'} if ok else {'CANCELLED'}
        except queue.Empty:
            pass

        return {'PASS_THROUGH'}

    def _on_done(self, context, ok, result):
        pass

    def cancel(self, context):
        if self._cancel_flag:
            self._cancel_flag.set()
        self._stop_progress(context)


# ═══════════════════════════════════════════════════════════
#  GENERATE PBR
# ═══════════════════════════════════════════════════════════
class ALBEDOLIZER_OT_generate_pbr(_ModalGenerateBase):
    bl_idname = "albedolizer.generate_pbr"
    bl_label = "Generate PBR"
    bl_description = "Run Albedolizer CLI and build PBR nodes"

    _mat = None
    _base_name = None
    _out_dir = None

    def invoke(self, context, event):
        prefs = _get_prefs(context)
        props = context.scene.albedolizer

        ok, msg = cli_bridge.check_cli(prefs.cli_path)
        if not ok:
            self.report({"ERROR"}, f"{tr(prefs, 'msg_cli_missing')}: {msg}")
            return {"CANCELLED"}

        albedo_path = props.pending_albedo
        if not albedo_path or not os.path.isfile(albedo_path):
            self.report({"ERROR"}, tr(prefs, "msg_no_albedo"))
            return {"CANCELLED"}

        obj = context.active_object
        if not obj:
            self.report({"ERROR"}, tr(prefs, "msg_no_object"))
            return {"CANCELLED"}

        maps_str = props.get_maps_string()
        if not maps_str:
            self.report({"ERROR"}, tr(prefs, "msg_no_maps"))
            return {"CANCELLED"}

        mat, created = node_builder.ensure_material(obj)
        if created:
            self.report({"INFO"}, f"{tr(prefs, 'msg_material_created')}: {mat.name}")

        self._mat = mat
        self._base_name = os.path.splitext(os.path.basename(albedo_path))[0]
        self._out_dir = os.path.join(os.path.dirname(albedo_path), prefs.output_subfolder)
        self._done = False

        self._start_progress(context, f"{tr(prefs, 'msg_generating')} {self._base_name}...")

        self._cancel_flag = threading.Event()
        self._queue = queue.Queue()
        self._thread, self._queue = cli_bridge.run_generate_async(
            cli_path=prefs.cli_path,
            albedo_path=albedo_path,
            output_dir=self._out_dir,
            preset=props.preset,
            correct_mode=props.correct_mode,
            ai_model=props.ai_model,
            maps_string=maps_str,
            engine=props.engine,
            seamless=props.seamless,
            seamless_hipass=props.seamless_hipass,
            metallic_override=props.metallic_override,
            result_queue=self._queue,
            cancel_flag=self._cancel_flag,
        )

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _on_done(self, context, ok, result):
        prefs = _get_prefs(context)
        if not ok:
            self.report({"ERROR"}, f"{tr(prefs, 'msg_failed')}: {result}")
            return
        report = result
        created = node_builder.build_pbr_nodes(
            self._mat, report, self._out_dir, self._base_name
        )
        context.scene.albedolizer.last_output_dir = self._out_dir
        self.report(
            {"INFO"},
            f"{tr(prefs, 'msg_generated')}: {len(created)} nodes → {self._out_dir}"
        )


# ═══════════════════════════════════════════════════════════
#  BATCH GENERATE
# ═══════════════════════════════════════════════════════════
class ALBEDOLIZER_OT_batch_generate(_ModalGenerateBase):
    bl_idname = "albedolizer.batch_generate"
    bl_label = "Batch Generate"
    bl_description = "Generate PBR for all selected objects (using one Albedo source)"

    _batch_objects = None
    _base_name = None
    _out_dir = None

    def invoke(self, context, event):
        prefs = _get_prefs(context)
        props = context.scene.albedolizer

        ok, msg = cli_bridge.check_cli(prefs.cli_path)
        if not ok:
            self.report({"ERROR"}, f"{tr(prefs, 'msg_cli_missing')}: {msg}")
            return {"CANCELLED"}

        albedo_path = props.pending_albedo
        if not albedo_path or not os.path.isfile(albedo_path):
            self.report({"ERROR"}, tr(prefs, "msg_no_albedo"))
            return {"CANCELLED"}

        selected = [o for o in context.selected_objects if o.type == "MESH"]
        if not selected:
            self.report({"ERROR"}, tr(prefs, "msg_batch_no_objects"))
            return {"CANCELLED"}

        maps_str = props.get_maps_string()
        if not maps_str:
            self.report({"ERROR"}, tr(prefs, "msg_no_maps"))
            return {"CANCELLED"}

        self._batch_objects = selected
        self._base_name = os.path.splitext(os.path.basename(albedo_path))[0]
        self._out_dir = os.path.join(os.path.dirname(albedo_path), prefs.output_subfolder)
        self._done = False

        self._start_progress(context, f"{tr(prefs, 'msg_generating')} {self._base_name}...")

        self._cancel_flag = threading.Event()
        self._queue = queue.Queue()
        self._thread, self._queue = cli_bridge.run_generate_async(
            cli_path=prefs.cli_path,
            albedo_path=albedo_path,
            output_dir=self._out_dir,
            preset=props.preset,
            correct_mode=props.correct_mode,
            ai_model=props.ai_model,
            maps_string=maps_str,
            engine=props.engine,
            seamless=props.seamless,
            seamless_hipass=props.seamless_hipass,
            metallic_override=props.metallic_override,
            result_queue=self._queue,
            cancel_flag=self._cancel_flag,
        )

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _on_done(self, context, ok, result):
        prefs = _get_prefs(context)
        if not ok:
            self.report({"ERROR"}, f"{tr(prefs, 'msg_failed')}: {result}")
            return
        report = result
        total = len(self._batch_objects)
        for i, obj in enumerate(self._batch_objects, 1):
            try:
                mat, _ = node_builder.ensure_material(obj)
                node_builder.build_pbr_nodes(mat, report, self._out_dir, self._base_name)
            except Exception as e:
                self.report({"WARNING"}, f"{obj.name}: {e}")
        context.scene.albedolizer.last_output_dir = self._out_dir
        self.report({"INFO"}, f"{tr(prefs, 'msg_batch_done')}: {total} objects")


# ═══════════════════════════════════════════════════════════
#  OPEN OUTPUT FOLDER
# ═══════════════════════════════════════════════════════════
class ALBEDOLIZER_OT_open_output_folder(Operator):
    bl_idname = "albedolizer.open_output_folder"
    bl_label = "Open Output Folder"
    bl_description = "Open the PBR output folder in the system file browser"

    def execute(self, context):
        prefs = _get_prefs(context)
        props = context.scene.albedolizer

        folder = props.last_output_dir

        if (not folder or not os.path.isdir(folder)) and props.pending_albedo:
            albedo_dir = os.path.dirname(props.pending_albedo)
            candidate = os.path.join(albedo_dir, prefs.output_subfolder)
            if os.path.isdir(candidate):
                folder = candidate

        if (not folder or not os.path.isdir(folder)) and props.pending_albedo:
            albedo_dir = os.path.dirname(props.pending_albedo)
            if os.path.isdir(albedo_dir):
                folder = albedo_dir

        if not folder or not os.path.isdir(folder):
            self.report({"ERROR"}, tr(prefs, "msg_folder_missing"))
            return {"CANCELLED"}

        if _open_in_explorer(folder):
            self.report({"INFO"}, f"Opened: {folder}")
            return {"FINISHED"}

        self.report({"ERROR"}, f"Cannot open: {folder}")
        return {"CANCELLED"}


# ═══════════════════════════════════════════════════════════
#  DONATE / LINKS
# ═══════════════════════════════════════════════════════════
class ALBEDOLIZER_OT_show_donate(Operator):
    bl_idname = "albedolizer.show_donate"
    bl_label = "Support"
    bl_description = "Show donation wallets"

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=440)

    def draw(self, context):
        prefs = _get_prefs(context)
        layout = self.layout

        layout.label(text=tr(prefs, "support_title"), icon="FUND")
        layout.separator()
        for line in tr(prefs, "support_text").split("\n"):
            layout.label(text=line)

        layout.separator()
        for w in WALLETS:
            row = layout.row(align=True)
            row.label(text=w["label"])
            sub = row.row(align=True)
            sub.label(text=w["address"])
            op = sub.operator("albedolizer.copy_wallet", text="", icon="COPYDOWN")
            op.address = w["address"]

        layout.separator()
        row = layout.row()
        row.operator("wm.url_open", text=tr(prefs, "github_btn"), icon="URL").url = GITHUB_URL
        row.operator("wm.url_open", text=tr(prefs, "itch_btn"), icon="URL").url = ITCH_URL

    def execute(self, context):
        return {"FINISHED"}


class ALBEDOLIZER_OT_copy_wallet(Operator):
    bl_idname = "albedolizer.copy_wallet"
    bl_label = "Copy wallet"

    address: StringProperty(default="")

    def execute(self, context):
        prefs = _get_prefs(context)
        try:
            context.window_manager.clipboard = self.address
            self.report({"INFO"}, tr(prefs, "support_copied"))
        except Exception as e:
            self.report({"ERROR"}, f"Clipboard error: {e}")
        return {"FINISHED"}


class ALBEDOLIZER_OT_open_github(Operator):
    bl_idname = "albedolizer.open_github"
    bl_label = "Open GitHub"

    def execute(self, context):
        bpy.ops.wm.url_open(url=GITHUB_URL)
        return {"FINISHED"}


class ALBEDOLIZER_OT_open_itch(Operator):
    bl_idname = "albedolizer.open_itch"
    bl_label = "Open itch.io"

    def execute(self, context):
        bpy.ops.wm.url_open(url=ITCH_URL)
        return {"FINISHED"}