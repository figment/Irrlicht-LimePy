import System
from System import *
from System.Collections.Generic import *
from System.ComponentModel import *
from System.Drawing import *
from System.Data import *
from System.Linq import *
from System.Text import *
from System.Windows.Forms import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *

class WinFormsUserControl(UserControl):

	class Command(object):
		""" <summary>
		 Some simple class to store command data.
		 We will use it to send commands to rendering thread (like command to call VideoDriver.ResizeNotify())
		 </summary>
		"""
		def __init__(self):
			""" <summary>
			 Some simple class to store command data.
			 We will use it to send commands to rendering thread (like command to call VideoDriver.ResizeNotify())
			 </summary>
			"""
			self.Type = Kind.None
			self.Value = None
			pass

		class Kind(object):
			None = 0
			Resized = None + 1
		def SetCommand(self, type, value):
			self.Type = type
			self.Value = value

		def Clear(self):
			self.Type = Kind.None
			self.Value = None

	def __init__(self):
		self.Type = Kind.None
		self.Value = None
		pass
	# <summary>
	# Indicates that rendering thread is working.
	# </summary>
	def get_IsRendering(self):
		return backgroundWorker.IsBusy

	IsRendering = property(fget=get_IsRendering)

	# <summary>
	# Indicates that Irrlicht will be notifyed (or not) about resize of client area of this control.
	# </summary>
	def get_IsNotifyResizes(self):
		return self._isnotifyresizes

	def set_IsNotifyResizes(self, value):
		self._isnotifyresizes = value

	IsNotifyResizes = property(fget=get_IsNotifyResizes, fset=set_IsNotifyResizes)

	def Shutdown(self):
		""" <summary>
		 Shuts down rendering thread.
		 This method must be called before this controls is going to be released.
		 </summary>
		"""
		if backgroundWorker.IsBusy:
			backgroundWorker.CancelAsync()
			while backgroundWorker.IsBusy:
				Application.DoEvents()

	def OnResize(self, e):
		self.OnResize(e)
		if not self.IsNotifyResizes:
			return 
		Threading.Monitor.Enter(backgroundCommand)
		try:
			newSize = Dimension2Di(self._Width, self._Height)
			if newSize.Area > 0:
				backgroundCommand.SetCommand(Command.Kind.Resized, newSize)
		finally:
			Threading.Monitor.Exit(backgroundCommand)

	def backgroundWorker_DoWork(self, sender, e):
		worker = sender
		p = IrrlichtCreationParameters()
		p.DriverType = DriverType.Direct3D9
		p.WindowID = e.Argument
		device = IrrlichtDevice.CreateDevice(p)
		if device == None:
			# if device cannot be created by any reason - we just leave this thread,
			# after all IsRedering will report false, so it is all OK.
			return 
		driver = device.VideoDriver
		smgr = device.SceneManager
		gui = device.GUIEnvironment
		# setup a simple 3d scene
		cam = smgr.AddCameraSceneNode()
		cam.Target = Vector3Df(0)
		anim = smgr.CreateFlyCircleAnimator(Vector3Df(0, 15, 0), Single(30))
		cam.AddAnimator(anim)
		anim.Drop()
		cube = smgr.AddCubeSceneNode(20)
		cube.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
		cube.SetMaterialTexture(1, driver.GetTexture("../../media/water.jpg"))
		cube.SetMaterialFlag(MaterialFlag.Lighting, False)
		cube.SetMaterialType(MaterialType.Reflection2Layer)
		smgr.AddSkyBoxSceneNode("../../media/irrlicht2_up.jpg", "../../media/irrlicht2_dn.jpg", "../../media/irrlicht2_lf.jpg", "../../media/irrlicht2_rt.jpg", "../../media/irrlicht2_ft.jpg", "../../media/irrlicht2_bk.jpg")
		gui.AddImage(driver.GetTexture("../../media/lime_logo_alpha.png"), Vector2Di(30, 0))
		# draw all
		while device.Run():
			driver.BeginScene(False)
			smgr.DrawAll()
			gui.DrawAll()
			# draw stats
			x = 20
			y = driver.ScreenSize.Height - 50
			driver.Draw2DRectangle(Recti(x, y, x + driver.ScreenSize.Width - 2 * x, y + 30), Color(0, 0, 0, 128))
			device.GUIEnvironment.BuiltInFont.Draw("Driver: " + driver.Name, Vector2Di(x + 5, y + 5), Color(255, 255, 255))
			device.GUIEnvironment.BuiltInFont.Draw("FPS: " + driver.FPS.ToString(), Vector2Di(x + 5, y + 15), Color(255, 255, 255))
			driver.EndScene()
			# check for cancellation
			if worker.CancellationPending:
				device.Close()
			# check for new command
			Threading.Monitor.Enter(backgroundCommand)
			try:
				if backgroundCommand.Type == Command.Kind.Resized:
					driver.ResizeNotify(backgroundCommand.Value)
					backgroundCommand.Clear()
			finally:
				Threading.Monitor.Exit(backgroundCommand)
		# drop the device
		device.Drop()