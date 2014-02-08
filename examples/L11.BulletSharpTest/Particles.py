import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class Particles(object):
	def __init__(self, device):
		self._device = device
		self._particleNodes = List[ParticleNode]()

	def Add(self, parent, time):
		ps = self._device.SceneManager.AddParticleSystemSceneNode(False, parent)
		em = ps.CreateBoxEmitter(AABBox(parent.BoundingBox.MinEdge / 4, parent.BoundingBox.MaxEdge / 4), Vector3Df(Single(0), Single(0.025), Single(0)), 100, 200, Color(UInt32(4294967295)), Color(UInt32(4294967295)), 1500, 2500)
		em.MinStartSize = Dimension2Df(parent.BoundingBox.Extent.X, parent.BoundingBox.Extent.Y)
		em.MaxStartSize = em.MinStartSize * Single(1.5)
		ps.Emitter = em
		em.Drop()
		paf = ps.CreateFadeOutParticleAffector()
		ps.AddAffector(paf)
		paf.Drop()
		ps.SetMaterialFlag(MaterialFlag.Lighting, False)
		ps.SetMaterialFlag(MaterialFlag.ZWrite, False)
		ps.SetMaterialTexture(0, self._device.VideoDriver.GetTexture("../../media/fireball.bmp"))
		ps.SetMaterialType(MaterialType.TransparentAddColor)
		self._particleNodes.Add(ParticleNode(ps, time))

	def Winnow(self, time, simPaused):
		r = List[ParticleNode]()
		for n in particleNodes:
			if simPaused:
				n.TimeOfSteady = time
				continue
			m = n.Node.AbsoluteTransformation
			if m.Translation.Y < -20000:
				r.Add(n)
			else:
				if n.LastAbsoluteTransformation != m:
					n.LastAbsoluteTransformation = m
					n.TimeOfSteady = time
				else:
					if time - n.TimeOfSteady > 1000:
						r.Add(n)
		for n in r:
			n.Node.Remove()
			self._particleNodes.Remove(n)

	class ParticleNode(object):
		def __init__(self, n, time):
			self.Node = n
			self.TimeOfSteady = time
			self.LastAbsoluteTransformation = Matrix.Identity