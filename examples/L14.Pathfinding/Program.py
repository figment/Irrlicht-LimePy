import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
from IrrlichtLime.GUI import *
from Pathfinding import *

class Program(object):
	device = None
	pathfinding = None
	workMode = True
	def __init__(self):
		pass
	def Main(args):
		Program.device = IrrlichtDevice.CreateDevice(DriverType.Direct3D9, Dimension2Di(1280, 768))
		if Program.device == None:
			return 
		Program.device.SetWindowCaption("Pathfinding - Irrlicht Engine")
		Program.device.OnEvent += Program.device_OnEvent
		driver = Program.device.VideoDriver
		font = Program.device.GUIEnvironment.GetFont("../../media/fontlucida.png")
		fontNormalColor = Color.OpaqueWhite
		fontActionColor = Color.OpaqueYellow
		pathfindingTexture = driver.GetTexture("../../media/pathfinding.png")
		cellSize = pathfindingTexture.Size.Height
		Program.pathfinding = Pathfinding(64, 48, cellSize, 0, 0)
		Program.pathfinding.SetCell(4, 4, CellType.Start)
		Program.pathfinding.SetCell(Program.pathfinding.Width - 5, Program.pathfinding.Height - 5, CellType.Finish)
		while Program.device.Run():
			driver.BeginScene(True, False)
			Program.pathfinding.FindPath()
			Program.pathfinding.Draw(driver, pathfindingTexture)
			# draw info panel
			v = Vector2Di(Program.pathfinding.Width * Program.pathfinding.CellSize + 20, 20)
			font.Draw("FPS: " + str(driver.FPS), v, fontNormalColor)
			v.Y += 32
			font.Draw("Map size: " + str(Program.pathfinding.Width) + " x " + str(Program.pathfinding.Height), v, fontNormalColor)
			v.Y += 16
			font.Draw("Shortest path: " + ("N/A" if Program.pathfinding.PathLength == -1 else Program.pathfinding.PathLength.ToString()), v, fontNormalColor)
			v.Y += 16
			font.Draw("Calculation time: " + str(Program.pathfinding.PathCalcTimeMs) + " ms", v, fontNormalColor)
			v.Y += 32
			font.Draw("[LMB] Set cell impassable" if Program.workMode else "[LMB] Set Start cell", v, fontActionColor)
			v.Y += 16
			font.Draw("[RMB] Set cell passable" if Program.workMode else "[RMB] Set Finish cell", v, fontActionColor)
			v.Y += 16
			font.Draw("[Space] Change mode", v, fontActionColor)
			v.Y += 32
			font.Draw("[F1] Clean up the map", v, fontActionColor)
			v.Y += 16
			font.Draw("[F2] Add random blocks", v, fontActionColor)
			driver.EndScene()
		Program.device.Drop()

	Main = staticmethod(Main)

	def device_OnEvent(evnt):
		if evnt.Type == EventType.Mouse:
			if evnt.Mouse.IsLeftPressed():
				Program.pathfinding.SetCell(evnt.Mouse.X / Program.pathfinding.CellSize, evnt.Mouse.Y / Program.pathfinding.CellSize, CellType.Impassable if Program.workMode else CellType.Start)
				return True
			if evnt.Mouse.IsRightPressed():
				Program.pathfinding.SetCell(evnt.Mouse.X / Program.pathfinding.CellSize, evnt.Mouse.Y / Program.pathfinding.CellSize, CellType.Passable if Program.workMode else CellType.Finish)
				return True
		if evnt.Type == EventType.Key and evnt.Key.PressedDown:
			if evnt.Key.Key == KeyCode.Space:
				Program.workMode = not Program.workMode
				return True
			if evnt.Key.Key == KeyCode.F1:
				for i in xrange(0,Program.pathfinding.Width,1):
					for j in xrange(0,Program.pathfinding.Height,1):
						Program.pathfinding.SetCell(i, j, CellType.Passable)
				return True
			if evnt.Key.Key == KeyCode.F2:
				r = Random()
				for n in xrange(0,30,1): # generate random blocks
					w = r.Next(8) + 2
					h = r.Next(8) + 2
					x = r.Next(Program.pathfinding.Width - w)
					y = r.Next(Program.pathfinding.Height - h)
					c = CellType.Impassable if n < 10 else CellType.Passable
					i = 0
					while i <= w:
						j = 0
						while j <= h:
							Program.pathfinding.SetCell(x + i, y + j, c)
							j += 1
						i += 1
				return True
		return False

	device_OnEvent = staticmethod(device_OnEvent)

Program.Main(Environment.GetCommandLineArgs()[2:])