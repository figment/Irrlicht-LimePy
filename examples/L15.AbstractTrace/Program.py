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
from AbstractTrace import *

class Program(object):
	device = None
	trace = None
	def __init__(self):
		pass
	def Main(args):
		Program.device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(1280, 720))
		if Program.device == None:
			return 
		driver = Program.device.VideoDriver
		scene = Program.device.SceneManager
		camera = scene.AddCameraSceneNode()
		camera.FarValue = 20000
		a = scene.CreateFlyCircleAnimator(Vector3Df(), (AbstractTrace.CubeSize * AbstractTrace.GridDim) / Single(1.25), Single(2.5E-05), Vector3Df(Single(0.1), 1, 0))
		camera.AddAnimator(a)
		a.Drop()
		Program.trace = AbstractTrace(Program.device)
		Program.trace.Init()
		lastFps = -1
		while Program.device.Run():
			driver.BeginScene()
			scene.DrawAll()
			Program.trace.Step()
			Program.trace.Draw()
			driver.EndScene()
			fps = driver.FPS
			if fps != lastFps:
				Program.device.SetWindowCaption("Abstract Trace - Irrlicht Engine [" + str(fps) + " fps; " + str(Program.trace.GetTotalCubeCount()) + " cubes]")
				lastFps = fps
		Program.trace.Drop()
		Program.device.Drop()

	Main = staticmethod(Main)

Program.Main(Environment.GetCommandLineArgs()[2:])