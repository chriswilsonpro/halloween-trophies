# Halloween Costume Contest Trophies

3D-modeled trophies for our company Halloween costume contest, built in
Blender. Every trophy shares the same parametric base (a stepped black plinth
with gold trim and a front plaque) and is topped with a Halloween-themed
figure.

## The Trophies

| # | Award | Topper | Blender file |
|---|-------|--------|--------------|
| 1 | **Best Costume** | Pumpkin with a hat | `best-costume.blend1` |
| 2 | **Most Creative** | Brain | `creative-trophy.blend1` |
| 3 | **Funniest** | Skull | `funniest-trophy.blend1` |
| 4 | **Scariest** | Ghost | `scariest-trophy.blend1` |
| 5 | **Cutest** | _TBD_ | `cutest-trophy.blend1` |
| 6 | **Surprise** | _TBD_ | `suprise-trophy.blend1` |

### Best Costume - Pumpkin with a Hat
Awarded to the overall best costume of the night.

### Most Creative - Brain
Awarded to the most original, inventive, or clever costume.

### Funniest - Skull
Awarded to the costume that got the most laughs.

### Scariest - Ghost
Awarded to the costume that gave the most chills.

### Cutest - _TBD_
Awarded to the cutest costume.

### Surprise - _TBD_
A wildcard award for a costume that doesn't fit the other categories.

## Project Structure

| File | Description |
|------|-------------|
| `trophy.py` | Script that generates the shared trophy base and a `ContentMount` empty where each topper is attached |
| `trophy_base.blend` | Output of `trophy.py` (the blank base) |
| `halloween_costume_trophy.blend` | Combined trophy scene |
| `*-trophy.blend`, `best-costume.blend` | Per-award trophy files (`.blend1` files are Blender's automatic backups) |
| `requirements.txt` | Python dependencies (notably `bpy`) |

## Getting Started

### Requirements
- Python 3.11 or newer (required by `bpy` 5.x)
- [Blender](https://www.blender.org/) (to open and edit the `.blend` files)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Generate the trophy base

```bash
python3 trophy.py
```

This writes `trophy_base.blend` next to the script.

### Customizing a trophy

Edit the configuration at the top of `trophy.py`:

- `PLAQUE_TEXT`: the text on the front plaque (for example `"BEST COSTUME"`). Set it to `""` for a blank plaque.
- Size constants such as `LOWER_SIZE`, `UPPER_SIZE`, and `TOP_RADIUS`: the dimensions of the base.
- `COLORS`: the base and gold trim colors.

To add a topper, fill in `add_content(mount)` in `trophy.py`. Parent your
objects to the `ContentMount` empty and set their location after parenting.
`z = 0` is the top of the base.

```python
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08)
orb = bpy.context.active_object
orb.parent = mount
orb.location = (0, 0, 0.08)
```
