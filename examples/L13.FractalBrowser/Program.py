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
from FractalGenerator import FractalGenerator

class Program(object):
	device = None
	fGen = None
	mouseMoveStart = None
	showHelp = False
	def __init__(self):
		pass
	def Main(args):
		Program.device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(1024, 768))
		if Program.device == None:
			return 
		Program.device.SetWindowCaption("Fractal Generator - Irrlicht Engine")
		Program.device.OnEvent += Program.device_OnEvent
		driver = Program.device.VideoDriver
		font = Program.device.GUIEnvironment.GetFont("../../media/fontlucida.png")
		fontBackgroundColor = Color(0x7f000000)
		fontNormalColor = Color.OpaqueWhite
		fontActionColor = Color.OpaqueYellow
		Program.fGen = FractalGenerator(Program.device)
		Program.fGen.Generate(Rectd(-driver.ScreenSize.Width / 250.0, -driver.ScreenSize.Height / 250.0, driver.ScreenSize.Width / 250.0, driver.ScreenSize.Height / 250.0))
		while Program.device.Run():
			driver.BeginScene(False)
			o = None
			if Program.mouseMoveStart != None:
				o = Program.device.CursorControl.Position - Program.mouseMoveStart
			w = Program.fGen.DrawAll(o)
			# draw stats
			driver.Draw2DRectangle(Recti(10, 10, 160, 56 + (16 if w < 1 else 0)), fontBackgroundColor)
			v = Vector2Di(20, 16)
			font.Draw("Max iterations: " + str(Program.fGen.GetMaxIterations()), v, fontNormalColor)
			v.Y = v.Y + 16
			font.Draw("Zoom: " + str(Program.fGen.GetZoomFactor().X) + "x", v, fontNormalColor)
			if w < 1:
				v.Y = v.Y + 16
				font.Draw("Computing: " + str(w * 100) + "%...", v, fontActionColor)
			# draw help
			h = driver.ScreenSize.Height
			driver.Draw2DRectangle(Recti(10, h - 130 if Program.showHelp else h - 40, 220 if Program.showHelp else 160, h - 10), fontBackgroundColor)
			v.Y = h - 34
			font.Draw("[F1] " + ("Hide" if Program.showHelp else "Show") + " help", v, fontNormalColor)
			if Program.showHelp:
				v.Y = h - 124
				font.Draw("[Mouse Left Button] Navigate", v, fontNormalColor)
				v.Y = v.Y + 16
				font.Draw("[Mouse Wheel] Zoom in/out", v, fontNormalColor)
				v.Y = v.Y + 16
				font.Draw("[+][-][*][/] Max iterations", v, fontNormalColor)
				v.Y = v.Y + 16
				font.Draw("[PrintScreen] Save screenshot", v, fontNormalColor)
				v.Y = v.Y + 16
				font.Draw("[Esc] Exit application", v, fontNormalColor)
			driver.EndScene()
			Program.device.Yield()
		Program.fGen.Drop()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Mouse:
			s = Program.device.VideoDriver.ScreenSize
			if evnt.Mouse.Type == MouseEventType.Wheel:
				r = Rectd()
				if evnt.Mouse.Wheel > 0:
					# zoom in
					x1 = evnt.Mouse.X - s.Width / 2 + evnt.Mouse.Wheel * s.Width / 10
					y1 = evnt.Mouse.Y - s.Height / 2 + evnt.Mouse.Wheel * s.Height / 10
					r.UpperLeftCorner = Program.fGen.GetWindowCoord(x1, y1)
					r.LowerRightCorner = Program.fGen.GetWindowCoord(2 * evnt.Mouse.X - x1, 2 * evnt.Mouse.Y - y1)
					Program.device.CursorControl.Position = Vector2Di(s.Width / 2, s.Height / 2)
				else:
					# zoom out
					x1 = s.Width / 10
					y1 = s.Height / 10
					r.UpperLeftCorner = Program.fGen.GetWindowCoord(-x1, -y1)
					r.LowerRightCorner = Program.fGen.GetWindowCoord(s.Width + x1, s.Height + y1)
				Program.fGen.Generate(r)
				return True
			if evnt.Mouse.Type == MouseEventType.LeftDown:
				Program.mouseMoveStart = Vector2Di(evnt.Mouse.X, evnt.Mouse.Y)
				return True
			if evnt.Mouse.Type == MouseEventType.LeftUp:
				p1 = Program.fGen.GetWindowCoord(evnt.Mouse.X, evnt.Mouse.Y)
				p2 = Program.fGen.GetWindowCoord(Program.mouseMoveStart.X, Program.mouseMoveStart.Y)
				r = Program.fGen.GetWindow() + p2 - p1
				Program.fGen.Generate(r)
				Program.mouseMoveStart = None
				return True
		if evnt.Type == EventType.Key:
			if evnt.Key.PressedDown:
				if evnt.Key.Key == KeyCode.Esc:
					Program.device.Close()
					return True
				if evnt.Key.Key == KeyCode.F1:
					Program.showHelp = not Program.showHelp
					return True
				if evnt.Key.Char == '+':
					Program.fGen.Generate(Program.fGen.GetMaxIterations() + 1)
					return True
				elif evnt.Key.Char == '-':
					Program.fGen.Generate(Program.fGen.GetMaxIterations() - 1)
					return True
				elif evnt.Key.Char == '*':
					Program.fGen.Generate(Program.fGen.GetMaxIterations() + 10)
					return True
				elif evnt.Key.Char == '/':
					Program.fGen.Generate(Program.fGen.GetMaxIterations() - 10)
					return True
			if evnt.Key.Key == KeyCode.PrintScreen: # PrintScreen never comes with "evnt.Key.PressedDown == true" so we process it without checking that
				n = "Screenshot-" + DateTime.Now.Ticks + ".png"
				i = Program.device.VideoDriver.CreateScreenShot()
				Program.device.VideoDriver.WriteImage(i, n)
				i.Drop()
				Program.device.Logger.Log("Screenshot saved as " + n)
				return True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

Program.Main(Environment.GetCommandLineArgs()[2:])