import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import Color as VColor

class LightningShot(object):
	def get_TotalShots(self):
		return self._shots.Count

	TotalShots = property(fget=get_TotalShots)

	def get_TotalLightnings(self):
		return self._indexBuffer.Count / (2 * 10)

	TotalLightnings = property(fget=get_TotalLightnings)
 	# number of points for each line is 2, number of lines for each lightning is 10
  	# 11 colors (line count + 1, since each line has 2 points) 
  	# do not displace first and last points
	def __init__(self, sceneManager, worldTriangles, worldInfinity=5000, shotSpeed=Single(0.1), shotRadius=100):
		self._shots = List[LightningShot.Shot]()
		self._sceneManager = sceneManager
		self._worldTriangles = worldTriangles
		self._worldInfinity = worldInfinity
		self._shotSpeed = shotSpeed
		self._shotRadius = shotRadius
		self._indexBuffer = IndexBuffer.Create(IndexType._16Bit)
		self._indexBuffer.Reallocate(64000)
		for i in xrange(0,self._indexBuffer.AllocatedCount - 1,1):
			self._indexBuffer.Add(i)
		self._vertexBuffer = VertexBuffer.Create()

	def Fire(self, position, direction, time):
		s = LightningShot.Shot()
		s.direction = direction
		e = position + s.direction * self._worldInfinity
		l = Line3Df(position, e)
		_tmp53_60, cv, ct, cn = self._sceneManager.SceneCollisionManager.GetCollisionPoint(l, self._worldTriangles)
		if _tmp53_60:
			e = cv
		s.deathTime = time + ((e - position).Length / self._shotSpeed)
		s.node = self._sceneManager.AddSphereSceneNode(10)
		s.node.SetMaterialFlag(MaterialFlag.Lighting, False)
		self._sceneManager.MeshManipulator.SetVertexColors((s.node).Mesh, VColor.OpaqueWhite)
		s.node.AddAnimator(self._sceneManager.CreateFlyStraightAnimator(position, e, (s.deathTime - time) / Single(1000)))
		s.node.AnimatorList[0].Drop()
		self._sceneManager.AddLightSceneNode(s.node)
		self._shots.Add(s)

	def removeDead(self, time):
		deleteCandidates = List[int]()
		for i in xrange(0,self._shots.Count,1):
			if time >= self._shots[i].deathTime:
				deleteCandidates.Add(i)
		i = deleteCandidates.Count - 1
		while i >= 0:
			j = deleteCandidates[i]
			self._shots[j].node.Remove()
			self._shots.RemoveAt(j)
			i -= 1

	def Draw(self, time):
		self.removeDead(time)
		mat = Material()
		mat.Type = MaterialType.TransparentVertexAlpha
		mat.Lighting = False
		self._sceneManager.VideoDriver.SetMaterial(mat)
		self._sceneManager.VideoDriver.SetTransform(TransformationState.World, Matrix.Identity)
		random = Random()
		colors = Array.CreateInstance(VColor, 11)
		for i in xrange(0,colors.Length,1):
			colors[i] = VColor(255, 255, 255, 255 - (10 - i) * 25)
		self._vertexBuffer.SetCount(0)
		for shot in self._shots:
			pos = shot.node.Position
			box = AABBox(pos - Vector3Df(self._shotRadius), pos + Vector3Df(self._shotRadius))
			tris = self._worldTriangles.GetTriangles(box, 1000)
			if tris.Count == 0:
				continue
			uniquePoints = Dictionary[Single, Vector3Df]()
			for t in tris:
				p = t.GetClosestPointOnTriangle(pos)
				k = p.X + p.Y * 1000 + p.Z * 1000000
				uniquePoints[k] = p
			for point in uniquePoints.Values:
				n = self._sceneManager.AddBillboardSceneNode(None, Dimension2Df(Single(7.5)))
				n.SetMaterialFlag(MaterialFlag.Lighting, False)
				n.SetMaterialType(MaterialType.TransparentAddColor)
				n.SetMaterialTexture(0, self._sceneManager.VideoDriver.GetTexture("../../media/particlewhite.bmp"))
				n.Position = point
				n.AddAnimator(self._sceneManager.CreateDeleteAnimator(Single(0.1)))
				n.AnimatorList[0].Drop()
				v1 = Vertex3D(point)
				v2 = Vertex3D()
				for i in xrange(0,10,1):
					v1.Color = colors[i]
					v2.Color = colors[i + 1]
					v2.Position = pos.GetInterpolated(point, i * 0.111)
					if i != 0 and i != 9:
						v2.Position += Vector3Df((random.Next() % 10) - 5, (random.Next() % 10) - 5, (random.Next() % 10) - 5);
					self._vertexBuffer.Add(v1)
					self._vertexBuffer.Add(v2)
					v1.Position = v2.Position
		self._indexBuffer.SetCount(self._vertexBuffer.Count)
		self._sceneManager.VideoDriver.DrawVertexPrimitiveList(self._vertexBuffer, self._indexBuffer, PrimitiveType.Lines)

	def Drop(self):
		self._indexBuffer.Drop()
		self._vertexBuffer.Drop()
		self._shots.ForEach(lambda s: s.node.Remove())
		self._shots.Clear()

	class Shot(object):
		def __init__(self):
			self.node = None
			self.direction = None
			self.deathTime = UInt32(0)
			