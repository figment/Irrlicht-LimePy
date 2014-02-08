import System

class WinFormsUserControl(object):
	def __init__(self):
		# <summary> 
		# Required designer variable.
		# </summary>
		self._components = None
		pass
	def Dispose(self, disposing):
		""" <summary> 
		 Clean up any resources being used.
		 </summary>
		 <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		"""
		if disposing and (self._components != None):
			self._components.Dispose()
		self.Dispose(disposing)

	def InitializeComponent(self):
		""" <summary> 
		 Required method for Designer support - do not modify 
		 the contents of this method with the code editor.
		 </summary>
		"""
		self._components = System.ComponentModel.Container()
		self._AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font