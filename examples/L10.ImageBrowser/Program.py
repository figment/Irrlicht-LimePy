import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Data")
clr.AddReferenceByPartialName("System.Windows.Forms")
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.IO import *
from System.Threading import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *
from AnimationManager import *
from TextureManager import *
from IrrDevice import *

class Program(object):
	irr = None
	textureManager = None
	animationManager = None
	wantChangeFolder = False
	wantUpdateActiveCameraAspectRatio = False
	PreviewTextureSize = Dimension2Di(128)
	maxScrollPosition = 0
	tasksAddedToTextureManager = 0
	TextureManagerThreadCount = 4
	PreviewPlateSize = 80
	PreviewRootNodeId = 1001
	ChooseFolderButtonId = 1002
	CurrentFolderStaticTextId = 1003
	PreviewPlateMeshName = "previewPlate"
	PreviewPlateNodeIdFlag = 1 << 17
	SelectableNodeIdFlag = 1 << 18
	hoveredNode = None
	selectedNode = None
	previewPlateInfo = Dictionary[int, str]()
	def __init__(self):
		pass
	def Main(args):
		Program.irr = IrrDevice()
		Program.irr.CreateDevice(DriverType.Direct3D9, Dimension2Di(1024, 600))
		Program.animationManager = AnimationManager(Program.irr)
		Program.textureManager = TextureManager(Program.irr)
		Program.textureManager.OnTextureLoaded += Program.textureManager_OnTextureLoaded
		Program.irr.Lock()
		Program.irr.Device.SetWindowResizable(True)
		Program.irr.Device.OnEvent += Program.Device_OnEvent
		Program.irr.Scene.AddCameraSceneNode()
		Program.irr.Scene.AddEmptySceneNode(None, 1001)
		Program.irr.Scene.AddHillPlaneMesh("previewPlate", Dimension2Df(80), Dimension2Di(1))
		Program.initUI()
		Program.openFolder(Path.GetFullPath("../../media"))
		lastFPS = -1
		while Program.irr.Device.Run():
			Program.irr.Driver.BeginScene(True, True, Color(0x112233))
			Program.irr.Scene.DrawAll()
			if Program.selectedNode == None:
				Program.irr.GUI.DrawAll()
			Program.drawScrollPosition()
			Program.drawTextureManagerActivity()
			Program.drawPreviewPlateTooltip()
			Program.irr.Driver.EndScene()
			fps = Program.irr.Driver.FPS
			if lastFPS != fps:
				Program.irr.Device.SetWindowCaption(String.Format("Image Browser - Irrlicht Lime [{0}] fps: {1}", Program.irr.Driver.Name, fps))
				lastFPS = fps
			Program.irr.Unlock()
			Program.animationManager.Run()
			if Program.wantChangeFolder:
				Program.wantChangeFolder = False
				p = Program.irr.GUI.RootElement.GetElementFromID(1003).Text
				d = Windows.Forms.FolderBrowserDialog()
				d.SelectedPath = p
				if d.ShowDialog() == System.Windows.Forms.DialogResult.OK and d.SelectedPath != p:
					Program.openFolder(d.SelectedPath)
			if Program.wantUpdateActiveCameraAspectRatio:
				Program.wantUpdateActiveCameraAspectRatio = False
				Program.irr.Scene.ActiveCamera.AspectRatio = Program.irr.DriverNoCheck.ScreenSize.Width / Program.irr.DriverNoCheck.ScreenSize.Height
			Program.irr.Lock()
		Program.irr.Unlock()
		Program.textureManager.Stop()
		Program.animationManager.Clear()
		Program.irr.Drop()

	Main = staticmethod(Main)

	def textureManager_OnTextureLoaded(node, texture, sourceDimension):
		if texture.Size == Program.PreviewTextureSize or texture.Name.Path == "NoPreviewTexture":
			a = sourceDimension.Height / sourceDimension.Width
			Program.animationManager.Remove(node)
			Program.animationManager.Add(node, 400, Vector3Df(node.Position.X, 0, node.Position.Z), None, Vector3Df(1, 1, a))
			if texture.Name.Path != "NoPreviewTexture":
				Program.previewPlateInfo[node.ID] += "\n" + sourceDimension.ToString()
				node.ID |= 1 << 18

	textureManager_OnTextureLoaded = staticmethod(textureManager_OnTextureLoaded)

	def Device_OnEvent(evnt):
		if evnt.Type == EventType.GUI and evnt.GUI.Type == GUIEventType.ButtonClicked and evnt.GUI.Caller.ID == 1002:
			Program.wantChangeFolder = True
			return True
		if evnt.Type == EventType.Mouse and evnt.Mouse.Type == MouseEventType.Wheel and Program.selectedNode == None:
			p = Program.irr.Scene.ActiveCamera.Position
			t = Program.irr.Scene.ActiveCamera.Target
			s = Program.irr.Scene.ActiveCamera.Position.Z + evnt.Mouse.Wheel * 16
			if s < 0:
				s = 0
			if s > Program.maxScrollPosition:
				s = Program.maxScrollPosition
			t.Z = t.Z - p.Z + s
			p.Z = s
			Program.irr.Scene.ActiveCamera.Position = p
			Program.irr.Scene.ActiveCamera.Target = t
			return True
		if evnt.Type == EventType.Mouse and evnt.Mouse.Type == MouseEventType.Move and Program.selectedNode == None:
			n = Program.irr.Scene.SceneCollisionManager.GetSceneNodeFromScreenCoordinatesBB(Vector2Di(evnt.Mouse.X, evnt.Mouse.Y), 0, Program.irr.Scene.GetSceneNodeFromID(1001))
			if Program.hoveredNode != n:
				if Program.hoveredNode != None:
					Program.animationManager.Remove(Program.hoveredNode)
					Program.animationManager.Add(Program.hoveredNode, 500, Vector3Df(Program.hoveredNode.Position.X, Program.hoveredNode.Position.Y - 15, Program.hoveredNode.Position.Z), Vector3Df(0), Program.hoveredNode.Scale / Single(1.5))
				if n != None:
					Program.animationManager.Remove(n)
					Program.animationManager.Add(n, 40, Vector3Df(n.Position.X, n.Position.Y + 15, n.Position.Z), Vector3Df(-20, 0, 0), n.Scale * Single(1.5))
				Program.hoveredNode = n
			return True
		if evnt.Type == EventType.Mouse and evnt.Mouse.Type == MouseEventType.LeftUp and Program.hoveredNode != None and (Program.hoveredNode.ID & 1 << 18) == 1 << 18 and Program.selectedNode == None:
			Program.animationManager.Remove(Program.hoveredNode)
			m = Program.irr.Scene.MeshCache.GetMesh("previewPlate")
			n = Program.irr.Scene.AddMeshSceneNode(m)
			n.SetMaterialFlag(MaterialFlag.Lighting, False)
			n.Position = Program.hoveredNode.Position
			n.Rotation = Program.hoveredNode.Rotation
			n.Scale = Program.hoveredNode.Scale
			t = Program.hoveredNode.GetMaterial(0).GetTexture(0).Name.Path.Split('|')[0]
			d = Dimension2Di(2048)
			if d.Area > Program.irr.Driver.MaxTextureSize.Area:
				d = Program.irr.Driver.MaxTextureSize
			n.SetMaterialTexture(0, Program.hoveredNode.GetMaterial(0).GetTexture(0))
			Program.textureManager.LoadTexture(n, t, d, True) # TODO: this magic numbers should be calculated somehow # using current active camera info (like view matrix or projection one)
			Program.animationManager.Add(n, 200, Program.irr.Scene.ActiveCamera.AbsolutePosition + Vector3Df(0, -48, 40), Vector3Df(-Single(39.85), 0, 0), n.Scale * ((Program.irr.Scene.ActiveCamera.FOV - Single(0.125)) / n.Scale.Z))
			Program.selectedNode = n
			Program.hoveredNode.Visible = False
			Program.irr.GUI.RootElement.GetElementFromID(1002).Enabled = False
			return True
		if evnt.Type == EventType.Mouse and evnt.Mouse.Type == MouseEventType.LeftUp and Program.selectedNode != None and Program.selectedNode.GetMaterial(0).GetTexture(0) != Program.hoveredNode.GetMaterial(0).GetTexture(0):
			if Program.animationManager.IsAnimated(Program.selectedNode):
				return True
			t = Program.selectedNode.GetMaterial(0).GetTexture(0)
			if t != None:
				s = t.Name.Path
				Program.selectedNode.SetMaterialTexture(0, None)
				Program.textureManager.UnloadTexture(s)
			Program.selectedNode.Remove()
			Program.selectedNode = None
			Program.hoveredNode.Visible = True
			Program.irr.GUI.RootElement.GetElementFromID(1002).Enabled = True
			return True
		if evnt.Type == EventType.Log and evnt.Log.Text.StartsWith("Resizing window"):
			Program.wantUpdateActiveCameraAspectRatio = True
		return False

	Device_OnEvent = staticmethod(Device_OnEvent)

	def initUI():
		Program.irr.GUI.Skin.SetFont(Program.irr.GUI.GetFont("../../media/fontlucida.png"))
		Program.irr.GUI.AddButton(Recti(20, 10, 160, 40), None, 1002, "Choose folder...")
		t = Program.irr.GUI.AddStaticText("???", Recti(180, 10, Program.irr.Device.VideoDriver.ScreenSize.Width - 20, 40), False, False, None, 1003)
		t.SetTextAlignment(GUIAlignment.UpperLeft, GUIAlignment.Center)
		t.OverrideColor = Color.OpaqueWhite

	initUI = staticmethod(initUI)

	def openFolder(newFolder):
		Program.textureManager.Stop()
		Program.textureManager.Start(4)
		Program.textureManager.EnqueueUnloadingOfAllLoadedTextures()
		Program.animationManager.Clear()
		Program.previewPlateInfo.Clear()
		Program.irr.GUI.RootElement.GetElementFromID(1003).Text = newFolder
		p = Program.irr.Scene.GetSceneNodeFromID(1001)
		p.RemoveChildren()
		r = 10
		x = 0
		z = 0
		m = Program.irr.Scene.MeshCache.GetMesh("previewPlate")
		f = Directory.GetFiles(newFolder, "*.*", SearchOption.TopDirectoryOnly)
		for i in xrange(0,f.Length,1):
			x += 80 * Single(1.1)
			if (i % r) == 0:
				x = 0
				z += 80 * Single(1.1)
			n = Program.irr.Scene.AddMeshSceneNode(m, p, i | 1 << 17)
			n.SetMaterialFlag(MaterialFlag.Lighting, False)
			n.Position = Vector3Df(x, 1000, z)
			Program.textureManager.LoadTexture(n, f[i], Program.PreviewTextureSize)
			s = Program.irr.Scene.CreateTriangleSelector(n.Mesh, n)
			n.TriangleSelector = s
			s.Drop()
			Program.previewPlateInfo.Add(n.ID, Path.GetFileName(f[i]))
		Program.irr.Scene.ActiveCamera.Position = Vector3Df(80 * (r - 1) * Single(1.1) / 2, 6 * 80, 0)
		Program.irr.Scene.ActiveCamera.Target = Vector3Df(Program.irr.Scene.ActiveCamera.Position.X, 0, 80 * 5)
		Program.maxScrollPosition = (f.Length / r) * 80 * Single(1.1)
		Program.tasksAddedToTextureManager = Program.textureManager.GetCommandQueueLength()

	openFolder = staticmethod(openFolder)

	def drawScrollPosition():
		if Program.selectedNode != None:
			return 
		if Program.maxScrollPosition < 1:
			return 
		v = Program.irr.Driver
		if v.ScreenSize.Height < 200:
			return 
		p = Program.irr.Scene.ActiveCamera.Position.Z / Program.maxScrollPosition
		v.Draw2DLine(v.ScreenSize.Width - 26, 80, v.ScreenSize.Width - 26, v.ScreenSize.Height - 80, Color(UInt32(2286184089)))
		y = (v.ScreenSize.Height - 80 - 80 - 40) * (Single(1) - p)
		r = Recti(v.ScreenSize.Width - 30, y + 80, v.ScreenSize.Width - 23, y + 80 + 40)
		v.Draw2DRectangle(r, Color(UInt32(2286184089)))

	drawScrollPosition = staticmethod(drawScrollPosition)

	def drawTextureManagerActivity():
		if Program.selectedNode != None:
			return 
		if Program.tasksAddedToTextureManager == 0:
			return 
		l = Program.textureManager.GetCommandQueueLength()
		if l == 0:
			Program.tasksAddedToTextureManager = 0
			return 
		v = Program.irr.Driver
		p = (Program.tasksAddedToTextureManager - l) / Program.tasksAddedToTextureManager
		if p > 1:
			p = 1
		r = Recti(v.ScreenSize.Width - 140, 20, v.ScreenSize.Width - 24, 30)
		v.Draw2DRectangleOutline(r, Color(UInt32(2286184089)))
		r.Inflate(-4, -4)
		r.LowerRightCorner = Vector2Di(r.UpperLeftCorner.X + (r.Width * p), r.LowerRightCorner.Y)
		v.Draw2DRectangle(r, Color(UInt32(2286184089)))

	drawTextureManagerActivity = staticmethod(drawTextureManagerActivity)

	def drawPreviewPlateTooltip():
		if Program.hoveredNode == None or not Program.hoveredNode.Visible:
			return 
		k = Program.hoveredNode.ID
		t = Program.hoveredNode.GetMaterial(0).GetTexture(0)
		if t != None and t.Name.Path != "NoPreviewTexture":
			k = Program.hoveredNode.ID & (0xFFFFFFF ^ 1 << 18)
		s = Program.previewPlateInfo[k] if Program.previewPlateInfo.ContainsKey(k) else "???"
		if s != None:
			p = Program.irr.Device.CursorControl.Position + Vector2Di(16)
			f = Program.irr.GUI.Skin.GetFont(GUIDefaultFont.Default)
			d = f.GetDimension(s)
			d.Inflate(16, 12)
			r = Recti(p, d)
			v = Program.irr.Driver
			ax = r.LowerRightCorner.X - v.ScreenSize.Width
			ay = r.LowerRightCorner.Y - v.ScreenSize.Height
			if ax > 0 or ay > 0:
				if ax < 0:
					ax = 0
				if ay < 0:
					ay = 0
				r.Offset(-ax, -ay)
			v.Draw2DRectangle(r, Color(UInt32(3139580757)))
			v.Draw2DRectangleOutline(r, Color(UInt32(3141817719)))
			f.Draw(s, r.UpperLeftCorner + Vector2Di(8, 6), Color.OpaqueYellow)

	drawPreviewPlateTooltip = staticmethod(drawPreviewPlateTooltip)

Program.Main(Environment.GetCommandLineArgs()[2:])