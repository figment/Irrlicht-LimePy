import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *

class CommandType(object):
	# Abort request.
	# Param: N/A
	Abort = 0
	# Axes visibility on/off.
	# Param: bool
	Axes = Abort + 1
	# Plane visibility on/off.
	# Param: bool
	Plane = Axes + 1
	# New particle.
	# Param: ParticleInfo
	Particle = Plane + 1
	# Viewport resize.
	# Param: int[3] (Width, Height and KeepAspect? (1 == keep))
	Resize = Particle + 1
	# Emitter position.
	# Param: float[3] (X, Y and Z coords)
	Position = Resize + 1
	# Emitter radius.
	# Param: float
	Radius = Position + 1
	# Camera look-at Y coord.
	# Param: float
	CameraView = Radius + 1
	# Particle rate.
	# Param: int
	Rate = CameraView + 1
	# Particle size.
	# Param: int
	Size = Rate + 1
	# Particle emitting direction.
	# Param: float[3] (X, Y and Z coords)
	Direction = Size + 1
	# On/off fade out affector.
	# Param: bool
	FadeOut = Direction + 1
	# On/off rotation affector.
	# Param: bool
	Rotation = FadeOut + 1
	# On/off gravity affector.
	# Param: bool
	Gravity = Rotation + 1

class Command(object):
	""" Command info for sending to rendering thread.
	"""
	def __init__(self):
		# Type of command
		self.Type = CommandType.Abort
		# Command parameter
		self.Param = None