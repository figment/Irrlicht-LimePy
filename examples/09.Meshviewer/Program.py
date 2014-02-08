import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.IO import *
from System.Xml import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *
from IrrlichtLime.IO import *

class guiID(object):
	DialogRootWindow = 0x10000
	XScale = DialogRootWindow + 1
	YScale = XScale + 1
	ZScale = YScale + 1
	OpenModel = ZScale + 1
	SetModelArchive = OpenModel + 1
	LoadAsOctree = SetModelArchive + 1
	SkyBoxVisible = LoadAsOctree + 1
	ToggleDebugInfo = SkyBoxVisible + 1
	DebugOff = ToggleDebugInfo + 1
	DebugBoundingBox = DebugOff + 1
	DebugNormals = DebugBoundingBox + 1
	DebugSkeleton = DebugNormals + 1
	DebugWireOverlay = DebugSkeleton + 1
	DebugHalfTransparent = DebugWireOverlay + 1
	DebugBuffersBoundingBoxes = DebugHalfTransparent + 1
	DebugAll = DebugBuffersBoundingBoxes + 1
	ModelMaterialSolid = DebugAll + 1
	ModelMaterialTransparent = ModelMaterialSolid + 1
	ModelMaterialReflection = ModelMaterialTransparent + 1
	CameraMaya = ModelMaterialReflection + 1
	CameraFirstPerson = CameraMaya + 1
	PositionText = CameraFirstPerson + 1
	About = PositionText + 1
	Quit = About + 1
	TextureFilter = Quit + 1
	SkinTransparency = TextureFilter + 1
	SkinAnimationFPS = SkinTransparency + 1
	ButtonSetScale = SkinAnimationFPS + 1
	ButtonScaleMul10 = ButtonSetScale + 1
	ButtonScaleDiv10 = ButtonScaleMul10 + 1
	ButtonOpenModel = ButtonScaleDiv10 + 1
	ButtonShowAbout = ButtonOpenModel + 1
	ButtonShowToolbox = ButtonShowAbout + 1
	ButtonSelectArchive = ButtonShowToolbox + 1
	Logo = ButtonSelectArchive + 1

class Program(object):
	device = None
	startUpModelFile = None
	messageText = None
	caption = None
	model = None
	skybox = None
	octree = False
	useLight = False
	camera = Array.CreateInstance(CameraSceneNode, 2)
	# Values used to identify individual GUI elements
	# And some magic numbers
	MaxFramerate = 1000
	DefaultFramerate = 30
	def __init__(self):
		pass
		
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		Program.device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(800, 600), 16)
		if Program.device == None:
			return 
		Program.device.OnEvent += Program.device_OnEvent
		Program.device.SetWindowResizable(True)
		Program.device.SetWindowCaption("Irrlicht Engine - Loading...")
		driver = Program.device.VideoDriver
		env = Program.device.GUIEnvironment
		smgr = Program.device.SceneManager
		smgr.Attributes.SetValue(SceneParameters.COLLADA_CreateSceneInstances, True)
		driver.SetTextureCreationFlag(TextureCreationFlag.Always32Bit, True)
		smgr.AddLightSceneNode(None, Vector3Df(200), Colorf(Single(1), Single(1), Single(1)), 2000)
		smgr.AmbientLight = Colorf(Single(0.3), Single(0.3), Single(0.3))
		# add our media directory as "search path"
		Program.device.FileSystem.AddFileArchive("../../media/")
		# read configuration from xml file
		# (we use .NET way to do this, since Lime doesn't support native Irrlicht' xml reader)
		xml = XmlDocument()
		xml.Load("../../media/config.xml")
		Program.startUpModelFile = xml.DocumentElement["startUpModel"].Attributes["file"].Value
		Program.caption = xml.DocumentElement["messageText"].Attributes["caption"].Value
		Program.messageText = xml.DocumentElement["messageText"].InnerText
		if args.Length > 0:
			Program.startUpModelFile = args[0]
		# set a nicer font
		font = env.GetFont("fonthaettenschweiler.bmp")
		if font != None:
			env.Skin.SetFont(font)
		# load the irrlicht engine logo
		img = env.AddImage(driver.GetTexture("irrlichtlogoalpha2.tga"), Vector2Di(10, driver.ScreenSize.Height - 128))
		img.ID = guiID.Logo
		# lock the logo's edges to the bottom left corner of the screen
		img.SetAlignment(GUIAlignment.UpperLeft, GUIAlignment.UpperLeft, GUIAlignment.LowerRight, GUIAlignment.LowerRight)
		# create menu
		menu = env.AddMenu()
		menu.AddItem("File", -1, True, True)
		menu.AddItem("View", -1, True, True)
		menu.AddItem("Camera", -1, True, True)
		menu.AddItem("Help", -1, True, True)
		submenu = menu.GetSubMenu(0)
		submenu.AddItem("Open Model File & Texture...", guiID.OpenModel)
		submenu.AddItem("Set Model Archive...", guiID.SetModelArchive)
		submenu.AddItem("Load as Octree", guiID.LoadAsOctree)
		submenu.AddSeparator()
		submenu.AddItem("Quit", guiID.Quit)
		submenu = menu.GetSubMenu(1)
		submenu.AddItem("sky box visible", guiID.SkyBoxVisible, True, False, True)
		submenu.AddItem("toggle model debug information", guiID.ToggleDebugInfo, True, True)
		submenu.AddItem("model material", -1, True, True)
		submenu = submenu.GetSubMenu(1)
		submenu.AddItem("Off", guiID.DebugOff)
		submenu.AddItem("Bounding Box", guiID.DebugBoundingBox)
		submenu.AddItem("Normals", guiID.DebugNormals)
		submenu.AddItem("Skeleton", guiID.DebugSkeleton)
		submenu.AddItem("Wire overlay", guiID.DebugWireOverlay)
		submenu.AddItem("Half-Transparent", guiID.DebugHalfTransparent)
		submenu.AddItem("Buffers bounding boxes", guiID.DebugBuffersBoundingBoxes)
		submenu.AddItem("All", guiID.DebugAll)
		submenu = menu.GetSubMenu(1).GetSubMenu(2)
		submenu.AddItem("Solid", guiID.ModelMaterialSolid)
		submenu.AddItem("Transparent", guiID.ModelMaterialTransparent)
		submenu.AddItem("Reflection", guiID.ModelMaterialReflection)
		submenu = menu.GetSubMenu(2)
		submenu.AddItem("Maya Style", guiID.CameraMaya)
		submenu.AddItem("First Person", guiID.CameraFirstPerson)
		submenu = menu.GetSubMenu(3)
		submenu.AddItem("About", guiID.About)
		# create toolbar
		bar = env.AddToolBar()
		image = driver.GetTexture("open.png")
		bar.AddButton(guiID.ButtonOpenModel, None, "Open a model", image, None, False, True)
		image = driver.GetTexture("tools.png")
		bar.AddButton(guiID.ButtonShowToolbox, None, "Open Toolset", image, None, False, True)
		image = driver.GetTexture("zip.png")
		bar.AddButton(guiID.ButtonSelectArchive, None, "Set Model Archive", image, None, False, True)
		image = driver.GetTexture("help.png")
		bar.AddButton(guiID.ButtonShowAbout, None, "Open Help", image, None, False, True)
		# create a combobox with some senseless texts
		box = env.AddComboBox(Recti(250, 4, 350, 23), bar, guiID.TextureFilter)
		box.AddItem("No filtering")
		box.AddItem("Bilinear")
		box.AddItem("Trilinear")
		box.AddItem("Anisotropic")
		box.AddItem("Isotropic")
		# disable alpha
		Program.setSkinTransparency(255, env.Skin)
		# add a tabcontrol
		Program.createToolBox()
		# create fps text
		fpstext = env.AddStaticText("", Recti(400, 4, 570, 23), True, False, bar)
		postext = env.AddStaticText("", Recti(10, 50, 470, 80), False, False, None, guiID.PositionText)
		postext.Visible = False
		# show about message box and load default model
		if args.Length == 0:
			Program.showAboutText()
		Program.loadModel(Program.startUpModelFile)
		# add skybox
		Program.skybox = smgr.AddSkyBoxSceneNode("irrlicht2_up.jpg", "irrlicht2_dn.jpg", "irrlicht2_lf.jpg", "irrlicht2_rt.jpg", "irrlicht2_ft.jpg", "irrlicht2_bk.jpg")
		# add a camera scene node
		Program.camera[0] = smgr.AddCameraSceneNodeMaya()
		Program.camera[0].FarValue = 20000
		# Maya cameras reposition themselves relative to their target,
		# so target the location where the mesh scene node is placed.
		Program.camera[0].Target = Vector3Df(0, 30, 0)
		Program.camera[1] = smgr.AddCameraSceneNodeFPS()
		Program.camera[1].FarValue = 20000
		Program.camera[1].Position = Vector3Df(0, 0, -70)
		Program.camera[1].Target = Vector3Df(0, 30, 0)
		Program.setActiveCamera(Program.camera[0])
		# set window caption
		Program.caption = String.Format("{0} - [{1}]", Program.caption, driver.Name)
		Program.device.SetWindowCaption(Program.caption)
		# remember state so we notice when the window does lose the focus
		hasFocus = Program.device.WindowFocused
		# draw everything
		while Program.device.Run() and driver != None:
			# Catch focus changes (workaround until Irrlicht has events for this)
			focused = Program.device.WindowFocused
			if hasFocus and not focused:
				Program.onKillFocus()
			hasFocus = focused
			if Program.device.WindowActive:
				driver.BeginScene(True, True, Color(50, 50, 50))
				smgr.DrawAll()
				env.DrawAll()
				driver.EndScene()
				str = String.Format("FPS: {0} Tris: {1}", driver.FPS, driver.PrimitiveCountDrawn)
				fpstext.Text = str
				cam = Program.device.SceneManager.ActiveCamera
				str = String.Format("Pos: {0} Tgt: {1}", cam.Position, cam.Target)
				postext.Text = str
			else:
				Program.device.Yield()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(e):
		# Escape swaps Camera Input
		if e.Type == EventType.Key and not e.Key.PressedDown and Program.OnKeyUp(e.Key.Key):
			return True
		if e.Type == EventType.GUI:
			id = e.GUI.Caller.ID
			env = Program.device.GUIEnvironment
			if e.GUI.Type == GUIEventType.MenuItemSelected:
				# a menu item was clicked
				Program.OnMenuItemSelected(e.GUI.Caller)
			elif e.GUI.Type == GUIEventType.FileDialogFileSelected:
				# load the model file, selected in the file open dialog
				Program.loadModel((e.GUI.Caller).FileName)
			elif e.GUI.Type == GUIEventType.ScrollBarChanged:
				if id == guiID.SkinTransparency:
					# control skin transparency
					p = (e.GUI.Caller).Position
					Program.setSkinTransparency(p, env.Skin)
				elif id == guiID.SkinAnimationFPS:
					# control animation speed
					p = (e.GUI.Caller).Position
					if Program.model.Type == SceneNodeType.AnimatedMesh:
						(Program.model).AnimationSpeed = p
			elif e.GUI.Type == GUIEventType.ComboBoxChanged:
				if id == guiID.TextureFilter:
					# control anti-aliasing/filtering
					Program.OnTextureFilterSelected(e.GUI.Caller)
			elif e.GUI.Type == GUIEventType.ButtonClicked:
				if id == guiID.ButtonSetScale:
					# set scale
					r = env.RootElement
					s = Vector3Df(Convert.ToSingle(r.GetElementFromID(guiID.XScale, True).Text), Convert.ToSingle(r.GetElementFromID(guiID.YScale, True).Text), Convert.ToSingle(r.GetElementFromID(guiID.ZScale, True).Text))
					if Program.model != None:
						Program.model.Scale = s
					Program.updateScaleInfo(Program.model)
				elif id == guiID.ButtonScaleMul10:
					if Program.model != None:
						Program.model.Scale *= 10
					Program.updateScaleInfo(Program.model)
				elif id == guiID.ButtonScaleDiv10:
					if Program.model != None:
						Program.model.Scale *= Single(0.1)
					Program.updateScaleInfo(Program.model)
				elif id == guiID.ButtonOpenModel:
					env.AddFileOpenDialog("Please select a model file to open")
				elif id == guiID.ButtonSelectArchive:
					env.AddFileOpenDialog("Please select your game archive/directory")
				elif id == guiID.ButtonShowAbout:
					Program.showAboutText()
				elif id == guiID.ButtonShowToolbox:
					Program.createToolBox() # case GUIEventType.ButtonClicked:
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def hasModalDialog():
		if Program.device == None:
			return False
		focused = Program.device.GUIEnvironment.Focus
		while focused != None:
			if focused.Visible and focused.Type == GUIElementType.ModalScreen:
				return True
			focused = focused.Parent
		return False

	hasModalDialog = staticmethod(hasModalDialog)

	def OnKeyUp(keyCode):
		if Program.device == None:
			return False
		if Program.hasModalDialog():
			return False
		if keyCode == KeyCode.Esc:
			c = Program.device.SceneManager.ActiveCamera
			if c != None:
				c.InputReceiverEnabled = not c.InputReceiverEnabled
			return True
		elif keyCode == KeyCode.F1:
			e = Program.device.GUIEnvironment.RootElement.GetElementFromID(guiID.PositionText)
			if e != None:
				e.Visible = not e.Visible
		elif keyCode == KeyCode.KeyM:
			Program.device.MinimizeWindow()
		elif keyCode == KeyCode.KeyL:
			Program.useLight = not Program.useLight
			if Program.model != None:
				Program.model.SetMaterialFlag(MaterialFlag.Lighting, Program.useLight)
				Program.model.SetMaterialFlag(MaterialFlag.NormalizeNormals, Program.useLight)
		return False

	OnKeyUp = staticmethod(OnKeyUp)

	def OnMenuItemSelected(menu):
		id = menu.SelectedCommandID
		env = Program.device.GUIEnvironment
		if id == guiID.OpenModel: # FilOnButtonSetScalinge -> Open Model
			env.AddFileOpenDialog("Please select a model file to open")
		elif id == guiID.SetModelArchive: # File -> Set Model Archive
			env.AddFileOpenDialog("Please select your game archive/directory")
		elif id == guiID.LoadAsOctree: # File -> LoadAsOctree
			Program.octree = not Program.octree
			menu.SetItemChecked(menu.SelectedIndex, Program.octree)
		elif id == guiID.Quit: # File -> Quit
			Program.device.Close()
		elif id == guiID.SkyBoxVisible: # View -> Skybox
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			Program.skybox.Visible = not Program.skybox.Visible
		elif id == guiID.DebugOff: # View -> Debug Information -> Off
			i = 1
			while i <= 6:
				menu.SetItemChecked(menu.SelectedIndex + i, False)
				i += 1
			if Program.model != None:
				Program.model.DebugDataVisible = DebugSceneType.Off
		elif id == guiID.DebugBoundingBox: # View -> Debug Information -> Bounding Box
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			if Program.model != None:
				Program.model.DebugDataVisible ^= DebugSceneType.BBox
		elif id == guiID.DebugNormals: # View -> Debug Information -> Normals
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			if Program.model != None:
				Program.model.DebugDataVisible ^= DebugSceneType.Normals
		elif id == guiID.DebugSkeleton: # View -> Debug Information -> Skeleton
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			if Program.model != None:
				Program.model.DebugDataVisible ^= DebugSceneType.Skeleton
		elif id == guiID.DebugWireOverlay: # View -> Debug Information -> Wire overlay
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			if Program.model != None:
				Program.model.DebugDataVisible ^= DebugSceneType.MeshWireOverlay
		elif id == guiID.DebugHalfTransparent: # View -> Debug Information -> Half-Transparent
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			if Program.model != None:
				Program.model.DebugDataVisible ^= DebugSceneType.HalfTransparency
		elif id == guiID.DebugBuffersBoundingBoxes: # View -> Debug Information -> Buffers bounding boxes
			menu.SetItemChecked(menu.SelectedIndex, not menu.GetItemChecked(menu.SelectedIndex))
			if Program.model != None:
				Program.model.DebugDataVisible ^= DebugSceneType.BBoxBuffers
		elif id == guiID.DebugAll: # View -> Debug Information -> All
			i = 1
			while i <= 6:
				menu.SetItemChecked(menu.SelectedIndex - i, True)
				i += 1
			if Program.model != None:
				Program.model.DebugDataVisible = DebugSceneType.Full
		elif id == guiID.About: # Help->About
			Program.showAboutText()
		elif id == guiID.ModelMaterialSolid: # View -> Material -> Solid
			if Program.model != None:
				Program.model.SetMaterialType(MaterialType.Solid)
		elif id == guiID.ModelMaterialTransparent: # View -> Material -> Transparent
			if Program.model != None:
				Program.model.SetMaterialType(MaterialType.TransparentAddColor)
		elif id == guiID.ModelMaterialReflection: # View -> Material -> Reflection
			if Program.model != None:
				Program.model.SetMaterialType(MaterialType.SphereMap)
		elif id == guiID.CameraMaya:
			Program.setActiveCamera(Program.camera[0])
		elif id == guiID.CameraFirstPerson:
			Program.setActiveCamera(Program.camera[1])

	OnMenuItemSelected = staticmethod(OnMenuItemSelected)

	def OnTextureFilterSelected(combo):
		if Program.model == None:
			return 
		p = combo.SelectedIndex
		if p == 0: # No filtering
			Program.model.SetMaterialFlag(MaterialFlag.BilinearFilter, False)
			Program.model.SetMaterialFlag(MaterialFlag.TrilinearFilter, False)
			Program.model.SetMaterialFlag(MaterialFlag.AnisotropicFilter, False)
		elif p == 1: # Bilinear
			Program.model.SetMaterialFlag(MaterialFlag.BilinearFilter, True)
			Program.model.SetMaterialFlag(MaterialFlag.TrilinearFilter, False)
		elif p == 2: # Trilinear
			Program.model.SetMaterialFlag(MaterialFlag.BilinearFilter, False)
			Program.model.SetMaterialFlag(MaterialFlag.TrilinearFilter, True)
		elif p == 3: # Anisotropic
			Program.model.SetMaterialFlag(MaterialFlag.AnisotropicFilter, True)
		elif p == 4: # Isotropic
			Program.model.SetMaterialFlag(MaterialFlag.AnisotropicFilter, False)

	OnTextureFilterSelected = staticmethod(OnTextureFilterSelected)

	def onKillFocus():
		# Avoid that the FPS-camera continues moving when the user presses alt-tab while moving the camera.
		for a in Program.camera[1].AnimatorList:
			f = a
			if f != None:
				# we send a key-down event for all keys used by this animator
				for l in f.KeyMap.Map.Values:
					for k in l:
						e = Event('\0', k, False)
						Program.device.PostEvent(e)

	onKillFocus = staticmethod(onKillFocus)

	def setActiveCamera(newActive):
		if Program.device == None:
			return 
		c = Program.device.SceneManager.ActiveCamera
		c.InputReceiverEnabled = False
		newActive.InputReceiverEnabled = True
		Program.device.SceneManager.ActiveCamera = newActive

	setActiveCamera = staticmethod(setActiveCamera)

	def setSkinTransparency(alpha, skin):
		for i in Enum.GetValues(clr.GetClrType(GUIDefaultColor)):
			c = skin.GetColor(i)
			c.Alpha = alpha
			skin.SetColor(c, i)

	setSkinTransparency = staticmethod(setSkinTransparency)

	def updateScaleInfo(model):
		t = Program.device.GUIEnvironment.RootElement.GetElementFromID(guiID.DialogRootWindow, True)
		if t == None:
			return 
		if model == None:
			t.GetElementFromID(guiID.XScale, True).Text = "-"
			t.GetElementFromID(guiID.YScale, True).Text = "-"
			t.GetElementFromID(guiID.ZScale, True).Text = "-"
		else:
			s = model.Scale
			t.GetElementFromID(guiID.XScale, True).Text = s.X.ToString()
			t.GetElementFromID(guiID.YScale, True).Text = s.Y.ToString()
			t.GetElementFromID(guiID.ZScale, True).Text = s.Z.ToString()

	updateScaleInfo = staticmethod(updateScaleInfo)

	def showAboutText():
		Program.device.GUIEnvironment.AddMessageBox(Program.caption, Program.messageText)

	showAboutText = staticmethod(showAboutText)

	def loadModel(f):
		e = Path.GetExtension(f)
		# if a texture is loaded apply it to the current model
		if e == ".jpg" or e == ".pcx" or e == ".png" or e == ".ppm" or e == ".pgm" or e == ".pbm" or e == ".psd" or e == ".tga" or e == ".bmp" or e == ".wal" or e == ".rgb" or e == ".rgba":
			t = Program.device.VideoDriver.GetTexture(f)
			if t != None and Program.model != None:
				# always reload texture
				Program.device.VideoDriver.RemoveTexture(t)
				t = Program.device.VideoDriver.GetTexture(f)
				Program.model.SetMaterialTexture(0, t)
			return 
		# if a archive is loaded add it to the FileArchive
		elif e == ".pk3" or e == ".zip" or e == ".pak" or e == ".npk":
			Program.device.FileSystem.AddFileArchive(f)
			return 
		# load a model into the engine
		if Program.model != None:
			Program.model.Remove()
		Program.model = None
		if e == ".irr":
			Program.device.SceneManager.LoadScene(f)
			Program.model = Program.device.SceneManager.GetSceneNodeFromType(SceneNodeType.AnimatedMesh)
			return 
		m = Program.device.SceneManager.GetMesh(f)
		if m == None:
			# model could not be loaded
			if Program.startUpModelFile != f:
				Program.device.GUIEnvironment.AddMessageBox(Program.caption, "The model could not be loaded. Maybe it is not a supported file format.")
			return 
		# set default material properties
		if Program.octree:
			Program.model = Program.device.SceneManager.AddOctreeSceneNode(m.GetMesh(0))
		else:
			n = Program.device.SceneManager.AddAnimatedMeshSceneNode(m)
			n.AnimationSpeed = 30
			Program.model = n
		Program.model.SetMaterialFlag(MaterialFlag.Lighting, Program.useLight)
		Program.model.SetMaterialFlag(MaterialFlag.NormalizeNormals, Program.useLight)
		Program.model.DebugDataVisible = DebugSceneType.Off
		# we need to uncheck the menu entries. would be cool to fake a menu event, but
		# that's not so simple. so we do it brute force
		u = Program.device.GUIEnvironment.RootElement.GetElementFromID(guiID.ToggleDebugInfo, True)
		if u != None:
			for i in xrange(0,6,1):
				u.SetItemChecked(i, False)
		Program.updateScaleInfo(Program.model)

	loadModel = staticmethod(loadModel)

	def createToolBox():
		env = Program.device.GUIEnvironment
		root = env.RootElement
		# remove tool box if already there
		e = root.GetElementFromID(guiID.DialogRootWindow, True)
		if e != None:
			e.Remove()
		# create the toolbox window
		w = env.AddWindow(Recti(600, 45, 800, 480), False, "Toolset", None, guiID.DialogRootWindow)
		# create tab control and tabs
		tab = env.AddTabControl(Recti(2, 20, 800 - 602, 480 - 7), w, -1, True, True)
		t1 = tab.AddTab("Config")
		# add some edit boxes and a button to tab one
		env.AddStaticText("Scale:", Recti(10, 20, 60, 45), False, False, t1)
		env.AddStaticText("X:", Recti(22, 48, 40, 66), False, False, t1)
		env.AddEditBox("1.0", Recti(40, 46, 130, 66), True, t1, guiID.XScale)
		env.AddStaticText("Y:", Recti(22, 78, 40, 96), False, False, t1)
		env.AddEditBox("1.0", Recti(40, 76, 130, 96), True, t1, guiID.YScale)
		env.AddStaticText("Z:", Recti(22, 108, 40, 126), False, False, t1)
		env.AddEditBox("1.0", Recti(40, 106, 130, 126), True, t1, guiID.ZScale)
		env.AddButton(Recti(10, 134, 85, 165), t1, guiID.ButtonSetScale, "Set")
		# quick scale buttons
		env.AddButton(Recti(65, 20, 95, 40), t1, guiID.ButtonScaleMul10, "* 10")
		env.AddButton(Recti(100, 20, 130, 40), t1, guiID.ButtonScaleDiv10, "* 0.1")
		Program.updateScaleInfo(Program.model)
		# add transparency control
		env.AddStaticText("GUI Transparency Control:", Recti(10, 200, 150, 225), True, False, t1)
		b = env.AddScrollBar(True, Recti(10, 225, 150, 240), t1, guiID.SkinTransparency)
		b.MaxValue = 255
		b.Position = 255
		# add framerate control
		env.AddStaticText("Framerate:", Recti(10, 240, 150, 265), True, False, t1)
		b = env.AddScrollBar(True, Recti(10, 265, 150, 280), t1, guiID.SkinAnimationFPS)
		b.MaxValue = 1000
		b.MinValue = -1000
		b.Position = 30
		# bring irrlicht engine logo to front, because it now may be below the newly created toolbox
		root.BringToFront(root.GetElementFromID(guiID.Logo, True))

	createToolBox = staticmethod(createToolBox)

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

Program.Main(Environment.GetCommandLineArgs()[2:])