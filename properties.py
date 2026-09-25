import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty

PRESET_ITEMS = [
    ("metal", "Metal", ""),
    ("rust", "Rust", ""),
    ("oxidized_metal", "Oxidized Metal", ""),
    ("patina", "Patina", ""),
    ("brass", "Brass", ""),
    ("aluminum", "Aluminum", ""),
    ("copper", "Copper", ""),
    ("wood", "Wood", ""),
    ("leaves", "Leaves", ""),
    ("moss", "Moss", ""),
    ("organic", "Organic", ""),
    ("grass", "Grass", ""),
    ("bark", "Bark", ""),
    ("stone", "Stone", ""),
    ("concrete", "Concrete", ""),
    ("brick", "Brick", ""),
    ("ground", "Ground", ""),
    ("asphalt", "Asphalt", ""),
    ("marble", "Marble", ""),
    ("sand", "Sand", ""),
    ("clay", "Clay", ""),
    ("granite", "Granite", ""),
    ("stucco", "Stucco", ""),
    ("gemstone", "Gemstone", ""),
    ("tile", "Tile", ""),
    ("gravel", "Gravel", ""),
    ("coal", "Coal", ""),
    ("roof_tiles", "Roof Tiles", ""),
    ("plastic", "Plastic", ""),
    ("rubber", "Rubber", ""),
    ("glass", "Glass", ""),
    ("ceramic", "Ceramic", ""),
    ("painted_metal", "Painted Metal", ""),
    ("carbon", "Carbon", ""),
    ("cardboard", "Cardboard", ""),
    ("cotton", "Cotton", ""),
    ("wool", "Wool", ""),
    ("silk", "Silk", ""),
    ("denim", "Denim", ""),
    ("carpet", "Carpet", ""),
    ("velvet", "Velvet", ""),
    ("water", "Water", ""),
    ("mud", "Mud", ""),
    ("snow", "Snow", ""),
    ("ice", "Ice", ""),
    ("leather", "Leather", ""),
    ("fur", "Fur", ""),
    ("skin", "Skin", ""),
    ("scales", "Scales", ""),
    ("bone", "Bone", ""),
]


class AlbedolizerProperties(PropertyGroup):

    pending_albedo: StringProperty(
        name="Pending Albedo",
        subtype="FILE_PATH",
        default="",
    )

    last_output_dir: StringProperty(
        name="Last Output Dir",
        subtype="DIR_PATH",
        default="",
    )

    preset: EnumProperty(
        name="Material Preset",
        items=PRESET_ITEMS,
        default="metal",
    )

    correct_mode: EnumProperty(
        name="Correction",
        items=[
            ("none", "None", "No correction, just PBR"),
            ("ai", "AI", "AI correction"),
            ("math", "Math", "CLAHE fallback"),
        ],
        default="ai",
    )

    ai_model: EnumProperty(
        name="AI Model",
        items=[
            ("autolevels", "Autolevels", ""),
            ("lutwithbgrid", "LUTwithBGrid", ""),
        ],
        default="autolevels",
    )

    seamless: BoolProperty(name="Seamless", default=False)
    seamless_hipass: BoolProperty(name="Hi-pass", default=True)

    maps_height: BoolProperty(name="Height", default=True)
    maps_normal: BoolProperty(name="Normal", default=True)
    maps_ao: BoolProperty(name="AO", default=True)
    maps_roughness: BoolProperty(name="Roughness", default=True)
    maps_metallic: BoolProperty(name="Metallic", default=True)
    maps_edge: BoolProperty(name="Edge", default=True)
    maps_orm: BoolProperty(name="ORM", default=True)

    engine: EnumProperty(
        name="Engine",
        items=[
            ("", "None", "No engine packing"),
            ("unity_hdrp", "Unity HDRP", ""),
            ("unity_urp", "Unity URP", ""),
            ("unreal", "Unreal", ""),
            ("godot", "Godot", ""),
        ],
        default="",
    )

    # ═══ Прогресс-бар ═══
    progress: FloatProperty(
        name="Progress",
        default=0.0,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
    )

    progress_label: StringProperty(
        name="Progress Label",
        default="",
    )

    is_generating: BoolProperty(
        name="Is Generating",
        default=False,
    )

    def get_maps_string(self):
        maps = []
        if self.maps_height:
            maps.append("height")
        if self.maps_normal:
            maps.append("normal")
        if self.maps_ao:
            maps.append("ao")
        if self.maps_roughness:
            maps.append("roughness")
        if self.maps_metallic:
            maps.append("metallic")
        if self.maps_edge:
            maps.append("edge")
        if self.maps_orm:
            maps.append("orm")
        return ",".join(maps)