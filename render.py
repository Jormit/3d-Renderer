import math
import numpy as np

def cross_product(v0, v1):
	return [v0[1]*v1[2] - v0[2]*v1[1], v0[2]*v1[0] - v0[0]*v1[2], v0[0]*v1[1] - v0[1]*v1[0]]

def dot_product(v0, v1):
	return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

def normalize(v):
	size = math.sqrt((v[0]**2) + (v[1]**2) + (v[2]**2))
	if (size == 0):
		return [0,0,0]
	return [v[0]/size, v[1]/size, v[2]/size]


def barycentric_coords(v0, v1, v2, P):
	# Compute baycentric scalars.
	cross = cross_product([v2[0]-v0[0], v1[0]-v0[0], v0[0]-P[0]], [v2[1]-v0[1], v1[1]-v0[1], v0[1]-P[1]])
	# Avoid division by 0.
	if (cross[2] < 1):
		return [-1, 1, 1]
		
	# Return the baycentric basis.
	return [1-(cross[0]+cross[1])/cross[2], cross[1]/cross[2], cross[0]/cross[2]]

def bounding_box(v0, v1, v2):
	min_x = min([v0[0], v1[0], v2[0]])
	max_x = max([v0[0], v1[0], v2[0]])
	min_y = min([v0[1], v1[1], v2[1]])
	max_y = max([v0[1], v1[1], v2[1]])

	return min_x, max_x, min_y, max_y

def scaled_vertices(face, vertices):
	v0 = [int((x + 1) * 300) for x in vertices[face[0][0]-1]]
	v1 = [int((x + 1) * 300) for x in vertices[face[1][0]-1]]
	v2 = [int((x + 1) * 300) for x in vertices[face[2][0]-1]]

	return v0, v1, v2

def scaled_texture_vertices(face, vertices, tex_dim):
	v0 = [int((x) * tex_dim[0]) for x in vertices[face[0][1]-1]]
	v1 = [int((x) * tex_dim[0]) for x in vertices[face[1][1]-1]]
	v2 = [int((x) * tex_dim[0]) for x in vertices[face[2][1]-1]]

	return v0, v1, v2

def render_line(pixels, start, end):		
	# Setup initial conditions
	x1, y1 = start
	x2, y2 = end
	dx = x2 - x1
	dy = y2 - y1

	# Determine how steep the line is
	is_steep = abs(dy) > abs(dx)

	# Rotate line
	if is_steep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2

	# Swap start and end points if necessary.
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		
	# Recalculate differentials
	dx = x2 - x1
	dy = y2 - y1

	# Calculate error
	err = int(dx / 2.0)
	ystep = 1 if y1 < y2 else -1

	# Iterate over bounding box generating points between start and end
	y = y1
	
	for x in range(x1, x2 + 1):
		coord = (y, x) if is_steep else (x, y)
		try:
			pixels[coord[0], coord[1]] = (255,255,255)
		except:
			pass
		err -= abs(dy)
		if err < 0:
			y += ystep
			err += dx
		

def draw_triangle(pixels, vertices, face):
	v0, v1, v2 = scaled_vertices(face, vertices)

	render_line(pixels, (v0[0], v0[1]), (v1[0], v1[1]))
	render_line(pixels, (v0[0], v0[1]), (v2[0], v2[1]))
	render_line(pixels, (v1[0], v1[1]), (v2[0], v2[1]))

def shade_triangle_texture(pixels, vertices, texture_vertices, face, z_buffer, texture_array, tex_dim):
	# We scale the vertices to the screen size first so everything
	# between -1 and 1 neatly maps onto the image.
	v0, v1, v2 = scaled_vertices(face, vertices)
	t0, t1, t2 = scaled_texture_vertices(face, texture_vertices, tex_dim)
	min_x, max_x, min_y, max_y = bounding_box(v0, v1, v2)

	# Compute a normal and normalize so it's length is 0. 
	# Dot product then gets the cos() of angle away from viewing direction which corresponds to intensity.
	normal = cross_product([v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]], [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]])
	normal = normalize(normal)
	intensity = dot_product([0,0,1], normal)

	# Backface culling.
	if (intensity < 0):
		return
	
	# We will loop through bounding box and calculate baycentric vectors (1 − u − v,u,v)
	# for each point. If any of the components are less than 0 we know that the point is
	# not in the triangle.
	for x in range(min_x, max_x + 1):
		for y in range(min_y, max_y + 1):
			barycentric_vec = barycentric_coords(v0, v2, v1, (x,y))		
			if any(t < 0 for t in barycentric_vec):				
				continue

			# Interpolate vertex point to texture point.
			tx = t0[0] + (t2[0]-t0[0])*barycentric_vec[1] + (t1[0]-t0[0])*barycentric_vec[2]
			ty = t0[1] + (t2[1]-t0[1])*barycentric_vec[1] + (t1[1]-t0[1])*barycentric_vec[2]

			# Calculate z-buffer depth.
			depth = int(v0[2] + (v2[2]-v0[2])*barycentric_vec[1] + (v1[2]-v0[2])*barycentric_vec[2])
			
			try:
				if z_buffer[x,y] < depth:
					# Set pixel to interpolated texture value.
					pixels[x, y] = (int(intensity * texture_array[tx, ty][0]), int(intensity * texture_array[tx, ty][1]), int(intensity * texture_array[tx, ty][2]))
					z_buffer[x,y] = depth
			except:
				pass

def shade_triangle(pixels, vertices, face, z_buffer):
	# We scale the vertices to the screen size first so everything
	# between -1 and 1 neatly maps onto the image.
	v0, v1, v2 = scaled_vertices(face, vertices)
	min_x, max_x, min_y, max_y = bounding_box(v0, v1, v2)

	# Compute a normal and normalize so it's length is 0. 
	# Dot product then gets the cos() of angle away from viewing direction which corresponds to intensity.
	normal = cross_product([v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]], [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]])
	normal = normalize(normal)
	intensity = dot_product([0,0,1], normal)
	
	if (intensity < 0):
		return

	color = int(intensity*255)

	# We will loop through bounding box and calculate baycentric vectors (1 − u − v,u,v)
	# for each point. If any of the components are less than 0 we know that the point is
	# not in the triangle.
	for x in range(min_x, max_x + 1):
		for y in range(min_y, max_y + 1):
			barycentric_vec = barycentric_coords(v0, v2, v1, (x,y))		
			if any(t < 0 for t in barycentric_vec):				
				continue

			# Calculate z-buffer depth.
			depth = int(v0[2] + (v2[2]-v0[2])*barycentric_vec[1] + (v1[2]-v0[2])*barycentric_vec[2])
			
			try:
				if z_buffer[x,y] < depth:
					pixels[x, y] = (color,color,color)
					z_buffer[x,y] = depth
			except:
				pass			

def render_shaded(pixels, vertices, texture_vertices, faces, texture_array, tex_dim):
	z_buffer = np.zeros((600,600))
	z_buffer.fill(-999)
	for face in faces:
		#shade_triangle_texture(pixels, vertices, texture_vertices, face, z_buffer, texture_array, tex_dim)
		shade_triangle(pixels, vertices, face, z_buffer)


# Interpolation Algorithms.
#print("x:{} xint:{}".format(x, v0[0] + (v2[0]-v0[0])*barycentric_vec[1] + (v1[0]-v0[0])*barycentric_vec[2]))
#print("y:{} yint:{}".format(y, v0[1] + (v2[1]-v0[1])*barycentric_vec[1] + (v1[1]-v0[1])*barycentric_vec[2]))
#print("z:{} zint:{}".format(y, int(v0[2] + (v2[2]-v0[2])*barycentric_vec[1] + (v1[2]-v0[2])*barycentric_vec[2])))	