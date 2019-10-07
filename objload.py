
def parse_obj(file):
	objFile = open(file, 'r')

	vertexList = []
	textureList = []
	faceList = []

	for line in objFile:
		if len(line) == 1:
			continue
		split = line.split()
		if split[0] == "#":
			continue
		elif split[0] == "v":
			vertexList.append(list(map(float, split[1:])))
		elif split[0] == "vt":
			textureList.append(list(map(float, split[1:])))
		elif split[0] == "f":
			faceList.append([list(map(int, split[1].split("/"))), list(map(int, split[2].split("/"))), list(map(int, split[3].split("/")))])
	objFile.close()

	print(str(len(faceList)) + " faces")
	print(str(len(vertexList)) + " vertices")


	return vertexList, textureList , faceList

