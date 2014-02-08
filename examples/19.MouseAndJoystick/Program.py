import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Threading import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class MouseStateInfo(object):
	def __init__(self):
		self.Position = Vector2Di()
		self.IsLeftButtonDown = False
		pass

class Program(object):
	# Initialize device.
	# Add event handling.
	# Save important pointers.
	# Initialize joysticks and print info about them.
	# Create an arrow mesh and move it around either with the joystick axis/hat,
	# or make it follow the mouse pointer (when no joystick movement).
	# As in example #4, we'll use framerate independent movement.
	# Run main cycle.
	# Work out a frame delta time. # in seconds # range is -1.0 for full left to +1.0 for full right # range is -1.0 for full down to +1.0 for full up
	# We receive the full analog range of the axes, and so have to implement our own dead zone.
	# This is an empirical value, since some joysticks have more jitter or creep around the center
	# point than others. We'll use 5% of the range as the dead zone, but generally you would want
	# to give the user the option to change this. # "0" for X axis # "1" for Y axis
	# POV will contain 65535 if POV hat info no0t supported, so we can check its range.
	# If we have any movement, apply it.
	# If the arrow node isn't being moved with the joystick, then have it follow the mouse cursor.
	# Create a ray through the mouse cursor.
	# And intersect the ray with a plane around the node facing towards the camera.
	# We now have a mouse position in 3d space; move towards it. # jump to the final position # move towards it
	# Turn lighting on and off depending on whether the left mouse button is down.
	# Draw all.
	# Drop the device.
	# We'll create a class to record info on the mouse state.
	mouseState = MouseStateInfo()
	joystickState = None
	sync = Object()
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if device == None:
			return 
		Program.sync = Object()
		device.OnEvent += Program.device_OnEvent
		driver = device.VideoDriver
		smgr = device.SceneManager
		logger = device.Logger
		joystickList = device.ActivateJoysticks()
		if joystickList != None:
			logger.Log("Joystick support is enabled and " + joystickList.Count.ToString() + " joystick(s) are present.")
			for j in joystickList:
				logger.Log("Joystick " + j.Joystick.ToString() + ":")
				logger.Log("\tName: \"" + j.Name + "\"")
				logger.Log("\tAxisCount: " + j.AxisCount.ToString())
				logger.Log("\tButtonCount: " + j.ButtonCount.ToString())
				logger.Log("\tPovHat: " + j.PovHat.ToString())
		else:
			logger.Log("Joystick support is not enabled.")
		device.SetWindowCaption("Mouse and joystick - Irrlicht Lime - " + joystickList.Count.ToString() + " joystick(s)")
		node = smgr.AddMeshSceneNode(smgr.AddArrowMesh("Arrow", Color(255, 0, 0), Color(0, 255, 0), 16, 16, Single(2), Single(1.3), Single(0.1), Single(0.6)))
		node.SetMaterialFlag(MaterialFlag.Lighting, False)
		camera = smgr.AddCameraSceneNode()
		camera.Position = Vector3Df(0, 0, -10)
		then = device.Timer.Time
		MovementSpeed = Single(5)
		while device.Run():
			Monitor.Enter(Program.sync)
			now = device.Timer.Time
			frameDeltaTime = (now - then) / Single(1000)
			then = now
			movedWithJoystick = False
			nodePosition = node.Position
			if joystickList.Count > 0:
				moveHorizontal = Single(0)
				moveVertical = Single(0)
				DeadZone = Single(0.05)
				moveHorizontal = Program.joystickState.Axis[0] / Single(32767)
				if Math.Abs(moveHorizontal) < DeadZone:
					moveHorizontal = Single(0)
				moveVertical = Program.joystickState.Axis[1] / -Single(32767)
				if Math.Abs(moveVertical) < DeadZone:
					moveVertical = Single(0)
				povDegrees = (Program.joystickState.POV / 100)
				if povDegrees < 360:
					if povDegrees > 0 and povDegrees < 180:
						moveHorizontal = +Single(1)
					elif povDegrees > 180:
						moveHorizontal = -Single(1)
					if povDegrees > 90 and povDegrees < 270:
						moveVertical = -Single(1)
					elif povDegrees > 270 or povDegrees < 90:
						moveVertical = +Single(1)
				if Math.Abs(moveHorizontal) > Single(0.0001) or Math.Abs(moveVertical) > Single(0.0001):
					m = frameDeltaTime * MovementSpeed
					nodePosition = Vector3Df(moveHorizontal * m, moveVertical * m, nodePosition.Z)
					movedWithJoystick = True
			if not movedWithJoystick:
				ray = smgr.SceneCollisionManager.GetRayFromScreenCoordinates(Program.mouseState.Position, camera)
				plane = Plane3Df(nodePosition, Vector3Df(0, 0, -1))
				_tmp147_39, mousePosition = plane.GetIntersectionWithLine(ray.Start, ray.Vector)
				if _tmp147_39:
					toMousePosition = mousePosition - nodePosition
					availableMovement = frameDeltaTime * MovementSpeed
					if toMousePosition.Length <= availableMovement:
						nodePosition = mousePosition
					else:
						nodePosition += toMousePosition.Normalize() * availableMovement
			node.Position = nodePosition
			node.SetMaterialFlag(MaterialFlag.Lighting, Program.mouseState.IsLeftButtonDown)
			driver.BeginScene(True, True, Color(113, 113, 133))
			smgr.DrawAll()
			driver.EndScene()
			Monitor.Exit(Program.sync)
		device.Drop()

	Main = staticmethod(Main)
			
	def device_OnEvent(evnt):
		Monitor.Enter(Program.sync)
		# Remember the mouse state.
		if evnt.Type == EventType.Mouse:
			if evnt.Mouse.Type == MouseEventType.LeftDown:
				Program.mouseState.IsLeftButtonDown = True
			elif evnt.Mouse.Type == MouseEventType.LeftUp:
				Program.mouseState.IsLeftButtonDown = False
			elif evnt.Mouse.Type == MouseEventType.Move:
				Program.mouseState.Position = Vector2Di(evnt.Mouse.X, evnt.Mouse.Y)
			else:
				pass
		# We won't use any other mouse events.
		# The state of each connected joystick is sent to us once every run() of the Irrlicht device.
		# Store the state of the first joystick, ignoring other joysticks.
		if evnt.Type == EventType.Joystick and evnt.Joystick.Joystick == 0:
			Program.joystickState = evnt.Joystick
		Monitor.Exit(Program.sync)
		return False

	device_OnEvent = staticmethod(device_OnEvent)

	def AskUserForDriver():
		driverType = DriverType.Null
		Console.Write("Please select the driver you want for this example:\n" + " (a) OpenGL\n (b) Direct3D 9.0c\n (c) Direct3D 8.1\n" + " (d) Burning's Software Renderer\n (e) Software Renderer\n" + " (f) NullDevice\n (otherKey) exit\n\n")
		i = Console.ReadKey()
		if i.Key == ConsoleKey.A:
			driverType = DriverType.OpenGL
		elif i.Key == ConsoleKey.B:
			driverType = DriverType.Direct3D9
		elif i.Key == ConsoleKey.C:
			driverType = DriverType.Direct3D8
		elif i.Key == ConsoleKey.D:
			driverType = DriverType.BurningsVideo
		elif i.Key == ConsoleKey.E:
			driverType = DriverType.Software
		elif i.Key == ConsoleKey.F:
			driverType = DriverType.Null
		else:
			return (False, driverType)
		return (True, driverType)

	AskUserForDriver = staticmethod(AskUserForDriver)

Program.Main(Environment.GetCommandLineArgs()[2:])