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
	device = None
	listbox = None
	winPosCounter = 0
	GUI_ID_ButtonQuit = 101
	GUI_ID_ButtonWindowNew = 102
	GUI_ID_ButtonFileOpen = 103
	GUI_ID_ScrollbarTransparency = 104
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		Program.device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if Program.device == None:
			return 
		Program.device.SetWindowCaption("Irrlicht Engine - User Interface Demo")
		Program.device.SetWindowResizable(True)
		driver = Program.device.VideoDriver
		env = Program.device.GUIEnvironment
		skin = env.Skin
		font = env.GetFont("../../media/fonthaettenschweiler.bmp")
		if font != None:
			skin.SetFont(font)
		skin.SetFont(env.BuiltInFont, GUIDefaultFont.Tooltip)
		env.AddButton(Recti(10, 240, 110, 240 + 32), None, 101, "Quit", "Exits Program")
		env.AddButton(Recti(10, 280, 110, 280 + 32), None, 102, "New Window", "Launches a new Window")
		env.AddButton(Recti(10, 320, 110, 320 + 32), None, 103, "File Open", "Opens a file")
		env.AddStaticText("Transparent Control:", Recti(150, 20, 350, 40), True)
		scrollbar = env.AddScrollBar(True, Recti(150, 45, 350, 60), None, 104)
		scrollbar.MaxValue = 255
		scrollbar.Position = env.Skin.GetColor(GUIDefaultColor.WindowBackground).Alpha
		trq = env.AddStaticText("Logging ListBox:", Recti(50, 110, 250, 130), True)
		Program.listbox = env.AddListBox(Recti(50, 140, 250, 210))
		env.AddEditBox("Editable Text", Recti(350, 80, 550, 100))
		Program.device.OnEvent += Program.device_OnEvent
		env.AddImage(driver.GetTexture("../../media/irrlichtlogoalpha2.tga"), Vector2Di(10, 10))
		while Program.device.Run():
			if Program.device.WindowActive:
				driver.BeginScene(True, True, Color(200, 200, 200))
				env.DrawAll()
				driver.EndScene()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(e):
		if e.Type == EventType.GUI:
			id = e.GUI.Caller.ID
			env = Program.device.GUIEnvironment
			if e.GUI.Type == GUIEventType.ScrollBarChanged:
				if id == 104:
					pos = (e.GUI.Caller).Position
					for which in Enum.GetValues(clr.GetClrType(GUIDefaultColor)):
						color = env.Skin.GetColor(which)
						color.Alpha = pos
						env.Skin.SetColor(color, which)
			elif e.GUI.Type == GUIEventType.ButtonClicked:
				if id == 101:
					Program.device.Close()
					return True
				elif id == 102:
					Program.listbox.AddItem("Window created")
					Program.winPosCounter += 30
					if Program.winPosCounter > 200:
						Program.winPosCounter = 0
					c = Program.winPosCounter
					window = env.AddWindow(Recti(100 + c, 100 + c, 300 + c, 200 + c), False, "Test window")
					env.AddStaticText("Please close me", Recti(35, 35, 140, 50), True, False, window)
					return True
				elif id == 103:
					Program.listbox.AddItem("File open")
					# There are some options for the file open dialog
					# We set the title, make it a modal window, and make sure
					# that the working directory is restored after the dialog
					# is finished.
					env.AddFileOpenDialog("Please choose a file", True, None, -1, True)
					return True
				else:
					return False
			elif e.GUI.Type == GUIEventType.FileDialogFileSelected:
				# show the filename, selected in the file dialog
				d = e.GUI.Caller
				Program.listbox.AddItem(d.FileName)
				pass #break
			else:
				pass
		return False

	device_OnEvent = staticmethod(device_OnEvent)

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