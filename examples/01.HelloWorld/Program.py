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
		device = IrrlichtDevice.CreateDevice(DriverType.Software, Dimension2Di(640, 480), 16, False, False, False)
		device.SetWindowCaption("Hello World! - Irrlicht Engine Demo")
		driver = device.VideoDriver
		smgr = device.SceneManager
		gui = device.GUIEnvironment
		gui.AddStaticText("Hello World! This is the Irrlicht Software renderer!", Recti(10, 10, 260, 22), True)
		mesh = smgr.GetMesh("../../media/sydney.md2")
		node = smgr.AddAnimatedMeshSceneNode(mesh)
		if node != None:
			node.SetMaterialFlag(MaterialFlag.Lighting, False)
			node.SetMD2Animation(AnimationTypeMD2.Stand)
			node.SetMaterialTexture(0, driver.GetTexture("../../media/sydney.bmp"))
		smgr.AddCameraSceneNode(None, Vector3Df(0, 30, -40), Vector3Df(0, 5, 0))
		while device.Run():
			driver.BeginScene(True, True, Color(100, 101, 140))
			smgr.DrawAll()
			gui.DrawAll()
			driver.EndScene()
		device.Drop()

	Main = staticmethod(Main)

Program.Main(None)