import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Linq")
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("System.Xml.Linq")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *
from SphereCamera import *
from SpherePath import *

class Program(object):
	device = None
	driver = None
	scene = None
	sphere = None
	camera = None
	path = None
	def __init__(self):
		pass
	def Main(args):
		Program.device = IrrlichtDevice.CreateDevice(DriverType.OpenGL, Dimension2Di(800, 600))
		Program.device.SetWindowCaption("Sphere Camera - Irrlicht Engine")
		Program.driver = Program.device.VideoDriver
		Program.scene = Program.device.SceneManager
		Program.sphere = Program.scene.AddSphereSceneNode(5, 100)
		Program.sphere.SetMaterialTexture(0, Program.driver.GetTexture("../../media/earth.jpg"))
		Program.sphere.TriangleSelector = Program.scene.CreateTriangleSelector(Program.sphere.Mesh, Program.sphere)
		Program.sphere.TriangleSelector.Drop()
		Program.scene.AmbientLight = Colorf(Single(0.2), Single(0.2), Single(0.2))
		light = Program.scene.AddLightSceneNode()
		light.Position = Vector3Df(-10, 10, -10)
		Program.camera = SphereCamera(Program.device, Vector3Df(0), 8, 20, 10, 0, 0)
		Program.camera.Inclination = 200
		Program.path = SpherePath(Single(5.4))
		font = Program.device.GUIEnvironment.BuiltInFont
		Program.device.OnEvent += Program.device_OnEvent
		Program.device.PostEvent(Event('r', KeyCode.KeyR, True)) # pretend user pressed [R]
		while Program.device.Run():
			Program.driver.BeginScene()
			Program.scene.DrawAll()
			Program.path.Draw(Program.driver)
			font.Draw("Press [Arrows], [LMB] and [Mouse Scroll] to change view", 10, 10, Color.OpaqueYellow)
			font.Draw("Press [RMB] on Earth to place new path point", 10, 20, Color.OpaqueYellow)
			font.Draw("Press [R] to reload path data from file", 10, 30, Color.OpaqueYellow)
			font.Draw("Press [C] to clean up", 10, 40, Color.OpaqueYellow)
			font.Draw(Program.driver.FPS.ToString() + " fps", 10, Program.driver.ScreenSize.Height - 40, Color.OpaqueYellow)
			font.Draw(Program.path.PointCount.ToString() + " point(s)", 10, Program.driver.ScreenSize.Height - 30, Color.OpaqueYellow)
			font.Draw(Program.camera.ToString(), 10, Program.driver.ScreenSize.Height - 20, Color.OpaqueYellow)
			Program.driver.EndScene()
		Program.path.Drop()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Mouse and evnt.Mouse.Type == MouseEventType.RightDown:
			l = Program.scene.SceneCollisionManager.GetRayFromScreenCoordinates(Vector2Di(evnt.Mouse.X, evnt.Mouse.Y))
			ok, v, t, n = Program.scene.SceneCollisionManager.GetCollisionPoint(l, Program.sphere.TriangleSelector)
			if ok:
				Program.path.AddPoint(v)
				return True
		if evnt.Type == EventType.Key:
			if evnt.Key.Key == KeyCode.Left:
				Program.camera.Inclination += 1
				return True
			elif evnt.Key.Key == KeyCode.Right:
				Program.camera.Inclination -= 1
				return True
			elif evnt.Key.Key == KeyCode.Up:
				Program.camera.Azimuth -= 1
				return True
			elif evnt.Key.Key == KeyCode.Down:
				Program.camera.Azimuth += 1
				return True
			elif evnt.Key.Key == KeyCode.KeyC:
				Program.path.Clear()
				return True
			elif evnt.Key.Key == KeyCode.KeyR:
				Program.path.Load("../../media/SphereCameraPath.xml")
				return True
 			#elif evnt.Key.Key == KeyCode.KeyS:
			#    path.Save("../../media/SphereCameraPath.xml");
			#    return true;
		return False

	device_OnEvent = staticmethod(device_OnEvent)

Program.Main(Environment.GetCommandLineArgs()[2:])