import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *
from Shadows import *

class Program(object):
	device = None
	shadows = None
	cameraNode = None
	quakeLevelNode = None
	faerieNode = None
	lightMovementHelperNode = None
	lightNode = None
	flashlightNode = None
	useLightBinding = True
	useShadowsRendering = True
	useShadowsRebuilding = True
	useShadowsQuakeLevel = False
	useFlashlight = False
	def __init__(self):
		pass
	def Main(args):
		# setup Irrlicht
		Program.device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(1024, 768), 32, False, True)
		if Program.device == None:
			return 
		Program.device.SetWindowCaption("Stencil Shadows - Irrlicht Engine")
		Program.device.OnEvent += Program.device_OnEvent
		driver = Program.device.VideoDriver
		scene = Program.device.SceneManager
		statsFont = Program.device.GUIEnvironment.GetFont("../../media/fontlucida.png")
		statsMaterial = Material.IdentityNoLighting
		Program.cameraNode = scene.AddCameraSceneNodeFPS()
		Program.cameraNode.FarValue = 20000
		Program.device.CursorControl.Visible = False
		# setup shadows
		Program.shadows = Shadows(Color(UInt32(2684354560)), 4000)
		# load quake level
		Program.device.FileSystem.AddFileArchive("../../media/map-20kdm2.pk3")
		m = scene.GetMesh("20kdm2.bsp").GetMesh(0)
		n = scene.AddOctreeSceneNode(m, None, -1, 1024)
		n.Position = Vector3Df(-1300, -144, -1249)
		Program.quakeLevelNode = n
		# add faerie
		Program.faerieNode = scene.AddAnimatedMeshSceneNode(scene.GetMesh("../../media/faerie.md2"), None, -1, Vector3Df(100, -40, 80), Vector3Df(0, 30, 0), Vector3Df(Single(1.6)))
		Program.faerieNode.SetMD2Animation(AnimationTypeMD2.Wave)
		Program.faerieNode.AnimationSpeed = 20
		Program.faerieNode.GetMaterial(0).SetTexture(0, driver.GetTexture("../../media/faerie2.bmp"))
		Program.faerieNode.GetMaterial(0).Lighting = False
		Program.faerieNode.GetMaterial(0).NormalizeNormals = True
		Program.shadows.AddObject(Program.faerieNode)
		# add light
		Program.lightMovementHelperNode = scene.AddEmptySceneNode()
		n = scene.AddSphereSceneNode(2, 6, Program.lightMovementHelperNode, -1, Vector3Df(15, -10, 15))
		n.SetMaterialFlag(MaterialFlag.Lighting, False)
		Program.lightNode = n
		Program.shadows.AddLight(Program.lightNode)
		# add flashlight
		m = scene.GetMesh("../../media/flashlight.obj")
		n = scene.AddMeshSceneNode(m, Program.lightNode, -1, Vector3Df(0), Vector3Df(0), Vector3Df(5))
		n.SetMaterialFlag(MaterialFlag.Lighting, False)
		Program.flashlightNode = n
		Program.flashlightNode.Visible = False
		# render
		shdFrameTime = 0
		shdFrames = 0
		shdFps = 0
		while Program.device.Run():
			if Program.useShadowsRebuilding and Program.shadows.BuildShadowVolume():
				shdFrames += 1
			t = Program.device.Timer.Time
			if t - shdFrameTime > 1000:
				shdFrameTime = t
				shdFps = shdFrames
				shdFrames = 0
			if Program.useLightBinding:
				Program.lightMovementHelperNode.Position = Program.cameraNode.AbsolutePosition.GetInterpolated(Program.lightMovementHelperNode.Position, 0.1)
				Program.lightMovementHelperNode.Rotation = Program.cameraNode.AbsoluteTransformation.Rotation
			driver.BeginScene(True, True, Color(UInt32(4279312964)))
			scene.DrawAll()
			if Program.useShadowsRendering:
				Program.shadows.DrawShadowVolume(driver)
			# display stats
			Program.device.VideoDriver.SetMaterial(statsMaterial)
			driver.Draw2DRectangle(Recti(10, 10, 150, 220), Color(0x7f000000))
			v = Vector2Di(20, 20)
			statsFont.Draw("Rendering", v, Color.OpaqueYellow)
			v.Y += 16
			statsFont.Draw(str(driver.FPS) + " fps", v, Color.OpaqueWhite)
			v.Y += 16
			statsFont.Draw("[S]hadows " + ("ON" if Program.useShadowsRendering else "OFF"), v, Color.OpaqueGreen)
			v.Y += 16
			statsFont.Draw("[L]ight binding " + ("ON" if Program.useLightBinding else "OFF"), v, Color.OpaqueGreen)
			v.Y += 16
			statsFont.Draw("[F]lashlight " + ("ON" if Program.useFlashlight else "OFF"), v, Color.OpaqueGreen)
			v.Y += 32
			statsFont.Draw("Shadows", v, Color.OpaqueYellow)
			v.Y += 16
			statsFont.Draw(str(shdFps) + " fps", v, Color.OpaqueWhite)
			v.Y += 16
			statsFont.Draw(str(Program.shadows.VerticesBuilt) + " vertices", v, Color.OpaqueWhite)
			v.Y += 16
			statsFont.Draw("[R]ebuilding " + ("ON" if Program.useShadowsRebuilding else "OFF"), v, Color.OpaqueGreen)
			v.Y += 16
			statsFont.Draw("[Q]uake level " + ("ON" if Program.useShadowsQuakeLevel else "OFF"), v, Color.OpaqueGreen)
			driver.EndScene()
		Program.shadows.Drop()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Key and evnt.Key.PressedDown:
			if evnt.Key.Key == KeyCode.KeyL:
				Program.useLightBinding = not Program.useLightBinding
				return True
			elif evnt.Key.Key == KeyCode.KeyS:
				Program.useShadowsRendering = not Program.useShadowsRendering
				return True
			elif evnt.Key.Key == KeyCode.KeyR:
				Program.useShadowsRebuilding = not Program.useShadowsRebuilding
				return True
			elif evnt.Key.Key == KeyCode.KeyQ:
				Program.useShadowsQuakeLevel = not Program.useShadowsQuakeLevel
				if Program.useShadowsQuakeLevel:
					Program.shadows.AddObject(Program.quakeLevelNode)
				else:
					Program.shadows.RemoveObject(Program.quakeLevelNode)
				return True
			elif evnt.Key.Key == KeyCode.KeyF:
				Program.useFlashlight = not Program.useFlashlight
				if Program.useFlashlight:
					Program.shadows.AddObject(Program.flashlightNode)
				else:
					Program.shadows.RemoveObject(Program.flashlightNode)
				Program.flashlightNode.Visible = Program.useFlashlight
				return True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

Program.Main(Environment.GetCommandLineArgs()[2:])