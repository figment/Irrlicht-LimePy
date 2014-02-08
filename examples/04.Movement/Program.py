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
	KeyIsDown = Dictionary[KeyCode, Boolean]()
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		device.OnEvent += Program.device_OnEvent
		driver = device.VideoDriver
		smgr = device.SceneManager
		node = smgr.AddSphereSceneNode()
		if node != None:
			node.Position = Vector3Df(0, 0, 30)
			node.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
			node.SetMaterialFlag(MaterialFlag.Lighting, False)
		n = smgr.AddCubeSceneNode()
		if n != None:
			n.SetMaterialTexture(0, driver.GetTexture("../../media/t351sml.jpg"))
			n.SetMaterialFlag(MaterialFlag.Lighting, False)
			anim = smgr.CreateFlyCircleAnimator(Vector3Df(0, 0, 30), Single(20))
			if anim != None:
				n.AddAnimator(anim)
				anim.Drop()
		anms = smgr.AddAnimatedMeshSceneNode(smgr.GetMesh("../../media/ninja.b3d"))
		if anms != None:
			anim = smgr.CreateFlyStraightAnimator(Vector3Df(100, 0, 60), Vector3Df(-100, 0, 60), Single(3.5), True)
			if anim != None:
				anms.AddAnimator(anim)
				anim.Drop()
			anms.SetMaterialFlag(MaterialFlag.Lighting, False)
			anms.SetFrameLoop(0, 13)
			anms.AnimationSpeed = 15
			anms.Scale = Vector3Df(2)
			anms.Rotation = Vector3Df(0, -90, 0)
		smgr.AddCameraSceneNodeFPS()
		device.CursorControl.Visible = False
		device.GUIEnvironment.AddImage(driver.GetTexture("../../media/irrlichtlogoalpha2.tga"), Vector2Di(10, 20))
		lastFPS = -1
		then = device.Timer.Time
		MOVEMENT_SPEED = Single(5)
		while device.Run():
			now = device.Timer.Time
			frameDeltaTime = (now - then) / Single(1000)
			then = now
			nodePosition = node.Position
			if Program.IsKeyDown(KeyCode.KeyW):
				nodePosition.Y += MOVEMENT_SPEED * frameDeltaTime
			elif Program.IsKeyDown(KeyCode.KeyS):
				nodePosition.Y -= MOVEMENT_SPEED * frameDeltaTime
			if Program.IsKeyDown(KeyCode.KeyA):
				nodePosition.X -= MOVEMENT_SPEED * frameDeltaTime
			elif Program.IsKeyDown(KeyCode.KeyD):
				nodePosition.X += MOVEMENT_SPEED * frameDeltaTime
			node.Position = nodePosition
			driver.BeginScene(True, True, Color(113, 113, 113))
			smgr.DrawAll()
			device.GUIEnvironment.DrawAll()
			driver.EndScene()
			fps = driver.FPS
			if lastFPS != fps:
				device.SetWindowCaption(String.Format("Movement example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
				lastFPS = fps
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

Program.Main(None)