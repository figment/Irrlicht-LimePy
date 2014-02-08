import clr
import System
from System import *
from System.Collections.Generic import *
from System.ComponentModel import *
from System.Data import *
from System.Linq import *
from System.Text import *
from System.Windows.Forms import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class Form1(Form):
	# this class will hold all settings that we need to pass to background worker,
	# which will create Irrlicht device, do all rendering and drop it when needed;
	# we are extending IrrlichtCreationParameters with our custom settings
	class DeviceSettings(IrrlichtCreationParameters): # "null" for skybox
		def __init__(self, hh, dt, aa, bc, vs):
			self.WindowID = hh
			self.DriverType = dt
			self.AntiAliasing = aa
			self.BackColor = bc
			self.VSync = vs
			
	def __new__(self):
		return Form.__new__(self)
	
	def __init__(self):
		# <summary>
		# Required designer variable.
		# </summary>
		self._components = None
		self._userWantExit = False # if "true", we shut down rendering thread and then exit app
		self.InitializeComponent()
		
	def Dispose(self, disposing):
		""" <summary>
		 Clean up any resources being used.
		 </summary>
		 <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		"""
		if disposing and (self._components != None):
			self._components.Dispose()
		Form.Dispose(self, disposing)

	def InitializeComponent(self):
		""" <summary>
		 Required method for Designer support - do not modify
		 the contents of this method with the code editor.
		 </summary>
		"""
		self._panelRenderingWindow = System.Windows.Forms.Panel()
		self._labelRenderingStatus = System.Windows.Forms.Label()
		self._backgroundRendering = System.ComponentModel.BackgroundWorker()
		self._comboBoxVideoDriver = System.Windows.Forms.ComboBox()
		self._checkBoxUseSeparateWindow = System.Windows.Forms.CheckBox()
		self._comboBoxAntiAliasing = System.Windows.Forms.ComboBox()
		self._label2 = System.Windows.Forms.Label()
		self._label3 = System.Windows.Forms.Label()
		self._comboBoxBackground = System.Windows.Forms.ComboBox()
		self._label4 = System.Windows.Forms.Label()
		self._checkBoxUseVSync = System.Windows.Forms.CheckBox()
		self.SuspendLayout()
		# 
		# panelRenderingWindow
		# 
		self._panelRenderingWindow.Location = System.Drawing.Point(12, 85)
		self._panelRenderingWindow.Name = "panelRenderingWindow"
		self._panelRenderingWindow.Size = System.Drawing.Size(540, 400)
		self._panelRenderingWindow.TabIndex = 0
		# 
		# labelRenderingStatus
		# 
		self._labelRenderingStatus.AutoSize = True
		self._labelRenderingStatus.Font = System.Drawing.Font("Tahoma", Single(11.25), System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((204)))
		self._labelRenderingStatus.Location = System.Drawing.Point(12, 64)
		self._labelRenderingStatus.Name = "labelRenderingStatus"
		self._labelRenderingStatus.Size = System.Drawing.Size(187, 18)
		self._labelRenderingStatus.TabIndex = 1
		self._labelRenderingStatus.Text = "Select video driver to use..."
		# 
		# backgroundRendering
		# 
		self._backgroundRendering.WorkerReportsProgress = True
		self._backgroundRendering.WorkerSupportsCancellation = True
		self._backgroundRendering.DoWork += self.backgroundRendering_DoWork
		self._backgroundRendering.RunWorkerCompleted += self.backgroundRendering_RunWorkerCompleted
		self._backgroundRendering.ProgressChanged += self.backgroundRendering_ProgressChanged
		# 
		# comboBoxVideoDriver
		# 
		self._comboBoxVideoDriver.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboBoxVideoDriver.FormattingEnabled = True
		self._comboBoxVideoDriver.Location = System.Drawing.Point(12, 32)
		self._comboBoxVideoDriver.Name = "comboBoxVideoDriver"
		self._comboBoxVideoDriver.Size = System.Drawing.Size(130, 21)
		self._comboBoxVideoDriver.TabIndex = 2
		self._comboBoxVideoDriver.SelectedIndexChanged += self.initializeIrrlichtDevice
		# 
		# checkBoxUseSeparateWindow
		# 
		self._checkBoxUseSeparateWindow.AutoSize = True
		self._checkBoxUseSeparateWindow.Location = System.Drawing.Point(349, 38)
		self._checkBoxUseSeparateWindow.Name = "checkBoxUseSeparateWindow"
		self._checkBoxUseSeparateWindow.Size = System.Drawing.Size(128, 17)
		self._checkBoxUseSeparateWindow.TabIndex = 3
		self._checkBoxUseSeparateWindow.Text = "Use separate window"
		self._checkBoxUseSeparateWindow.UseVisualStyleBackColor = True
		self._checkBoxUseSeparateWindow.CheckedChanged += self.initializeIrrlichtDevice
		# 
		# comboBoxAntiAliasing
		# 
		self._comboBoxAntiAliasing.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboBoxAntiAliasing.FormattingEnabled = True
		self._comboBoxAntiAliasing.Items.AddRange(System.Array[object](("No", "2x", "4x", "8x", "16x")))
		self._comboBoxAntiAliasing.Location = System.Drawing.Point(158, 32)
		self._comboBoxAntiAliasing.Name = "comboBoxAntiAliasing"
		self._comboBoxAntiAliasing.Size = System.Drawing.Size(80, 21)
		self._comboBoxAntiAliasing.TabIndex = 4
		self._comboBoxAntiAliasing.SelectedIndexChanged += self.initializeIrrlichtDevice
		# 
		# label2
		# 
		self._label2.AutoSize = True
		self._label2.Location = System.Drawing.Point(12, 16)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(63, 13)
		self._label2.TabIndex = 5
		self._label2.Text = "Video driver"
		# 
		# label3
		# 
		self._label3.AutoSize = True
		self._label3.Location = System.Drawing.Point(155, 16)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(61, 13)
		self._label3.TabIndex = 6
		self._label3.Text = "AntiAliasing"
		# 
		# comboBoxBackground
		# 
		self._comboBoxBackground.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._comboBoxBackground.FormattingEnabled = True
		self._comboBoxBackground.Items.AddRange(System.Array[object](("Skybox", "Black", "White")))
		self._comboBoxBackground.Location = System.Drawing.Point(253, 32)
		self._comboBoxBackground.Name = "comboBoxBackground"
		self._comboBoxBackground.Size = System.Drawing.Size(80, 21)
		self._comboBoxBackground.TabIndex = 7
		self._comboBoxBackground.SelectedIndexChanged += self.initializeIrrlichtDevice
		# 
		# label4
		# 
		self._label4.AutoSize = True
		self._label4.Location = System.Drawing.Point(250, 16)
		self._label4.Name = "label4"
		self._label4.Size = System.Drawing.Size(65, 13)
		self._label4.TabIndex = 6
		self._label4.Text = "Background"
		# 
		# checkBoxUseVSync
		# 
		self._checkBoxUseVSync.AutoSize = True
		self._checkBoxUseVSync.Location = System.Drawing.Point(349, 15)
		self._checkBoxUseVSync.Name = "checkBoxUseVSync"
		self._checkBoxUseVSync.Size = System.Drawing.Size(79, 17)
		self._checkBoxUseVSync.TabIndex = 8
		self._checkBoxUseVSync.Text = "Use VSync"
		self._checkBoxUseVSync.UseVisualStyleBackColor = True
		self._checkBoxUseVSync.CheckedChanged += self.initializeIrrlichtDevice
		# 
		# Form1
		# 
		self.AutoScaleDimensions = System.Drawing.SizeF(Single(6), Single(13))
		self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		self.ClientSize = System.Drawing.Size(564, 497)
		self.Controls.Add(self._checkBoxUseVSync)
		self.Controls.Add(self._comboBoxBackground)
		self.Controls.Add(self._label4)
		self.Controls.Add(self._label3)
		self.Controls.Add(self._label2)
		self.Controls.Add(self._comboBoxAntiAliasing)
		self.Controls.Add(self._checkBoxUseSeparateWindow)
		self.Controls.Add(self._comboBoxVideoDriver)
		self.Controls.Add(self._labelRenderingStatus)
		self.Controls.Add(self._panelRenderingWindow)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		self.MaximizeBox = False
		self.Name = "Form1"
		self.Text = "WinForms window example - Irrlicht Engine"
		self.Load += self.Form1_Load
		self.FormClosing += self.Form1_FormClosing
		self.ResumeLayout(False)
		self.PerformLayout()
		
	def Form1_Load(self, sender, e):
		# select "No AntiAliasing"
		self._comboBoxAntiAliasing.SelectedIndex = 0
		# select "Skybox"
		self._comboBoxBackground.SelectedIndex = 0
		# fill combobox with all available video drivers, except Null
		for v in Enum.GetValues(clr.GetClrType(DriverType)):
			if v != DriverType.Null:
				self._comboBoxVideoDriver.Items.Add(v)

	def initializeIrrlichtDevice(self, sender, e):
		if self._comboBoxVideoDriver.SelectedItem == None:
			return 
		# if rendering in progress, we are sending cancel request and waiting for its
		# finishing
		if self._backgroundRendering.IsBusy:
			self._backgroundRendering.CancelAsync()
			while self._backgroundRendering.IsBusy:
				Application.DoEvents() # this is not very correct way, but its very short, so we use it
			# redraw the panel, otherwise last rendered frame will stay as garbage
			self._panelRenderingWindow.Invalidate()
		# collect settings and start background worker with these settings
		hh = IntPtr.Zero if self._checkBoxUseSeparateWindow.Checked else self._panelRenderingWindow.Handle
		dt = self._comboBoxVideoDriver.SelectedItem
		aa = (0 if self._comboBoxAntiAliasing.SelectedIndex == 0 else Math.Pow(2, self._comboBoxAntiAliasing.SelectedIndex))
		bc = None if self._comboBoxBackground.SelectedIndex == 0 else Color(UInt32(0xFF000000) if self._comboBoxBackground.SelectedIndex == 1 else UInt32(0xFFFFFFFF))
		vs = self._checkBoxUseVSync.Checked
		print "Device", hh,dt, aa, bc, vs
		s = Form1.DeviceSettings(hh, dt, aa, bc, vs)
		self._backgroundRendering.RunWorkerAsync(s)
		self._labelRenderingStatus.Text = "Starting rendering..."

	def backgroundRendering_DoWork(self, sender, e):
		worker = sender
		settings = e.Argument
		print settings
		# create irrlicht device using provided settings
		dev = IrrlichtDevice.CreateDevice(settings)
		if dev == None:
			raise Exception("Failed to create Irrlicht device.")
		drv = dev.VideoDriver
		smgr = dev.SceneManager
		# setup a simple 3d scene
		cam = smgr.AddCameraSceneNode()
		cam.Target = Vector3Df(0)
		anim = smgr.CreateFlyCircleAnimator(Vector3Df(0, 15, 0), Single(30))
		cam.AddAnimator(anim)
		anim.Drop()
		cube = smgr.AddCubeSceneNode(20)
		cube.SetMaterialTexture(0, drv.GetTexture("../../media/wall.bmp"))
		cube.SetMaterialTexture(1, drv.GetTexture("../../media/water.jpg"))
		cube.SetMaterialFlag(MaterialFlag.Lighting, False)
		cube.SetMaterialType(MaterialType.Reflection2Layer)
		if settings.BackColor == None:
			smgr.AddSkyBoxSceneNode(
						   "../../media/irrlicht2_up.jpg"
						   , "../../media/irrlicht2_dn.jpg"
						   , "../../media/irrlicht2_lf.jpg"
						   , "../../media/irrlicht2_rt.jpg"
						   , "../../media/irrlicht2_ft.jpg"
						   , "../../media/irrlicht2_bk.jpg")
		dev.GUIEnvironment.AddImage(drv.GetTexture("../../media/lime_logo_alpha.png"), Vector2Di(30, 0))
		# draw all
		lastFPS = -1
		while dev.Run():
			if settings.BackColor == None:
				# indeed, we do not need to spend time on cleaning color buffer if we use
				# skybox
				drv.BeginScene(False)
			else:
				drv.BeginScene(True, True, settings.BackColor)
			smgr.DrawAll()
			dev.GUIEnvironment.DrawAll()
			drv.EndScene()
			fps = drv.FPS
			if lastFPS != fps:
				# report progress using common BackgroundWorker' method
				# note: we cannot do just labelRenderingStatus.Text = "...",
				# because we are running another thread
				worker.ReportProgress(fps, drv.Name)
				lastFPS = fps
			# if we requested to stop, we close the device
			if worker.CancellationPending:
				dev.Close()
		# drop device
		dev.Drop()

	def Form1_FormClosing(self, sender, e):
		# if background worker still running, we send request to stop
		if self._backgroundRendering.IsBusy:
			self._backgroundRendering.CancelAsync()
			e.Cancel = True
			self._userWantExit = True

	def backgroundRendering_ProgressChanged(self, sender, e):
		# process reported progress
		f = e.ProgressPercentage
		d = e.UserState
		self._labelRenderingStatus.Text = str.Format("Rendering {1} fps using {0} driver", d, f)

	def backgroundRendering_RunWorkerCompleted(self, sender, e):
		# if exception occured in rendering thread -- we display the message
		if e.Error != None:
			MessageBox.Show(e.Error.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
		# if user want exit - we close main form
		# note: it is the only way to close form correctly -- only when device
		# dropped,
		# so background worker not running
		if self._userWantExit:
			self.Close()
		self._labelRenderingStatus.Text = "No rendering"