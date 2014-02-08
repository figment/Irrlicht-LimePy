import System
from System import *
from System.Collections.Generic import *
from System.ComponentModel import *
from System.Data import *
from System.Drawing import *
from System.Linq import *
from System.Text import *
from System.Windows.Forms import *
from System.IO import *
from Command import *
from ParticleInfo import *
from Viewport import *

class MainForm(Form):
	def __new__(self):
		return Form.__new__(self)
	
	def __init__(self):
		self._viewport = None
		# <summary>
		# Required designer variable.
		# </summary>
		self._components = None
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
		self._groupBox1 = System.Windows.Forms.GroupBox()
		self._pictureBoxParticlePreview = System.Windows.Forms.PictureBox()
		self._listBoxParticleList = System.Windows.Forms.ListBox()
		self._groupBox2 = System.Windows.Forms.GroupBox()
		self._label3 = System.Windows.Forms.Label()
		self._checkBoxPlane = System.Windows.Forms.CheckBox()
		self._checkBoxAxes = System.Windows.Forms.CheckBox()
		self._trackBarCameraView = System.Windows.Forms.TrackBar()
		self._panelViewport = System.Windows.Forms.Panel()
		self._groupBox3 = System.Windows.Forms.GroupBox()
		self._label6 = System.Windows.Forms.Label()
		self._label5 = System.Windows.Forms.Label()
		self._label4 = System.Windows.Forms.Label()
		self._label2 = System.Windows.Forms.Label()
		self._trackBarDirectionZ = System.Windows.Forms.TrackBar()
		self._trackBarDirectionY = System.Windows.Forms.TrackBar()
		self._trackBarDirectionX = System.Windows.Forms.TrackBar()
		self._trackBarSize = System.Windows.Forms.TrackBar()
		self._label1 = System.Windows.Forms.Label()
		self._trackBarRate = System.Windows.Forms.TrackBar()
		self._trackBarRadius = System.Windows.Forms.TrackBar()
		self._trackBarPosition = System.Windows.Forms.TrackBar()
		self._checkBoxEmitt = System.Windows.Forms.CheckBox()
		self._groupBox4 = System.Windows.Forms.GroupBox()
		self._checkBoxAffectorRotation = System.Windows.Forms.CheckBox()
		self._checkBoxAffectorGravity = System.Windows.Forms.CheckBox()
		self._checkBoxAffectorFadeOut = System.Windows.Forms.CheckBox()
		self._checkBoxKeepAspect = System.Windows.Forms.CheckBox()
		self._label7 = System.Windows.Forms.Label()
		self._buttonBrowseForTexture = System.Windows.Forms.Button()
		self._groupBox1.SuspendLayout()
		((self._pictureBoxParticlePreview)).BeginInit()
		self._groupBox2.SuspendLayout()
		((self._trackBarCameraView)).BeginInit()
		self._groupBox3.SuspendLayout()
		((self._trackBarDirectionZ)).BeginInit()
		((self._trackBarDirectionY)).BeginInit()
		((self._trackBarDirectionX)).BeginInit()
		((self._trackBarSize)).BeginInit()
		((self._trackBarRate)).BeginInit()
		((self._trackBarRadius)).BeginInit()
		((self._trackBarPosition)).BeginInit()
		self._groupBox4.SuspendLayout()
		self.SuspendLayout()
		# 
		# groupBox1
		# 
		self._groupBox1.Anchor = ((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) | System.Windows.Forms.AnchorStyles.Left)))
		self._groupBox1.Controls.Add(self._buttonBrowseForTexture)
		self._groupBox1.Controls.Add(self._label7)
		self._groupBox1.Controls.Add(self._pictureBoxParticlePreview)
		self._groupBox1.Controls.Add(self._listBoxParticleList)
		self._groupBox1.Location = System.Drawing.Point(12, 12)
		self._groupBox1.Name = "groupBox1"
		self._groupBox1.Size = System.Drawing.Size(140, 380)
		self._groupBox1.TabIndex = 0
		self._groupBox1.TabStop = False
		self._groupBox1.Text = "Particle Texture"
		# 
		# pictureBoxParticlePreview
		# 
		self._pictureBoxParticlePreview.Location = System.Drawing.Point(6, 19)
		self._pictureBoxParticlePreview.Name = "pictureBoxParticlePreview"
		self._pictureBoxParticlePreview.Size = System.Drawing.Size(128, 128)
		self._pictureBoxParticlePreview.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom
		self._pictureBoxParticlePreview.TabIndex = 1
		self._pictureBoxParticlePreview.TabStop = False
		# 
		# listBoxParticleList
		# 
		self._listBoxParticleList.Anchor = ((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) | System.Windows.Forms.AnchorStyles.Left)))
		self._listBoxParticleList.FormattingEnabled = True
		self._listBoxParticleList.IntegralHeight = False
		self._listBoxParticleList.Location = System.Drawing.Point(6, 153)
		self._listBoxParticleList.Name = "listBoxParticleList"
		self._listBoxParticleList.Size = System.Drawing.Size(128, 80)
		self._listBoxParticleList.TabIndex = 0
		self._listBoxParticleList.SelectedIndexChanged += self.listBoxParticleList_SelectedIndexChanged
		# 
		# groupBox2
		# 
		self._groupBox2.Anchor = (((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) | System.Windows.Forms.AnchorStyles.Left) | System.Windows.Forms.AnchorStyles.Right)))
		self._groupBox2.Controls.Add(self._label3)
		self._groupBox2.Controls.Add(self._checkBoxPlane)
		self._groupBox2.Controls.Add(self._checkBoxKeepAspect)
		self._groupBox2.Controls.Add(self._checkBoxAxes)
		self._groupBox2.Controls.Add(self._trackBarCameraView)
		self._groupBox2.Controls.Add(self._panelViewport)
		self._groupBox2.Location = System.Drawing.Point(158, 12)
		self._groupBox2.Name = "groupBox2"
		self._groupBox2.Size = System.Drawing.Size(412, 380)
		self._groupBox2.TabIndex = 1
		self._groupBox2.TabStop = False
		self._groupBox2.Text = "Viewport"
		# 
		# label3
		# 
		self._label3.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
		self._label3.AutoSize = True
		self._label3.Location = System.Drawing.Point(141, 332)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(69, 13)
		self._label3.TabIndex = 2
		self._label3.Text = "Camera View"
		# 
		# checkBoxPlane
		# 
		self._checkBoxPlane.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
		self._checkBoxPlane.AutoSize = True
		self._checkBoxPlane.Checked = True
		self._checkBoxPlane.CheckState = System.Windows.Forms.CheckState.Checked
		self._checkBoxPlane.Location = System.Drawing.Point(6, 325)
		self._checkBoxPlane.Name = "checkBoxPlane"
		self._checkBoxPlane.Size = System.Drawing.Size(53, 17)
		self._checkBoxPlane.TabIndex = 2
		self._checkBoxPlane.Text = "Plane"
		self._checkBoxPlane.UseVisualStyleBackColor = True
		self._checkBoxPlane.CheckedChanged += self.checkBoxPlane_CheckedChanged
		# 
		# checkBoxAxes
		# 
		self._checkBoxAxes.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
		self._checkBoxAxes.AutoSize = True
		self._checkBoxAxes.Location = System.Drawing.Point(65, 325)
		self._checkBoxAxes.Name = "checkBoxAxes"
		self._checkBoxAxes.Size = System.Drawing.Size(49, 17)
		self._checkBoxAxes.TabIndex = 1
		self._checkBoxAxes.Text = "Axes"
		self._checkBoxAxes.UseVisualStyleBackColor = True
		self._checkBoxAxes.CheckedChanged += self.checkBoxAxes_CheckedChanged
		# 
		# trackBarCameraView
		# 
		self._trackBarCameraView.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
		self._trackBarCameraView.AutoSize = False
		self._trackBarCameraView.LargeChange = 10
		self._trackBarCameraView.Location = System.Drawing.Point(6, 348)
		self._trackBarCameraView.Maximum = 250
		self._trackBarCameraView.Minimum = -100
		self._trackBarCameraView.Name = "trackBarCameraView"
		self._trackBarCameraView.Size = System.Drawing.Size(204, 26)
		self._trackBarCameraView.TabIndex = 1
		self._trackBarCameraView.TickFrequency = 10
		self._trackBarCameraView.Value = 80
		self._trackBarCameraView.Scroll += self.trackBarCameraView_Scroll
		# 
		# panelViewport
		# 
		self._panelViewport.Anchor = (((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) | System.Windows.Forms.AnchorStyles.Left) | System.Windows.Forms.AnchorStyles.Right)))
		self._panelViewport.Location = System.Drawing.Point(6, 19)
		self._panelViewport.Name = "panelViewport"
		self._panelViewport.Size = System.Drawing.Size(400, 300)
		self._panelViewport.TabIndex = 0
		# 
		# groupBox3
		# 
		self._groupBox3.Anchor = (((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)))
		self._groupBox3.Controls.Add(self._label6)
		self._groupBox3.Controls.Add(self._label5)
		self._groupBox3.Controls.Add(self._label4)
		self._groupBox3.Controls.Add(self._label2)
		self._groupBox3.Controls.Add(self._trackBarDirectionZ)
		self._groupBox3.Controls.Add(self._trackBarDirectionY)
		self._groupBox3.Controls.Add(self._trackBarDirectionX)
		self._groupBox3.Controls.Add(self._trackBarSize)
		self._groupBox3.Controls.Add(self._label1)
		self._groupBox3.Controls.Add(self._trackBarRate)
		self._groupBox3.Controls.Add(self._trackBarRadius)
		self._groupBox3.Controls.Add(self._trackBarPosition)
		self._groupBox3.Controls.Add(self._checkBoxEmitt)
		self._groupBox3.Location = System.Drawing.Point(576, 12)
		self._groupBox3.Name = "groupBox3"
		self._groupBox3.Size = System.Drawing.Size(216, 274)
		self._groupBox3.TabIndex = 2
		self._groupBox3.TabStop = False
		self._groupBox3.Text = "Emitter"
		# 
		# label6
		# 
		self._label6.AutoSize = True
		self._label6.Location = System.Drawing.Point(6, 223)
		self._label6.Name = "label6"
		self._label6.Size = System.Drawing.Size(91, 13)
		self._label6.TabIndex = 2
		self._label6.Text = "Direction (X, Y, Z)"
		# 
		# label5
		# 
		self._label5.AutoSize = True
		self._label5.Location = System.Drawing.Point(6, 178)
		self._label5.Name = "label5"
		self._label5.Size = System.Drawing.Size(27, 13)
		self._label5.TabIndex = 2
		self._label5.Text = "Size"
		# 
		# label4
		# 
		self._label4.AutoSize = True
		self._label4.Location = System.Drawing.Point(6, 133)
		self._label4.Name = "label4"
		self._label4.Size = System.Drawing.Size(30, 13)
		self._label4.TabIndex = 2
		self._label4.Text = "Rate"
		# 
		# label2
		# 
		self._label2.AutoSize = True
		self._label2.Location = System.Drawing.Point(6, 88)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(40, 13)
		self._label2.TabIndex = 2
		self._label2.Text = "Radius"
		# 
		# trackBarDirectionZ
		# 
		self._trackBarDirectionZ.AutoSize = False
		self._trackBarDirectionZ.LargeChange = 20
		self._trackBarDirectionZ.Location = System.Drawing.Point(148, 239)
		self._trackBarDirectionZ.Maximum = 50
		self._trackBarDirectionZ.Minimum = -50
		self._trackBarDirectionZ.Name = "trackBarDirectionZ"
		self._trackBarDirectionZ.Size = System.Drawing.Size(62, 26)
		self._trackBarDirectionZ.TabIndex = 1
		self._trackBarDirectionZ.TickFrequency = 10
		self._trackBarDirectionZ.Scroll += self.trackBarDirection_Scroll
		# 
		# trackBarDirectionY
		# 
		self._trackBarDirectionY.AutoSize = False
		self._trackBarDirectionY.LargeChange = 20
		self._trackBarDirectionY.Location = System.Drawing.Point(78, 239)
		self._trackBarDirectionY.Maximum = 50
		self._trackBarDirectionY.Minimum = -50
		self._trackBarDirectionY.Name = "trackBarDirectionY"
		self._trackBarDirectionY.Size = System.Drawing.Size(62, 26)
		self._trackBarDirectionY.TabIndex = 1
		self._trackBarDirectionY.TickFrequency = 10
		self._trackBarDirectionY.Value = 10
		self._trackBarDirectionY.Scroll += self.trackBarDirection_Scroll
		# 
		# trackBarDirectionX
		# 
		self._trackBarDirectionX.AutoSize = False
		self._trackBarDirectionX.LargeChange = 20
		self._trackBarDirectionX.Location = System.Drawing.Point(10, 239)
		self._trackBarDirectionX.Maximum = 50
		self._trackBarDirectionX.Minimum = -50
		self._trackBarDirectionX.Name = "trackBarDirectionX"
		self._trackBarDirectionX.Size = System.Drawing.Size(62, 26)
		self._trackBarDirectionX.TabIndex = 1
		self._trackBarDirectionX.TickFrequency = 10
		self._trackBarDirectionX.Scroll += self.trackBarDirection_Scroll
		# 
		# trackBarSize
		# 
		self._trackBarSize.AutoSize = False
		self._trackBarSize.LargeChange = 10
		self._trackBarSize.Location = System.Drawing.Point(5, 194)
		self._trackBarSize.Maximum = 200
		self._trackBarSize.Minimum = 5
		self._trackBarSize.Name = "trackBarSize"
		self._trackBarSize.Size = System.Drawing.Size(205, 26)
		self._trackBarSize.TabIndex = 1
		self._trackBarSize.TickFrequency = 10
		self._trackBarSize.Value = 40
		self._trackBarSize.Scroll += self.trackBarSize_Scroll
		# 
		# label1
		# 
		self._label1.AutoSize = True
		self._label1.Location = System.Drawing.Point(7, 43)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(60, 13)
		self._label1.TabIndex = 2
		self._label1.Text = "Position (X)"
		# 
		# trackBarRate
		# 
		self._trackBarRate.AutoSize = False
		self._trackBarRate.LargeChange = 100
		self._trackBarRate.Location = System.Drawing.Point(5, 149)
		self._trackBarRate.Maximum = 2000
		self._trackBarRate.Minimum = 50
		self._trackBarRate.Name = "trackBarRate"
		self._trackBarRate.Size = System.Drawing.Size(205, 26)
		self._trackBarRate.TabIndex = 1
		self._trackBarRate.TickFrequency = 50
		self._trackBarRate.Value = 300
		self._trackBarRate.Scroll += self.trackBarRate_Scroll
		# 
		# trackBarRadius
		# 
		self._trackBarRadius.AutoSize = False
		self._trackBarRadius.LargeChange = 10
		self._trackBarRadius.Location = System.Drawing.Point(5, 104)
		self._trackBarRadius.Maximum = 100
		self._trackBarRadius.Minimum = 1
		self._trackBarRadius.Name = "trackBarRadius"
		self._trackBarRadius.Size = System.Drawing.Size(205, 26)
		self._trackBarRadius.TabIndex = 1
		self._trackBarRadius.TickFrequency = 10
		self._trackBarRadius.Value = 20
		self._trackBarRadius.Scroll += self.trackBarRadius_Scroll
		# 
		# trackBarPosition
		# 
		self._trackBarPosition.AutoSize = False
		self._trackBarPosition.LargeChange = 10
		self._trackBarPosition.Location = System.Drawing.Point(6, 59)
		self._trackBarPosition.Maximum = 100
		self._trackBarPosition.Minimum = -100
		self._trackBarPosition.Name = "trackBarPosition"
		self._trackBarPosition.Size = System.Drawing.Size(204, 26)
		self._trackBarPosition.TabIndex = 1
		self._trackBarPosition.TickFrequency = 10
		self._trackBarPosition.Scroll += self.trackBarPosition_Scroll
		# 
		# checkBoxEmitt
		# 
		self._checkBoxEmitt.AutoSize = True
		self._checkBoxEmitt.Checked = True
		self._checkBoxEmitt.CheckState = System.Windows.Forms.CheckState.Checked
		self._checkBoxEmitt.Location = System.Drawing.Point(6, 19)
		self._checkBoxEmitt.Name = "checkBoxEmitt"
		self._checkBoxEmitt.Size = System.Drawing.Size(49, 17)
		self._checkBoxEmitt.TabIndex = 0
		self._checkBoxEmitt.Text = "Emitt"
		self._checkBoxEmitt.UseVisualStyleBackColor = True
		self._checkBoxEmitt.CheckedChanged += self.checkBoxEmitt_CheckedChanged
		# 
		# groupBox4
		# 
		self._groupBox4.Anchor = (((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)))
		self._groupBox4.Controls.Add(self._checkBoxAffectorRotation)
		self._groupBox4.Controls.Add(self._checkBoxAffectorGravity)
		self._groupBox4.Controls.Add(self._checkBoxAffectorFadeOut)
		self._groupBox4.Location = System.Drawing.Point(576, 292)
		self._groupBox4.Name = "groupBox4"
		self._groupBox4.Size = System.Drawing.Size(216, 100)
		self._groupBox4.TabIndex = 3
		self._groupBox4.TabStop = False
		self._groupBox4.Text = "Affectors"
		# 
		# checkBoxAffectorRotation
		# 
		self._checkBoxAffectorRotation.AutoSize = True
		self._checkBoxAffectorRotation.Checked = True
		self._checkBoxAffectorRotation.CheckState = System.Windows.Forms.CheckState.Checked
		self._checkBoxAffectorRotation.Location = System.Drawing.Point(6, 42)
		self._checkBoxAffectorRotation.Name = "checkBoxAffectorRotation"
		self._checkBoxAffectorRotation.Size = System.Drawing.Size(66, 17)
		self._checkBoxAffectorRotation.TabIndex = 0
		self._checkBoxAffectorRotation.Text = "Rotation"
		self._checkBoxAffectorRotation.UseVisualStyleBackColor = True
		self._checkBoxAffectorRotation.CheckedChanged += self.checkBoxAffectorRotation_CheckedChanged
		# 
		# checkBoxAffectorGravity
		# 
		self._checkBoxAffectorGravity.AutoSize = True
		self._checkBoxAffectorGravity.Location = System.Drawing.Point(6, 65)
		self._checkBoxAffectorGravity.Name = "checkBoxAffectorGravity"
		self._checkBoxAffectorGravity.Size = System.Drawing.Size(59, 17)
		self._checkBoxAffectorGravity.TabIndex = 0
		self._checkBoxAffectorGravity.Text = "Gravity"
		self._checkBoxAffectorGravity.UseVisualStyleBackColor = True
		self._checkBoxAffectorGravity.CheckedChanged += self.checkBoxAffectorGravity_CheckedChanged
		# 
		# checkBoxAffectorFadeOut
		# 
		self._checkBoxAffectorFadeOut.AutoSize = True
		self._checkBoxAffectorFadeOut.Checked = True
		self._checkBoxAffectorFadeOut.CheckState = System.Windows.Forms.CheckState.Checked
		self._checkBoxAffectorFadeOut.Location = System.Drawing.Point(6, 19)
		self._checkBoxAffectorFadeOut.Name = "checkBoxAffectorFadeOut"
		self._checkBoxAffectorFadeOut.Size = System.Drawing.Size(68, 17)
		self._checkBoxAffectorFadeOut.TabIndex = 0
		self._checkBoxAffectorFadeOut.Text = "Fade out"
		self._checkBoxAffectorFadeOut.UseVisualStyleBackColor = True
		self._checkBoxAffectorFadeOut.CheckedChanged += self.checkBoxAffectorFadeOut_CheckedChanged
		# 
		# checkBoxKeepAspect
		# 
		self._checkBoxKeepAspect.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)))
		self._checkBoxKeepAspect.AutoSize = True
		self._checkBoxKeepAspect.Checked = True
		self._checkBoxKeepAspect.CheckState = System.Windows.Forms.CheckState.Checked
		self._checkBoxKeepAspect.Location = System.Drawing.Point(297, 325)
		self._checkBoxKeepAspect.Name = "checkBoxKeepAspect"
		self._checkBoxKeepAspect.Size = System.Drawing.Size(109, 17)
		self._checkBoxKeepAspect.TabIndex = 1
		self._checkBoxKeepAspect.Text = "Keep aspect ratio"
		self._checkBoxKeepAspect.UseVisualStyleBackColor = True
		self._checkBoxKeepAspect.CheckedChanged += self.MainForm_Resize
		# 
		# label7
		# 
		self._label7.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
		self._label7.Enabled = False
		self._label7.Location = System.Drawing.Point(6, 236)
		self._label7.Name = "label7"
		self._label7.Size = System.Drawing.Size(128, 80)
		self._label7.TabIndex = 2
		self._label7.Text = "Above listed files with the \"particle\" word in its name from \"media\" folder only." + " Use button below to add your own texture to the list."
		self._label7.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# buttonBrowseForTexture
		# 
		self._buttonBrowseForTexture.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
		self._buttonBrowseForTexture.Location = System.Drawing.Point(6, 322)
		self._buttonBrowseForTexture.Name = "buttonBrowseForTexture"
		self._buttonBrowseForTexture.Size = System.Drawing.Size(128, 52)
		self._buttonBrowseForTexture.TabIndex = 3
		self._buttonBrowseForTexture.Text = "Browse for own texture..."
		self._buttonBrowseForTexture.UseVisualStyleBackColor = True
		self._buttonBrowseForTexture.Click += self.buttonBrowseForTexture_Click
		# 
		# MainForm
		# 
		self.AutoScaleDimensions = System.Drawing.SizeF(Single(6), Single(13))
		self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		self.ClientSize = System.Drawing.Size(804, 404)
		self.Controls.Add(self._groupBox4)
		self.Controls.Add(self._groupBox3)
		self.Controls.Add(self._groupBox2)
		self.Controls.Add(self._groupBox1)
		self.MinimumSize = System.Drawing.Size(820, 442)
		self.Name = "MainForm"
		self.Text = "Particle Emitter Viewer - Irrlicht Lime"
		self.Load += self.MainForm_Load
		self.FormClosed += self.MainForm_FormClosed
		self.Resize += self.MainForm_Resize
		self._groupBox1.ResumeLayout(False)
		((self._pictureBoxParticlePreview)).EndInit()
		self._groupBox2.ResumeLayout(False)
		self._groupBox2.PerformLayout()
		((self._trackBarCameraView)).EndInit()
		self._groupBox3.ResumeLayout(False)
		self._groupBox3.PerformLayout()
		((self._trackBarDirectionZ)).EndInit()
		((self._trackBarDirectionY)).EndInit()
		((self._trackBarDirectionX)).EndInit()
		((self._trackBarSize)).EndInit()
		((self._trackBarRate)).EndInit()
		((self._trackBarRadius)).EndInit()
		((self._trackBarPosition)).EndInit()
		self._groupBox4.ResumeLayout(False)
		self._groupBox4.PerformLayout()
		self.ResumeLayout(False)

	def MainForm_Load(self, sender, e):
		self.refreshParticleList()
		self.initViewport()

	def initViewport(self):
		self._viewport = Viewport()
		self._viewport.Start(self._panelViewport.Handle)

	def MainForm_FormClosed(self, sender, e):
		self._viewport.Stop()

	def refreshParticleList(self):
		self._listBoxParticleList.Items.Clear()
		l = Directory.GetFiles("../../media", "*particle*", SearchOption.TopDirectoryOnly)
		for f in l:
			self.addImageToParticleList(f, False)
		if self._listBoxParticleList.Items.Count > 0:
			self._listBoxParticleList.SelectedIndex = 0

	def addImageToParticleList(self, f, makeThisImageSelected):
		i = Bitmap(f)
		p = ParticleInfo()
		p.FileName = f
		p.Preview = i.GetThumbnailImage(128, 128, None, IntPtr.Zero)
		p.DisplayName = Path.GetFileName(f) + " (" + str(i.Width) + "x" + str(i.Height) + ")"
		s = self._listBoxParticleList.Items.Add(p)
		if makeThisImageSelected:
			self._listBoxParticleList.SelectedIndex = s

	def listBoxParticleList_SelectedIndexChanged(self, sender, e):
		p = self._listBoxParticleList.SelectedItem
		if p != None:
			if self._viewport != None:
				self._viewport.EnqueueCommand(CommandType.Particle, p)
			self._pictureBoxParticlePreview.Image = p.Preview

	def buttonBrowseForTexture_Click(self, sender, e):
		f = OpenFileDialog()
		f.Filter = "Image files (*.bmp;*.jpg;*.png;*.tga)|*.bmp;*.jpg;*.png;*.tga|All files (*.*)|*.*"
		r = f.ShowDialog()
		if r == DialogResult.OK:
			self.addImageToParticleList(f.FileName, True)

	def checkBoxAxes_CheckedChanged(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Axes, self._checkBoxAxes.Checked)

	def checkBoxPlane_CheckedChanged(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Plane, self._checkBoxPlane.Checked)

	def checkBoxEmitt_CheckedChanged(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Rate, self._trackBarRate.Value if self._checkBoxEmitt.Checked else 0)

	def MainForm_Resize(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Resize
			, Array[int]((self._panelViewport.ClientSize.Width, self._panelViewport.ClientSize.Height, 1 if self._checkBoxKeepAspect.Checked else 0)))

	def trackBarPosition_Scroll(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Position, Array[Single]((self._trackBarPosition.Value, 0, 0)))

	def trackBarRadius_Scroll(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Radius, self._trackBarRadius.Value)

	def trackBarCameraView_Scroll(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.CameraView, self._trackBarCameraView.Value)

	def trackBarRate_Scroll(self, sender, e):
		if self._checkBoxEmitt.Checked:
			self._viewport.EnqueueCommand(CommandType.Rate, self._trackBarRate.Value)

	def trackBarSize_Scroll(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Size, self._trackBarSize.Value)

	def trackBarDirection_Scroll(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Direction
			, Array[Single]((
				  self._trackBarDirectionX.Value / Single(100)
				, self._trackBarDirectionY.Value / Single(100)
				, self._trackBarDirectionZ.Value / Single(100))))

	def checkBoxAffectorFadeOut_CheckedChanged(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.FadeOut, self._checkBoxAffectorFadeOut.Checked)

	def checkBoxAffectorRotation_CheckedChanged(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Rotation, self._checkBoxAffectorRotation.Checked)

	def checkBoxAffectorGravity_CheckedChanged(self, sender, e):
		self._viewport.EnqueueCommand(CommandType.Gravity, self._checkBoxAffectorGravity.Checked)