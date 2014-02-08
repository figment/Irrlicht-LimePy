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
import IrrlichtLime.Scene

class HeightMap(object):
	""" <summary>
	 A simple class for representing heightmaps.
	 </summary>
	"""
	
	class HeightFunc(object):
		""" <summary>
		 The type of the function which generate the heightmap.
		 </summary>
		"""
		EggBox = 0
		MoreSine = EggBox + 1
		JustExp = MoreSine + 1
	
	# <summary>
	# An interesting sample function :-)
	# </summary>
	# <summary>
	# A rather dumb sine function :-/
	# </summary>
	# <summary>
	# A simple function
	# </summary>
	def get_Width(self):
		return self._width

	def set_Width(self, value):
		self._width = value

	Width = property(fget=get_Width, fset=set_Width)

	def get_Height(self):
		return self._height

	def set_Height(self, value):
		self._height = value

	Height = property(fget=get_Height, fset=set_Height)

	def __init__(self, w, h):
		""" <summary>
		 Creates new instance with given width and height. 
		 </summary>
		"""
		self._width = UInt16()
		self._height = UInt16()
		self.Width = w
		self.Height = h
		self._scale = Math.Sqrt((w * w + h * h))
		self._data = Array.CreateInstance(Single, w * h)

	def GetHeight(self, x, y):
		""" <summary>
		 Gets height value for specified coordinates.
		 </summary>
		"""
		if x < 0 or x > self.Width or y < 0 or y > self.Height:
			raise ArgumentOutOfRangeException()
		return self._data[x + self.Width * y]

	def Generate(self, func):
		""" <summary>
		 Fills the heightmap with values generated from given function.
		 </summary>
		"""
		i = 0
		for y in xrange(0,self.Height,1):
			for x in xrange(0,self.Width,1):
				self._data[i] = self.calculate(func, x, y)
				i += 1

	def GetNormal(self, x, y, s):
		""" <summary>
		 Gets the normal vector at (x, y) to be the cross product of the vectors between the adjacent
		 points in the horizontal and vertical directions.
		 </summary>
		"""
		if x < 0 or x > self.Width or y < 0 or y > self.Height:
			raise ArgumentOutOfRangeException()
		zc = self.GetHeight(x, y)
		if x == 0:
			zr = self.GetHeight(x + 1, y)
			zl = zc + zc - zr
		elif x == self.Width - 1:
			zl = self.GetHeight(x - 1, y)
			zr = zc + zc - zl
		else:
			zr = self.GetHeight(x + 1, y)
			zl = self.GetHeight(x - 1, y)
		if y == 0:
			zd = self.GetHeight(x, y + 1)
			zu = zc + zc - zd
		elif y == self.Height - 1:
			zu = self.GetHeight(x, y - 1)
			zd = zc + zc - zu
		else:
			zd = self.GetHeight(x, y + 1)
			zu = self.GetHeight(x, y - 1)
		return Vector3Df(self._scale * 2 * (zl - zr), 4, self._scale * 2 * (zd - zu)).Normalize()

	def calculate(self, func, x, y):
		""" <summary>
		 Calculates single height value for specified function and coordinates.
		 </summary>
		"""
		xu = x - self.Width / Single(2)
		yu = y - self.Height / Single(2)
		if func == HeightMap.HeightFunc.EggBox:
			r = Single(4) * Math.Sqrt((xu * xu + yu * yu)) / self._scale
			z = Math.Exp(-r * 2) * (Math.Cos(Single(0.2) * xu) + Math.Cos(Single(0.2) * yu))
			o = (Single(0.32) + Single(0.25) * z)
			return o
		elif func == HeightMap.HeightFunc.MoreSine:
			xf = Single(0.3) * xu / self._scale
			yf = Single(12) * yu / self._scale
			z = Math.Sin(xf * xf + yf) * Math.Sin(xf + yf * yf)
			o = (Single(0.25) + Single(0.25) * z)
			return o
		elif func == HeightMap.HeightFunc.JustExp:
			xf = 6 * xu / self._scale
			yf = 6 * yu / self._scale
			z = xf * xf + yf * yf
			o = (Single(0.3) * z * Math.Cos(xf * yf))
			return o
		else:
			raise ArgumentException("Unexpected height function value: " + func.ToString())

class HeightMesh(object):
	""" <summary>
	 Generates a mesh from a heightmap.
	 </summary>
	"""
	class ColorFunc(object):
		""" <summary>
		 Set of functions which can be used for coloring the nodes while creating the mesh.
		 </summary>
		"""
		GreyscaleBasedOnTheHeight = 0
		CoordinateInterpolation = GreyscaleBasedOnTheHeight + 1
		PureWhite = CoordinateInterpolation + 1

	def get_Mesh(self):
		return self._mesh

	def set_Mesh(self, value):
		self._mesh = value

	Mesh = property(fget=get_Mesh, fset=set_Mesh)

	def __init__(self):
		self._mesh = None
		self._width = 0
		self._height = 0
		self._scale = Single(1)
		self.Mesh = IrrlichtLime.Scene.Mesh.Create()

	def Drop(self):
		self.Mesh.Drop()

	def Init(self, driver, map, s, cf):
		""" <summary>
		 Initializes mesh with new value.
		 Unless the heightmap is small, it won't all fit into a single MeshBuffer.
		 This function chops it into pieces and generates a buffer from each one.
		 </summary>
		"""
		self._width = map.Width
		self._height = map.Height
		self._scale = s
		if self.Mesh.MeshBufferCount > 0:
			self.Mesh.RemoveMeshBuffer(0, self.Mesh.MeshBufferCount)
		sw = 0xffff / (self._height + 1) # maximum vertices per meshbuffer
		for y0 in xrange(0,self._height,sw):
			y1 = y0 + sw
			if y1 >= self._height:
				y1 = self._height - 1 # the last one might be narrower
			self.addStrip(map, cf, y0, y1)
		self.Mesh.RecalculateBoundingBox()

	def addStrip(self, map, cf, y0, y1):
		""" <summary>
		 Generates a MeshBuffer which represents all the vertices and indices for values of y
		 between y0 and y1, and add it to the mesh.
		 </summary>
		"""
		vertices = Array.CreateInstance(Vertex3D, (y1 - y0 + 1) * self._width)
		indices = Array.CreateInstance(UInt16, (y1 - y0) * (self._width - 1) * 6) # "6" is a number of indices in 2 triangles (which forms a quad)
		# calculate vertices
		i = 0
		y = y0
		while y <= y1:
			for x in xrange(0,self._width,1):
				z = map.GetHeight(x, y)
				xf = x / self._width
				yf = y / self._height # position # normal # color
				vertices[i] = Vertex3D(Vector3Df(x, self._scale * z, y), map.GetNormal(x, y, self._scale), self.calculate(cf, xf, yf, z), Vector2Df(xf, yf))
				i += 1
			y += 1 # tcoords
		# calculate indices
		i = 0
		for y in xrange(y0,y1,1):
			for x in xrange(0,self._width - 1,1):
				n = (y - y0) * self._width + x
				indices[i] = n
				i += 1
				indices[i] = (n + self._width)
				i += 1
				indices[i] = (n + self._width + 1)
				i += 1
				indices[i] = (n + self._width + 1)
				i += 1
				indices[i] = (n + 1)
				i += 1
				indices[i] = n
				i += 1
		# append calculated verices and indices to mesh buffer
		buf = MeshBuffer.Create(VertexType.Standard, IndexType._16Bit) # create new buffer
		self.Mesh.AddMeshBuffer(buf)
		buf.Append(vertices, indices)
		buf.RecalculateBoundingBox()
		buf.Drop()

	def calculate(self, cf, x, y, z):
		""" <summary>
		 Calculates single color value for given coordinates.
		 </summary>
		"""
		if cf == HeightMesh.ColorFunc.GreyscaleBasedOnTheHeight:
			n = (Single(255) * z)
			return Color(n, n, n)
		elif cf == HeightMesh.ColorFunc.CoordinateInterpolation:
			return Color(128 + (Single(127) * x), 128 + (Single(127) * y), 255)
		elif cf == HeightMesh.ColorFunc.PureWhite:
			return Color.OpaqueWhite
		else:
			raise ArgumentException("Unexpected color function value: " + cf.ToString())

class Program(object):
	# Generate starting height map and mesh
	# Add the mesh to the scene graph
	# Add light (just for nice effects)
	# Add camera
	# Main loop
	# Clean up
	KeyIsDown = Dictionary[KeyCode, Boolean]()
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(800, 600))
		if device == None:
			return 
		device.OnEvent += Program.device_OnEvent
		device.SetWindowCaption("Mesh handling - Irrlicht Lime")
		driver = device.VideoDriver
		scene = device.SceneManager
		map = HeightMap(255, 255)
		map.Generate(HeightMap.HeightFunc.EggBox)
		mesh = HeightMesh()
		mesh.Init(driver, map, Single(50), HeightMesh.ColorFunc.GreyscaleBasedOnTheHeight)
		meshnode = scene.AddMeshSceneNode(mesh.Mesh)
		meshnode.SetMaterialFlag(MaterialFlag.BackFaceCulling, False)
		lightnode = scene.AddLightSceneNode(None, Vector3Df(0, 100, 0), Colorf(1, 1, 1), Single(500))
		anim = scene.CreateFlyCircleAnimator(Vector3Df(0, 150, 0), Single(250))
		lightnode.AddAnimator(anim)
		anim.Drop()
		camera = scene.AddCameraSceneNodeFPS()
		camera.Position = Vector3Df(-Single(20), Single(100), -Single(20))
		camera.Target = Vector3Df(Single(200), -Single(100), Single(200))
		camera.FarValue = Single(20000)
		while device.Run():
			if not device.WindowActive:
				device.Sleep(100)
				continue
			if Program.IsKeyDown(KeyCode.KeyW):
				meshnode.SetMaterialFlag(MaterialFlag.Wireframe, not meshnode.GetMaterial(0).Wireframe)
			elif Program.IsKeyDown(KeyCode.Key1):
				map.Generate(HeightMap.HeightFunc.EggBox)
				mesh.Init(driver, map, Single(50), HeightMesh.ColorFunc.GreyscaleBasedOnTheHeight)
			elif Program.IsKeyDown(KeyCode.Key2):
				map.Generate(HeightMap.HeightFunc.MoreSine)
				mesh.Init(driver, map, Single(50), HeightMesh.ColorFunc.CoordinateInterpolation)
			elif Program.IsKeyDown(KeyCode.Key3):
				map.Generate(HeightMap.HeightFunc.JustExp)
				mesh.Init(driver, map, Single(50), HeightMesh.ColorFunc.CoordinateInterpolation)
			driver.BeginScene()
			scene.DrawAll()
			driver.EndScene()
		mesh.Drop()
		device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(e):
		if e.Type == EventType.Key:
			if Program.KeyIsDown.ContainsKey(e.Key.Key):
				Program.KeyIsDown[e.Key.Key] = e.Key.PressedDown
			else:
				Program.KeyIsDown.Add(e.Key.Key, e.Key.PressedDown)
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def IsKeyDown(keyCode):
		return Program.KeyIsDown[keyCode] if Program.KeyIsDown.ContainsKey(keyCode) else False

	IsKeyDown = staticmethod(IsKeyDown)

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

Program.Main(Environment.GetCommandLineArgs()[2:])