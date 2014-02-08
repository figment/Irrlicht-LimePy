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
	ID_IsNotPickable = 0
	IDFlag_IsPickable = 1 << 0
	IDFlag_IsHighlightable = 1 << 1
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		driver = device.VideoDriver
		smgr = device.SceneManager
		device.FileSystem.AddFileArchive("../../media/map-20kdm2.pk3")
		q3levelmesh = smgr.GetMesh("20kdm2.bsp")
		q3node = None
		# The Quake mesh is pickable, but doesn't get highlighted.
		if q3levelmesh != None:
			q3node = smgr.AddOctreeSceneNode(q3levelmesh.GetMesh(0), None, 1 << 0)
		selector = None
		if q3node != None:
			q3node.Position = Vector3Df(-1350, -130, -1400)
			selector = smgr.CreateOctreeTriangleSelector(q3node.Mesh, q3node, 128)
			q3node.TriangleSelector = selector
		# We're not done with this selector yet, so don't drop it.
		# Set a jump speed of 3 units per second, which gives a fairly realistic jump
		# when used with the gravity of (0, -10, 0) in the collision response animator.
		camera = smgr.AddCameraSceneNodeFPS(None, Single(100), Single(0.3), 0, None, True, Single(3))
		camera.Position = Vector3Df(50, 50, -60)
		camera.Target = Vector3Df(-70, 30, -60)
		if selector != None:
			anim = smgr.CreateCollisionResponseAnimator(selector, camera, Vector3Df(30, 50, 30), Vector3Df(0, -10, 0), Vector3Df(0, 30, 0))
			selector.Drop() # As soon as we're done with the selector, drop it.
			camera.AddAnimator(anim)
			anim.Drop() # And likewise, drop the animator when we're done referring to it.
		# Now I create three animated characters which we can pick, a dynamic light for
		# lighting them, and a billboard for drawing where we found an intersection.
		# First, let's get rid of the mouse cursor. We'll use a billboard to show what we're looking at.
		device.CursorControl.Visible = False
		# Add the billboard.
		bill = smgr.AddBillboardSceneNode()
		bill.SetMaterialType(MaterialType.TransparentAddColor)
		bill.SetMaterialTexture(0, driver.GetTexture("../../media/particle.bmp"))
		bill.SetMaterialFlag(MaterialFlag.Lighting, False)
		bill.SetMaterialFlag(MaterialFlag.ZBuffer, False)
		bill.SetSize(20, 20, 20)
		bill.ID = 0 # This ensures that we don't accidentally ray-pick it
		node = None
		# Add an MD2 node, which uses vertex-based animation.
		node = smgr.AddAnimatedMeshSceneNode(smgr.GetMesh("../../media/faerie.md2"), None, 1 << 0 | 1 << 1)
		node.Position = Vector3Df(-90, -15, -140) # Put its feet on the floor.
		node.Scale = Vector3Df(Single(1.6)) # Make it appear realistically scaled
		node.SetMD2Animation(AnimationTypeMD2.Point)
		node.AnimationSpeed = Single(20)
		node.GetMaterial(0).SetTexture(0, driver.GetTexture("../../media/faerie2.bmp"))
		node.GetMaterial(0).Lighting = True
		node.GetMaterial(0).NormalizeNormals = True
		# Now create a triangle selector for it.  The selector will know that it
		# is associated with an animated node, and will update itself as necessary.
		selector = smgr.CreateTriangleSelector(node)
		node.TriangleSelector = selector
		selector.Drop() # We're done with this selector, so drop it now.
		# And this B3D file uses skinned skeletal animation.
		node = smgr.AddAnimatedMeshSceneNode(smgr.GetMesh("../../media/ninja.b3d"), None, 1 << 0 | 1 << 1)
		node.Scale = Vector3Df(10)
		node.Position = Vector3Df(-75, -66, -80)
		node.Rotation = Vector3Df(0, 90, 0)
		node.AnimationSpeed = Single(8)
		node.GetMaterial(0).NormalizeNormals = True
		# Just do the same as we did above.
		selector = smgr.CreateTriangleSelector(node)
		node.TriangleSelector = selector
		selector.Drop()
		# This X files uses skeletal animation, but without skinning.
		node = smgr.AddAnimatedMeshSceneNode(smgr.GetMesh("../../media/dwarf.x"), None, 1 << 0 | 1 << 1)
		node.Position = Vector3Df(-70, -66, -30) # Put its feet on the floor.
		node.Rotation = Vector3Df(0, -90, 0) # And turn it towards the camera.
		node.AnimationSpeed = Single(20)
		selector = smgr.CreateTriangleSelector(node)
		node.TriangleSelector = selector
		selector.Drop()
		# And this mdl file uses skinned skeletal animation.
		node = smgr.AddAnimatedMeshSceneNode(smgr.GetMesh("../../media/yodan.mdl"), None, 1 << 0 | 1 << 1)
		node.Position = Vector3Df(-90, -25, 20)
		node.Scale = Vector3Df(Single(0.8))
		node.GetMaterial(0).Lighting = True
		node.AnimationSpeed = Single(20)
		# Just do the same as we did above.
		selector = smgr.CreateTriangleSelector(node)
		node.TriangleSelector = selector
		selector.Drop()
		# Add a light, so that the unselected nodes aren't completely dark.
		light = smgr.AddLightSceneNode(None, Vector3Df(-60, 100, 400), Colorf(Single(1), Single(1), Single(1)), Single(600))
		light.ID = 0 # Make it an invalid target for selection.
		# Remember which scene node is highlighted
		highlightedSceneNode = None
		collMan = smgr.SceneCollisionManager
		lastFPS = -1
		# draw the selection triangle only as wireframe
		material = Material()
		material.Lighting = False
		material.Wireframe = True
		while device.Run():
			if device.WindowActive:
				driver.BeginScene(True, True, Color(0))
				smgr.DrawAll()
				# Unlight any currently highlighted scene node
				if highlightedSceneNode != None:
					highlightedSceneNode.SetMaterialFlag(MaterialFlag.Lighting, True)
					highlightedSceneNode = None
				# All intersections in this example are done with a ray cast out from the camera to
				# a distance of 1000.  You can easily modify this to check (e.g.) a bullet
				# trajectory or a sword's position, or create a ray from a mouse click position using
				# ISceneCollisionManager::getRayFromScreenCoordinates()
				ray = Line3Df()
				ray.Start = Vector3Df(camera.Position)
				ray.End = ray.Start + (camera.Target - ray.Start).Normalize() * Single(1000)
				# Tracks the current intersection point with the level or a mesh
				# Used to show with triangle has been hit
				# This call is all you need to perform ray/triangle collision on every scene node
				# that has a triangle selector, including the Quake level mesh.  It finds the nearest
				# collision point/triangle, and returns the scene node containing that point.
				# Irrlicht provides other types of selection, including ray/triangle selector,
				# ray/box and ellipse/triangle selector, plus associated helpers.
				# See the methods of ISceneCollisionManager
				_tmp183_50, intersection, hitTriangle = collMan.GetSceneNodeAndCollisionPointFromRay(ray, 1 << 0)
				selectedSceneNode = _tmp183_50 # This ensures that only nodes that we have set up to be pickable are considered
				# If the ray hit anything, move the billboard to the collision position
				# and draw the triangle that was hit.
				if selectedSceneNode != None:
					bill.Position = Vector3Df(intersection)
					# We need to reset the transform before doing our own rendering.
					driver.SetTransform(TransformationState.World, Matrix.Identity)
					driver.SetMaterial(material)
					driver.Draw3DTriangle(hitTriangle, Color(255, 0, 0))
					# We can check the flags for the scene node that was hit to see if it should be
					# highlighted. The animated nodes can be highlighted, but not the Quake level mesh
					if (selectedSceneNode.ID & 1 << 1) == 1 << 1:
						highlightedSceneNode = selectedSceneNode
						# Highlighting in this case means turning lighting OFF for this node,
						# which means that it will be drawn with full brightness.
						highlightedSceneNode.SetMaterialFlag(MaterialFlag.Lighting, False)
				# We're all done drawing, so end the scene.
				driver.EndScene()
				fps = driver.FPS
				if lastFPS != fps:
					device.SetWindowCaption(String.Format("Collision detection example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
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

Program.Main(None)