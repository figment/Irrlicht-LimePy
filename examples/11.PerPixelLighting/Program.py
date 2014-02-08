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
from IrrlichtLime.GUI import *

class Program(object):
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		driver = device.VideoDriver
		smgr = device.SceneManager
		env = device.GUIEnvironment
		driver.SetTextureCreationFlag(TextureCreationFlag.Always32Bit, True)
		# add irrlicht logo
		env.AddImage(driver.GetTexture("../../media/irrlichtlogoalpha2.tga"), Vector2Di(10))
		# add camera
		camera = smgr.AddCameraSceneNodeFPS()
		camera.Position = Vector3Df(-200, 200, -200)
		# disable mouse cursor
		device.CursorControl.Visible = False
		driver.Fog = Fog(Color(138, 125, 81, 0), FogType.Linear, 250, 1000, Single(0.003), True, False)
		roomMesh = smgr.GetMesh("../../media/room.3ds")
		room = None
		earth = None
		if roomMesh != None:
			# the room mesh doesn't have proper texture mapping on the floor,
			# so we can recreate them on runtime
			smgr.MeshManipulator.MakePlanarTextureMapping(roomMesh.GetMesh(0), Single(0.003))
			normalMap = driver.GetTexture("../../media/rockwall_height.bmp")
			if normalMap != None:
				driver.MakeNormalMapTexture(normalMap, Single(9))
			tangentMesh = smgr.MeshManipulator.CreateMeshWithTangents(roomMesh.GetMesh(0))
			room = smgr.AddMeshSceneNode(tangentMesh)
			room.SetMaterialTexture(0, driver.GetTexture("../../media/rockwall.jpg"))
			room.SetMaterialTexture(1, normalMap)
			room.GetMaterial(0).SpecularColor = Color(0)
			room.GetMaterial(0).Shininess = Single(0)
			room.SetMaterialFlag(MaterialFlag.Fog, True)
			room.SetMaterialType(MaterialType.ParallaxMapSolid)
			room.GetMaterial(0).MaterialTypeParam = Single(1) / Single(64) # adjust height for parallax effect
			tangentMesh.Drop() # drop mesh because we created it with a "create" call
		# add earth sphere
		earthMesh = smgr.GetMesh("../../media/earth.x")
		if earthMesh != None:
			# perform various task with the mesh manipulator
			manipulator = smgr.MeshManipulator
			# create mesh copy with tangent informations from original earth.x mesh
			tangentSphereMesh = manipulator.CreateMeshWithTangents(earthMesh.GetMesh(0))
			# set the alpha value of all vertices to 200
			manipulator.SetVertexColorAlpha(tangentSphereMesh, 200)
			# scale the mesh by factor 50
			m = Matrix()
			m.Scale = Vector3Df(50)
			manipulator.Transform(tangentSphereMesh, m)
			earth = smgr.AddMeshSceneNode(tangentSphereMesh)
			earth.Position = Vector3Df(-70, 130, 45)
			# load heightmap, create normal map from it and set it
			earthNormalMap = driver.GetTexture("../../media/earthbump.jpg")
			if earthNormalMap != None:
				driver.MakeNormalMapTexture(earthNormalMap, 20)
				earth.SetMaterialTexture(1, earthNormalMap)
				earth.SetMaterialType(MaterialType.NormalMapTransparentVertexAlpha)
			# adjust material settings
			earth.SetMaterialFlag(MaterialFlag.Fog, True)
			# add rotation animator
			anim = smgr.CreateRotationAnimator(Vector3Df(0, Single(0.1), 0))
			earth.AddAnimator(anim)
			anim.Drop()
			# drop mesh because we created it with a "create" call.
			tangentSphereMesh.Drop()
		# add light 1 (more green)
		light1 = smgr.AddLightSceneNode(None, Vector3Df(), Colorf(Single(0.5), Single(1), Single(0.5), Single(0)), 800)
		if light1 != None:
			light1.DebugDataVisible = DebugSceneType.BBox
			# add fly circle animator to light
			anim = smgr.CreateFlyCircleAnimator(Vector3Df(50, 300, 0), Single(190), -Single(0.003))
			light1.AddAnimator(anim)
			anim.Drop()
			# attach billboard to the light
			bill = smgr.AddBillboardSceneNode(light1, Dimension2Df(60, 60))
			bill.SetMaterialFlag(MaterialFlag.Lighting, False)
			bill.SetMaterialFlag(MaterialFlag.ZWrite, False)
			bill.SetMaterialType(MaterialType.TransparentAddColor)
			bill.SetMaterialTexture(0, driver.GetTexture("../../media/particlegreen.jpg"))
		# add light 2 (red)
		light2 = smgr.AddLightSceneNode(None, Vector3Df(), Colorf(Single(1), Single(0.2), Single(0.2), Single(0)), Single(800))
		if light2 != None:
			# add fly circle animator to light
			anim = smgr.CreateFlyCircleAnimator(Vector3Df(0, 150, 0), Single(200), Single(0.001), Vector3Df(Single(0.2), Single(0.9), Single(0)))
			light2.AddAnimator(anim)
			anim.Drop()
			# attach billboard to light
			bill = smgr.AddBillboardSceneNode(light2, Dimension2Df(120, 120))
			bill.SetMaterialFlag(MaterialFlag.Lighting, False)
			bill.SetMaterialFlag(MaterialFlag.ZWrite, False)
			bill.SetMaterialType(MaterialType.TransparentAddColor)
			bill.SetMaterialTexture(0, driver.GetTexture("../../media/particlered.bmp"))
			# add particle system
			ps = smgr.AddParticleSystemSceneNode(False, light2)
			# create and set emitter
			em = ps.CreateBoxEmitter(AABBox(-3, 0, -3, 3, 1, 3), Vector3Df(Single(0), Single(0.03), Single(0)), 80, 100, Color(255, 255, 255, 10), Color(255, 255, 255, 10), 400, 1100)
			em.MinStartSize = Dimension2Df(Single(30), Single(40))
			em.MaxStartSize = Dimension2Df(Single(30), Single(40))
			ps.Emitter = em
			em.Drop()
			# create and set affector
			paf = ps.CreateFadeOutParticleAffector()
			ps.AddAffector(paf)
			paf.Drop()
			# adjust some material settings
			ps.SetMaterialFlag(MaterialFlag.Lighting, False)
			ps.SetMaterialFlag(MaterialFlag.ZWrite, False)
			ps.SetMaterialTexture(0, driver.GetTexture("../../media/fireball.bmp"))
			ps.SetMaterialType(MaterialType.TransparentAddColor)
		receiver = MyEventReceiver(device, room, earth)
		lastFPS = -1
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(0))
				smgr.DrawAll()
				env.DrawAll()
				driver.EndScene()
				fps = driver.FPS
				if lastFPS != fps:
					device.SetWindowCaption(String.Format("Per pixel lighting example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
					lastFPS = fps
		device.Drop()

	Main = staticmethod(Main)

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

class MyEventReceiver(object):
	def __init__(self, device, room, earth):
		device.OnEvent += self.device_OnEvent
		# store pointer to room so we can change its drawing mode
		self._driver = device.VideoDriver
		self._room = room
		self._earth = earth
		env = device.GUIEnvironment
		# set a nicer font
		font = env.GetFont("../../media/fonthaettenschweiler.bmp")
		if font != None:
			env.Skin.SetFont(font)
		# add window and listbox
		window = env.AddWindow(Recti(460, 375, 630, 470), False, "Use 'E' + 'R' to change")
		self._listBox = env.AddListBox(Recti(2, 22, 165, 88), window)
		self._listBox.AddItem("Diffuse")
		self._listBox.AddItem("Bump mapping")
		self._listBox.AddItem("Parallax mapping")
		self._listBox.SelectedIndex = 1
		# create problem text
		self._problemText = env.AddStaticText("Your hardware or this renderer is not able to use the needed shaders for this material. Using fall back materials.", Recti(150, 20, 470, 80))
		self._problemText.OverrideColor = Color(255, 255, 255, 100)
		# set start material (prefer parallax mapping if available)
		renderer = self._driver.GetMaterialRenderer(MaterialType.ParallaxMapSolid)
		if renderer != None and renderer.Capability == 0:
			self._listBox.SelectedIndex = 2
		# set the material which is selected in the listbox
		self.setMaterial()

	def device_OnEvent(self, e):
		# check if user presses the key 'E' or 'R'
		if e.Type == EventType.Key and not e.Key.PressedDown and self._room != None and self._listBox != None:
			# change selected item in listbox
			sel = self._listBox.SelectedIndex
			if e.Key.Key == KeyCode.KeyR:
				sel += 1
			elif e.Key.Key == KeyCode.KeyE:
				sel -= 1
			else:
				return False
			if sel > 2:
				sel = 0
			if sel < 0:
				sel = 2
			self._listBox.SelectedIndex = sel
			# set the material which is selected in the listbox
			self.setMaterial()
		return False

	def setMaterial(self):
		roomMat = MaterialType.Solid
		earthMat = MaterialType.Solid
		# change material setting
		if self._listBox.SelectedIndex == 0:
			roomMat = MaterialType.Solid
			earthMat = MaterialType.TransparentVertexAlpha
		elif self._listBox.SelectedIndex == 1:
			roomMat = MaterialType.NormalMapSolid
			earthMat = MaterialType.NormalMapTransparentVertexAlpha
		elif self._listBox.SelectedIndex == 2:
			roomMat = MaterialType.ParallaxMapSolid
			earthMat = MaterialType.ParallaxMapTransparentVertexAlpha
		self._room.SetMaterialType(roomMat)
		self._earth.SetMaterialType(earthMat)
		# display some problem text when problem
		roomRenderer = self._driver.GetMaterialRenderer(roomMat)
		earthRenderer = self._driver.GetMaterialRenderer(earthMat)
		self._problemText.Visible = roomRenderer == None or roomRenderer.Capability != 0 or earthRenderer == None or earthRenderer.Capability != 0

Program.Main(Environment.GetCommandLineArgs()[2:])