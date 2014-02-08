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
from ClockNode import *

class Program(object):
	def Main(args):
		device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9)
		device.SetWindowCaption("Analogue Clock - Irrlicht Lime")
		device.CursorControl.Visible = False
		ClockNode.AddClockNode(device.SceneManager.RootNode)
		camera = device.SceneManager.AddCameraSceneNodeFPS(None, 100, Single(0.1))
		camera.Position = Vector3Df(40, -20, -100) # start up position
		camera.Target = Vector3Df() # prev position change has also moved target, so we update it
		while device.Run():
			device.VideoDriver.BeginScene()
			device.SceneManager.DrawAll()
			s = String.Format("{0}\n{1}\n{2}\n{3} tris\n{4} fps", device.Timer.RealTimeAndDate, device.VideoDriver.VendorInfo, device.VideoDriver.Name, device.VideoDriver.PrimitiveCountDrawn, device.VideoDriver.FPS)
			device.GUIEnvironment.BuiltInFont.Draw(s, 11, 11, Color(0, 0, 0))
			device.GUIEnvironment.BuiltInFont.Draw(s, 10, 10, Color(255, 255, 255))
			device.VideoDriver.EndScene()
		device.Drop()

	Main = staticmethod(Main)

Program.Main(Environment.GetCommandLineArgs()[2:])