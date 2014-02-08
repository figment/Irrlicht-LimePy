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
		shadows = Program.AskUserForRealtimeShadows()
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480), 16, False, shadows)
		if device == None:
			return 
		driver = device.VideoDriver
		smgr = device.SceneManager
		mesh = smgr.GetMesh("../../media/room.3ds")
		smgr.MeshManipulator.MakePlanarTextureMapping(mesh.GetMesh(0), Single(0.004))
		node = None
		node = smgr.AddAnimatedMeshSceneNode(mesh)
		node.SetMaterialTexture(0, driver.GetTexture("../../media/wall.jpg"))
		node.GetMaterial(0).SpecularColor.Set(0, 0, 0, 0)
		mesh = smgr.AddHillPlaneMesh("myHill", Dimension2Df(20, 20), Dimension2Di(40, 40), None, 0, Dimension2Df(0), Dimension2Df(10, 10))
		node = smgr.AddWaterSurfaceSceneNode(mesh.GetMesh(0), Single(3), Single(300), Single(30))
		node.Position = Vector3Df(0, 7, 0)
		node.SetMaterialTexture(0, driver.GetTexture("../../media/stones.jpg"))
		node.SetMaterialTexture(1, driver.GetTexture("../../media/water.jpg"))
		node.SetMaterialType(MaterialType.Reflection2Layer)
		# create light
		node = smgr.AddLightSceneNode(None, Vector3Df(0), Colorf(Single(1), Single(0.6), Single(0.7), Single(1)), 800)
		anim = smgr.CreateFlyCircleAnimator(Vector3Df(0, 150, 0), 250)
		node.AddAnimator(anim)
		anim.Drop()
		# attach billboard to light
		node = smgr.AddBillboardSceneNode(node, Dimension2Df(50, 50))
		node.SetMaterialFlag(MaterialFlag.Lighting, False)
		node.SetMaterialType(MaterialType.TransparentAddColor)
		node.SetMaterialTexture(0, driver.GetTexture("../../media/particlewhite.bmp"))
		# create a particle system
		ps = smgr.AddParticleSystemSceneNode(False)
		if ps != None: # emitter size # initial direction # emit rate # darkest color # brightest color # min and max age, angle # min size
			em = ps.CreateBoxEmitter(AABBox(-7, 0, -7, 7, 1, 7), Vector3Df(Single(0), Single(0.06), Single(0)), 80, 100, Color(255, 255, 255, 0), Color(255, 255, 255, 0), 800, 2000, 0, Dimension2Df(Single(10)), Dimension2Df(Single(20))) # max size
			ps.Emitter = em # this grabs the emitter
			em.Drop() # so we can drop it here without deleting it
			paf = ps.CreateFadeOutParticleAffector()
			ps.AddAffector(paf) # same goes for the affector
			paf.Drop()
			ps.Position = Vector3Df(-70, 60, 40)
			ps.Scale = Vector3Df(2)
			ps.SetMaterialFlag(MaterialFlag.Lighting, False)
			ps.SetMaterialFlag(MaterialFlag.ZWrite, False)
			ps.SetMaterialTexture(0, driver.GetTexture("../../media/fire.bmp"))
			ps.SetMaterialType(MaterialType.TransparentAddColor) # Subdivisions on U axis # Subdivisions on V axis # foot color
		n = smgr.AddVolumeLightSceneNode(None, -1, 32, 32, Color(255, 255, 255, 0), Color(0, 0, 0, 0)) # tail color
		if n != None:
			n.Scale = Vector3Df(56)
			n.Position = Vector3Df(-120, 50, 40)
			# load textures for animation
			textures = List[Texture]()
			for i in xrange(7,0,-1):
				s = str.Format("../../media/portal{0}.bmp", i)
				textures.Add(driver.GetTexture(s))
			# create texture animator
			glow = smgr.CreateTextureAnimator(textures, Single(0.15))
			# add the animator
			n.AddAnimator(glow)
			# drop the animator because it was created with a create() function
			glow.Drop()
		# add animated character
		mesh = smgr.GetMesh("../../media/dwarf.x")
		anode = smgr.AddAnimatedMeshSceneNode(mesh)
		anode.Position = Vector3Df(-50, 20, -60)
		anode.AnimationSpeed = 15
		# add shadow
		anode.AddShadowVolumeSceneNode()
		smgr.ShadowColor = Color(0, 0, 0, 150)
		# make the model a little bit bigger and normalize its normals
		# because of the scaling, for correct lighting
		anode.Scale = Vector3Df(2)
		anode.SetMaterialFlag(MaterialFlag.NormalizeNormals, True)
		camera = smgr.AddCameraSceneNodeFPS()
		camera.Position = Vector3Df(-50, 50, -150)
		# disable mouse cursor
		device.CursorControl.Visible = False
		lastFPS = -1
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(0))
				smgr.DrawAll()
				driver.EndScene()
				fps = driver.FPS
				if lastFPS != fps:
					device.SetWindowCaption(String.Format("SpecialFX example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
					lastFPS = fps
		device.Drop()

	Main = staticmethod(Main)

	def AskUserForRealtimeShadows():
		Console.WriteLine("Please press 'y' if you want to use realtime shadows.")
		return Console.ReadKey().Key == ConsoleKey.Y

	AskUserForRealtimeShadows = staticmethod(AskUserForRealtimeShadows)

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

Program.Main(None)