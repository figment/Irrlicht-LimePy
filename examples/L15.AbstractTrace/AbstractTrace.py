import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Video import *
from System.Diagnostics import *
from System.Threading import *

class AbstractTrace(object): # defines size of the grid: GridDim x GridDim; if we would place cube into each cell, that would be also cube count for single grid (but actual cube count is much much less) # defines trace length and total number of distinct meshes # maximum is 65536 div 8 (where 8 is number of vertices per cube); we could pick 8000+ and reduce number of meshbuffers, but on some video cards fully loaded meshbuffers works much slower # actual state of the grid # previous state of the grid; needed for generating Conway's Game of Life algorithm (see implementation in meshGeneratorThread_generateGrid()) # here we store number of "1"s in grid array; we count them while generating next step and cache this value, so we don't need to calc again when needed # actual generation of the grid; this number increases each time grid regenerates in meshGeneratorThread_generateGrid(); we use this value when picking next free GridLayer in Step() # color of the cubes; we could change it over time giving nice transitions; we even can give each single cube different color: if you want to implement this - simply add color to Vertex3D constructors and remove SetVertexColors() call of MeshManipulator at the end of mesh generation in meshGeneratorThread_generateMesh() # material used to draw all grid layers; if you want separate material for each GridLayer - simple move this material definition inside GridLayer class and use that value in Draw() for each GridLayer
	GridDim = 500
	GridLayerCount = 200
	CubeSize = 10
	maxCubesPerBuffer = 3600
	def __init__(self, device):
		self._grid = [[0 for x in xrange(0,AbstractTrace.GridDim,1)] for x in xrange(0,AbstractTrace.GridDim,1)]
		self._gridPrev = [[0 for x in xrange(0,AbstractTrace.GridDim,1)] for x in xrange(0,AbstractTrace.GridDim,1)]
		self._gridCubeCount = 0
		self._gridGeneration = 0
		self._cubeColor = Color(50, 150, 250, 25)
		self._cubeMaterial = Material()
		self._layers = [ AbstractTrace.GridLayer() for x in xrange(0,AbstractTrace.GridLayerCount,1)]
		self._meshGeneratorThread = None
		self._device = device
		device.Grab()
		self._cubeMaterial.Type = MaterialType.TransparentVertexAlpha
		self._cubeMaterial.Lighting = False

	def Init(self):
		self._gridGeneration = 0
		self._gridCubeCount = 0
		r = Random()
		for row in self._grid:
			for j in xrange(0,500,1):
				if r.Next(100) < 50:
					row[j] = 1
					self._gridCubeCount += 1
				else:
					row[j] = 0

	def Step(self):
		if self._meshGeneratorThread != None:
			return 
		def ParameterizedThreadStart_75_83(i):
			self.meshGeneratorThread_generateGrid()
			self.meshGeneratorThread_generateMesh(i)
			self._meshGeneratorThread = None

		self._meshGeneratorThread = Thread(ParameterizedThreadStart(ParameterizedThreadStart_75_83))
		# search for layer with oldest generation
		gmin = int.MaxValue
		igmin = -1
		for i,layer in enumerate(self._layers):
			if layer.Generation < gmin:
				gmin = layer.Generation
				igmin = i
		# start mesh generation
		self._layers[igmin].MeshIsReady = False
		self._meshGeneratorThread.Start(igmin)

	def meshGeneratorThread_generateGrid(self):
		self._gridGeneration += 1
		self._gridCubeCount = 0
		t = self._grid
		self._grid = self._gridPrev
		self._gridPrev = t
		# process grid with Conway's Game of Life algorithm (details: http://en.wikipedia.org/wiki/Conway's_Game_of_Life)
		for i in xrange(0,500,1):
			for j in xrange(0,500,1):
				# calc number of neighbours
				n = 0
				il = i - 1 if i > 0 else 500 - 1
				ir = i + 1 if i < 500 - 1 else 0
				jt = j - 1 if j > 0 else 500 - 1
				jb = j + 1 if j < 500 - 1 else 0
				if self._gridPrev[il][j] == 1:
					n += 1 # left
				if self._gridPrev[ir][j] == 1:
					n += 1 # right
				if self._gridPrev[i][jt] == 1:
					n += 1 # top
				if self._gridPrev[i][jb] == 1:
					n += 1 # bottom
				if self._gridPrev[il][jt] == 1:
					n += 1 # left-top
				if self._gridPrev[il][jb] == 1:
					n += 1 # left-bottom
				if self._gridPrev[ir][jt] == 1:
					n += 1 # right-top
				if self._gridPrev[ir][jb] == 1:
					n += 1 # right-bottom
				# update cell
				if (n == 2 and self._gridPrev[i][j] == 1) or (n == 3 and self._gridPrev[i][j] == 0):
					self._grid[i][j] = 1
					self._gridCubeCount += 1
				else:
					self._grid[i][j] = 0

	def meshGeneratorThread_generateMesh(self, layerIndex):
		l = self._layers[layerIndex]
		if l.Mesh != None:
			l.Mesh.Drop()
		l.Mesh = Mesh.Create()
		if self._gridCubeCount > 0:
			cubeVerts = None
			cubeInds = None
			cubeIndex = 3600 # this way we force buffers to be recreated at next new cube
			totalCubesAdded = 0
			baseX = -(10 * 500) / 2
			baseZ = -(10 * 500) / 2
			for i in xrange(0,500,1):
				for j in xrange(0,500,1):
					if self._grid[i][j] == 0:
						continue
					# check if current buffer is out of room, if so make a mesh buffer and attach it to the gridMesh and init next cubeVerts&Inds
					if cubeIndex == 3600:
						if cubeVerts != None and cubeInds != None:
							b = MeshBuffer.Create(VertexType.Standard, IndexType._16Bit)
							b.Append(cubeVerts, cubeInds)
							l.Mesh.AddMeshBuffer(b)
							b.Drop()
							totalCubesAdded += cubeIndex
						cubeCount = self._gridCubeCount - totalCubesAdded
						if cubeCount > 3600:
							cubeCount = 3600
						cubeIndex = 0
						cubeVerts = Array.CreateInstance(Vertex3D, cubeCount * 8) # 8 verts per cube
						cubeInds = Array.CreateInstance(UInt16, cubeCount * 3 * 2 * 6) # 3 indices per triangle; 2 triangles per face; 6 faces per cube
					# build the cube and add it
					# note: we build 8 vertices cube because we don't need to texture it; if you want to change that (to use texture instead of vertex colors) - you need to build 12 vertices cube and initialize UV coords
					x = baseX + i * 10
					y = 0
					z = baseZ + j * 10
					iv = cubeIndex * 8
					cubeVerts[iv + 0] = Vertex3D(x, y, z)
					cubeVerts[iv + 1] = Vertex3D(x + 10, y, z)
					cubeVerts[iv + 2] = Vertex3D(x + 10, y + 10, z)
					cubeVerts[iv + 3] = Vertex3D(x, y + 10, z)
					cubeVerts[iv + 4] = Vertex3D(x, y, z + 10)
					cubeVerts[iv + 5] = Vertex3D(x + 10, y, z + 10)
					cubeVerts[iv + 6] = Vertex3D(x + 10, y + 10, z + 10)
					cubeVerts[iv + 7] = Vertex3D(x, y + 10, z + 10)
					ii = cubeIndex * 3 * 2 * 6
					# top
					cubeInds[ii + 0] = (iv + 3)
					cubeInds[ii + 1] = (iv + 7)
					cubeInds[ii + 2] = (iv + 6)
					cubeInds[ii + 3] = (iv + 3)
					cubeInds[ii + 4] = (iv + 6)
					cubeInds[ii + 5] = (iv + 2)
					# front
					cubeInds[ii + 6] = (iv + 0)
					cubeInds[ii + 7] = (iv + 3)
					cubeInds[ii + 8] = (iv + 2)
					cubeInds[ii + 9] = (iv + 0)
					cubeInds[ii + 10] = (iv + 2)
					cubeInds[ii + 11] = (iv + 1)
					# right
					cubeInds[ii + 12] = (iv + 1)
					cubeInds[ii + 13] = (iv + 2)
					cubeInds[ii + 14] = (iv + 6)
					cubeInds[ii + 15] = (iv + 1)
					cubeInds[ii + 16] = (iv + 6)
					cubeInds[ii + 17] = (iv + 5)
					# left
					cubeInds[ii + 18] = (iv + 0)
					cubeInds[ii + 19] = (iv + 4)
					cubeInds[ii + 20] = (iv + 7)
					cubeInds[ii + 21] = (iv + 0)
					cubeInds[ii + 22] = (iv + 7)
					cubeInds[ii + 23] = (iv + 3)
					# back
					cubeInds[ii + 24] = (iv + 4)
					cubeInds[ii + 25] = (iv + 5)
					cubeInds[ii + 26] = (iv + 6)
					cubeInds[ii + 27] = (iv + 4)
					cubeInds[ii + 28] = (iv + 6)
					cubeInds[ii + 29] = (iv + 7)
					# bottom
					cubeInds[ii + 30] = (iv + 0)
					cubeInds[ii + 31] = (iv + 1)
					cubeInds[ii + 32] = (iv + 5)
					cubeInds[ii + 33] = (iv + 0)
					cubeInds[ii + 34] = (iv + 5)
					cubeInds[ii + 35] = (iv + 4)
					cubeIndex += 1
			if cubeIndex > 0:
				b = MeshBuffer.Create(VertexType.Standard, IndexType._16Bit)
				b.Append(cubeVerts, cubeInds)
				l.Mesh.AddMeshBuffer(b)
				b.Drop()
			self._device.SceneManager.MeshManipulator.SetVertexColors(l.Mesh, self._cubeColor)
		l.Transform.Rotation = Vector3Df(self._gridGeneration * Single(0.93), self._gridGeneration * Single(0.81), self._gridGeneration * Single(0.69))
		l.Generation = self._gridGeneration
		l.CubeCount = self._gridCubeCount
		l.MeshIsReady = True

	def Draw(self, debugDrawGenerator=False):
		driver = self._device.VideoDriver
		# draw
		driver.SetMaterial(self._cubeMaterial)
		for l in self._layers:
			if not l.MeshIsReady:
				continue
			driver.SetTransform(TransformationState.World, l.Transform)
			for mb in l.Mesh.MeshBuffers:
				driver.DrawMeshBuffer(mb)
		# draw debug info
		if debugDrawGenerator:
			for l in self._layers:
				if not l.MeshIsReady:
					continue
				if l.Generation == self._gridGeneration - 1:
					driver.SetMaterial(Material.IdentityRedWireframe)
					driver.SetTransform(TransformationState.World, l.Transform)
					c = Color.OpaqueRed
					x1 = -(10 * 500) / 2
					z1 = -(10 * 500) / 2
					x2 = x1 + (500 - 1) * 10
					z2 = z1 + (500 - 1) * 10
					driver.Draw3DLine(Line3Df(x1, 0, z1, x2, 0, z1), c)
					driver.Draw3DLine(Line3Df(x1, 0, z1, x1, 0, z2), c)
					driver.Draw3DLine(Line3Df(x2, 0, z1, x2, 0, z2), c)
					driver.Draw3DLine(Line3Df(x1, 0, z2, x2, 0, z2), c)
					for mb in l.Mesh.MeshBuffers:
						driver.DrawMeshBuffer(mb)
					break

	def Drop(self):
		if self._meshGeneratorThread != None:
			self._meshGeneratorThread.Join()
		self._device.Drop()

	def GetTotalCubeCount(self):
		c = 0
		for l in self._layers:
			if not l.MeshIsReady:
				continue
			c += l.CubeCount
		return c

	class GridLayer(object):
		def __init__(self):
			self.MeshIsReady = False
			self.Generation = -1
			self.CubeCount = -1
			self.Mesh = None
			self.Transform = Matrix()
			pass
		