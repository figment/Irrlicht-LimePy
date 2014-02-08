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
from DriverSettingsForm import DriverSettingsForm
from Application import Application

class Program(object):
	def __init__(self):
		pass
	def Main(args):
		driverSettings = DriverSettingsForm("Texture paint example", "This example shows how to use TexturePainter and render-to-texture (RTT) technique.\n\n" + "Use mouse to draw on the 2D image (texture) and see changes on the mesh and on RTT target.")
		if not driverSettings.ShowDialog():
			return 
		device = IrrlichtDevice.CreateDevice(driverSettings.DriverType, driverSettings.VideoMode.Resolution, driverSettings.VideoMode.Depth, driverSettings.Fullscreen)
		if device == None:
			Console.WriteLine("\nDevice creation failed!\n<Press any key to exit>")
			Console.ReadKey()
			return 
		app = Application(device)
		lastFPS = -1
		while device.Run():
			device.VideoDriver.BeginScene()
			app.Render()
			device.VideoDriver.EndScene()
			fps = VideoDriver.FPS
			if fps != lastFPS:
				device.SetWindowCaption(String.Format("Texture painting example - Irrlicht Lime [{0}] {1} fps", device.VideoDriver.Name, fps))
				lastFPS = fps
		device.Drop()

	Main = staticmethod(Main)

Program.Main(Environment.GetCommandLineArgs()[2:])