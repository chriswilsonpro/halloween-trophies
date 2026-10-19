"""Parametric trophy base for Blender (bpy 5.x).

Builds a stepped plinth with gold trim, a front plaque, and an empty named
"ContentMount" on the top surface. Parent anything to the mount and it will
sit centered on the base. See the CUSTOM CONTENT section at the bottom.

Run with:  python3 trophy.py
"""

import math
import os

import bpy

# --------------------------------------------------------------------------
# Configuration (units are Blender units, treated as meters)
# --------------------------------------------------------------------------
PLAQUE_TEXT = "FIRST PLACE"     # set to "" for a blank plaque

LOWER_SIZE = 0.40               # width/depth of the bottom tier
LOWER_HEIGHT = 0.04
UPPER_SIZE = 0.32               # width/depth of the upper tier
UPPER_HEIGHT = 0.07
TRIM_HEIGHT = 0.008             # thin gold band between the tiers
TOP_RADIUS = 0.11               # gold disc the content stands on
TOP_HEIGHT = 0.02
BEVEL = 0.004                   # edge softening on all pieces

PLAQUE_WIDTH = 0.20
PLAQUE_HEIGHT = 0.04
PLAQUE_THICKNESS = 0.004

COLORS = {
    "gold": (0.95, 0.75, 0.15, 1.0),
    "base": (0.04, 0.04, 0.05, 1.0),
}

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trophy_base.blend")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def make_material(name, color, roughness, metallic):
    mat = bpy.data.materials.new(name=name)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def finish(obj, name, material, bevel=BEVEL):
    """Name the active object, apply scale, assign material, add a bevel."""
    obj.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def add_box(name, width, depth, height, z_bottom, material, y_offset=0.0, bevel=BEVEL):
    """Box centered on X/Y (plus y_offset), with its bottom face at z_bottom."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y_offset, z_bottom + height / 2))
    obj = bpy.context.active_object
    obj.scale = (width, depth, height)
    return finish(obj, name, material, bevel)


def add_disc(name, radius, height, z_bottom, material, bevel=BEVEL):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=height, vertices=64, location=(0, 0, z_bottom + height / 2)
    )
    return finish(bpy.context.active_object, name, material, bevel)


def add_plaque_text(text, y_front, z_center, material):
    """Flat text on the front face of the plaque, readable from -Y."""
    bpy.ops.object.text_add(
        location=(0, y_front, z_center), rotation=(math.radians(90), 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = "PlaqueText"
    obj.data.body = text
    obj.data.size = PLAQUE_HEIGHT * 0.45
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.extrude = 0.0005
    obj.data.materials.append(material)
    return obj


# --------------------------------------------------------------------------
# Build the base
# --------------------------------------------------------------------------
def build_trophy_base():
    """Create the base and return the ContentMount empty."""
    bpy.ops.wm.read_factory_settings(use_empty=True)

    base_mat = make_material("TrophyBase", COLORS["base"], roughness=0.35, metallic=0.1)
    gold_mat = make_material("TrophyGold", COLORS["gold"], roughness=0.2, metallic=1.0)

    z = 0.0
    add_box("LowerTier", LOWER_SIZE, LOWER_SIZE, LOWER_HEIGHT, z, base_mat)
    z += LOWER_HEIGHT

    add_box("Trim", UPPER_SIZE + 0.01, UPPER_SIZE + 0.01, TRIM_HEIGHT, z, gold_mat, bevel=0.002)
    z += TRIM_HEIGHT

    add_box("UpperTier", UPPER_SIZE, UPPER_SIZE, UPPER_HEIGHT, z, base_mat)
    upper_bottom = z
    z += UPPER_HEIGHT

    add_disc("TopDisc", TOP_RADIUS, TOP_HEIGHT, z, gold_mat)
    z += TOP_HEIGHT

    # Plaque sits slightly proud of the upper tier's front (-Y) face.
    plaque_z = upper_bottom + UPPER_HEIGHT / 2 - PLAQUE_HEIGHT / 2
    plaque_y = -(UPPER_SIZE / 2) - PLAQUE_THICKNESS / 2
    add_box(
        "Plaque", PLAQUE_WIDTH, PLAQUE_THICKNESS, PLAQUE_HEIGHT, plaque_z, gold_mat,
        y_offset=plaque_y, bevel=0.0008,
    )
    if PLAQUE_TEXT:
        add_plaque_text(
            PLAQUE_TEXT,
            y_front=plaque_y - PLAQUE_THICKNESS / 2 - 0.0003,
            z_center=plaque_z + PLAQUE_HEIGHT / 2,
            material=base_mat,
        )

    # Attachment point for your content: origin = center of the top surface.
    mount = bpy.data.objects.new("ContentMount", None)
    mount.empty_display_type = "PLAIN_AXES"
    mount.empty_display_size = 0.03
    mount.location = (0, 0, z)
    bpy.context.collection.objects.link(mount)
    return mount


# --------------------------------------------------------------------------
# CUSTOM CONTENT
# --------------------------------------------------------------------------
def add_content(mount):
    """Put your trophy topper here.

    Parent objects to `mount` and set their location AFTER parenting; the
    location is then relative to the mount (z=0 is the top of the base).
    Example (a sphere resting on the base):

        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08)
        orb = bpy.context.active_object
        orb.parent = mount
        orb.location = (0, 0, 0.08)
    """


if __name__ == "__main__":
    mount = build_trophy_base()
    add_content(mount)
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_PATH)
    print(f"Saved trophy to: {OUTPUT_PATH}")
