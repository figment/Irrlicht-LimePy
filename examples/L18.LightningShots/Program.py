import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("System.Data")
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
from LightningShot import *

class Program(object):
	device = None
	lightningShot = None
	mouseCanShoot = True
	def Main(args):
		Program.device = IrrlichtDevice.CreateDevice(DriverType.OpenGL, Dimension2Di(1024, 600))
		Program.device.SetWindowCaption("LightningShots - Irrlicht Engine")
		driver = Program.device.VideoDriver
		smgr = Program.device.SceneManager
		Program.device.FileSystem.AddFileArchive("../../media/map-20kdm2.pk3")
		mesh = smgr.GetMesh("20kdm2.bsp")
		node = smgr.AddMeshSceneNode(mesh.GetMesh(0))
		node.Position = Vector3Df(-1300, -144, -1249)
		node.SetMaterialType(MaterialType.LightMapLightingM4)
		node.SetMaterialFlag(MaterialFlag.Lighting, True)
		node.TriangleSelector = smgr.CreateTriangleSelector(node.Mesh, node)
		node.TriangleSelector.Drop()
		smgr.AmbientLight = Colorf(Single(0.15), Single(0.14), Single(0.13))
		camera = smgr.AddCameraSceneNodeFPS()
		Program.lightningShot = LightningShot(smgr, node.TriangleSelector)
		Program.device.OnEvent += Program.device_OnEvent
		Program.device.CursorControl.Visible = False
		while Program.device.Run():
			driver.BeginScene(True, True, Color(100, 80, 75))
			smgr.DrawAll()
			Program.lightningShot.Draw(Program.device.Timer.Time)
			f = Program.device.GUIEnvironment.BuiltInFont
			f.Draw("Use [LMB] to shoot", 10, 10, Color.OpaqueYellow)
			f.Draw("Total lightnings: " + str(Program.lightningShot.TotalLightnings), 10, 20, Color.OpaqueWhite)
			f.Draw("Total shots: " + str(Program.lightningShot.TotalShots), 10, 30, Color.OpaqueWhite)
			f.Draw(str(driver.FPS) + " fps", 10, 40, Color.OpaqueWhite)
			driver.EndScene()
		Program.lightningShot.Drop()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Mouse:
			if evnt.Mouse.IsLeftPressed():
				if not Program.mouseCanShoot:
					return True
				p = Program.device.SceneManager.ActiveCamera.Position
				d = (Program.device.SceneManager.ActiveCamera.Target - p).Normalize()
				Program.lightningShot.Fire(p + d * 20, d, Program.device.Timer.Time)
				Program.mouseCanShoot = False
				return True
			else:
				Program.mouseCanShoot = True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

Program.Main(None)