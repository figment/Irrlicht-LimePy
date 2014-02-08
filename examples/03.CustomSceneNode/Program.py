import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")

import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class Program(object):
	def Main(args):
		device = IrrlichtDevice.CreateDevice(DriverType.OpenGL, Dimension2Di(640, 480), 16, False)
		driver = device.VideoDriver
		smgr = device.SceneManager
		smgr.AddCameraSceneNode(None, Vector3Df(0, -40, 0), Vector3Df(0))
		myNode = CSampleSceneNode(smgr.RootNode, smgr, 667)
		anim = smgr.CreateRotationAnimator(Vector3Df(Single(0.8), 0, Single(0.8)))
		if anim != None:
			myNode.AddAnimator(anim)
			anim.Drop()
			anim = None
		myNode.Drop()
		myNode = None
		frames = 0
		while device.Run():
			driver.BeginScene(True, True, Color(100, 100, 100))
			smgr.DrawAll()
			driver.EndScene()
			frames += 1
			if frames == 100:
				device.SetWindowCaption(String.Format("Custom Scene Node - Irrlicht Engine [{0}] fps: {1}", driver.Name, driver.FPS))
				frames = 0
		device.Drop()

	Main = staticmethod(Main)

class CSampleSceneNode(SceneNode):
	def __init__(self, parent, smgr, id):
		self._bbox = AABBox()
		self._material = Material()
		self.OnRegisterSceneNode += self.CSampleSceneNode_OnRegisterSceneNode
		self.OnRender += self.CSampleSceneNode_OnRender
		self.OnGetBoundingBox += self.CSampleSceneNode_OnGetBoundingBox
		self.OnGetMaterialCount += self.CSampleSceneNode_OnGetMaterialCount
		self.OnGetMaterial += self.CSampleSceneNode_OnGetMaterial
		self._material.Wireframe = False
		self._material.Lighting = False
		self._vertices = Array.CreateInstance(Vertex3D, 4)
		self._vertices[0] = Vertex3D(0, 0, 10, 1, 1, 0, Color(0, 255, 255), 0, 1)
		self._vertices[1] = Vertex3D(10, 0, -10, 1, 0, 0, Color(255, 0, 255), 1, 1)
		self._vertices[2] = Vertex3D(0, 20, 0, 0, 1, 1, Color(255, 255, 0), 1, 0)
		self._vertices[3] = Vertex3D(-10, 0, -10, 0, 0, 1, Color(0, 255, 0), 0, 0)
		self._bbox.Set(self._vertices[0].Position)
		for i in xrange(1,self._vertices.Length,1):
			self._bbox.AddInternalPoint(self._vertices[i].Position)

	def CSampleSceneNode_OnRegisterSceneNode(self):
		if self.Visible:
			self.SceneManager.RegisterNodeForRendering(self)

	def CSampleSceneNode_OnRender(self):
		indices = Array[UInt16]((0, 2, 3, 2, 1, 3, 1, 0, 3, 2, 0, 1))
		driver = self.SceneManager.VideoDriver
		driver.SetMaterial(self._material)
		driver.SetTransform(TransformationState.World, self.AbsoluteTransformation)
		driver.DrawVertexPrimitiveList(self._vertices, indices)

	def CSampleSceneNode_OnGetBoundingBox(self):
		return self._bbox

	def CSampleSceneNode_OnGetMaterialCount(self):
		return 1

	def CSampleSceneNode_OnGetMaterial(self, index):
		return self._material

Program.Main(None)