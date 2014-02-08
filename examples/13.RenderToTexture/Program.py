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
		# load and display animated fairy mesh
		fairy = smgr.AddAnimatedMeshSceneNode(smgr.GetMesh("../../media/faerie.md2"))
		if fairy != None:
			fairy.SetMaterialTexture(0, driver.GetTexture("../../media/faerie2.bmp")) # set diffuse texture
			fairy.SetMaterialFlag(MaterialFlag.Lighting, True) # enable dynamic lighting
			fairy.GetMaterial(0).Shininess = Single(20) # set size of specular highlights
			fairy.Position = Vector3Df(-10, 0, -100)
			fairy.SetMD2Animation(AnimationTypeMD2.Stand)
		# add white light
		smgr.AddLightSceneNode(None, Vector3Df(-15, 5, -105), Colorf(1, 1, 1))
		# set ambient light
		smgr.AmbientLight = Colorf(Single(0.25), Single(0.25), Single(0.25))
		# add fps camera
		fpsCamera = smgr.AddCameraSceneNodeFPS()
		fpsCamera.Position = Vector3Df(-50, 50, -150)
		# disable mouse cursor
		device.CursorControl.Visible = False
		# create test cube
		test = smgr.AddCubeSceneNode(60)
		# let the cube rotate and set some light settings
		anim = smgr.CreateRotationAnimator(Vector3Df(Single(0.3), Single(0.3), 0))
		test.Position = Vector3Df(-100, 0, -100)
		test.SetMaterialFlag(MaterialFlag.Lighting, False) # disable dynamic lighting
		test.AddAnimator(anim)
		anim.Drop()
		# create render target
		rt = None
		fixedCam = None
		if driver.QueryFeature(VideoDriverFeature.RenderToTarget):
			rt = driver.AddRenderTargetTexture(Dimension2Di(256), "RTT1")
			test.SetMaterialTexture(0, rt) # set material of cube to render target
			# add fixed camera
			fixedCam = smgr.AddCameraSceneNode(None, Vector3Df(10, 10, -80), Vector3Df(-10, 10, -100))
		else:
			# create problem text
			font = env.GetFont("../../media/fonthaettenschweiler.bmp")
			if font != None:
				env.Skin.SetFont(font)
			text = env.AddStaticText("Your hardware or this renderer is not able to use the " + "render to texture feature. RTT Disabled.", Recti(150, 20, 470, 60))
			text.OverrideColor = Color(255, 255, 255, 100)
		lastFPS = -1
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(0))
				if rt != None:
					# draw scene into render target
					# set render target texture
					driver.SetRenderTarget(rt, True, True, Color(0, 0, 255))
					# make cube invisible and set fixed camera as active camera
					test.Visible = False
					smgr.ActiveCamera = fixedCam
					# draw whole scene into render buffer
					smgr.DrawAll()
					# set back old render target
					# The buffer might have been distorted, so clear it
					driver.SetRenderTarget(None, True, True, Color(0))
					# make the cube visible and set the user controlled camera as active one
					test.Visible = True
					smgr.ActiveCamera = fpsCamera
				# draw scene normally
				smgr.DrawAll()
				env.DrawAll()
				driver.EndScene()
				# display frames per second in window title
				fps = driver.FPS
				if lastFPS != fps:
					device.SetWindowCaption(String.Format("Render to Texture and Specular Highlights example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
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

Program.Main(Environment.GetCommandLineArgs()[2:])