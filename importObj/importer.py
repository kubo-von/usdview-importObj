print("Imported obj importer!")
from pxr.Usdviewq.qt import QtWidgets, QtCore
from pxr import Usd, UsdGeom, Kind, Sdf

def importObj(usdviewApi):
	
	filepath = QtWidgets.QFileDialog.getOpenFileName(usdviewApi.qMainWindow, 'Import file', '',".obj files (*.obj *.OBJ)")[0]
	stage = usdviewApi.stage
	file = open(filepath, "r")
	root = filepath.split("/")[-1].split(".")[0]

	#OBJobjects = file.read().split("o ")

	points =[]
	normals =[]
	facesVcount =[]
	faces =[]
	faceUvIndexes =[]
	uvVtxs =[]
	uvs = []
	 
	for line in file.readlines():
		#point positions
		if line.startswith("v "): 
			v = line.replace("v ","").strip().split(" ")
			points.append((float(v[0]),float(v[1]),float(v[2])))
		#normals
		if line.startswith("vn "): 
			n = line.replace("vn ","").strip().split(" ")
			normals.append((float(n[0]),float(n[1]),float(n[2])))
		#faces
		if line.startswith("f "):
			facedata = line.replace("f ","").strip().split(" ")
			facesVcount.append(len(facedata))
			faceVtxs = []
			for i in facedata:
				faces.append(int(i.split("/")[0])-1)
				faceUvIndexes.append(int(i.split("/")[1])-1)
		#uv vertextes
		if line.startswith("vt "): 
			uv = line.replace("vt ","").strip().split(" ")
			uvVtxs.append((float(uv[0]),float(uv[1])))

	#get uv vertexes by each face
	for i in faceUvIndexes:
		uvs.append(uvVtxs[i])

	"""
	#debug
	print(points)
	print(normals)
	print(facesVcount)
	print(faces)
	print(uvs)

	print len(points)
	print len(normals)
	print len(facesVcount)
	print len(faces)
	print len(uvs)
	"""

	modelRoot = UsdGeom.Xform.Define(stage, "/"+root)
	Usd.ModelAPI(modelRoot).SetKind(Kind.Tokens.component)
	mesh = UsdGeom.Mesh.Define(stage, "/"+root+"/mesh_0")


	mesh.CreateSubdivisionSchemeAttr("none") #Valid values are "catmullClark" (the default), "loop", "bilinear", and "none" 
	#create points and faces
	mesh.CreatePointsAttr(points)
	mesh.CreateFaceVertexCountsAttr(facesVcount)
	mesh.CreateFaceVertexIndicesAttr(faces)

	#add normals
	normalPrimvar = mesh.CreatePrimvar("normal", 
	                                    Sdf.ValueTypeNames.Normal3fArray, 
	                                    UsdGeom.Tokens.faceVarying)
	normalPrimvar.Set(normals)

	#bounds
	# mesh.CreateExtentAttr([(-1, -1+i, 0), (1, 1+i, 0)])

	#add uv coordinates
	texCoords = mesh.CreatePrimvar("st", 
	                                    Sdf.ValueTypeNames.TexCoord2fArray, 
	                                    UsdGeom.Tokens.faceVarying)
	texCoords.Set(uvs)

	"""
	#add Material -WORK IN PROGRESS
	texturepath = "/media/colin/Black/dev/usd/uvs.png"

	material = UsdShade.Material.Define(stage, '/TexModel/boardMat')
	pbrShader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader')
	pbrShader.CreateIdAttr("UsdPreviewSurface")
	pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
	pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

	material.CreateSurfaceOutput().ConnectToSource(pbrShader, "surface")

	stReader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/stReader')
	stReader.CreateIdAttr('UsdPrimvarReader_float2')

	diffuseTextureSampler = UsdShade.Shader.Define(stage,'/TexModel/boardMat/diffuseTexture')
	diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
	diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(texturepath)
	diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
	diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
	pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')

	stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
	stInput.Set('st')

	stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)


	UsdShade.MaterialBindingAPI(mesh).Bind(material)
	"""