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

class Application(object):
	def __init__(self, dev):
		self._oldMouseX = 0
		self._oldMouseY = 0
		self._device = None
		self._texture = None
		self._sceneNodePainter = None
		self._textureRTT = None
		self._sceneNodeRTT = None
		self._guiWindow = None
		self._guiImage = None
		self._guiSize128 = None
		self._guiSize256 = None
		self._guiSize512 = None
		
		self._device = dev
		self._device.OnEvent += self.OnEvent
		self.initScene()
		self.initGUI(128)
		self.createTexture(128)

	def Render(self):
		drv = self._device.VideoDriver
		drv.SetRenderTarget(self._textureRTT, True, True, Color(20, 80, 180))
		self._sceneNodeRTT.Visible = False
		self._device.SceneManager.DrawAll()
		self._device.GUIEnvironment.DrawAll()
		drv.SetRenderTarget(RenderTarget.FrameBuffer, True, True, Color(40, 180, 240))
		self._sceneNodeRTT.Visible = True
		self._device.SceneManager.DrawAll()
		self._device.GUIEnvironment.DrawAll()

	def initScene(self):
		smgr = self._device.SceneManager
		m = smgr.AddHillPlaneMesh("plane", Dimension2Df(16), Dimension2Di(16), None, 8)
		self._sceneNodePainter = smgr.AddAnimatedMeshSceneNode(m)
		self._sceneNodePainter.Scale = Vector3Df(Single(0.4))
		self._sceneNodePainter.SetMaterialTexture(0, self._texture)
		self._sceneNodePainter.SetMaterialFlag(MaterialFlag.Lighting, False)
		a = smgr.CreateRotationAnimator(Vector3Df(0, Single(0.1), 0))
		self._sceneNodePainter.AddAnimator(a)
		a.Drop()
		self._sceneNodeRTT = smgr.AddWaterSurfaceSceneNode(m.GetMesh(0), 2, 100, 20)
		self._sceneNodeRTT.SetMaterialFlag(MaterialFlag.Lighting, False)
		self._sceneNodeRTT.SetMaterialType(MaterialType.Solid)
		self._sceneNodeRTT.Scale = Vector3Df(Single(0.2))
		self._sceneNodeRTT.Position = Vector3Df(60, 10, 40)
		self._sceneNodeRTT.Rotation = Vector3Df(-30, 20, 0)
		self._textureRTT = smgr.VideoDriver.AddRenderTargetTexture(Dimension2Di(512))
		self._sceneNodeRTT.SetMaterialTexture(0, self._textureRTT)
		smgr.AddCameraSceneNode(None, Vector3Df(0, 40, -60), Vector3Df(0, -15, 0))

	def initGUI(self, size):
		gui = self._device.GUIEnvironment
		drv = gui.VideoDriver
		gui.Clear()
		gui.AddImage(drv.GetTexture("../../media/lime_logo_alpha.png"), Vector2Di(30, 0))
		self._guiWindow = gui.AddWindow(Recti(20, 120, size + 20 + 20, size + 120 + 20 + 20 + 30), False, "Paint")
		self._guiSize128 = gui.AddButton(Recti(10, 30, 40, 30 + 20), self._guiWindow, -1, "128")
		self._guiSize256 = gui.AddButton(Recti(50, 30, 80, 30 + 20), self._guiWindow, -1, "256")
		self._guiSize512 = gui.AddButton(Recti(90, 30, 120, 30 + 20), self._guiWindow, -1, "512")
		self._guiImage = gui.AddImage(Recti(10, 30 + 30, size + 10 - 1, size + 30 - 1 + 30), True, self._guiWindow)
		gui.Focus = self._guiImage

	def createTexture(self, size):
		drv = self._device.VideoDriver
		o = self._texture
		self._texture = drv.AddTexture(Dimension2Di(size), "tex")
		p = self._texture.Painter
		p.Lock(TextureLockMode.WriteOnly)
		for i in xrange(0,p.MipMapLevelHeight,1):
			p.SetLine(0, i, p.MipMapLevelWidth - 1, i, Color(200, 200, 200))
		p.Unlock(True)
		self._guiImage.Image = self._texture
		self._sceneNodePainter.SetMaterialTexture(0, self._texture)
		if o != None:
			drv.RemoveTexture(o)

	def OnEvent(self, e):
		if e.Type == EventType.Mouse:
			x = e.Mouse.X
			y = e.Mouse.Y
			l = e.Mouse.IsLeftPressed()
			if l and self._guiImage.AbsolutePosition.IsPointInside(Vector2Di(x, y)):
				p = Vector2Di(x, y) - self._guiImage.AbsolutePosition.UpperLeftCorner
				if e.Mouse.Type == MouseEventType.Move:
					t = self._texture.Painter
					if p.X < self._texture.Size.Width and p.Y < self._texture.Size.Height and t.Lock(TextureLockMode.WriteOnly):
						t.SetLine(self._oldMouseX, self._oldMouseY, p.X, p.Y, Color(255, 0, 0))
						t.Unlock(True)
				self._oldMouseX = p.X
				self._oldMouseY = p.Y
				return True
		if e.Type == EventType.GUI:
			if e.GUI.Type == GUIEventType.ElementClosed and isinstance(e.GUI.Caller,GUIWindow):
				self._device.Close()
				return True
			if e.GUI.Type == GUIEventType.ButtonClicked:
				if e.GUI.Caller == self._guiSize128:
					self.initGUI(128)
					self.createTexture(128)
					return True
				if e.GUI.Caller == self._guiSize256:
					self.initGUI(256)
					self.createTexture(256)
					return True
				if e.GUI.Caller == self._guiSize512:
					self.initGUI(512)
					self.createTexture(512)
					return True
		return False