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
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		driver = device.VideoDriver
		smgr = device.SceneManager
		# load the scene
		if args.Length > 0:
			smgr.LoadScene(args[0])
		else:
			smgr.LoadScene("../../media/example.irr")
		camera = smgr.AddCameraSceneNodeFPS(None, 50, Single(0.1))
		# create a meta triangle selector to hold several triangle selectors
		meta = smgr.CreateMetaTriangleSelector()
		nodes = smgr.GetSceneNodesFromType(SceneNodeType.Any) # find all nodes
		for n in nodes:
			selector = None
			if n.Type == SceneNodeType.Cube or n.Type == SceneNodeType.AnimatedMesh:
				# because the selector won't animate with the mesh,
				# and is only being used for camera collision, we'll just use an approximate
				# bounding box instead of "(node as AnimatedMeshSceneNode).GetMesh(0)"
				selector = smgr.CreateTriangleSelectorFromBoundingBox(n)
			elif n.Type == SceneNodeType.Mesh or n.Type == SceneNodeType.Sphere:
				# derived from MeshSceneNode
				selector = smgr.CreateTriangleSelector((n).Mesh, n)
			elif n.Type == SceneNodeType.Terrain:
				selector = smgr.CreateTerrainTriangleSelector(n)
			elif n.Type == SceneNodeType.Octree:
				selector = smgr.CreateOctreeTriangleSelector((n).Mesh, n)
			if selector != None:
				# add it to the meta selector, which will take a reference to it
				meta.AddTriangleSelector(selector)
				# and drop my reference to it, so that the meta selector owns it
				selector.Drop()
		anim = smgr.CreateCollisionResponseAnimator(meta, camera, Vector3Df(5), Vector3Df(0))
		meta.Drop() # i'm done with the meta selector now
		camera.AddAnimator(anim)
		anim.Drop() # i'm done with the animator now
		# and set the camera position so that it doesn't start off stuck in the geometry
		camera.Position = Vector3Df(0, 20, 0)
		# point the camera at the cube node, by finding the first node of type SceneNodeType.Cube
		cube = smgr.GetSceneNodeFromType(SceneNodeType.Cube)
		if cube != None:
			camera.Target = cube.AbsolutePosition
		lastFPS = -1
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(200, 200, 200))
				smgr.DrawAll()
				driver.EndScene()
				fps = driver.FPS
				if lastFPS != fps:
					device.SetWindowCaption(String.Format("Load Irrlicht File example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
					lastFPS = fps
		device.Drop()

	Main = staticmethod(Main)

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