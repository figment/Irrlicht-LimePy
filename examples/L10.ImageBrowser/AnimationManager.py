import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Scene import *
from AnimationManager import *

class AnimationItem(object):
	def __init__(self):
		self.Node = None
		self.Duration = 0
		self.StartTime = 0
		self.StartPosition = None
		self.StartRotation = None
		self.StartScale = None
		self.TargetPosition = None
		self.TargetRotation = None
		self.TargetScale = None
	
class AnimationManager(object):
	def __init__(self, irrDevice):
		self._animationItems = List[AnimationItem]()
		self._irrDevice = irrDevice

	def Add(self, node, duration, targetPosition, targetRotation, targetScale):
		self.Remove(node)
		self._irrDevice.Timer.Tick()
		a = AnimationItem()
		a.Node = node
		a.Node.Grab()
		a.Duration = duration
		a.StartTime = self._irrDevice.Timer.Time
		if targetPosition != None:
			a.TargetPosition = targetPosition
			a.StartPosition = node.Position
		if targetRotation != None:
			a.TargetRotation = targetRotation
			a.StartRotation = node.Rotation
		if targetScale != None:
			a.TargetScale = targetScale
			a.StartScale = node.Scale
		Threading.Monitor.Enter(self._animationItems)
		try:
			self._animationItems.Add(a)
		finally:
			Threading.Monitor.Exit(self._animationItems)

	def Remove(self, node):
		Threading.Monitor.Enter(self._animationItems)
		try:
			i = 0
			for i in xrange(0,self._animationItems.Count,1):
				if self._animationItems[i].Node == node:
					break
			if i < self._animationItems.Count:
				self.setFinalAnimationState(i)
				self._animationItems[i].Node.Drop()
				self._animationItems.RemoveAt(i)
		finally:
			Threading.Monitor.Exit(self._animationItems)

	def IsAnimated(self, node):
		Threading.Monitor.Enter(self._animationItems)
		try:
			i = 0
			for i in xrange(0,self._animationItems.Count,1):
				if self._animationItems[i].Node == node:
					break
			return i < self._animationItems.Count
		finally:
			Threading.Monitor.Exit(self._animationItems)

	def Run(self):
		Threading.Monitor.Enter(self._animationItems)
		try:
			t = self._irrDevice.Timer.Time
			candidatesToBeRemoved = List[int]()
			for i in xrange(0,self._animationItems.Count,1):
				a = self._animationItems[i]
				if t >= a.StartTime + a.Duration:
					self.setFinalAnimationState(i)
					candidatesToBeRemoved.Add(i)
				else:
					d = (t - a.StartTime) / a.Duration
					if a.TargetPosition != None:
						v = a.Node.Position
						v.Interpolate(a.TargetPosition, a.StartPosition, d)
						a.Node.Position = v
					if a.TargetRotation != None:
						v = a.Node.Rotation
						v.Interpolate(a.TargetRotation, a.StartRotation, d)
						a.Node.Rotation = v
					if a.TargetScale != None:
						v = a.Node.Scale
						v.Interpolate(a.TargetScale, a.StartScale, d)
						a.Node.Scale = v
			i = candidatesToBeRemoved.Count - 1
			while i >= 0:
				self._animationItems[candidatesToBeRemoved[i]].Node.Drop()
				self._animationItems.RemoveAt(candidatesToBeRemoved[i])
				i -= 1
		finally:
			Threading.Monitor.Exit(self._animationItems)

	def Clear(self):
		Threading.Monitor.Enter(self._animationItems)
		try:
			for i in xrange(0,self._animationItems.Count,1):
				self._animationItems[i].Node.Drop()
			self._animationItems.Clear()
		finally:
			Threading.Monitor.Exit(self._animationItems)

	def setFinalAnimationState(self, i):
		a = self._animationItems[i]
		if a.TargetPosition != None:
			a.Node.Position = a.TargetPosition
		if a.TargetRotation != None:
			a.Node.Rotation = a.TargetRotation
		if a.TargetScale != None:
			a.Node.Scale = a.TargetScale

		