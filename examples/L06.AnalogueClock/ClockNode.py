import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class ClockNode(SceneNode):
	def __new__(cls, parent, smgr):
		return SceneNode.__new__(cls, parent, smgr)
	
	def AddClockNode(parent):
		n = ClockNode(parent, parent.SceneManager)
		n.Drop()
		return n

	AddClockNode = staticmethod(AddClockNode)

	def __init__(self, parent, smgr):
		self._materialList = List[Material]()
		self._boundingBox = None
		self._arrowHours = None
		self._arrowMinutes = None
		self._arrowSeconds = None
		SceneManager = self.SceneManager
		self.OnGetBoundingBox += self.ClockNode_OnGetBoundingBox
		self.OnGetMaterialCount += self.ClockNode_OnGetMaterialCount
		self.OnGetMaterial += self.ClockNode_OnGetMaterial
		self.OnRegisterSceneNode += self.ClockNode_OnRegisterSceneNode
		self.OnRender += self.ClockNode_OnRender
		self.OnAnimate += self.ClockNode_OnAnimate
		# add clock face
		mesh = SceneManager.GeometryCreator.CreateCylinderMesh(100, 32, 6, Color(180, 180, 180))
		clockFace = SceneManager.AddMeshSceneNode(mesh, self)
		clockFace.Rotation = Vector3Df(90, 0, 0)
		clockFace.Position = Vector3Df(0, 0, 10)
		mesh.Drop()
		clockFace.UpdateAbsolutePosition()
		self._boundingBox = clockFace.BoundingBoxTransformed
		for i in xrange(0,clockFace.MaterialCount,1):
			self._materialList.Add(clockFace.GetMaterial(i))
		# add clock center
		mesh = SceneManager.GeometryCreator.CreateCylinderMesh(10, 24, 16, Color(255, 255, 255), False)
		clockCenter = SceneManager.AddMeshSceneNode(mesh, self)
		clockCenter.Rotation = Vector3Df(90, 0, 0)
		clockCenter.Position = Vector3Df(0, 0, -14)
		mesh.Drop()
		clockCenter.UpdateAbsolutePosition()
		self._boundingBox.AddInternalBox(clockCenter.BoundingBoxTransformed)
		for i in xrange(0,clockCenter.MaterialCount,1):
			self._materialList.Add(clockCenter.GetMaterial(i))
		# add clock ticks
		for j in xrange(0,12,1):
			mesh = SceneManager.GeometryCreator.CreateCylinderMesh(5, 10, 16, Color(255, 255, 255), False)
			clockTick = SceneManager.AddMeshSceneNode(mesh, self)
			clockTick.Rotation = Vector3Df(90, 0, 0)
			s = Math.Sin((j * (360 / 12)) / (180 / Math.PI))
			c = Math.Cos((j * (360 / 12)) / (180 / Math.PI))
			clockTick.Position = Vector3Df(s * 80, c * 80, 0)
			if (j % 3) == 0:
				clockTick.Scale = Vector3Df(2, 1, 2)
			mesh.Drop()
			clockTick.UpdateAbsolutePosition()
			self._boundingBox.AddInternalBox(clockTick.BoundingBoxTransformed)
			for i in xrange(0,clockTick.MaterialCount,1):
				self._materialList.Add(clockTick.GetMaterial(i))
		# add hour arrow
		mesh = SceneManager.GeometryCreator.CreateArrowMesh(12, 12, 40, 35, 4, 4, Color(40, 40, 255), Color(40, 40, 255))
		self._arrowHours = SceneManager.AddMeshSceneNode(mesh, self)
		self._arrowHours.GetMaterial(0).EmissiveColor = Color(0, 0, 255)
		self._arrowHours.GetMaterial(1).EmissiveColor = Color(0, 0, 255)
		self._arrowHours.Position = Vector3Df(0, 0, 3)
		mesh.Drop()
		self._arrowHours.UpdateAbsolutePosition()
		self._boundingBox.AddInternalBox(self._arrowHours.BoundingBoxTransformed)
		for i in xrange(0,self._arrowHours.MaterialCount,1):
			self._materialList.Add(self._arrowHours.GetMaterial(i))
		# add minute arrow
		mesh = SceneManager.GeometryCreator.CreateArrowMesh(12, 12, 60, 50, 4, 4, Color(40, 255, 40), Color(40, 255, 40))
		self._arrowMinutes = SceneManager.AddMeshSceneNode(mesh, self)
		self._arrowMinutes.GetMaterial(0).EmissiveColor = Color(0, 255, 0)
		self._arrowMinutes.GetMaterial(1).EmissiveColor = Color(0, 255, 0)
		self._arrowMinutes.Position = Vector3Df(0, 0, -5)
		mesh.Drop()
		self._arrowMinutes.UpdateAbsolutePosition()
		self._boundingBox.AddInternalBox(self._arrowMinutes.BoundingBoxTransformed)
		for i in xrange(0,self._arrowMinutes.MaterialCount,1):
			self._materialList.Add(self._arrowMinutes.GetMaterial(i))
		# add second arrow
		mesh = SceneManager.GeometryCreator.CreateArrowMesh(12, 12, 70, 60, 2, 2, Color(255, 40, 40), Color(255, 40, 40))
		self._arrowSeconds = SceneManager.AddMeshSceneNode(mesh, self)
		self._arrowSeconds.GetMaterial(0).EmissiveColor = Color(255, 0, 0)
		self._arrowSeconds.GetMaterial(1).EmissiveColor = Color(255, 0, 0)
		self._arrowSeconds.Position = Vector3Df(0, 0, -11)
		mesh.Drop()
		self._arrowSeconds.UpdateAbsolutePosition()
		self._boundingBox.AddInternalBox(self._arrowSeconds.BoundingBoxTransformed)
		for i in xrange(0,self._arrowSeconds.MaterialCount,1):
			self._materialList.Add(self._arrowSeconds.GetMaterial(i))
		SceneManager.AddLightSceneNode(self._arrowSeconds, Vector3Df(0, 70, 0), Colorf(self._arrowSeconds.GetMaterial(0).EmissiveColor), 80)
		SceneManager.AddLightSceneNode(self._arrowMinutes, Vector3Df(0, 60, 0), Colorf(self._arrowMinutes.GetMaterial(0).EmissiveColor), 60)
		SceneManager.AddLightSceneNode(self._arrowHours, Vector3Df(0, 40, 0), Colorf(self._arrowHours.GetMaterial(0).EmissiveColor), 40)

	def ClockNode_OnGetBoundingBox(self):
		return self._boundingBox

	def ClockNode_OnGetMaterialCount(self):
		return self._materialList.Count

	def ClockNode_OnGetMaterial(self, index):
		return self._materialList[index]

	def ClockNode_OnRegisterSceneNode(self):
		if self.Visible:
			self.SceneManager.RegisterNodeForRendering(self)

	def ClockNode_OnRender(self):
		pass

	# we need to add code here if we want to draw something that is not fitted into scene nodes,
	# but now our clock elements all is done via scene nodes.
	def ClockNode_OnAnimate(self, time):
		t = DateTime.Now
		self._arrowSeconds.Rotation = Vector3Df(0, 0, -t.Second * (360 / 60))
		self._arrowMinutes.Rotation = Vector3Df(0, 0, -t.Minute * (360 / 60))
		self._arrowHours.Rotation = Vector3Df(0, 0, -(t.Hour % 12) * (360 / 12))