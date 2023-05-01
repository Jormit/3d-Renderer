from PIL import Image
import render as r
import objload as objload

width = 600
height = 600

# Create image buffer
img = Image.new("RGB", (width, height), "black")
pixels = img.load()

# Open texture
texture = Image.open("test files/african_head_diffuse.tga")
texture = texture.rotate(180)  # magic
tex_dim = texture.size
texture_array = texture.load()

# Open objF
vertices, texture_vertices, faces = objload.parse_obj("test files/african_head.obj")

# Render obj to buffer
r.render_shaded(pixels, vertices, texture_vertices, faces, texture_array, tex_dim)

# Save render.
img.save("out.bmp")
