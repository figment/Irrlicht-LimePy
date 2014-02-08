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
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		driver = device.VideoDriver
		smgr = device.SceneManager
		device.FileSystem.AddFileArchive("../../media/map-20kdm2.pk3")
		mesh = smgr.GetMesh("20kdm2.bsp")
		node = None
		if mesh != None:
			node = smgr.AddOctreeSceneNode(mesh.GetMesh(0), None, -1, 1024)
		if node != None:
			node.Position = Vector3Df(-1300, -144, -1249)
		smgr.AddCameraSceneNodeFPS()
		device.CursorControl.Visible = False
		lastFPS = -1
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(200, 200, 200))
				smgr.DrawAll()
				driver.EndScene()
				fps = driver.FPS
				if lastFPS != fps:
					device.SetWindowCaption(String.Format("Quake 3 Map Example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
					lastFPS = fps
		device.Drop()

	Main = staticmethod(Main)

Program.Main(None)