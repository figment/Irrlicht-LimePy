import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Windows import *
from System.Windows.Controls import *
from System.Windows.Data import *
from System.Windows.Documents import *
from System.Windows.Input import *
from System.Windows.Media import *
from System.Windows.Media.Imaging import *
from System.Windows.Navigation import *
from System.Windows.Shapes import *

class MainWindow(Window):
	def __init__(self):
		self.InitializeComponent()

	def Window_Loaded(self, sender, e):
		self._userControl = WinFormsUserControl()
		wfHost.Child = self._userControl

	def Window_Closing(self, sender, e):
		if self._userControl.IsRendering:
			self._userControl.Shutdown()

	def buttonClose_Click(self, sender, e):
		self.Close()

	def checkboxNotifyResizes_Checked(self, sender, e):
		if self._userControl != None:
			self._userControl.IsNotifyResizes = checkboxNotifyResizes.IsChecked == False

	def checkboxDockViewport_Checked(self, sender, e):
		if wfHost != None:
			wfHost.Width = Double.NaN if checkboxDockViewport.IsChecked else wfHost.ActualWidth
			wfHost.Height = Double.NaN if checkboxDockViewport.IsChecked else wfHost.ActualHeight