import os
import bpy


def get_principled(mat):
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            return node
    return None


def ensure_image(path, name):
    if not os.path.isfile(path):
        return None

    for img in bpy.data.images:
        if img.filepath == path:
            return img

    try:
        img = bpy.data.images.load(path, check_existing=True)
        img.name = name
        return img
    except Exception:
        return None


def ensure_material(obj):
    """Гарантирует, что у объекта есть активный материал. Возвращает (mat, created)."""
    if obj.active_material is None:
        mat = bpy.data.materials.new(name=f"{obj.name}_Albedolizer")
        mat.use_nodes = True
        obj.data.materials.append(mat)
        return mat, True
    return obj.active_material, False


def build_pbr_nodes(mat, report, output_dir, base_name):
    if not mat.use_nodes:
        mat.use_nodes = True

    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    principled = get_principled(mat)
    if not principled:
        return []

    maps = report.get("maps", {})
    created = []

    px = principled.location.x + 350
    py = principled.location.y

    def load_and_place(key, label, y_off=0):
        path = maps.get(key)
        if not path or not os.path.isfile(path):
            return None
        img = ensure_image(path, f"{base_name}_{key}")
        if not img:
            return None
        node = nodes.new("ShaderNodeTexImage")
        node.image = img
        node.label = label
        node.location = (px, py + y_off)
        node.width = 200
        created.append(node)
        return node

    albedo_node = load_and_place("albedo", "Albedo", 0)
    if not albedo_node and report.get("input"):
        src = report["input"]
        if os.path.isfile(src):
            img = ensure_image(src, f"{base_name}_albedo_src")
            if img:
                albedo_node = nodes.new("ShaderNodeTexImage")
                albedo_node.image = img
                albedo_node.label = "Albedo (source)"
                albedo_node.location = (px, py)
                albedo_node.width = 200
                created.append(albedo_node)

    if albedo_node:
        links.new(albedo_node.outputs["Color"], principled.inputs["Base Color"])

    rough_node = load_and_place("roughness", "Roughness", -320)
    if rough_node:
        links.new(rough_node.outputs["Color"], principled.inputs["Roughness"])

    metal_node = load_and_place("metallic", "Metallic", -640)
    if metal_node:
        links.new(metal_node.outputs["Color"], principled.inputs["Metallic"])

    normal_node = load_and_place("normal", "Normal", -960)
    if normal_node:
        nmap = nodes.new("ShaderNodeNormalMap")
        nmap.location = (px + 300, py - 960)
        created.append(nmap)
        links.new(normal_node.outputs["Color"], nmap.inputs["Color"])
        links.new(nmap.outputs["Normal"], principled.inputs["Normal"])

    return created