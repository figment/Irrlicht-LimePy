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
# NOTE: this example requires BulletSharp.dll for compiling and for running.
# Well, I don't want to ship 1.6 megs dll with Lime just for this example.
# In future if there are will be more examples using BulletSharp.dll - probably i will include it into Lime package.
# For now I will left it like this - if you want to see example running - you should download dll manually.
# See checkBulletSharpDllPresence() implementation for more details: what url and what version to use.
class Program(object):
	worldGravity = 200
	cubeMass = 1
	cubeSize = 40
	sphereMass = 1 * 5
	sphereRadius = 40 * Single(0.75)
	device = None
	physics = None
	particles = None
	simPaused = False
	useTrails = False
	# setup Irrlicht
	# setup physics
	# setup particles
	# load quake level
	# generate dynamic objects
	# main loop
	# simulate physics
	# winnow particles
	# render scene
	# display stats
	# drop
	mouseCanShoot = True
	def __init__(self):
		pass
	def Main(args):
		Program.checkBulletSharpDllPresence()
		Program.device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(1024, 768))
		if Program.device == None:
			return 
		Program.device.SetWindowCaption("BulletSharp Test - Irrlicht Engine")
		Program.device.OnEvent += Program.device_OnEvent
		driver = Program.device.VideoDriver
		scene = Program.device.SceneManager
		font = Program.device.GUIEnvironment.GetFont("../../media/fontlucida.png")
		camera = scene.AddCameraSceneNodeFPS()
		camera.Position = Vector3Df(100, 800, -1000)
		camera.Target = Vector3Df(0, 100, 0)
		camera.FarValue = 30000
		camera.AutomaticCulling = CullingType.FrustumBox
		Program.device.CursorControl.Visible = False
		Program.physics = Physics()
		Program.physics.Setup(Vector3Df(0, -200, 0))
		Program.particles = Particles(Program.device)
		Program.device.FileSystem.AddFileArchive("../../media/map-20kdm2.pk3")
		mesh = scene.GetMesh("20kdm2.bsp").GetMesh(0)
		quakeLevel = scene.AddOctreeSceneNode(mesh, None, -1, 1024)
		quakeLevel.Position = Vector3Df(-1300, -144, -1249)
		Program.physics.AddShape(Physics.Shape.Mesh, quakeLevel)
		for i in xrange(0,3,1):
			for j in xrange(0,30,1):
				for k in xrange(0,3,1):
					n = scene.AddCubeSceneNode(40)
					n.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
					n.SetMaterialFlag(MaterialFlag.Lighting, False)
					n.Position = Vector3Df(70 + i * 40, 520 + j * 40, -650 + k * 40)
					Program.physics.AddShape(Physics.Shape.Box, n, 1)
		curTime = 0
		lastTime = 0
		simFps = 0
		simFrames = 0
		simFramesTime = 0
		while Program.device.Run():
			if Program.device.WindowActive:
				lastTime = curTime
				curTime = Program.device.Timer.Time
				if not Program.simPaused:
					deltaTime = (curTime - lastTime) / Single(1000)
					b = Program.physics.StepSimulation(deltaTime)
					if b:
						simFrames += 1
				if curTime - simFramesTime > 1000:
					simFramesTime = curTime
					simFps = simFrames
					simFrames = 0
				Program.particles.Winnow(curTime, Program.simPaused)
				driver.BeginScene(True, True, Color(40, 80, 160))
				scene.DrawAll()
				material = Material()
				material.Lighting = False
				Program.device.VideoDriver.SetMaterial(material)
				driver.Draw2DRectangle(Recti(10, 10, 140, 180), Color(0x7f000000))
				v = Vector2Di(20, 20)
				font.Draw("Rendering", v, Color.OpaqueYellow)
				v.Y += 16
				font.Draw(scene.Attributes.GetValue("calls") + " nodes", v, Color.OpaqueWhite)
				v.Y += 16
				font.Draw(driver.FPS + " fps", v, Color.OpaqueWhite)
				v.Y += 16
				font.Draw("[T]rails " + ("ON" if Program.useTrails else "OFF"), v, Color.OpaqueGreen)
				v.Y += 32
				font.Draw("Physics" + (" (paused)" if Program.simPaused else ""), v, Color.OpaqueYellow)
				v.Y += 16
				font.Draw(Program.physics.NumCollisionObjects + " shapes", v, Color.OpaqueWhite)
				v.Y += 16
				font.Draw(simFps + " fps", v, Color.OpaqueWhite)
				v.Y += 16
				font.Draw("[Space] to pause", v, Color.OpaqueGreen)
				driver.EndScene()
			Program.device.Yield()
		Program.physics.Drop()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Key and evnt.Key.PressedDown:
			if evnt.Key.Key == KeyCode.Space:
				Program.simPaused = not Program.simPaused
				return True
			elif evnt.Key.Key == KeyCode.KeyT:
				Program.useTrails = not Program.useTrails
				return True
		if evnt.Type == EventType.Mouse:
			if evnt.Mouse.IsLeftPressed():
				if not Program.mouseCanShoot:
					return True
				n = Program.device.SceneManager.AddSphereSceneNode(40 * Single(0.75))
				n.SetMaterialTexture(0, Program.device.VideoDriver.GetTexture("../../media/wall.bmp"))
				n.SetMaterialFlag(MaterialFlag.Lighting, False)
				v = (Program.device.SceneManager.ActiveCamera.Target - Program.device.SceneManager.ActiveCamera.Position).Normalize()
				n.Position = Program.device.SceneManager.ActiveCamera.Position + v * 100
				if Program.useTrails:
					Program.particles.Add(n, Program.device.Timer.Time)
				Program.physics.AddShape(Physics.Shape.Shpere, n, 1 * 5, False, v * 1 * 10000)
				Program.mouseCanShoot = False
				return True
			else:
				Program.mouseCanShoot = True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def checkBulletSharpDllPresence():
		bulletSharpDllFilename = "BulletSharp.dll"
		bulletSharpUrl = "http://code.google.com/p/bulletsharp/"
		bulletSharpDllUrl = "http://code.google.com/p/bulletsharp/downloads/detail?name=bulletsharp-r396.zip"
		if System.IO.File.Exists(bulletSharpDllFilename):
			return 
		Console.ForegroundColor = ConsoleColor.Yellow
		Console.WriteLine(bulletSharpDllFilename + " not found.")
		Console.ForegroundColor = ConsoleColor.Gray
		Console.WriteLine()
		Console.WriteLine("If you want to run this example you have to place it near this EXE file.")
		Console.WriteLine("This example was tested with bulletsharp-r396 a \"Release Generic\" dll.")
		Console.WriteLine("You can get it from " + bulletSharpUrl)
		Console.WriteLine()
		Console.WriteLine("Press any key to exit or F1 if you want to navigate your web browser right now.")
		k = Console.ReadKey()
		if k.Key == ConsoleKey.F1:
			System.Diagnostics.Process.Start(bulletSharpDllUrl)
		Environment.Exit(0)

	checkBulletSharpDllPresence = staticmethod(checkBulletSharpDllPresence)

Program.Main(Environment.GetCommandLineArgs()[2:])