import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *

class Tile(object):
	def __init__(self, screenX, screenY, screenDimension, driver):
		self.ScreenPos = Vector2Di(screenX, screenY)
		self.Texture = driver.AddTexture(screenDimension, str.Format("TileTexture({0},{1})", screenX, screenY))
		self.TexturePainter = self.Texture.Painter

class FractalGenerator(object): # [0] - tile manager; [1+] - single tile generator
	TileSize = 64
	def __init__(self, device):
		self._device = None
		self._driver = None
		self._screen = Recti(0, 0, 640, 480)
		self._window = Rectd(-1, -1, 1, 1)
		self._tiles = List[Tile]()
		self._threads = Array.CreateInstance(Thread, 1 + 8)
		self._maxIterations = 10
		self._device = device
		self._driver = device.VideoDriver
		self._screen = self._driver.ViewPort
		self.regenerateTiles()

	def Drop(self):
		self.abortThreads()
		self.clearTiles()

	def Generate2(self, window, maxIterations):
		if window.Width < 0.000004 or window.Width > 20 or window.Height < 0.000004 or window.Height > 20:
			return 
		if maxIterations < 0:
			maxIterations = 0
		self.abortThreads()
		self._window = window
		self._maxIterations = maxIterations
		for t in self._tiles:
			t.MaxIterations = maxIterations
			t.TextureIsReady = False
			t.WindowRect = Rectd(self.GetWindowCoord(t.ScreenPos.X, t.ScreenPos.Y), self.GetWindowCoord(t.ScreenPos.X + 64, t.ScreenPos.Y + 64))
		self._threads[0] = Thread(ThreadStart(self.threadTileManager_main))
		self._threads[0].Start()

	def Generate(self, arg):
		if isinstance(arg, Rectd):
			self.Generate2(arg, self._maxIterations)
		else:
			self.Generate2(self._window, arg)

	#def Generate(self, maxIterations):
	#	self.Generate(self._window, maxIterations)

	def GetZoomFactor(self):
		return Vector2Dd(self._screen.Width / self._window.Width, self._screen.Height / self._window.Height)

	def GetMaxIterations(self):
		return self._maxIterations

	def GetWindow(self):
		return self._window

	def GetWindowCoord(self, screenX, screenY):
		dx = self._screen.Width / self._window.Width
		x = self._window.UpperLeftCorner.X + screenX / dx
		dy = self._screen.Height / self._window.Height
		y = self._window.UpperLeftCorner.Y + screenY / dy
		return Vector2Dd(x, y)

	def DrawAll(self, screenOffset):
		zero = Vector2Di(0)
		n = 0
		for tile in self._tiles:
			if tile.TextureIsReady:
				self._driver.Draw2DImage(tile.Texture, tile.ScreenPos + (screenOffset == zero))
				n += 1
		return n / self._tiles.Count

	def abortThreads(self):
		for i in xrange(0,self._threads.Length,1):
			if self._threads[i] != None:
				self._threads[i].Abort()
				self._threads[i] = None

	def regenerateTiles(self):
		self.clearTiles()
		o = self._driver.GetTextureCreationFlag(TextureCreationFlag.CreateMipMaps)
		self._driver.SetTextureCreationFlag(TextureCreationFlag.CreateMipMaps, False)
		y = 0
		x = 0
		d = Dimension2Di(64)
		while y < self._screen.Height:
			self._tiles.Add(Tile(x, y, d, self._driver))
			x += 64
			if x >= self._screen.Width:
				x = 0
				y += 64
		self._driver.SetTextureCreationFlag(TextureCreationFlag.CreateMipMaps, o)
		# sort tiles: closest to center of the screen goes first
		swh = self._screen.Width / 2
		shh = self._screen.Height / 2
		b = True
		while b:
			b = False
			for i in xrange(0,self._tiles.Count - 1,1):
				tx1 = self._tiles[i].ScreenPos.X + 64 / 2
				ty1 = self._tiles[i].ScreenPos.Y + 64 / 2
				td1 = Math.Abs(swh - tx1) + Math.Abs(shh - ty1)
				tx2 = self._tiles[i + 1].ScreenPos.X + 64 / 2
				ty2 = self._tiles[i + 1].ScreenPos.Y + 64 / 2
				td2 = Math.Abs(swh - tx2) + Math.Abs(shh - ty2)
				if td1 > td2:
					t = self._tiles[i]
					self._tiles[i] = self._tiles[i + 1]
					self._tiles[i + 1] = t
					b = True

	def clearTiles(self):
		for t in self._tiles:
			self._driver.RemoveTexture(t.Texture)
		self._tiles.Clear()

	def threadTileManager_main(self):
		for tile in self._tiles:
			while True:
				j = -1
				for i in xrange(1,self._threads.Length,1):
					if self._threads[i] == None or self._threads[i].ThreadState == ThreadState.Stopped:
						j = i
						break
				if j != -1:
					break
				Thread.Sleep(1)
			self._threads[j] = Thread(ParameterizedThreadStart(self.threadTileGenerator_main))
			self._threads[j].Start(tile)

	def threadTileGenerator_main(self, tileObject):
		tile = tileObject
		if not tile.TexturePainter.Lock(TextureLockMode.WriteOnly):
			return 
		try:
			# generate Mandelbrot set
			w = tile.TexturePainter.MipMapLevelWidth
			rx = tile.WindowRect.UpperLeftCorner.X
			rxu = tile.WindowRect.Width / w
			h = tile.TexturePainter.MipMapLevelHeight
			ry = tile.WindowRect.UpperLeftCorner.Y
			ryu = tile.WindowRect.Height / h
			c = Color()
			for y in xrange(0,h,1):
				for x in xrange(0,w,1):
					ax0 = rx + x * rxu
					ay0 = ry + y * ryu
					ax1 = ax0
					ay1 = ay0
					ac = ax0 * ax0 + ay0 * ay0
					i = 0
					while i < tile.MaxIterations and ac < 16:
						ax2 = ax1 * ax1 - ay1 * ay1 + ax0
						ay1 = 2 * ax1 * ay1 + ay0
						ax1 = ax2
						ac = ax1 * ax1 + ay1 * ay1
						i += 1
					if i < tile.MaxIterations:
						c.Set((i * 0x0102f4))
					else:
						c.Set(0)
					tile.TexturePainter.SetPixel(x, y, c)
		finally:
			tile.TexturePainter.Unlock()
			tile.TextureIsReady = True

