import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("System.Data")
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
from Game import *

class Program(object):
	TextStart = "PRESS [ESC] FOR GAME MENU"
	TextLost = "YOU LOST\n" + "PRESS [ESC] FOR GAME MENU"
	TextWon = "YOU WON\n" + "PRESS [ESC] FOR GAME MENU"
	device = None
	camera = None
	light = None
	text = None
	window = None
	game = None
	optionShadows = True
	optionBackground = True
	optionFPS = False

	def Main(args):
		Program.device = IrrlichtDevice.CreateDevice(DriverType.OpenGL, Dimension2Di(1024, 768), 32, False, True)
		Program.device.OnEvent += Program.device_OnEvent
		Program.device.SetWindowCaption("Minesweeper - Irrlicht Engine")
		driver = Program.device.VideoDriver
		scene = Program.device.SceneManager
		gui = Program.device.GUIEnvironment
		Program.device.FileSystem.AddFileArchive("../../media/minesweeper.media.files")
		Program.game = Game(Program.device)
		# set up camera
		Program.camera = scene.AddCameraSceneNode() # Maya(null, -500, 50, 200);
		Program.setupCameraPositionAndTarget()
		# set up background
		m = scene.GetMesh("back.obj")
		scene.MeshManipulator.Scale(m, Vector3Df(80))
		scene.MeshManipulator.FlipSurfaces(m)
		scene.MeshManipulator.RecalculateNormals(m)
		scene.MeshManipulator.SetVertexColors(m, Color(80, 80, 80))
		t = Material()
		t.Type = MaterialType.Reflection2Layer
		t.Lighting = False
		t.SetTexture(0, Program.device.VideoDriver.GetTexture("TEXTURE-ref.jpg"))
		t.SetTexture(1, Program.device.VideoDriver.GetTexture("TEXTURE-ref.jpg"))
		n = scene.AddMeshSceneNode(m, None, 7777)
		n.SetMaterial(0, t)
		n.Position = Program.game.CenterOfTheBoard
		a = scene.CreateRotationAnimator(Vector3Df(Single(0.07), Single(0.01), Single(0.05)))
		n.AddAnimator(a)
		a.Drop()
		# set up light
		Program.light = scene.AddLightSceneNode(None, Program.game.CenterOfTheBoard, Colorf(1, 1, 1), 200)
		m = scene.AddVolumeLightMesh("lvol1", 32, 32, Color(5, 5, 5))
		scene.MeshManipulator.Scale(m, Vector3Df(15, 30, 15))
		n = scene.AddMeshSceneNode(m, Program.light)
		n.Position = Vector3Df(0, -10, 0)
		n.Rotation = Vector3Df(180, 0, 0)
		n.SetMaterialType(MaterialType.TransparentAddColor)
		m = scene.AddVolumeLightMesh("lvol2", 32, 32, Color(5, 5, 5))
		scene.MeshManipulator.Scale(m, Vector3Df(15, 30, 15))
		n = scene.AddMeshSceneNode(m, Program.light)
		n.Position = Vector3Df(0, -10, 0)
		n.SetMaterialType(MaterialType.TransparentAddColor)
		# add gui hint
		Program.text = gui.AddStaticText("PRESS [ESC] FOR GAME MENU", Recti(10, 10, 200, 40))
		Program.text.OverrideColor = Color.OpaqueYellow
		# main loop
		while Program.device.Run():
			driver.BeginScene()
			scene.DrawAll()
			gui.DrawAll()
			if Program.optionFPS:
				gui.BuiltInFont.Draw(str(driver.FPS) + " FPS", driver.ScreenSize.Width - 50, 10, Color.OpaqueWhite)
			driver.EndScene()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Mouse and evnt.Mouse.Type == MouseEventType.Move:
			m = Vector2Di(evnt.Mouse.X, evnt.Mouse.Y)
			l = Program.device.SceneManager.SceneCollisionManager.GetRayFromScreenCoordinates(m)
			p = Plane3Df(Vector3Df(0, 0, 0), Vector3Df(100, 0, 0), Vector3Df(0, 0, 100))
			_tmp119_41, i = p.GetIntersectionWithLimitedLine(l.Start, l.End)
			if _tmp119_41:
				Program.camera.Target = Program.game.CenterOfTheBoard + Vector3Df((m.Y - Program.device.VideoDriver.ScreenSize.Height / 2) / Single(100), 0, (m.X - Program.device.VideoDriver.ScreenSize.Width / 2) / Single(100))
				i.Y += 25 # we want light to be a little bit above
				Program.light.Position = i
		if Program.window == None and evnt.Type == EventType.Mouse and (evnt.Mouse.Type == MouseEventType.LeftDown or evnt.Mouse.Type == MouseEventType.RightDown):
			Program.text.Visible = False # if user started to play - remove the gui text
			Program.game.MouseClick(evnt.Mouse.X, evnt.Mouse.Y, evnt.Mouse.Type == MouseEventType.RightDown)
			if Program.game.StateOfTheGame != Game.State.Playing:
				Program.text.Visible = True
				Program.text.Text = "YOU WON\n" + "PRESS [ESC] FOR GAME MENU" if Program.game.StateOfTheGame == Game.State.Won else "YOU LOST\n" + "PRESS [ESC] FOR GAME MENU"
			return True
		if evnt.Type == EventType.Key and evnt.Key.PressedDown and evnt.Key.Key == KeyCode.Esc:
			if Program.window != None:
				Program.window.Remove()
				Program.window = None
				return True
			gui = Program.device.GUIEnvironment
			Program.window = gui.AddWindow(Recti(100, 100, 400, 400), True, "GAME MENU")
			gui.AddButton(Recti(20, 40, Program.window.ClientRect.Width - 20, 60), Program.window, 1510, "NEW GAME 5x5")
			gui.AddButton(Recti(20, 60, Program.window.ClientRect.Width - 20, 80), Program.window, 1520, "NEW GAME 10x10")
			gui.AddButton(Recti(20, 80, Program.window.ClientRect.Width - 20, 100), Program.window, 1530, "NEW GAME 15x15")
			gui.AddButton(Recti(20, 100, Program.window.ClientRect.Width - 20, 120), Program.window, 1540, "NEW GAME 20x20")
			gui.AddCheckBox(Program.optionShadows, Recti(20, 140, Program.window.ClientRect.Width - 20, 160), "SHOW REALTIME SHADOWS", Program.window, 1710)
			gui.AddCheckBox(Program.optionBackground, Recti(20, 160, Program.window.ClientRect.Width - 20, 180), "SHOW BACKGROUND", Program.window, 1720)
			gui.AddCheckBox(Program.optionFPS, Recti(20, 180, Program.window.ClientRect.Width - 20, 200), "SHOW FPS", Program.window, 1730)
			gui.AddButton(Recti(20, 260, Program.window.ClientRect.Width - 20, 280), Program.window, 1590, "EXIT GAME")
			return True
		if Program.window != None and evnt.Type == EventType.GUI:
			if evnt.GUI.Caller == Program.window and evnt.GUI.Type == GUIEventType.ElementClosed:
				Program.window.Remove()
				Program.window = None
				return True
			if evnt.GUI.Caller.ID == 1510 and evnt.GUI.Type == GUIEventType.ButtonClicked:
				Program.window.Remove()
				Program.window = None
				Program.game.NewGame(5, 5)
				Program.setupCameraPositionAndTarget()
				return True
			if evnt.GUI.Caller.ID == 1520 and evnt.GUI.Type == GUIEventType.ButtonClicked:
				Program.window.Remove()
				Program.window = None
				Program.game.NewGame(10, 10)
				Program.setupCameraPositionAndTarget()
				return True
			if evnt.GUI.Caller.ID == 1530 and evnt.GUI.Type == GUIEventType.ButtonClicked:
				Program.window.Remove()
				Program.window = None
				Program.game.NewGame(15, 15)
				Program.setupCameraPositionAndTarget()
				return True
			if evnt.GUI.Caller.ID == 1540 and evnt.GUI.Type == GUIEventType.ButtonClicked:
				Program.window.Remove()
				Program.window = None
				Program.game.NewGame(20, 20)
				Program.setupCameraPositionAndTarget()
				return True
			if evnt.GUI.Caller.ID == 1590 and evnt.GUI.Type == GUIEventType.ButtonClicked:
				Program.device.Close()
				return True
			if evnt.GUI.Caller.ID == 1710 and evnt.GUI.Type == GUIEventType.CheckBoxChanged:
				Program.optionShadows = (evnt.GUI.Caller).Checked
				Program.light.CastShadows = Program.optionShadows
				return True
			if evnt.GUI.Caller.ID == 1720 and evnt.GUI.Type == GUIEventType.CheckBoxChanged:
				Program.optionBackground = (evnt.GUI.Caller).Checked
				Program.device.SceneManager.GetSceneNodeFromID(7777).Visible = Program.optionBackground
				return True
			if evnt.GUI.Caller.ID == 1730 and evnt.GUI.Type == GUIEventType.CheckBoxChanged:
				Program.optionFPS = (evnt.GUI.Caller).Checked
				return True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def setupCameraPositionAndTarget():
		Program.camera.Position = Program.game.CenterOfTheBoard + Vector3Df(Program.game.CenterOfTheBoard.X, Program.game.CenterOfTheBoard.X * Single(1.5), 0)
		Program.camera.Target = Program.game.CenterOfTheBoard

	setupCameraPositionAndTarget = staticmethod(setupCameraPositionAndTarget)

Program.Main(Environment.GetCommandLineArgs()[2:])