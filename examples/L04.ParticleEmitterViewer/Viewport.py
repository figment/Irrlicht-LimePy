import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from IrrlichtLime import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Core import *
from Command import *
from ParticleInfo import *
from IrrlichtLime.Video import Color as VColor

class SceneNodeID(object):
	Camera = 0
	AxisX = Camera + 1
	AxisY = AxisX + 1
	AxisZ = AxisY + 1
	Plane = AxisZ + 1
	ParticleSystem = Plane + 1 

class Viewport(object):
	""" <summary>
	 This class do all the rendering work.
	 This class is the only place where we actually use IrrlichtLime.
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 This class do all the rendering work.
		 This class is the only place where we actually use IrrlichtLime.
		 </summary>
		"""
		self._irrThread = None
		self._irrDevice = None
		self._commandQueue = None
		self._affFadeOut = None  # We store these pointers because when affector once added 
		self._affGravity = None  # to particle system, there is no any method to retrieve 
		self._affRotation = None # its pointer back later :(
		pass
	
	def Start(self, windowHandle):
		if self._irrThread != None:
			raise InvalidOperationException("Previous viewport needs to be stopped!")
		self._commandQueue = Queue[Command]()
		self._irrThread = Thread(ParameterizedThreadStart(self.irrThreadMain))
		self._irrThread.Name = "Irrlicht rendering"
		p = IrrlichtCreationParameters()
		#p.AntiAliasing = 4;
		p.DriverType = DriverType.Direct3D9
		p.WindowID = windowHandle
		self._irrThread.Start(p)
		print "Started", self._commandQueue

	def Stop(self):
		self.EnqueueCommand(CommandType.Abort, None)
		if self._irrThread != None:
			self._irrThread.Join(200)
			if self._irrThread.IsAlive:
				self._irrThread.Abort()
		self._irrThread = None

	def EnqueueCommand(self, type, param):
		if self._commandQueue == None:
			return
		c = Command()
		c.Type = type
		c.Param = param
		# If this is Abort command -- we clean up all the queue (all old commands that still waiting
		# for processing) and add this Abort command, since it is a top priority command.
		if c.Type == CommandType.Abort:
			Monitor.Enter(self._commandQueue)
			try:
				self._commandQueue.Clear()
				self._commandQueue.Enqueue(c)
			finally:
				Monitor.Exit(self._commandQueue)
			return 
		# We check for old same command and use it instead of adding new one -- for optimization.
		# This way we make not more than only one command of same type to be in the queue.
		Monitor.Enter(self._commandQueue)
		try:
			for n in self._commandQueue:
				if n.Type == c.Type:
					n.Param = c.Param
					return 
		finally:
			Monitor.Exit(self._commandQueue)
		# We add new command to queue.
		Monitor.Enter(self._commandQueue)
		try:
			self._commandQueue.Enqueue(c)
		finally:
			Monitor.Exit(self._commandQueue)

		
	def irrThreadMain(self, args):
		self._irrDevice = IrrlichtDevice.CreateDevice(args)
		if self._irrDevice == None:
			return
		# Camera
		camera = self._irrDevice.SceneManager.AddCameraSceneNode(None, Vector3Df(0), Vector3Df(0, 80, 0), SceneNodeID.Camera)
		anim = self._irrDevice.SceneManager.CreateFlyCircleAnimator(Vector3Df(0, 100, 0), Single(200), Single(0.0002))
		camera.AddAnimator(anim)
		anim.Drop()
		# Skydome
		self._irrDevice.SceneManager.AddSkyDomeSceneNode(self._irrDevice.VideoDriver.GetTexture("../../media/skydome.jpg"), 16, 8, Single(0.95), Single(2))
		# Plane
		m = self._irrDevice.SceneManager.AddHillPlaneMesh("plane", Dimension2Df(1000), Dimension2Di(1), None, 0, Dimension2Df(0), Dimension2Df(8))
		n = self._irrDevice.SceneManager.AddAnimatedMeshSceneNode(m, None, SceneNodeID.Plane)
		n.SetMaterialFlag(MaterialFlag.Lighting, False)
		n.SetMaterialTexture(0, self._irrDevice.VideoDriver.GetTexture("../../media/rockwall.jpg"))
		# Axes
		m = self._irrDevice.SceneManager.AddArrowMesh("axisX")
		n = self._irrDevice.SceneManager.AddAnimatedMeshSceneNode(m, None, SceneNodeID.AxisX, Vector3Df(), Vector3Df(0, 0, -90), Vector3Df(50, 120, 50))
		n.GetMaterial(0).EmissiveColor = VColor(250, 250, 250)
		n.GetMaterial(1).EmissiveColor = VColor(250, 0, 0)
		m = self._irrDevice.SceneManager.AddArrowMesh("axisY")
		n = self._irrDevice.SceneManager.AddAnimatedMeshSceneNode(m, None, SceneNodeID.AxisY, Vector3Df(), Vector3Df(0, 0, 0), Vector3Df(50, 120, 50))
		n.GetMaterial(0).EmissiveColor = VColor(250, 250, 250)
		n.GetMaterial(1).EmissiveColor = VColor(0, 250, 0)
		m = self._irrDevice.SceneManager.AddArrowMesh("axisZ")
		n = self._irrDevice.SceneManager.AddAnimatedMeshSceneNode(m, None, SceneNodeID.AxisZ, Vector3Df(), Vector3Df(90, 0, 0), Vector3Df(50, 120, 50))
		n.GetMaterial(0).EmissiveColor = VColor(250, 250, 250)
		n.GetMaterial(1).EmissiveColor = VColor(0, 0, 250)
		self.irrThreadShowAxes(False)
		# Particle system
		ps = self._irrDevice.SceneManager.AddParticleSystemSceneNode(False, None, SceneNodeID.ParticleSystem)
		ps.SetMaterialFlag(MaterialFlag.Lighting, False)
		ps.SetMaterialFlag(MaterialFlag.ZWrite, False)
		ps.SetMaterialTexture(0, self._irrDevice.VideoDriver.GetTexture("../../media/particle.bmp"))
		ps.SetMaterialType(MaterialType.TransparentAddColor) 
		em = ps.CreateSphereEmitter(Vector3Df(), 20 # position and radius
			, Vector3Df(Single(0), Single(0.1), Single(0)) # initial direction 
			, 150, 300 # emit rate
			, VColor(255, 255, 255, 0) # darkest color 
			, VColor(255, 255, 255, 0) # brightest color 
			, 750, 1500, 0 # min and max age, angle 
			, Dimension2Df(Single(20)) # min size
			, Dimension2Df(Single(40)) # max size
			) 
		ps.Emitter = em
		em.Drop()
		# Particle affectors
		self._affFadeOut = ps.CreateFadeOutParticleAffector()
		ps.AddAffector(self._affFadeOut)
		self._affFadeOut.Drop()
		self._affGravity = ps.CreateGravityAffector(Vector3Df(0, -1, 0), 3000)
		self._affGravity.Enabled = False
		ps.AddAffector(self._affGravity)
		self._affGravity.Drop()
		self._affRotation = ps.CreateRotationAffector(Vector3Df(-90, 240, -120), Vector3Df(0, 100, 0))
		ps.AddAffector(self._affRotation)
		self._affRotation.Drop()
		# Rendering loop
		rs = 0
		re = 0 # render frame time
		while self._irrDevice.Run():
			if self._irrDevice.VideoDriver.ScreenSize.Area != 0:
				self._irrDevice.VideoDriver.BeginScene()
				self._irrDevice.SceneManager.DrawAll()
				re = self._irrDevice.Timer.Time
				self.irrThreadDrawText(Vector2Di(8, 8), "Frame time: " + ("< 1" if self._irrDevice.VideoDriver.FPS > 1000 else (re - rs).ToString()) + " ms")
				self._irrDevice.VideoDriver.EndScene()
			else:
				Thread.Sleep(50)
			self.irrThreadProcessCommandQueue()
			rs = self._irrDevice.Timer.Time
		self._irrDevice.Drop()

	def irrThreadDrawText(self, p, s):
		if self._irrDevice == None:
			return
		d = self._irrDevice.GUIEnvironment.BuiltInFont.GetDimension(s)
		d.Width += 8
		d.Height += 6
		self._irrDevice.VideoDriver.Draw2DRectangle(Recti(p, d), VColor(UInt32(0x7F000000)))
		self._irrDevice.GUIEnvironment.BuiltInFont.Draw(s, p + Vector2Di(4, 3), VColor(250, 250, 250))

	def irrThreadShowAxes(self, v):
		if not self._irrDevice:
			return
		self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.AxisX).Visible = v
		self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.AxisY).Visible = v
		self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.AxisZ).Visible = v

	def irrThreadProcessCommandQueue(self):
		if self._commandQueue == None or self._irrDevice == None:
			return
		Monitor.Enter(self._commandQueue)
		try:
			if self._commandQueue.Count == 0:
				return 
			c = self._commandQueue.Dequeue()
		finally:
			Monitor.Exit(self._commandQueue)
		if c.Type == CommandType.Abort:
			self._irrDevice.Close()
			pass #break
		elif c.Type == CommandType.Axes:
			self.irrThreadShowAxes(c.Param)
			pass #break
		elif c.Type == CommandType.Plane:
			n = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.Plane)
			n.Visible = c.Param
			pass #break
		elif c.Type == CommandType.Particle:
			n = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.ParticleSystem)
			n.SetMaterialTexture(0, self._irrDevice.VideoDriver.GetTexture((c.Param).FileName))
			pass #break
		elif c.Type == CommandType.Resize:
			i = c.Param
			d = Dimension2Di(i[0], i[1])
			self._irrDevice.VideoDriver.ResizeNotify(d)
			(self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.Camera)).AspectRatio = i[0] / i[1] if i[2] == 1 else Single(1.333333)
			pass #break
		elif c.Type == CommandType.Position:
			f = c.Param
			p = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.ParticleSystem)
			(p.Emitter).Center = Vector3Df(f[0], f[1], f[2])
			pass #break
		elif c.Type == CommandType.Radius:
			f = c.Param
			p = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.ParticleSystem)
			(p.Emitter).Radius = f
			pass #break
		elif c.Type == CommandType.CameraView:
			f = c.Param
			p = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.Camera)
			p.Target = Vector3Df(p.Target.X, f, p.Target.Z)
			pass #break
		elif c.Type == CommandType.Rate:
			v = c.Param
			p = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.ParticleSystem)
			p.Emitter.MaxParticlesPerSecond = v
			p.Emitter.MinParticlesPerSecond = v / 2
			pass #break
		elif c.Type == CommandType.Size:
			v = c.Param
			p = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.ParticleSystem)
			p.Emitter.MaxStartSize = Dimension2Df(v)
			p.Emitter.MinStartSize = Dimension2Df(v / 2)
			pass #break
		elif c.Type == CommandType.Direction:
			f = c.Param
			p = self._irrDevice.SceneManager.GetSceneNodeFromID(SceneNodeID.ParticleSystem)
			p.Emitter.Direction = Vector3Df(f[0], f[1], f[2])
			pass #break
		elif c.Type == CommandType.FadeOut:
			self._affFadeOut.Enabled = c.Param
			pass #break
		elif c.Type == CommandType.Rotation:
			self._affRotation.Enabled = c.Param
			pass #break
		elif c.Type == CommandType.Gravity:
			self._affGravity.Enabled = c.Param
			pass #break
		else:
			raise InvalidOperationException("Unexpected command type: " + c.Type.ToString())