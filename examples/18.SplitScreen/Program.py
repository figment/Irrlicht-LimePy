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
	# resolution
	ResX = 800
	ResY = 600
	fullScreen = False
	# use split screen ?
	splitScreen = True
	# cameras
	camera = Array[CameraSceneNode]((None, None, None, None))
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(Program.ResX, Program.ResY), 32, Program.fullScreen)
		if device == None:
			return 
		device.OnEvent += Program.device_OnEvent
		driver = device.VideoDriver
		smgr = device.SceneManager
		# load model
		model = smgr.GetMesh("../../media/sydney.md2")
		if model == None:
			return 
		model_node = smgr.AddAnimatedMeshSceneNode(model)
		# load texture
		if model_node != None:
			texture = driver.GetTexture("../../media/sydney.bmp")
			model_node.SetMaterialTexture(0, texture)
			model_node.SetMD2Animation(AnimationTypeMD2.Run)
			model_node.SetMaterialFlag(MaterialFlag.Lighting, False)
		# load map
		device.FileSystem.AddFileArchive("../../media/map-20kdm2.pk3")
		map = smgr.GetMesh("20kdm2.bsp")
		if map != None:
			map_node = smgr.AddOctreeSceneNode(map.GetMesh(0))
			map_node.Position = Vector3Df(-850, -220, -850)
		# create 3 fixed and one user-controlled cameras
		Program.camera[0] = smgr.AddCameraSceneNode(None, Vector3Df(50, 0, 0), Vector3Df(0)) # font
		Program.camera[1] = smgr.AddCameraSceneNode(None, Vector3Df(0, 50, 0), Vector3Df(0)) # top
		Program.camera[2] = smgr.AddCameraSceneNode(None, Vector3Df(0, 0, 50), Vector3Df(0)) # left
		Program.camera[3] = smgr.AddCameraSceneNodeFPS() # user-controlled
		Program.camera[3].Position = Vector3Df(-50, 0, -50)
		device.CursorControl.Visible = False
		lastFPS = -1
		while device.Run():
			# set the viewpoint to the whole screen and begin scene
			driver.ViewPort = Recti(0, 0, Program.ResX, Program.ResY)
			driver.BeginScene(True, True, Color(100, 100, 100))
			if Program.splitScreen:
				smgr.ActiveCamera = Program.camera[0]
				driver.ViewPort = Recti(0, 0, Program.ResX / 2, Program.ResY / 2) # top left
				smgr.DrawAll()
				smgr.ActiveCamera = Program.camera[1]
				driver.ViewPort = Recti(Program.ResX / 2, 0, Program.ResX, Program.ResY / 2) # top right
				smgr.DrawAll()
				smgr.ActiveCamera = Program.camera[2]
				driver.ViewPort = Recti(0, Program.ResY / 2, Program.ResX / 2, Program.ResY) # bottom left
				smgr.DrawAll()
				driver.ViewPort = Recti(Program.ResX / 2, Program.ResY / 2, Program.ResX, Program.ResY) # bottom right
			smgr.ActiveCamera = Program.camera[3]
			smgr.DrawAll()
			driver.EndScene()
			fps = driver.FPS
			if lastFPS != fps:
				device.SetWindowCaption(String.Format("Split Screen example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
				lastFPS = fps
		device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(e):
		# key S enables/disables split screen
		if e.Type == EventType.Key and e.Key.Key == KeyCode.KeyS and e.Key.PressedDown:
			Program.splitScreen = not Program.splitScreen
			return True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

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