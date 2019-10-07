from PIL import Image
import render as r
import objload as objload

width = 600
height = 600

# Create a new black image and get a pixel map.
img = Image.new( 'RGB', (width,height), "black") 
pixels = img.load()

# Get diffuse texture.
texture = Image.open("head_diffuse.tga")
texture = texture.rotate(180) # magic
tex_dim = texture.size
texture_array = texture.load()

# Parse the obj file into vertices and faces.
vertices, texture_vertices , faces = objload.parse_obj("head.obj")

# Render obj to array. 
r.render_shaded(pixels, vertices, texture_vertices , faces, texture_array, tex_dim)

# Save render.
img.save("renders/out.bmp")