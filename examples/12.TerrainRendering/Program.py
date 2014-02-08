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
		# set gui font
		env.Skin.SetFont(env.GetFont("../../media/fontlucida.png"))
		# add some help text
		env.AddStaticText("Press 'W' to change wireframe mode\nPress 'D' to toggle detail map\nPress 'S' to toggle skybox/skydome", Recti(10, 421, 250, 475), True, True, None, -1, True)
		# add camera
		camera = smgr.AddCameraSceneNodeFPS(None, Single(100), Single(1.2))
		camera.Position = Vector3Df(2700 * 2, 255 * 2, 2600 * 2)
		camera.Target = Vector3Df(2397 * 2, 343 * 2, 2700 * 2)
		camera.FarValue = Single(42000)
		# disable mouse cursor
		device.CursorControl.Visible = False
		# add terrain scene node # heightmap # parent node # node id # position # rotation # scale # vertex color # max LOD # patch size
		terrain = smgr.AddTerrainSceneNode("../../media/terrain-heightmap.bmp", None, -1, Vector3Df(), Vector3Df(), Vector3Df(40, Single(4.4), 40), Color(255, 255, 255), 5, TerrainPatchSize._17, 4) # smooth factor
		terrain.SetMaterialFlag(MaterialFlag.Lighting, False)
		terrain.SetMaterialTexture(0, driver.GetTexture("../../media/terrain-texture.jpg"))
		terrain.SetMaterialTexture(1, driver.GetTexture("../../media/detailmap3.jpg"))
		terrain.SetMaterialType(MaterialType.DetailMap)
		terrain.ScaleTexture(1, 20)
		# create triangle selector for the terrain
		selector = smgr.CreateTerrainTriangleSelector(terrain, 0)
		terrain.TriangleSelector = selector
		# create collision response animator and attach it to the camera
		anim = smgr.CreateCollisionResponseAnimator(selector, camera, Vector3Df(60, 100, 60), Vector3Df(0, 0, 0), Vector3Df(0, 50, 0))
		selector.Drop()
		camera.AddAnimator(anim)
		anim.Drop()
		# create skybox and skydome
		driver.SetTextureCreationFlag(TextureCreationFlag.CreateMipMaps, False)
		skybox = smgr.AddSkyBoxSceneNode("../../media/irrlicht2_up.jpg", "../../media/irrlicht2_dn.jpg", "../../media/irrlicht2_lf.jpg", "../../media/irrlicht2_rt.jpg", "../../media/irrlicht2_ft.jpg", "../../media/irrlicht2_bk.jpg")
		skydome = smgr.AddSkyDomeSceneNode(driver.GetTexture("../../media/skydome.jpg"), 16, 8, Single(0.95), 2)
		driver.SetTextureCreationFlag(TextureCreationFlag.CreateMipMaps, True)
		# create event receiver
		MyEventReceiver(device, terrain, skybox, skydome)
		lastFPS = -1
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(0))
				smgr.DrawAll()
				env.DrawAll()
				driver.EndScene()
				# display frames per second in window title
				fps = driver.FPS
				if lastFPS != fps:
					# also print terrain height of current camera position
					# we can use camera position because terrain is located at coordinate origin
					device.SetWindowCaption(String.Format("Terrain rendering example - Irrlicht Engine [{0}] fps: {1} Height: {2}", driver.Name, fps, terrain.GetHeight(camera.AbsolutePosition.X, camera.AbsolutePosition.Z)))
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
	def __init__(self, device, terrain, skybox, skydome):
		self._terrain = terrain
		self._skybox = skybox
		self._skydome = skydome
		self._showBox = True
		self._showDebug = False
		skybox.Visible = True
		skydome.Visible = False
		device.OnEvent += self.device_OnEvent

	def device_OnEvent(self, e):
		# check if user presses the key 'W', 'P', 'D', 'S' or 'X'
		if e.Type == EventType.Key and e.Key.PressedDown:
			if e.Key.Key == KeyCode.KeyW: # switch wire frame mode
				self._terrain.SetMaterialFlag(MaterialFlag.Wireframe, not self._terrain.GetMaterial(0).Wireframe)
				self._terrain.SetMaterialFlag(MaterialFlag.PointCloud, False)
				return True
			elif e.Key.Key == KeyCode.KeyP: # switch point cloud mode
				self._terrain.SetMaterialFlag(MaterialFlag.PointCloud, not self._terrain.GetMaterial(0).PointCloud)
				self._terrain.SetMaterialFlag(MaterialFlag.Wireframe, False)
				return True
			elif e.Key.Key == KeyCode.KeyD: # toggle detail map
				self._terrain.SetMaterialType(MaterialType.DetailMap if self._terrain.GetMaterial(0).Type == MaterialType.Solid else MaterialType.Solid)
				return True
			elif e.Key.Key == KeyCode.KeyS: # toggle skies
				self._showBox = not self._showBox
				self._skybox.Visible = self._showBox
				self._skydome.Visible = not self._showBox
				return True
			elif e.Key.Key == KeyCode.KeyX: # toggle debug information
				self._showDebug = not self._showDebug
				self._terrain.DebugDataVisible = DebugSceneType.BBoxAll if self._showDebug else DebugSceneType.Off
				return True
		return False

Program.Main(Environment.GetCommandLineArgs()[2:])