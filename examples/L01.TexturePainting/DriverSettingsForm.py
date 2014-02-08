import clr
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.GUI import *
import IrrlichtLime.Video

class DriverSettingsForm(object):
	def get_DriverType(self):
		return self._driverType

	DriverType = property(fget=get_DriverType)

	def get_VideoMode(self):
		return self._videoMode

	VideoMode = property(fget=get_VideoMode)

	def get_Fullscreen(self):
		return self._fullscreen

	Fullscreen = property(fget=get_Fullscreen)

	def __init__(self, windowCaption, aboutText):
		# default settings {
		self._driverType = IrrlichtLime.Video.DriverType.Direct3D9
		self._videoMode = IrrlichtLime.Video.VideoMode(800, 600, 32)
		self._fullscreen = False
		# }
		self._run = False
		self._windowCaption = windowCaption
		self._aboutText = aboutText

	def ShowDialog(self):
		self._device = IrrlichtDevice.CreateDevice(IrrlichtLime.Video.DriverType.BurningsVideo, Dimension2Di(320, 320))
		self._device.FileSystem.AddFileArchive("../../media/")
		self._device.OnEvent += self.device_OnEvent
		self._device.SetWindowCaption(self._windowCaption)
		self.initGUI()
		while self._device.Run():
			self._device.VideoDriver.BeginScene(True, False, IrrlichtLime.Video.Color(40, 180, 80))
			self._device.GUIEnvironment.DrawAll()
			self._device.VideoDriver.EndScene()
		self._device.Drop()
		return self._run

	def initGUI(self):
		gui = self._device.GUIEnvironment
		gui.Skin.SetFont(gui.GetFont("fontlucida.png"))
		for c in Enum.GetValues(clr.GetClrType(GUIDefaultColor)):
			l = gui.Skin.GetColor(c)
			l.Alpha = 255
			gui.Skin.SetColor(l, c)
		v = self._device.VideoDriver.ViewPort
		tc = gui.AddTabControl(Recti(20, 20, v.Width - 20, v.Height - 70))
		t1 = tc.AddTab("Setup")
		gui.AddStaticText("Driver", Recti(20, 20, v.Width - 60, 40), False, False, t1)
		self._guiDriverType = gui.AddComboBox(Recti(20, 40, v.Width - 60, 60), t1)
		for t in Enum.GetValues(clr.GetClrType(IrrlichtLime.Video.DriverType)):
			if t == IrrlichtLime.Video.DriverType.Null:
				continue
			i = self._guiDriverType.AddItem(t.ToString(), int(t))
			if t == self._driverType:
				self._guiDriverType.SelectedIndex = i
		gui.AddStaticText("Resolution", Recti(20, 70, v.Width - 60, 90), False, False, t1)
		self._guiResolution = gui.AddComboBox(Recti(20, 90, v.Width - 60, 110), t1)
		for m in self._device.VideoModeList.ModeList:
			i = self._guiResolution.AddItem(m.ToString())
			if m.Resolution == self._videoMode.Resolution and m.Depth == self._videoMode.Depth:
				self._guiResolution.SelectedIndex = i
		self._guiFullscreen = gui.AddCheckBox(self._fullscreen, Recti(20, 130, v.Width - 60, 150), "Fullscreen", t1)
		t2 = tc.AddTab("About")
		gui.AddStaticText(self._aboutText, Recti(20, 20, v.Width - 60, 180), False, True, t2)
		self._guiButtonRun = gui.AddButton(Recti(v.Width - 190, v.Height - 50, v.Width - 110, v.Height - 20), None, -1, "Run")
		self._guiButtonExit = gui.AddButton(Recti(v.Width - 100, v.Height - 50, v.Width - 20, v.Height - 20), None, -1, "Exit")

	def device_OnEvent(self, e):
		if e.Type == EventType.GUI:
			if e.GUI.Type == GUIEventType.ButtonClicked:
				if e.GUI.Caller == self._guiButtonRun:
					i = self._guiDriverType.GetItemData(self._guiDriverType.SelectedIndex)
					self._driverType = Enum.ToObject(IrrlichtLime.Video.DriverType,i)
					self._videoMode = self._device.VideoModeList.ModeList[self._guiResolution.SelectedIndex]
					self._fullscreen = self._guiFullscreen.Checked
					self._run = True
					self._device.Close()
					return True
				if e.GUI.Caller == self._guiButtonExit:
					self._run = False
					self._device.Close()
					return True
		return False