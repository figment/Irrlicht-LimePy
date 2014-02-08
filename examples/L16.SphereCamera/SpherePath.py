import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Xml import *
from System.Xml.Linq import *
from System.Text import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class SpherePath(object): # we use this list only to simplify loading and saving routines # same indices for both vertex buffers
	def get_Center(self):
		return self._center

	def set_Center(self, value):
		self._center = value

	Center = property(fget=get_Center, fset=set_Center)

	def get_FrontColor(self):
		return self._frontcolor

	def set_FrontColor(self, value):
		self._frontcolor = value

	FrontColor = property(fget=get_FrontColor, fset=set_FrontColor)

	def get_BackColor(self):
		return self._backcolor

	def set_BackColor(self, value):
		self._backcolor = value

	BackColor = property(fget=get_BackColor, fset=set_BackColor)

	def get_PointCount(self):
		return self._points.Count

	PointCount = property(fget=get_PointCount)

	def __init__(self, height):
		self._points = List[Vector3Df]()
		self._vertFront = VertexBuffer.Create()
		self._vertBack = VertexBuffer.Create()
		self._indBoth = IndexBuffer.Create(IndexType._16Bit)
		self._center = None
		self._frontcolor = None
		self._backcolor = None
		self._height = height
		self.Center = Vector3Df(0)
		self.FrontColor = Color.OpaqueCyan
		self.BackColor = Color.OpaqueBlue
		# we allocated once 64000 indices, initialize the sequence and never touch them in future... we will only use SetCount() method to set actual number of used indices
		self._indBoth.Reallocate(64000)
		for i in xrange(0,self._indBoth.AllocatedCount - 1,1):
			self._indBoth.Add(i)

	def Drop(self):
		self._vertFront.Drop()
		self._vertBack.Drop()
		self._indBoth.Drop()

	def AddPoint(self, point):
		self._points.Add(point)
		# add front line
		v1front = Vertex3D(point, Vector3Df(0), Color(0))
		v2front = Vertex3D((point - self.Center).Normalize() * self._height, Vector3Df(0), self.FrontColor)
		self._vertFront.Add(v1front)
		self._vertFront.Add(v2front)
		# add back line
		v1back = v1front
		v2back = Vertex3D(v2front)
		v2back.Color = self.BackColor
		self._vertBack.Add(v1back)
		self._vertBack.Add(v2back)
		# add connection line if possible (front and back)
		if self._vertFront.Count >= 4:
			self._vertFront.Add(self._vertFront.Get(self._vertFront.Count - 3))
			self._vertFront.Add(v2front)
			self._vertBack.Add(self._vertBack.Get(self._vertBack.Count - 3))
			self._vertBack.Add(v2back)
		# update indices "used" count
		self._indBoth.SetCount(self._vertFront.Count)

	def Clear(self):
		self._points.Clear()
		self._vertFront.Clear()
		self._vertBack.Clear()
		self._indBoth.SetCount(0)
 # we don't deallocate indices, we only set "used" count
	def Draw(self, driver):
		driver.SetTransform(TransformationState.World, Matrix.Identity)
		# set material
		m = Material.IdentityNoLighting
		m.Wireframe = True
		m.BackfaceCulling = False
		m.Type = MaterialType.TransparentVertexAlpha
		m.ZWrite = False
		# draw back lines
		m.ZBuffer = ComparisonFunc.Greater
		driver.SetMaterial(m)
		driver.DrawVertexPrimitiveList(self._vertBack, self._indBoth, PrimitiveType.Lines)
		# draw front lines
		m.ZBuffer = ComparisonFunc.LessEqual
		driver.SetMaterial(m)
		driver.DrawVertexPrimitiveList(self._vertFront, self._indBoth, PrimitiveType.Lines)
		# draw front points
		m.Thickness = 10
		driver.SetMaterial(m)
		driver.DrawVertexPrimitiveList(self._vertFront, self._indBoth, PrimitiveType.Points)

	def Save(self, filename):
		d = XDocument()
		d.Add(XElement("path"))
		d.Root.Add(XElement("center", XAttribute("x", self.Center.X), XAttribute("y", self.Center.Y), XAttribute("z", self.Center.Z)))
		d.Root.Add(XElement("frontColor", self.FrontColor.ARGB))
		d.Root.Add(XElement("backColor", self.BackColor.ARGB))
		for p in points:
			d.Root.Add(XElement("point", XAttribute("x", p.X), XAttribute("y", p.Y), XAttribute("z", p.Z)))
		d.Save(filename)

	def Load(self, filename):
		self.Clear()
		d = XDocument.Load(filename)
		self.Center.X = Convert.ToSingle(d.Root.Element("center").Attribute("x").Value)
		self.Center.Y = Convert.ToSingle(d.Root.Element("center").Attribute("y").Value)
		self.Center.Z = Convert.ToSingle(d.Root.Element("center").Attribute("z").Value)
		self.FrontColor.ARGB = Convert.ToUInt32(d.Root.Element("frontColor").Value)
		self.BackColor.ARGB = Convert.ToUInt32(d.Root.Element("backColor").Value)
		for e in d.Root.Elements("point"):
			p = Vector3Df(Convert.ToSingle(e.Attribute("x").Value), Convert.ToSingle(e.Attribute("y").Value), Convert.ToSingle(e.Attribute("z").Value))
			self.AddPoint(p)