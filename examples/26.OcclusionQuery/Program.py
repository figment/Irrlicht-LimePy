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

class Program(object):
	# Create the node to be occluded. We create a sphere node with high poly count.
	# Now we create another node, the occluder. It's a simple plane. # mesh # parent # id # position # rotation
	# Here we create the occlusion query. Because we don't have a plain mesh scene node
	# (SceneNodeType.Mesh or SceneNodeType.AnimatedMesh), we pass the base geometry as well. Instead,
	# we could also pass a simpler mesh or the bounding box. But we will use a time
	# based method, where the occlusion query renders to the frame buffer and in case
	# of success (occlusion), the mesh is not drawn for several frames.
	# We have done everything, just a camera and draw it. We also write the
	# current frames per second and the name of the driver to the caption of the
	# window to examine the render speedup.
	# We also store the time for measuring the time since the last occlusion query ran
	# and store whether the node should be visible in the next frames.
	# First, we draw the scene, possibly without the occluded element. This is necessary
	# because we need the occluder to be drawn first. You can also use several scene
	# managers to collect a number of possible occluders in a separately rendered scene.
	# Once in a while, here every 100 ms, we check the visibility. We run the queries,
	# update the pixel value, and query the result. Since we already rendered the node
	# we render the query invisible. The update is made blocking, as we need the result
	# immediately. If you don't need the result immediately, e.g. because oyu have other
	# things to render, you can call the update non-blocking. This gives the GPU more
	# time to pass back the results without flushing the render pipeline.
	# If the update was called non-blocking, the result from getOcclusionQueryResult is
	# either the previous value, or 0xffffffff if no value has been generated at all, yet.
	# The result is taken immediately as visibility flag for the node.
	KeyIsDown = Dictionary[KeyCode, Boolean]()
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		device.OnEvent += Program.device_OnEvent
		driver = device.VideoDriver
		scene = device.SceneManager
		scene.GUIEnvironment.AddStaticText("Press Space to hide occluder.", Recti(10, 10, 200, 50))
		node = scene.AddSphereSceneNode(10, 64)
		if node != None:
			node.Position = Vector3Df(0, 0, 60)
			node.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
			node.SetMaterialFlag(MaterialFlag.Lighting, False)
		plane = scene.AddMeshSceneNode(scene.AddHillPlaneMesh("plane", Dimension2Df(10), Dimension2Di(2)), None, -1, Vector3Df(0, 0, 20), Vector3Df(270, 0, 0))
		if plane != None:
			plane.SetMaterialTexture(0, driver.GetTexture("../../media/t351sml.jpg"))
			plane.SetMaterialFlag(MaterialFlag.Lighting, False)
			plane.SetMaterialFlag(MaterialFlag.BackFaceCulling, True)
		driver.AddOcclusionQuery(node, node.Mesh)
		scene.AddCameraSceneNode()
		timeNow = device.Timer.Time
		nodeVisible = True
		while device.Run():
			plane.Visible = not Program.IsKeyDown(KeyCode.Space)
			driver.BeginScene(True, True, Color(113, 113, 133))
			node.Visible = nodeVisible
			scene.DrawAll()
			scene.GUIEnvironment.DrawAll()
			if device.Timer.Time - timeNow > 100:
				driver.RunAllOcclusionQueries(False)
				driver.UpdateAllOcclusionQueries()
				nodeVisible = driver.GetOcclusionQueryResult(node) > 0
				timeNow = device.Timer.Time
			driver.EndScene()
			device.SetWindowCaption(String.Format("Occlusion Query Example - Irrlicht Engine [{0}] fps: {1} (primitives: {2})", driver.Name, driver.FPS, driver.PrimitiveCountDrawn))
		device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(e):
		if e.Type == EventType.Key:
			if Program.KeyIsDown.ContainsKey(e.Key.Key):
				Program.KeyIsDown[e.Key.Key] = e.Key.PressedDown
			else:
				Program.KeyIsDown.Add(e.Key.Key, e.Key.PressedDown)
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def IsKeyDown(keyCode):
		return Program.KeyIsDown[keyCode] if Program.KeyIsDown.ContainsKey(keyCode) else False

	IsKeyDown = staticmethod(IsKeyDown)

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