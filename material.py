series = "wp01d"
name = "001b2"
body = f"a{name}"
scope = f"scope{name}"
attach = f"attach{name}"
muzzle = f"muzzle{name}"
magazine = f"magazine{name}"

item = scope

base_path = f"C:/Users/joshu/Desktop/SnowAssets"
d_path = f"{base_path}/{series}_{name}/{series}_{item}_d.tga"
r_path = f"{base_path}/{series}_{name}/{series}_{item}_r.tga"
n_path = f"{base_path}/{series}_{name}/{series}_{item}_n.tga"

import bpy

selected_object = bpy.context.active_object
material = selected_object.data.materials[0]
material.use_nodes = True

d_img = bpy.data.images.load(d_path)
r_img = bpy.data.images.load(r_path)
n_img = bpy.data.images.load(n_path)

d_tex = selected_object.active_material.node_tree.nodes.new(type='ShaderNodeTexImage')
d_tex.image = d_img
r_tex = selected_object.active_material.node_tree.nodes.new(type='ShaderNodeTexImage')
r_tex.image = r_img
n_tex = selected_object.active_material.node_tree.nodes.new(type='ShaderNodeTexImage')
n_tex.image = n_img

principled_bsdf_node = selected_object.active_material.node_tree.nodes.get("Principled BSDF")

selected_object.active_material.node_tree.links.new(principled_bsdf_node.inputs['Base Color'], d_tex.outputs['Color'])
selected_object.active_material.node_tree.links.new(principled_bsdf_node.inputs['Roughness'], r_tex.outputs['Color'])
selected_object.active_material.node_tree.links.new(principled_bsdf_node.inputs['Normal'], n_tex.outputs['Color'])

assert (material is not None and material.use_nodes), "No material or not node based"
linked_nodes = set()

for link in material.node_tree.links:
    linked_nodes.add(link.from_node)
    linked_nodes.add(link.to_node)
        
unlinked_nodes = set(material.node_tree.nodes) - linked_nodes
while unlinked_nodes:
    material.node_tree.nodes.remove(unlinked_nodes.pop())