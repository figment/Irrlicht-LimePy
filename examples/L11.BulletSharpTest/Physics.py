import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from BulletSharp import *

class Physics(object):
	def __init__(self):
		self._bulletShapes = List[CollisionShape]()
		self._simThread = None
		self._simTimeStep = 0
		pass

	class Shape(object):
		Box = 0
		Shpere = Box + 1
		Mesh = Shpere + 1
	def Setup(self, gravity):
		self._bulletCollisionConfiguration = DefaultCollisionConfiguration()
		self._bulletCollisionDispatcher = CollisionDispatcher(self._bulletCollisionConfiguration)
		self._bulletBroadphase = DbvtBroadphase()
		self._bulletWorld = DiscreteDynamicsWorld(self._bulletCollisionDispatcher, self._bulletBroadphase, None, self._bulletCollisionConfiguration)
		self._bulletWorld.Gravity = Vector3(gravity.X, gravity.Y, gravity.Z)

	def Drop(self):
		if self._simThread != None:
			self._simThread.Join()
		i = self._bulletWorld.NumConstraints - 1
		while i >= 0:
			c = self._bulletWorld.GetConstraint(i)
			self._bulletWorld.RemoveConstraint(c)
			c.Dispose()
			i -= 1
		i = self._bulletWorld.NumCollisionObjects - 1
		while i >= 0:
			o = self._bulletWorld.CollisionObjectArray[i]
			b = o
			if b != None and b.MotionState != None:
				b.MotionState.Dispose()
			self._bulletWorld.RemoveCollisionObject(o)
			o.Dispose()
			i -= 1
		for s in bulletShapes:
			s.Dispose()
		self._bulletShapes.Clear()
		self._bulletWorld.Dispose()
		self._bulletBroadphase.Dispose()
		self._bulletCollisionDispatcher.Dispose()
		self._bulletCollisionConfiguration.Dispose()

	def AddShape(self, shape, node, mass, sleeping, startImpulse):
		collShape = self.bulletGetCollisionShape(shape, node)
		if self._simThread != None:
			self._simThread.Join()
		self._bulletShapes.Add(collShape)
		body = self.bulletCreateRigidBody(mass, BulletSharp.Matrix.Translation(node.Position.X, node.Position.Y, node.Position.Z), collShape)
		if sleeping:
			body.ForceActivationState(ActivationState.IslandSleeping)
		if startImpulse != None:
			body.ApplyCentralImpulse(Vector3(startImpulse.X, startImpulse.Y, startImpulse.Z))
		body.SetSleepingThresholds(body.LinearSleepingThreshold * 20, body.AngularSleepingThreshold * 20)
		body.UserObject = node

	def StepSimulation(self, timeStep):
		self._simTimeStep += timeStep
		if self._simThread != None:
			return False
		def ParameterizedThreadStart_109_73(t):
			s = t
			if s > Single(1) / 60:
				s = Single(1) / 60
			self._bulletWorld.StepSimulation(s)
			m = Matrix()
			collObjects = self._bulletWorld.CollisionObjectArray
			i = collObjects.Count - 1
			while i >= 0:
				collObject = collObjects[i]
				if collObject.IsStaticObject or not collObject.IsActive:
					continue
				m.SetElementArray(collObject.WorldTransform.ToArray())
				n = collObject.UserObject
				n.Position = m.Translation
				n.Rotation = m.Rotation
				if m.Translation.Y < -40000:
					n.SceneManager.AddToDeletionQueue(n)
					self._bulletWorld.RemoveCollisionObject(collObject)
					collObject.Dispose()
				i -= 1
			self._simThread = None

		self._simThread = Thread(ParameterizedThreadStart(ParameterizedThreadStart_109_73))
		self._simThread.Start(self._simTimeStep)
		self._simTimeStep = 0
		return True

	def get_NumCollisionObjects(self):
		return self._bulletWorld.NumCollisionObjects

	NumCollisionObjects = property(fget=get_NumCollisionObjects)

	def bulletGetCollisionShape(self, shape, node):
		if shape == Shape.Box:
			return BoxShape(node.BoundingBox.Extent.X / 2)
		elif shape == Shape.Shpere:
			return SphereShape(node.BoundingBox.Extent.X / 2)
		elif shape == Shape.Mesh:
			meshNode = node
			if meshNode == None:
				raise ArgumentException()
			triangleMesh = TriangleMesh()
			for i in xrange(0,meshNode.Mesh.MeshBufferCount,1):
				b = meshNode.Mesh.GetMeshBuffer(i)
				inds = b.Indices
				verts = b.Vertices
				if inds == None or verts == None:
					raise ArgumentException()
				for j in xrange(0,inds.Length,3):
					v0 = verts[inds[j + 0]].Position
					v1 = verts[inds[j + 1]].Position
					v2 = verts[inds[j + 2]].Position
					triangleMesh.AddTriangle(Vector3(v0.X, v0.Y, v0.Z), Vector3(v1.X, v1.Y, v1.Z), Vector3(v2.X, v2.Y, v2.Z))
			return BvhTriangleMeshShape(triangleMesh, False)
		else:
			raise ArgumentException()

	def bulletCreateRigidBody(self, mass, startTransform, shape):
		isDynamic = (mass != Single(0))
		localInertia = Vector3.Zero
		if isDynamic:
			_tmp207_32, localInertia = shape.CalculateLocalInertia(mass)
			_tmp207_32
		motionState = DefaultMotionState(startTransform)
		rbInfo = RigidBodyConstructionInfo(mass, motionState, shape, localInertia)
		body = RigidBody(rbInfo)
		self._bulletWorld.AddRigidBody(body)
		return body