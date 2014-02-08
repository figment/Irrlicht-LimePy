import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Scene import *

class SphereCamera(object):
	def __init__(self, device, target, minRadius, maxRadius, initRadius, initInclination, initAzimuth):
		self._device = device
		self._target = target
		self._camera = device.SceneManager.AddCameraSceneNode()
		self._minRadius = minRadius
		self._maxRadius = maxRadius
		self._radius = initRadius
		self._inclination = initInclination
		self._azimuth = initAzimuth
		self.setupCameraProperties()
		device.OnEvent += self.device_OnEvent

	def get_Radius(self):
		return self._radius

	def set_Radius(self, value):
		if value < minRadius:
			value = minRadius
		if value > maxRadius:
			value = maxRadius
		self._radius = value
		self.setupCameraProperties()

	Radius = property(fget=get_Radius, fset=set_Radius)

	def get_Inclination(self):
		return self._inclination

	def set_Inclination(self, value):
		value %= 360 # (-360..+360)
		if value < 0:
			value = 360 + value # [0..360)
		self._inclination = value
		self.setupCameraProperties()

	Inclination = property(fget=get_Inclination, fset=set_Inclination)

	def get_Azimuth(self):
		return self._azimuth

	def set_Azimuth(self, value):
		if value > 75:
			value = 75
		if value < -75:
			value = -75
		self._azimuth = value
		self.setupCameraProperties()

	Azimuth = property(fget=get_Azimuth, fset=set_Azimuth)

	def device_OnEvent(self, evnt):
		if evnt.Type == EventType.Mouse:
			if evnt.Mouse.Type == MouseEventType.Wheel: # zoom
				self.Radius += evnt.Mouse.Wheel
				return True
			if evnt.Mouse.Type == MouseEventType.LeftDown:
				self._prevMouseX = evnt.Mouse.X
				self._prevMouseY = evnt.Mouse.Y
				return True # rotation
			if evnt.Mouse.Type == MouseEventType.Move and evnt.Mouse.IsLeftPressed():
				self.Inclination -= (evnt.Mouse.X - self._prevMouseX) / 4
				self.Azimuth += (evnt.Mouse.Y - self._prevMouseY) / 3
				self._prevMouseX = evnt.Mouse.X
				self._prevMouseY = evnt.Mouse.Y
				return True
		return False

	def setupCameraProperties(self):
		deg2rad = Math.PI / 180
		p = Vector3Df()
		p.X = (self._radius * Math.Cos(self._inclination * deg2rad) * Math.Cos(self._azimuth * deg2rad))
		p.Y = (self._radius * Math.Sin(self._azimuth * deg2rad))
		p.Z = (self._radius * Math.Sin(self._inclination * deg2rad) * Math.Cos(self._azimuth * deg2rad))
		self._camera.Position = p + self._target
		self._camera.Target = self._target

	def ToString(self):
		return str.Format("[SphereCamera] Radius={0} Inclination={1} Azimuth={2}", self.Radius, self.Inclination, self.Azimuth)