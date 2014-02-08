import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class Program(object):
	def Main(args):
		N = Program.AskUserForN()
		B = Program.AskUserForB()
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(800, 600))
		if device == None:
			return 
		device.CursorControl.Visible = False
		camera = device.SceneManager.AddCameraSceneNodeFPS()
		camera.FarValue = 20000
		camera.Position = Vector3Df(-200)
		camera.Target = Vector3Df(0)
		batch = MeshBuffersBatch(device, N, B)
		while device.Run():
			device.VideoDriver.BeginScene()
			device.SceneManager.DrawAll()
			batch.Draw()
			device.VideoDriver.EndScene()
			device.SetWindowCaption("Fast static rendering - Irrlicht Lime - " + device.VideoDriver.Name + " | " 
				+ str(device.VideoDriver.FPS) + " fps | " 
				+ str(N * N * N) + " cubes  | " 
				+ str(device.VideoDriver.PrimitiveCountDrawn) + " primitives | " 
				+ str(Program.MemUsageText()) + " of physical memory used")
		batch.Drop()
		device.Drop()

	Main = staticmethod(Main)

	def AskUserForN():
		Console.WriteLine("Enter size of bounding cube side")
		Console.WriteLine(" (10 to render 10*10*10=1k cubes; 20 for 8k; 40 => 64k; 50 => 125k)")
		Console.WriteLine(" (typing less than 1 or more than 80 (512k) is not recommended): ")
		s = Console.ReadLine()
		return Convert.ToInt32(s)

	AskUserForN = staticmethod(AskUserForN)

	def AskUserForB():
		Console.WriteLine("What meshbuffers to use?")
		Console.WriteLine(" (1) split to 16-bit meshbuffers")
		Console.WriteLine(" (2) use single 32-bit meshbuffer ")
		k = Console.ReadKey()
		return k.KeyChar == '1'

	AskUserForB = staticmethod(AskUserForB)

	def AskUserForDriver():
		driverType = DriverType.Null
		Console.Write("Please select the driver you want for this example:\n" + " (a) OpenGL\n (b) Direct3D 9.0c\n (c) Direct3D 8.1\n" + " (d) Burning's Software Renderer\n (e) Software Renderer\n" + " (f) NullDevice\n (otherKey) exit\n\n")
		i = Console.ReadKey()
		if i.Key == ConsoleKey.A:
			driverType = DriverType.OpenGL
		elif i.Key == ConsoleKey.B:
			driverType = DriverType.Direct3D9
		elif i.Key == ConsoleKey.C:
			driverType = DriverType.Direct3D8
		elif i.Key == ConsoleKey.D:
			driverType = DriverType.BurningsVideo
		elif i.Key == ConsoleKey.E:
			driverType = DriverType.Software
		elif i.Key == ConsoleKey.F:
			driverType = DriverType.Null
		else:
			return (False, driverType)
		return (True, driverType)

	AskUserForDriver = staticmethod(AskUserForDriver)

	@classmethod
	def MemUsageText(cls):
		return str(System.Diagnostics.Process.GetCurrentProcess().WorkingSet64 / (1024 * 1024)) + " Mb"

class MeshBuffersBatch(object):
	def __init__(self, device, N, B):
		self._device = device
		self._material = Material()
		self._material.Lighting = False
		self._matrix = Matrix()
		self._mesh = Mesh.Create()
		if B:
			self.generateMultiple16bitMeshbuffers(N)
		else:
			self.generateSingle32BitMeshbuffer(N)
		self._mesh.RecalculateBoundingBox()
		device.Logger.Log("Collecting garbage...")
		GC.Collect()

	def Drop(self):
		self._mesh.Drop()

	def Draw(self):
		self._device.VideoDriver.SetTransform(TransformationState.World, self._matrix)
		self._device.VideoDriver.SetMaterial(self._material)
		for i in xrange(0,self._mesh.MeshBufferCount,1):
			self._device.VideoDriver.DrawMeshBuffer(self._mesh.GetMeshBuffer(i))

	def generateMultiple16bitMeshbuffers(self, N):
		vertices32bit, indices32bit = self.generateVerticesAndIndices(N)
		verticesChunk = List[Vertex3D]()
		indicesChunk = List[UInt16]()
		totalCubes = N * N * N
		indicesInCube = indices32bit.Length / totalCubes
		verticesInCube = vertices32bit.Length / totalCubes
		maximumVerticesPerChunk = UInt16.MaxValue # must not be more than 0xffff (because we use 16-bit indices)
		verticesIndexOffset = 0
		self._device.Logger.Log("Batching cubes into 16-bit meshbuffers...")
		for cubeIndex in xrange(0,totalCubes,1):
			# add vertices
			for i in xrange(0,verticesInCube,1):
				verticesChunk.Add(vertices32bit[cubeIndex * verticesInCube + i])
			# add indices
			for i in xrange(0,indicesInCube,1):
				indicesChunk.Add((indices32bit[cubeIndex * indicesInCube + i] - verticesIndexOffset)) # if this chunk is full
			if verticesChunk.Count + verticesInCube > maximumVerticesPerChunk or cubeIndex == totalCubes - 1: # or this is last cube
				# we create meshbuffer and add it to the main mesh
				mb = MeshBuffer.Create(VertexType.Standard, IndexType._16Bit)
				mb.SetHardwareMappingHint(HardwareMappingHint.Static, HardwareBufferType.VertexAndIndex)
				mb.Append(verticesChunk.ToArray(), indicesChunk.ToArray())
				mb.RecalculateBoundingBox()
				self._mesh.AddMeshBuffer(mb)
				mb.Drop()
				# clean up vertex and index chunks
				verticesIndexOffset += verticesChunk.Count
				verticesChunk = List[Vertex3D]()
				indicesChunk = List[UInt16]()
				self._device.Logger.Log(str(((cubeIndex + 1) * 100) / totalCubes) + "%: " + self._mesh.ToString() + ". ~" + str(Program.MemUsageText()))
				GC.Collect()

	def generateSingle32BitMeshbuffer(self, N):
		vertices32bit, indices32bit = self.generateVerticesAndIndices(N)
		mb = MeshBuffer.Create(VertexType.Standard, IndexType._32Bit)
		self._mesh.AddMeshBuffer(mb)
		mb.Drop()
		self._device.Logger.Log("Appending " + str(vertices32bit.Length) + " vertices and " + str(indices32bit.Length) + " indices to 32-bit meshbuffer...")
		mb.Append(vertices32bit, indices32bit)
		mb.SetHardwareMappingHint(HardwareMappingHint.Static, HardwareBufferType.VertexAndIndex)

	def generateVerticesAndIndices(self, N):
		""" <param name="N">Number of cubes in single dimension (e.g. total cubes for 20 is 20^3=8000)</param>"""
		cubeSide = 32
		# ask Irrlicht to generate cube mesh for us (we use it like a template)
		cubeMesh = self._device.SceneManager.GeometryCreator.CreateCubeMesh(Vector3Df(cubeSide))
		cubeIndices = cubeMesh.GetMeshBuffer(0).Indices
		cubeVertices = cubeMesh.GetMeshBuffer(0).Vertices
		cubeMesh.Drop()
		# generate cubes
		self._device.Logger.Log("Generating " + str(N * N * N) + " cubes...")
		vertices = Array.CreateInstance(Vertex3D, N * N * N * cubeVertices.Length)
		indices = Array.CreateInstance(UInt32, N * N * N * cubeIndices.Length)
		verticesIndex = 0
		indicesIndex = 0
		colorBase = (255 - cubeVertices.Length) / N
		cubePosOffset = Single(2) * cubeSide
		for i in xrange(0,N,1):
			for j in xrange(0,N,1):
				for k in xrange(0,N,1):
					# add indices
					firstfreeIndex = verticesIndex
					for l in xrange(0,cubeIndices.Length,1):
						indices[indicesIndex] = firstfreeIndex + cubeIndices[l]
						indicesIndex += 1
					# add vertices
					for l in xrange(0,cubeVertices.Length,1):
						v = Vertex3D(cubeVertices[l])
						v.Color = Color(i * colorBase + l, j * colorBase + l, k * colorBase + l)
						v.Position += Vector3Df(i, j, k) * cubePosOffset
						vertices[verticesIndex] = v
						verticesIndex += 1
			self._device.Logger.Log(str(((i + 1) * 100) / N) + "%: " + str((i + 1) * N * N) + " cubes has been generated. ~" + str(Program.MemUsageText()))
			if (i & 0xf) == 0xf:
				GC.Collect()
		return (vertices, indices)

Program.Main(Environment.GetCommandLineArgs()[2:])