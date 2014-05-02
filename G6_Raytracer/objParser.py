# .obj parser
from math import sqrt

class Vertex(object):
	def __init__(self, newX, newY, newZ):
		self.x = newX
		self.y = newY
		self.z = newZ

class UVector(object):
	def __init__(self, newX, newY):
		self.x = newX
		self.y = newY

class Face(object):
	def __init__(self):
		self.vertices = []
		self.tex = ""
		self.surfNorm = Vertex(0,0,0)
	def add(self, v):
		self.vertices.append(v)

	def setT(self, t):
		self.tex = t

	def setSF(self, cx, cy, cz):
		self.surfNorm.x = cx
		self.surfNorm.y = cy
		self.surfNorm.z = cz

def crossproduct(v1, v2):
	cX = (v1.y*v2.z) - (v1.z*v2.y)
	cY = (v1.z*v2.x) - (v1.x*v2.z)
	cZ = (v1.x*v2.y) - (v1.y*v2.x)
	return cX, cY, cZ

# cx = aybz - azby
# cy = azbx - axbz
# cz = axby - aybx

def calculateNormals(allVerts, allFaces):
	print("Calculating Normals...")
	tempNorms = []
	for v1 in xrange(0,len(allVerts)):
		tempNeighbors = []
		for f in allFaces:
			for v2 in f.vertices:
				# if v1 found in face, add to tempNeighbors
				
				if (int(v2[0])-1 == int(v1)):
					tempNeighbors.append(f)

		#find average of all neighboring surface normals
		newX = 0
		newY = 0
		newZ = 0
		tempSize = len(tempNeighbors)

		for n in tempNeighbors:
			newX = newX + n.surfNorm.x 
			newY = newY + n.surfNorm.y
			newZ = newZ + n.surfNorm.z
		newX = newX/tempSize
		newY = newY/tempSize
		newZ = newZ/tempSize

		mag = sqrt((newX*newX) + (newY*newY) + (newZ*newZ))
		if(mag==0):
			mag = 1.0
		tempNorms.append(Vertex(newX/mag, newY/mag, newZ/mag))
		print v1
	return tempNorms

def main():
	uvVecs = []
	uvInd = []
	textureNames = {}
	vertices = []
	texturelist = []
	normals = []
	faces = []
	normInd = []
	outfile = raw_input("Enter your .inc filename (output): ")
	infile = raw_input("Enter a .obj filename (input): ")
	scale = float(raw_input("Enter a scalar: "))

	currentTex = ""
	#before parsing .obj file
	with open(infile, 'r') as fin:
		for line in fin:

			temp = line.split(" ")
			if(temp[0] == 'v'):
				#vertices.append(Vertex(float(temp[1])*scale, float(temp[2])*scale, float(temp[3])*scale))
				vertices.append(Vertex(float(temp[1])*scale, float(temp[2])*scale, float(temp[3])*scale))
				#fout.write("\t< "+temp[1]+", "+temp[2]+", "+(temp[3]).rstrip()+" >\n")

			elif(temp[0] == 'vn'):
				# comment this elif section to test normal generation
				normals.append(Vertex(float(temp[1])*1.0, float(temp[2])*1.0, float(temp[3])*1.0))
				
			elif(temp[0] == 'vt'):
				uvVecs.append(UVector(temp[1], temp[2]))

			elif(temp[0] == 'f'):
				faceList = []
				for p in xrange(1, len(temp)):
						faceList.append((temp[p].split("/")))
				if(len(faceList[0])==1):
					ni = False
					ui = False
				elif(len(faceList[0])==2):
					ni = False
					if(faceList[0][1] == ""):
						ui = False
					else:
						ui = True
				else:
					ni = True
					if(faceList[0][1] == ""):
						ui = False
					else:
						ui = True
				
				if(len(temp)-1>3):
					# print "LEN: " + str(len(temp[1:]))
					#triangulate non-triangle polygon
					p1 = 0
					p2 = 1
					p3 = 2
					for i in xrange(0,len(temp)-3):
						newFace = Face()
						newFace.add(faceList[p1])
						newFace.add(faceList[p2])
						newFace.add(faceList[p3])

						tempV1 = vertices[int(faceList[0][0])-1]
						tempV2 = vertices[int(faceList[1][0])-1]

						sX, sY, sZ = crossproduct(tempV1, tempV2)
						newFace.setT(currentTex)
						newFace.setSF(sX, sY, sZ)
						faces.append(newFace)
						temp = p3
						p3 = p3 + 1
						p2 = temp

				else:
					newFace = Face()
					for i in xrange(0,3):
						newFace.add(faceList[i])

					tempV1 = vertices[int(faceList[0][0])-1]
					tempV2 = vertices[int(faceList[1][0])-1]

					sX, sY, sZ = crossproduct(tempV1, tempV2)
					newFace.setT(currentTex)
					newFace.setSF(sX, sY, sZ)
					faces.append(newFace)

			elif(temp[0] == 'usemtl'):
				# texture
				currentTex = temp[1]
			elif(temp[0] == 'mtllib'):
				nextText = 0
				currT = ""
				# parse .mtl file for textures
				with open(temp[1].rstrip(), 'r') as mtlIn:
					for line in mtlIn:
						tempM = line.split(" ")
						if(tempM[0] == "newmtl"):
							ambient = []
							diffuse = []
							specular = []
							currT = tempM[1].rstrip()
							textureNames[currT] = nextText
							nextText = nextText + 1
							texturelist.append("\t\ttexture { finish { \n")

						if(tempM[0] == "Ka"):
							#ambient
							ambient.append(tempM[1])
							ambient.append(tempM[2])
							ambient.append(tempM[3])
							# amb = (float(ambient[0])+float(ambient[1])+float(ambient[2]))/3.0
							texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tambient " + str("amb")+"\n" 
							#texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tambient <" + ambient[0] + ", " + ambient[1] + ", " + ambient[2].rstrip()  + ">,\n" 
						
						if(tempM[0] == "Kd"):	
							#diffuse
							diffuse.append(tempM[1])
							diffuse.append(tempM[2])
							diffuse.append(tempM[3])
							# diff = (float(diffuse[0])+float(diffuse[1])+float(diffuse[2]))/3.0

							#texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tdiffuse <" + diffuse[0] + ", " + diffuse[1] + ", " + diffuse[2].rstrip()  + ">,\n" 
							texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tdiffuse " + str("diff")+"\n" 
						
						if(tempM[0] == "Ks"):	
							#specular
							specular.append(tempM[1])
							specular.append(tempM[2])
							specular.append(tempM[3])
							# spec = (float(specular[0])+float(specular[1])+float(specular[2]))/3.0

							#phong .75
      						#phong_size 25
							texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tphong " + str("spec")+"\n" 


						if(tempM[0] == "Ns"):	
							# # specular[0] = str(float(specular[0]) * float(tempM[1]))
							# # specular[1] = str(float(specular[1]) * float(tempM[1]))
							# # specular[2] = str(float(specular[2]) * float(tempM[1]))
							# # spec = (float(specular[0]) + float(specular[1]) + float(specular[2]))/3.0
							# texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tspecular " + str(specular[0])+"\n" 
							# #texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tspecular " + specular[0] + ", " + specular[1] + ", " + specular[2].rstrip()  + ">\n" 
							# texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\t}\n\t\t}"
							# # print (texturelist[textureNames[currT]])
							texturelist[textureNames[currT]] = texturelist[textureNames[currT]] + "\t\t\tphong_size " + tempM[1].rstrip()+"\n" 

				mtlIn.close();



	fin.close()

	if(len(normals)==0):
		normals = calculateNormals(vertices, faces)

	print textureNames
	fout = open(outfile, 'w')

	fout.write("// " +outfile+ "\n\n")
	fout.write("mesh2 {\n")

	fout.write("\tvertex_vectors {\n")
	fout.write("\t\t"+str(len(vertices))+",\n")
	counter = 0
	for eachV in vertices:
		if(counter == len(vertices)-1):
			fout.write("\t\t< "+str(eachV.x)+", "+str(eachV.y)+", "+(str(eachV.z)).rstrip()+" >\n")
		else:
			fout.write("\t\t< "+str(eachV.x)+", "+str(eachV.y)+", "+(str(eachV.z)).rstrip()+" >,\n")

		counter = counter + 1

	fout.write("\t}\n\n")

	fout.write("\tuv_vectors {\n")
	fout.write("\t\t"+str(len(uvVecs))+",\n")
	counter = 0
	for eachV in uvVecs:
		if(counter == len(vertices)-1):
			fout.write("\t\t< "+str(eachV.x)+", "+str(eachV.y).rstrip()+">\n")
		else:
			fout.write("\t\t< "+str(eachV.x)+", "+str(eachV.y).rstrip()+">,\n")

		counter = counter + 1

	fout.write("\t}\n\n")



	fout.write("\tnormal_vectors {\n")
	fout.write("\t\t"+str(len(normals))+",\n")
	counter = 0
	for eachN in normals:
		if(counter == len(normals)-1):
			fout.write("< "+str(eachN.x)+", "+str(eachN.y)+", "+(str(eachN.z)).rstrip()+" >\n")
		else:
			fout.write("\t\t< "+str(eachN.x)+", "+str(eachN.y)+", "+(str(eachN.z)).rstrip()+" >,\n")

		counter = counter + 1

	fout.write("\t}\n\n")



	fout.write("\ttexture_list {\n")
	fout.write("\t\t"+str(len(texturelist))+",\n")
	for i in xrange(0,len(texturelist)):
		fout.write(texturelist[i])
		if(i != 2):
			fout.write(",")
		fout.write("\n")
	fout.write("\t}\n\n")

	fout.write("\tface_indices {\n")
	fout.write("\t\t"+str(len(faces))+",\n")
	counter = 0
	c2 = 0
	for eachF in faces:
		print eachF.vertices
		# fout.write("\t\t< ")
		# c2 = 0
		# for v in eachF.vertices:
		
		# 	fout.write(str(int(v[0])-1))
		# 	if(c2 == len(eachF.vertices)-1):
		# 		if(len(textureNames)==0):
		# 			fout.write(" >,\n")
		# 		else:
		# 			fout.write(" >," + str(textureNames[eachF.tex])+ ",\n")
		# 	else:
		# 		fout.write(", ")
		# 	c2 = c2+1
		if(counter == len(faces)-1):
			if(len(texturelist)==0):
				fout.write("\t\t< "+str(int(eachF.vertices[0][0])-1)+", "+str(int(eachF.vertices[1][0])-1)+", "+(str(int(eachF.vertices[2][0])-1)).rstrip()+" >\n")
			else:
				fout.write("\t\t< "+str(int(eachF.vertices[0][0])-1)+", "+str(int(eachF.vertices[1][0])-1)+", "+(str(int(eachF.vertices[2][0])-1)).rstrip()+" >," + str(textureNames[eachF.tex.rstrip()])+ "\n")
		else:
			if(len(texturelist)==0):
				fout.write("\t\t< "+str(int(eachF.vertices[0][0])-1)+", "+str(int(eachF.vertices[1][0])-1)+", "+(str(int(eachF.vertices[2][0])-1)).rstrip()+" >,\n")
			else:
				fout.write("\t\t< "+str(int(eachF.vertices[0][0])-1)+", "+str(int(eachF.vertices[1][0])-1)+", "+(str(int(eachF.vertices[2][0])-1)).rstrip()+" >," + str(textureNames[eachF.tex.rstrip()])+ ",\n")

		counter = counter + 1

	fout.write("\t}\n\n")


	if(ni):
		fout.write("\tuv_indices {\n")
		fout.write("\t\t"+str(len(faces))+",\n")
		counter = 0
		c2 = 0
		for eachF in faces:
			
			if(counter == len(faces)-1):
				fout.write("\t\t< "+str(int(eachF.vertices[0][1])-1)+", "+str(int(eachF.vertices[1][1])-1)+", "+str(int(eachF.vertices[2][1])-1).rstrip()+" >\n")
			else:
				fout.write("\t\t< "+str(int(eachF.vertices[0][1])-1)+", "+str(int(eachF.vertices[1][1])-1)+", "+str(int(eachF.vertices[2][1])-1).rstrip()+" >,\n")

			counter = counter + 1

		fout.write("\t}\n\n")


	# fout.write("\tpigment { White }\n")
	if(ni):
		fout.write("\tnormal_indices {\n")
		fout.write("\t\t"+str(len(faces))+",\n")
		counter = 0
		c2 = 0
		for eachF in faces:
			
			if(counter == len(faces)-1):
				fout.write("\t\t< "+str(int(eachF.vertices[0][2])-1)+", "+str(int(eachF.vertices[1][2])-1)+", "+(str(int(eachF.vertices[2][2])-1)).rstrip()+" >\n")
			else:
				fout.write("\t\t< "+str(int(eachF.vertices[0][2])-1)+", "+str(int(eachF.vertices[1][2])-1)+", "+(str(int(eachF.vertices[2][2])-1)).rstrip()+" >,\n")

			counter = counter + 1

		fout.write("\t}\n\n")


	fout.write("}\n")

	fout.close()


if __name__ == '__main__':
	main()
