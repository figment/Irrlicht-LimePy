import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from IrrlichtLime.Core import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Video import *

class Shadows(object):
	def __init__(self, shadowColor, shadowInfinityRange):
		self._objects = List[SceneNode]()
		self._lights = List[SceneNode]()
		self._shadowColor = Color.OpaqueBlack
		self._shadowInfinityRange = Single(1000)
		self._shadowNearMultiplier = Single(1) / 40
		self._visibleShadowVerticesBuffer = None
		self._visibleShadowVerticesBufferLocker = object()
		self._buildThread = None
		self._shadowColor = shadowColor
		self._shadowInfinityRange = Single(shadowInfinityRange)
		self._shadowNearMultiplier = Single(Single(1) / Math.Sqrt(shadowInfinityRange))

	def Drop(self):
		if self._buildThread != None:
			self._buildThread.Join()

	def AddObject(self, node):
		if self._buildThread != None:
			self._buildThread.Join()
		if not (isinstance(node,MeshSceneNode)) and not (isinstance(node,AnimatedMeshSceneNode)):
			raise ArgumentException()
		node.UpdateAbsolutePosition()
		self._objects.Add(node)

	def RemoveObject(self, node):
		if self._buildThread != None:
			self._buildThread.Join()
		self._objects.Remove(node)

	def AddLight(self, node):
		if self._buildThread != None:
			self._buildThread.Join()
		node.UpdateAbsolutePosition()
		self._lights.Add(node)

	def RemoveLight(self, node):
		if self._buildThread != None:
			self._buildThread.Join()
		self._lights.Remove(node)

	def DrawShadowVolume(self, driver, isDebug=False):
		Monitor.Enter(self._visibleShadowVerticesBufferLocker)
		try:
			if self._visibleShadowVerticesBuffer == None or self._visibleShadowVerticesBuffer.Count == 0:
				return 
			driver.SetTransform(TransformationState.World, Matrix.Identity)
			if isDebug:
				material = Material()
				material.Lighting = False
				material.Type = MaterialType.TransparentVertexAlpha
				driver.SetMaterial(material)
				for i in xrange(0,self._visibleShadowVerticesBuffer.Count,3):
					driver.Draw3DTriangle(self._visibleShadowVerticesBuffer[i], self._visibleShadowVerticesBuffer[i + 1], self._visibleShadowVerticesBuffer[i + 2], Color(UInt32(2147483648)))
				material.Wireframe = True
				material.BackfaceCulling = False
				material.ZBuffer = ComparisonFunc.Always
				driver.SetMaterial(material)
				for i in xrange(0,self._visibleShadowVerticesBuffer.Count,3):
					driver.Draw3DTriangle(self._visibleShadowVerticesBuffer[i], self._visibleShadowVerticesBuffer[i + 1], self._visibleShadowVerticesBuffer[i + 2], Color(UInt32(2164195328)))
			else:
				driver.DrawStencilShadowVolume(self._visibleShadowVerticesBuffer)
				driver.DrawStencilShadow(False, self._shadowColor)
		finally:
			Monitor.Exit(self._visibleShadowVerticesBufferLocker)

	def get_VerticesBuilt(self):
		Monitor.Enter(self._visibleShadowVerticesBufferLocker)
		try:
			return self._visibleShadowVerticesBuffer.Count if self._visibleShadowVerticesBuffer != None else 0
		finally:
			Monitor.Exit(self._visibleShadowVerticesBufferLocker)

	VerticesBuilt = property(fget=get_VerticesBuilt)

	def BuildShadowVolume(self):
		if self._buildThread != None:
			return False
		def ThreadStart_136_45():
			va = 10000
			Monitor.Enter(self._visibleShadowVerticesBufferLocker)
			try:
				if self._visibleShadowVerticesBuffer != None:
					va = self._visibleShadowVerticesBuffer.Count
			finally:
				Monitor.Exit(self._visibleShadowVerticesBufferLocker)
			v = List[Vector3Df](va)
			for lightNode in self._lights:
				l = lightNode.AbsolutePosition
				for objectNode in self._objects:
					t = objectNode.AbsoluteTransformation
					m = None
					if isinstance(objectNode,MeshSceneNode):
						m = (objectNode).Mesh
					elif isinstance(objectNode,AnimatedMeshSceneNode):
						m = (objectNode).Mesh
					for i in xrange(0,m.MeshBufferCount,1):
						self.buildShadowVolume(v, m.GetMeshBuffer(i), t, l)
			Monitor.Enter(self._visibleShadowVerticesBufferLocker)
			try:
				if self._visibleShadowVerticesBuffer != None:
					self._visibleShadowVerticesBuffer.Clear()
				self._visibleShadowVerticesBuffer = v
			finally:
				Monitor.Exit(self._visibleShadowVerticesBufferLocker)
			self._buildThread = None

		self._buildThread = Thread(ThreadStart(ThreadStart_136_45))
		self._buildThread.Start()
		return True

	def buildShadowVolume(self, shadowVertices, meshbuffer, matrix, light):
		indices = meshbuffer.Indices
		if indices == None:
			raise ArgumentException()
		t123 = Triangle3Df()
		for i in xrange(0,indices.Length,3):
			v1 = meshbuffer.GetPosition(indices[i])
			v2 = meshbuffer.GetPosition(indices[i + 1])
			v3 = meshbuffer.GetPosition(indices[i + 2])
			v1 = matrix.TransformVector(v1)
			v2 = matrix.TransformVector(v2)
			v3 = matrix.TransformVector(v3)
			t123.Set(v1, v2, v3)
			v1Dir = v1 - light
			if not t123.IsFrontFacing(v1Dir):
				continue
			v2Dir = v2 - light
			v3Dir = v3 - light
			# calc near points
			v1near = v1 + v1Dir * self._shadowNearMultiplier
			v2near = v2 + v2Dir * self._shadowNearMultiplier
			v3near = v3 + v3Dir * self._shadowNearMultiplier
			# calc infinity points
			v1inf = v1 + v1Dir.Normalize() * self._shadowInfinityRange
			v2inf = v2 + v2Dir.Normalize() * self._shadowInfinityRange
			v3inf = v3 + v3Dir.Normalize() * self._shadowInfinityRange
			# top
			shadowVertices.Add(v1near)
			shadowVertices.Add(v2near)
			shadowVertices.Add(v3near)
			# bottom
			shadowVertices.Add(v3inf)
			shadowVertices.Add(v2inf)
			shadowVertices.Add(v1inf)
			# side1
			shadowVertices.Add(v1inf)
			shadowVertices.Add(v2near)
			shadowVertices.Add(v1near)
			shadowVertices.Add(v1inf)
			shadowVertices.Add(v2inf)
			shadowVertices.Add(v2near)
			# side2
			shadowVertices.Add(v2inf)
			shadowVertices.Add(v3near)
			shadowVertices.Add(v2near)
			shadowVertices.Add(v2inf)
			shadowVertices.Add(v3inf)
			shadowVertices.Add(v3near)
			# side3
			shadowVertices.Add(v1near)
			shadowVertices.Add(v3near)
			shadowVertices.Add(v1inf)
			shadowVertices.Add(v3near)
			shadowVertices.Add(v3inf)
			shadowVertices.Add(v1inf)