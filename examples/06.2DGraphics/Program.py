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
from IrrlichtLime.GUI import *

class Program(object):
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(512, 384))
		if device == None:
			return 
		device.SetWindowCaption("Irrlicht Engine - 2D Graphics Demo")
		driver = device.VideoDriver
		images = driver.GetTexture("../../media/2ddemo.png")
		driver.MakeColorKeyTexture(images, Vector2Di(0, 0))
		font = device.GUIEnvironment.BuiltInFont
		font2 = device.GUIEnvironment.GetFont("../../media/fonthaettenschweiler.bmp")
		imp1 = Recti(349, 15, 385, 78)
		imp2 = Recti(387, 15, 423, 78)
		driver.Material2D.Layer[0].BilinearFilter = True
		driver.Material2D.AntiAliasing = AntiAliasingMode.FullBasic
		while device.Run():
			if device.WindowActive:
				time = device.Timer.Time
				driver.BeginScene(True, True, Color(120, 102, 136))
				# draw fire & dragons background world
				driver.Draw2DImage(images, Vector2Di(50, 50), Recti(0, 0, 342, 224), None, Color(255, 255, 255), True)
				# draw flying imp
				driver.Draw2DImage(images, Vector2Di(164, 125), imp1 if (time / 500 % 2) == 1 else imp2, None, Color(255, 255, 255), True)
				# draw second flying imp with colorcylce
				driver.Draw2DImage(images, Vector2Di(270, 105), imp1 if (time / 500 % 2) == 1 else imp2, None, Color(time % 255, 255, 255), True)
				# draw some text
				if font != None:
					font.Draw("This demo shows that Irrlicht is also capable of drawing 2D graphics.", 130, 10, Color(255, 255, 255))
				# draw some other text
				if font2 != None:
					font2.Draw("Also mixing with 3d graphics is possible.", 130, 20, Color(time % 255, time % 255, 255))
				driver.EnableMaterial2D()
				driver.Draw2DImage(images, Recti(10, 10, 108, 48), Recti(354, 87, 442, 118))
				driver.EnableMaterial2D(False)
				m = device.CursorControl.Position
				driver.Draw2DRectangle(Recti(m.X - 20, m.Y - 20, m.X + 20, m.Y + 20), Color(255, 255, 255, 100))
				driver.EndScene()
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