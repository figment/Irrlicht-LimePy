import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *

class Program(object):
	def Main(args):
		device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(800, 600))
		device.SetWindowCaption("RGB swirl example - Irrlicht Lime")
		driver = device.VideoDriver
		scene = device.SceneManager
		camera = scene.AddCameraSceneNode(None, Vector3Df(0, 0, -15), Vector3Df())
		camera.ViewMatrixAffector = camera.ProjectionMatrix.GetInverse()
		lightRed = scene.AddLightSceneNode(None, Vector3Df(0, 40, 0))
		lightRed.LightData.DiffuseColor = Colorf(1, 0, 0)
		a = scene.CreateFlyCircleAnimator(Vector3Df(), 40, Single(0.0003), Vector3Df(0, 0, 1), Single(0))
		lightRed.AddAnimator(a)
		a.Drop()
		lightGreen = scene.AddLightSceneNode(None, Vector3Df(-30, -20, 0))
		lightGreen.LightData.DiffuseColor = Colorf(0, 1, 0)
		a = scene.CreateFlyCircleAnimator(Vector3Df(), 40, Single(0.0003), Vector3Df(0, 0, 1), Single(0.333))
		lightGreen.AddAnimator(a)
		a.Drop()
		lightBlue = scene.AddLightSceneNode(None, Vector3Df(30, -20, 0))
		lightBlue.LightData.DiffuseColor = Colorf(0, 0, 1)
		a = scene.CreateFlyCircleAnimator(Vector3Df(), 40, Single(0.0003), Vector3Df(0, 0, 1), Single(0.667))
		lightBlue.AddAnimator(a)
		a.Drop()
		node = scene.AddSphereSceneNode(Single(5.5), 255)
		node.SetMaterialFlag(MaterialFlag.BackFaceCulling, False)
		node.SetMaterialFlag(MaterialFlag.PointCloud, True)
		node.GetMaterial(0).Thickness = 4
		while device.Run():
			node.Rotation = Vector3Df(device.Timer.Time / 1, device.Timer.Time / 2, device.Timer.Time / 3)
			driver.BeginScene(False)
			scene.DrawAll()
			driver.EndScene()
		device.Drop()

	Main = staticmethod(Main)

Program.Main(Environment.GetCommandLineArgs()[2:])