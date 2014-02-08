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
from System.Windows.Forms import *
from Form1 import Form1

class Program(object):
	def Main():
		# <summary>
		# The main entry point for the application.
		# </summary>
		Application.EnableVisualStyles()
		Application.SetCompatibleTextRenderingDefault(False)
		Application.Run(Form1())

	Main = staticmethod(Main)

Program.Main()