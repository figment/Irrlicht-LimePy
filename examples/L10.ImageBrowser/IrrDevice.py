import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *

class IrrDevice(object):
	def __init__(self):
		self._locker = object()
		self._locked = False
		pass
	def get_Device(self):
		if not self.IsLocked():
			raise InvalidOperationException()
		else:
			return self._device

	Device = property(fget=get_Device)

	def get_Driver(self):
		if not self.IsLocked():
			raise InvalidOperationException()
		else:
			return self._device.VideoDriver

	Driver = property(fget=get_Driver)

	def get_DriverNoCheck(self):
		return self._device.VideoDriver

	DriverNoCheck = property(fget=get_DriverNoCheck)
 # this one used for creating software images
	def get_Scene(self):
		return self._device.SceneManager

	Scene = property(fget=get_Scene)

	def get_GUI(self):
		return self._device.GUIEnvironment

	GUI = property(fget=get_GUI)

	def get_Timer(self):
		return self._device.Timer

	Timer = property(fget=get_Timer)

	def get_Randomizer(self):
		return self._device.Randomizer

	Randomizer = property(fget=get_Randomizer)

	def get_Logger(self):
		return self._device.Logger

	Logger = property(fget=get_Logger)

	def Lock(self):
		while True:
			Thread.Sleep(1)
			Monitor.Enter(self._locker)
			try:
				if self._locked:
					continue
				self._locked = True
				break
			finally:
				Monitor.Exit(self._locker)

	def Unlock(self):
		Monitor.Enter(self._locker)
		try:
			if not self._locked:
				raise InvalidOperationException()
			self._locked = False
		finally:
			Monitor.Exit(self._locker)

	def IsLocked(self):
		Monitor.Enter(self._locker)
		try:
			return self._locked
		finally:
			Monitor.Exit(self._locker)

	def CreateDevice(self, driverType, windowSize):
		self._device = IrrlichtDevice.CreateDevice(driverType, windowSize)

	def Drop(self):
		if self.IsLocked():
			raise InvalidOperationException()
		self._device.Drop()