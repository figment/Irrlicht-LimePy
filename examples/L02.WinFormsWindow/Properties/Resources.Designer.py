﻿import clr
import System
#------------------------------------------------------------------------------
# <auto-generated>
#     This code was generated by a tool.
#     Runtime Version:4.0.30319.225
#
#     Changes to this file may cause incorrect behavior and will be lost if
#     the code is regenerated.
# </auto-generated>
#------------------------------------------------------------------------------
from System import *

class Resources(object):
	# <summary>
	#   A strongly-typed resource class, for looking up localized strings, etc.
	# </summary>
	# This class was auto-generated by the StronglyTypedResourceBuilder
	# class via a tool like ResGen or Visual Studio.
	# To add or remove a member, edit your .ResX file then rerun ResGen
	# with the /str option, or rebuild your VS project.
	resourceMan = None
	resourceCulture = None
	def __init__(self):
		pass
	def get_ResourceManager(self):
		# <summary>
		#   Returns the cached ResourceManager instance used by this class.
		# </summary>
		if object.ReferenceEquals(Resources.resourceMan, None):
			temp = Resources.ResourceManager("L02.WinFormsWindow.Properties.Resources", clr.GetClrType(Resources).Assembly)
			Resources.resourceMan = temp
		return Resources.resourceMan

	ResourceManager = property(fget=get_ResourceManager)

	def get_Culture(self):
		# <summary>
		#   Overrides the current thread's CurrentUICulture property for all
		#   resource lookups using this strongly typed resource class.
		# </summary>
		return Resources.resourceCulture

	def set_Culture(self, value):
		Resources.resourceCulture = value

	Culture = property(fget=get_Culture, fset=set_Culture)