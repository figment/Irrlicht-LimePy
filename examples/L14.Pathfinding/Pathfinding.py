import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
from System.Diagnostics import *

class CellType(object):
	Passable = 0
	Impassable = Passable + 1
	Start = Impassable + 1
	Finish = Start + 1
	Path = Finish + 1

class Pathfinding(object):

	def get_Width(self):
		return len(self._cells)

	Width = property(fget=get_Width)

	def get_Height(self):
		return len(self._cells[0])

	Height = property(fget=get_Height)

	def get_CellSize(self):
		return self._cellsize

	def set_CellSize(self, value):
		self._cellsize = value

	CellSize = property(fget=get_CellSize, fset=set_CellSize)

	def get_StartX(self):
		return self._startx

	def set_StartX(self, value):
		self._startx = value

	StartX = property(fget=get_StartX, fset=set_StartX)

	def get_StartY(self):
		return self._starty

	def set_StartY(self, value):
		self._starty = value

	StartY = property(fget=get_StartY, fset=set_StartY)

	def get_FinishX(self):
		return self._finishx

	def set_FinishX(self, value):
		self._finishx = value

	FinishX = property(fget=get_FinishX, fset=set_FinishX)

	def get_FinishY(self):
		return self._finishy

	def set_FinishY(self, value):
		self._finishy = value

	FinishY = property(fget=get_FinishY, fset=set_FinishY)

	def get_PathLength(self):
		return self._pathlength

	def set_PathLength(self, value):
		self._pathlength = value

	PathLength = property(fget=get_PathLength, fset=set_PathLength)

	def get_PathCalcTimeMs(self):
		return self._stopwatch.ElapsedMilliseconds

	PathCalcTimeMs = property(fget=get_PathCalcTimeMs)

	def __init__(self, width, height, cellSize, offsetX, offsetY):
		self._cells = None
		self._batchDestPos = None
		self._batchSrcRect = None
		self._stopwatch = Stopwatch()
		self._cellsize = int(0)
		self._startx = int(0)
		self._starty = int(0)
		self._finishx = int(0)
		self._finishy = int(0)
		self._pathlength = int(0)
		#self._cells = Array.CreateInstance(int, width, height)
		self._cells = [[0 for x in xrange(0,height,1)] for x in xrange(0,width,1)]
		self.CellSize = cellSize
		self._batchDestPos = List[Vector2Di]()
		self._batchSrcRect = List[Recti]()
		for i,row in enumerate(self._cells):
			for j in xrange(0,len(row),1):
				row[j] = -1
				self._batchDestPos.Add(Vector2Di(i * cellSize + offsetX, j * cellSize + offsetY))
				self._batchSrcRect.Add(Recti(0, 0, cellSize, cellSize))

	def Draw(self, driver, cellTexture):
		th = cellTexture.Size.Height # [0] passable == -1 # [1] impassable == -2 # [2] start == -3 # [3] finish == -4
		srcRect = Array[Recti]((Recti(th * 0, 0, th * 1, th), Recti(th * 1, 0, th * 2, th), Recti(th * 2, 0, th * 3, th), Recti(th * 3, 0, th * 4, th), Recti(th * 4, 0, th * 5, th))) # [4] path == -5
		for i,row in enumerate(self._cells):
			for j,cell in enumerate(row):
				k = -1 - cell
				if k >= 0 and k < srcRect.Length:
					self._batchSrcRect[i * len(row) + j] = srcRect[k]
		driver.Draw2DImageBatch(cellTexture, self._batchDestPos, self._batchSrcRect)

	def SetCell(self, x, y, c):
		if x < 0 or x >= len(self._cells) or y < 0 or y >= len(self._cells[0]):
			return 
		if c == CellType.Passable or c == CellType.Impassable:
			if (self.StartX == x and self.StartY == y) or (self.FinishX == x and self.FinishY == y):
				return 
		elif c == CellType.Start:
			if self._cells[x][y] == -2 or self._cells[x][y] == -4: # don't change if its impassable or "finish"
				return 
			self._cells[self.StartX][self.StartY] = -1
			self.StartX = x
			self.StartY = y
		elif c == CellType.Finish:
			if self._cells[x][y] == -2 or self._cells[x][y] == -3: # don't change if its impassable or "start"
				return 
			self._cells[self.FinishX][self.FinishY] = -1
			self.FinishX = x
			self.FinishY = y
		self._cells[x][y] = -c - 1

	def FindPath(self):
		self._stopwatch.Reset()
		self._stopwatch.Start()
		w = len(self._cells)
		h = len(self._cells[0])
		# clean up prev path
		for i,row in enumerate(self._cells):
			for j,cell in enumerate(row):
				if cell == -5:
					row[j] = -1
		# build path data
		c = [[y for y in row] for row in self._cells]
		c[self.FinishX][self.FinishY] = 0
		f = False # left # right # up # down
		b = True
		while b and not f:
			b = False
			prev = None
			for i,row in enumerate(c):
				prev = c[i - 1] if i > 0 else None
				next = c[i + 1] if i < w - 1 else None
				for j,cell in enumerate(row):
					if cell < 0:
						continue
					if prev != None:
						v = prev[j]
						if v == -1 or v == -3:
							prev[j] = cell + 1
							b = True
							if v == -3:
								f = True
					if next != None:
						v = next[j]
						if v == -1 or v == -3:
							next[j] = cell + 1
							b = True
							if v == -3:
								f = True
					if j > 0:
						v = row[j - 1]
						if v == -1 or v == -3:
							row[j - 1] = cell + 1
							b = True
							if v == -3:
								f = True
					if j < h - 1:
						v = row[j + 1]
						if v == -1 or v == -3:
							row[j + 1] = cell + 1
							b = True
							if v == -3:
								f = True

		if c[self.StartX][self.StartY] == -3:
			# path not found
			self.PathLength = -1
			self._stopwatch.Stop()
			return 
		self.PathLength = c[self.StartX][self.StartY]
		# find the path
		x = self.StartX
		y = self.StartY
		while True:
			v = c[x][y]
			# the idea of next loop is to execute "left+right" and "up+down" code alternatively;
			# this gives more natural diagonal path
			t = False
			for j in xrange(0,2,1):
				if ((x + y + j) & 1) == 1:
					if x > 0 and c[x - 1][y] == v - 1: # left
						x -= 1
						t = True
						break
					if x < w - 1 and c[x + 1][y] == v - 1: # right
						x += 1
						t = True
						break
				else:
					if y > 0 and c[x][y - 1] == v - 1: # up
						y -= 1
						t = True
						break
					if y < h - 1 and c[x][y + 1] == v - 1: # down
						y += 1
						t = True
						break
			if t:
				self._cells[x][y] = -5
			else:
				break
		self._cells[self.FinishX][self.FinishY] = -4 # restore "finish", since it got overwritten with "path"
		self._stopwatch.Stop()