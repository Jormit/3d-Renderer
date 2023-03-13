## 3d Renderer
This is a simple 3d renderer written in python that outputs to a bitmap file. The entirety of the renderer is written with no graphics libraries. Pillow is used for handling image creation and saving. Can render wireframe, shaded and textured images from .obj and .tga files. Based loosely on https://github.com/ssloy/tinyrenderer. 

## Example
Render of [this obj](https://github.com/ssloy/tinyrenderer/blob/f6fecb7ad493264ecd15e230411bfb1cca539a12/obj/african_head.obj). 
### UV textured.
![](renders/shaded.bmp)
### Flat shaded.
![](renders/out.bmp) 
### Wireframe.
![](renders/wire.bmp) 
 
