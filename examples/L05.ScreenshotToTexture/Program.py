import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Data")
clr.AddReferenceByPartialName("System.Drawing")
clr.AddReferenceByPartialName("System.Windows.Forms")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Drawing import *
from System.Drawing.Imaging import *
from System.Windows.Forms import * # for SystemInformation only
from System.IO import *
from IrrlichtLime import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
from IrrlichtLime.IO import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Video import Color as VColor

class Program(object):
	def Main(args):
		device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(512, 512))
		device.SetWindowCaption("Screenshot to texture - Irrlicht Lime")
		print device
		# set up very simple scene {{
		cam = device.SceneManager.AddCameraSceneNode()
		cam.Target = Vector3Df(0)
		anim = device.SceneManager.CreateFlyCircleAnimator(Vector3Df(0, 16, 0), 30, Single(0.0004))
		cam.AddAnimator(anim)
		anim.Drop()
		cube = device.SceneManager.AddCubeSceneNode(20)
		cube.SetMaterialFlag(MaterialFlag.Lighting, False)
		# }}
		while device.Run():
			cube.SetMaterialTexture(0, None)
			device.VideoDriver.RemoveAllTextures()
			t = Program.getDesktopTexture(device)
			cube.SetMaterialTexture(0, t)
			device.VideoDriver.BeginScene(False)
			device.VideoDriver.Draw2DImage(t, device.VideoDriver.ViewPort, Recti(Vector2Di(0), t.Size))
			device.VideoDriver.Draw2DRectangle(device.VideoDriver.ViewPort, VColor(0, 0, 0, 160))
			device.SceneManager.DrawAll()
			device.GUIEnvironment.BuiltInFont.Draw(device.Timer.ToString() 
				+ "\nMemory: " + (System.Diagnostics.Process.GetCurrentProcess().WorkingSet64 / (1 << 20)).ToString() + " Mb" 
				+ "\nFPS: " + device.VideoDriver.FPS.ToString(), Vector2Di(16), VColor(255, 255, 255))
			device.VideoDriver.EndScene()
		device.Drop()

	Main = staticmethod(Main)

	def getDesktopTexture(device):
		screenX = 0
		screenY = 0
		screenWidth = device.VideoDriver.ScreenSize.Width
		screenHeight = device.VideoDriver.ScreenSize.Height
		p = Program.GetCursorPos()
		screenX = p.X - screenWidth / 2
		screenY = p.Y - screenHeight / 2
		# validate grabbing rect (note: works fine without validation too) {{
		if screenX < 0:
			screenX = 0
		if screenX + screenWidth > SystemInformation.VirtualScreen.Width:
			screenX = SystemInformation.VirtualScreen.Width - screenWidth
		if screenY < 0:
			screenY = 0
		if screenY + screenHeight > SystemInformation.VirtualScreen.Height:
			screenY = SystemInformation.VirtualScreen.Height - screenHeight
		# }}
		b = Bitmap(screenWidth, screenHeight, PixelFormat.Format32bppArgb)
		g = Graphics.FromImage(b)
		g.CopyFromScreen(screenX, screenY, 0, 0, Size(screenWidth, screenHeight), CopyPixelOperation.SourceCopy)
		s = MemoryStream()
		b.Save(s, ImageFormat.Bmp)
		c = s.ToArray()
		s.Close()
		o = device.Logger.LogLevel
		device.Logger.LogLevel = LogLevel.Error # we hide all those "Loaded texture" messages in console {{
		f = device.FileSystem.CreateMemoryReadFile("screenTexture", c)
		t = device.VideoDriver.GetTexture(f)
		f.Drop()
		device.Logger.LogLevel = o # }}
		return t

	getDesktopTexture = staticmethod(getDesktopTexture)

	def GetCursorPos():
		return Cursor.Position
	GetCursorPos = staticmethod(GetCursorPos)

Program.Main(Environment.GetCommandLineArgs()[2:])