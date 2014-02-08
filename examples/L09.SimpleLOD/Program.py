import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Data")
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("System.Xml.Linq")
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
	device = None
	isWireframeMode = False
	isLabelMode = False
	isStatsMode = False
	def __init__(self):
		pass
	def Main(args):
		lodItemCount = Program.AskUserForLODItemCount()
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		Program.device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(800, 600))
		if Program.device == None:
			return 
		Program.device.OnEvent += Program.device_OnEvent
		Program.device.SetWindowCaption("Simple LOD - Irrlicht Lime")
		Program.device.CursorControl.Visible = False
		driver = Program.device.VideoDriver
		scene = Program.device.SceneManager
		# generate all LODs of mesh
		lodMesh = List[Mesh]()
		meshMaterial = None
		lodTriangleCount = List[int]()
		p = Array[int]((100, 50, 32, 20, 12, 6, 3))
		for i in xrange(0,p.Length,1):
			m = scene.GeometryCreator.CreateSphereMesh(50, p[i], p[i])
			mb = m.GetMeshBuffer(0)
			mb.Material.Type = MaterialType.Solid
			mb.Material.SetTexture(0, driver.GetTexture("../../media/earth.jpg"))
			m.SetMaterialFlag(MaterialFlag.Lighting, False)
			lodMesh.Add(m)
			if meshMaterial == None:
				meshMaterial = m.GetMeshBuffer(0).Material
			lodTriangleCount.Add(mb.IndexCount / 3)
		# generate world,
		# we generate a lot of objects with random positions in huge virtual cube
		virtualCubeSide = 20000
		lodItems = Array.CreateInstance(LODItem, lodItemCount)
		r = Random(12345000)
		for i in xrange(0,lodItemCount,1): # translation
			tmat = Matrix(Vector3Df(r.Next(virtualCubeSide) - virtualCubeSide / 2, r.Next(virtualCubeSide) - virtualCubeSide / 2, r.Next(virtualCubeSide) - virtualCubeSide / 2))
			rvect = Vector3Df(r.NextDouble() / Single(200), r.NextDouble() / Single(200), r.NextDouble() / Single(200))
			lodItems[i] = LODItem.Create(Program.device, lodMesh, tmat, rvect)
		# split world on virtual sectors (cubes) for faster visibility check
		lodSectorSide = 6 # total number of sectors will be lodSectorSide^3, so for 6 it is 216
		lodSectorSize = virtualCubeSide / lodSectorSide
		lodSectors = Array.CreateInstance(LODSector, lodSectorSide, lodSectorSide, lodSectorSide)
		for i in xrange(0,lodSectorSide,1):
			for j in xrange(0,lodSectorSide,1):
				for k in xrange(0,lodSectorSide,1):
					dimension = AABBox(Vector3Df(i * lodSectorSize, j * lodSectorSize, k * lodSectorSize), Vector3Df((i + 1) * lodSectorSize, (j + 1) * lodSectorSize, (k + 1) * lodSectorSize))
					dimension.MinEdge -= virtualCubeSide / 2
					dimension.MaxEdge -= virtualCubeSide / 2
					s = LODSector.Create(dimension)
					lodSectors[i,j,k] = s
		for i in xrange(0,lodItems.Length,1):
			pos = lodItems[i].Position
			pos += virtualCubeSide / 2
			pos /= lodSectorSize
			ix = pos.X
			iy = pos.Y
			iz = pos.Z
			if ix < 0:
				ix = 0
			if ix > lodSectorSide - 1:
				ix = lodSectorSide - 1
			if iy < 0:
				ix = 0
			if iy > lodSectorSide - 1:
				iy = lodSectorSide - 1
			if iz < 0:
				iz = 0
			if iz > lodSectorSide - 1:
				iz = lodSectorSide - 1
			lodSectors[ix,iy,iz].AddLODItem(lodItems[i])
		# camera
		camera = scene.AddCameraSceneNodeFPS()
		camera.FarValue = 30000
		# font, which we are going to use to show any text we need
		font = Program.device.GUIEnvironment.GetFont("../../media/fontlucida.png")
		# render loop
		while Program.device.Run():
			driver.BeginScene()
			scene.DrawAll()
			if Program.isLabelMode:
				LODItem.LabelPositions = List[Vector2Di]()
				LODItem.LabelTexts = List[str]()
			else:
				LODItem.LabelPositions = None
				LODItem.LabelTexts = None
			meshMaterial.Wireframe = Program.isWireframeMode
			Program.device.VideoDriver.SetMaterial(meshMaterial)
			timer = Program.device.Timer.Time
			cameraPosition = camera.AbsolutePosition
			cameraViewBox = camera.ViewFrustum.BoundingBox
			for i in xrange(0,lodSectorSide,1):
				for j in xrange(0,lodSectorSide,1):
					for k in xrange(0,lodSectorSide,1):
						lodSectors[i,j,k].Draw(timer, cameraPosition, cameraViewBox)
			if Program.isLabelMode:
				for i in xrange(0,LODItem.LabelPositions.Count,1):
					driver.Draw2DLine(LODItem.LabelPositions[i] - Vector2Di(10, 0), LODItem.LabelPositions[i] + Vector2Di(50, 0), Color.OpaqueGreen)
					driver.Draw2DLine(LODItem.LabelPositions[i] - Vector2Di(0, 10), LODItem.LabelPositions[i] + Vector2Di(0, 50), Color.OpaqueGreen)
					font.Draw(LODItem.LabelTexts[i], LODItem.LabelPositions[i], Color.OpaqueGreen)
			if Program.isStatsMode:
				# show LOD stats
				lodCount = Array[int]((0, 0, 0, 0, 0, 0, 0))
				for i in xrange(0,lodItems.Length,1):
					lodCount[lodItems[i].CurrentLOD] += 1
				f = ""
				for i in xrange(0,lodCount.Length,1):
					n = lodCount[i]
					f += "LOD" + i.ToString() + ": " + n.ToString() + " [" + ((n * 100) / lodItemCount).ToString() + "%] objects\n"
				l = "------------------------"
				font.Draw(String.Format("Stats\n{0}\n{1}{2}\nTotal: {3} [100%] objects", l, f, l, lodItemCount), Vector2Di(10, 140), Color.OpaqueMagenta)
			# show general stats
			font.Draw(String.Format("Camera position: {0}\nTotal LOD 0 triangles: {1}\nTriangles currently drawn: {2}\nDriver: {3}\nFPS: {4}", camera.AbsolutePosition, lodTriangleCount[0] * lodItemCount, driver.PrimitiveCountDrawn, driver.Name, driver.FPS), 10, 10, Color.OpaqueYellow)
			# show active keys
			font.Draw("[S] Toggle stats\n[W] Toggle wireframe\n[L] Toggle labels (only for LODs from 0 to 4)\n[Esc] Exit application", 10, driver.ScreenSize.Height - 80, Color.OpaqueCyan)
			driver.EndScene()
		# drop
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Key and evnt.Key.PressedDown:
			if evnt.Key.Key == KeyCode.KeyS:
				Program.isStatsMode = not Program.isStatsMode
				return True
			elif evnt.Key.Key == KeyCode.KeyW:
				Program.isWireframeMode = not Program.isWireframeMode
				return True
			elif evnt.Key.Key == KeyCode.KeyL:
				Program.isLabelMode = not Program.isLabelMode
				return True
			elif evnt.Key.Key == KeyCode.Esc:
				Program.device.Close()
				return True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def AskUserForLODItemCount():
		Console.Write("Enter number of planets to generate (recommended value is 5000): ")
		s = Console.ReadLine()
		i = Convert.ToInt32(s)
		if i < 1:
			i = 1
		return i

	AskUserForLODItemCount = staticmethod(AskUserForLODItemCount)

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

class LODItem(object):
	LabelPositions = None
	LabelTexts = None
	def __init__(self):
		self._transformation = None
		self._device = None
		self._driver = None
		self._screenSize = None
		self._meshLODs = None
		self._rotationVector = None
		self._currentLOD = 0
		
		self._nextUpdateAt = 0
		# we cache some really frequently accessed values (which will never get changed anyway) 
		# this values directly controls how many tringles we are drawing 
		# LOD 0: 0 ... 150 
		# LOD 1: 150 ... 300 
		# LOD 2: 300 ... 600 
		# LOD 3: 600 ... 1200 
		# LOD 4: 1200 ... 2500 
		# LOD 5: 2500 ... 6000
		# LOD 6: 6000+; value "-1" doesn't play any role,
		self._lodDistanceSQ = Array[Single]((150 * 150, 300 * 300, 600 * 600, 1200 * 1200, 2500 * 2500, 6000 * 6000, -1 * -1)) 
		# because anything that is further than 6000 will stay at the last available LOD, which is 6 
		# we can affort this speed of updating (which is almost "every frame") 
		# because we know that objects with LOD 0 and 1 - are very close to the camera, we want them to look
		# hipoly and rotate smoothly; also we understand that it is only couple of objects with this LOD is
		# going to be present at any time
		self._updateIntervals = Array[UInt32]((10, 20, 40, 80, 120, 200, 1500))
		
		pass
	def get_CurrentLOD(self):
		return self._currentLOD

	CurrentLOD = property(fget=get_CurrentLOD)

	def get_Position(self):
		return self._transformation.Translation

	Position = property(fget=get_Position)

	def Create(device, meshLODs, transformation, rotationVector):
		n = LODItem()
		n._device = device
		n._meshLODs = meshLODs
		n._transformation = transformation
		n._rotationVector = rotationVector
		n._currentLOD = meshLODs.Count - 1
		n._driver = device.VideoDriver
		n._screenSize = device.VideoDriver.ScreenSize
		return n

	Create = staticmethod(Create)

	def Draw(self, time, cameraPosition):
		if time > self._nextUpdateAt:
			# animation
			self._transformation.Rotation = self._rotationVector * time
			# recalculate current LOD
			self._currentLOD = self._meshLODs.Count - 1
			distanceSQ = (self._transformation.Translation - cameraPosition).LengthSQ
			for i in xrange(0,self._lodDistanceSQ.Length - 1,1):
				if distanceSQ < self._lodDistanceSQ[i]:
					self._currentLOD = i
					break
			# next line assigns new time for LOD to be recalculated in future,
			# we do not use same value for all LODs here, because we don't want all the LODItems
			# to be recalculated in the same time (same frame). So we assign a value
			# which higher when current LOD is higher - which also means that for now we are
			# a distant object and it is less possible that we will need to change LOD at all;
			# but close objects (with small LOD value, like 0, 1 or 2) we need to pick quite short time.
			# This is OK if it will be really short, because this objects are too close and indeed may
			# change their LOD value very soon, however, we also understand, that in general all the objects
			# takes very large area, so in general we will have something like less than 2% with LOD level 0, 1 or 2,
			# all other will get higher LOD, and about more than 50% will have maximum LOD value -- they take more time to recalc
			# their LOD than to draw them, so we need to calc their LOD less frequent.
			# p.s.: we also uses that fact, that we do not give ability to user to reach oposite side of our world in 1 frame,
			# the speed which user uses for movement is slow in general.
			self._nextUpdateAt = time + self._updateIntervals[self._currentLOD]
		# drawing
		# we do no set material here, because we draw all LODItems with the same material, we set material in main rendering loop
		self._driver.SetTransform(TransformationState.World, self._transformation) # this is also very time consuming operation; we can optimize it
		# to make something like 100 calls (instead of 5000 - the number of LODItems) - we need to group LODItems all this we increase FPS up on
		# 10%, BUT it that case we will not be able to move independent LODItems, becase they will not need (and will not have) own transformation
		# matrix (only LODGroup will has it). So grouping is really greate for some completly static objects like trees, shrubs, stones, etc.
		# we draw single 16-bit meshbuffer
		self._driver.DrawMeshBuffer(self._meshLODs[self._currentLOD].GetMeshBuffer(0))
		if LODItem.LabelPositions != None and self._currentLOD <= 4:
			p = self._device.SceneManager.SceneCollisionManager.GetScreenCoordinatesFrom3DPosition(self._transformation.Translation)
			# now we filter here results which will not be visible; we know that:
			# - GetScreenCoordinatesFrom3DPosition() returns {-10000,-10000} for behind camera 3d positions
			# - we do not need to draw out small text if its out of the screen
			# p.s.: without this filtering we will have about 200-300 labels to draw (instead of about 10-20 which are trully visible)
			if p.X > -200 and p.X < self._screenSize.Width + 200 and p.Y > -100 and p.Y < self._screenSize.Height + 100:
				t = self._meshLODs[self._currentLOD].GetMeshBuffer(0).IndexCount / 3
				d = (self._transformation.Translation - cameraPosition).Length
				LODItem.LabelPositions.Add(p)
				LODItem.LabelTexts.Add("LOD: " + self._currentLOD.ToString() + "\nTrinagles: " + t.ToString() + "\nDistance: " + d.ToString())

class LODSector(object):
	def __init__(self):
		pass
	def get_Dimension(self):
		return self._dimension

	Dimension = property(fget=get_Dimension)

	def Create(dimension):
		s = LODSector()
		s._dimension = dimension
		s._d1 = dimension.MinEdge
		s._d2 = Vector3Df(dimension.MinEdge.X, dimension.MinEdge.Y, dimension.MaxEdge.Z)
		s._d3 = Vector3Df(dimension.MinEdge.X, dimension.MaxEdge.Y, dimension.MinEdge.Z)
		s._d4 = Vector3Df(dimension.MinEdge.X, dimension.MaxEdge.Y, dimension.MaxEdge.Z)
		s._d5 = dimension.MaxEdge
		s._d6 = Vector3Df(dimension.MaxEdge.X, dimension.MinEdge.Y, dimension.MinEdge.Z)
		s._d7 = Vector3Df(dimension.MaxEdge.X, dimension.MinEdge.Y, dimension.MaxEdge.Z)
		s._d8 = Vector3Df(dimension.MaxEdge.X, dimension.MaxEdge.Y, dimension.MinEdge.Z)
		s._lodItems = List[LODItem]()
		return s

	Create = staticmethod(Create)

	def AddLODItem(self, lodItem):
		self._lodItems.Add(lodItem)

	def Draw(self, time, cameraPosition, cameraViewBox):
		if cameraViewBox.IsInside(self._d1) or cameraViewBox.IsInside(self._d2) or cameraViewBox.IsInside(self._d3) or cameraViewBox.IsInside(self._d4) or cameraViewBox.IsInside(self._d5) or cameraViewBox.IsInside(self._d6) or cameraViewBox.IsInside(self._d7) or cameraViewBox.IsInside(self._d8):
			for i in xrange(0,self._lodItems.Count,1):
				self._lodItems[i].Draw(time, cameraPosition)

Program.Main(Environment.GetCommandLineArgs()[2:])