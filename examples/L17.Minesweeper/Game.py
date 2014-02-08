import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *

class Game(object):
	SIZE_OF_MESH = Single(10.0);
	SIZE_OF_CELL = SIZE_OF_MESH * Single(1.15);

	class State(object):
		Playing = 0
		Lost = Playing + 1
		Won = Lost + 1

	class Cell(object):
		def __init__(self):
			self.i = 0
			self.j = 0
			self.number = 0 # -1=bomb, 0..8=number of bombs around
			self.flagged = False
			self.revealed = False
			pass
		def get_IsBomb(self):
			return self.number == -1

		IsBomb = property(fget=get_IsBomb)

	def get_CenterOfTheBoard(self):
		return Vector3Df(self._boardDimWidth * Game.SIZE_OF_CELL / 2, 0, self._boardDimHeight * Game.SIZE_OF_CELL / 2)

	CenterOfTheBoard = property(fget=get_CenterOfTheBoard)

	def get_StateOfTheGame(self):
		return self._state

	StateOfTheGame = property(fget=get_StateOfTheGame)

	def __init__(self, device):
		self._device = device;
		self._root = device.SceneManager.AddEmptySceneNode();
		
		self.loadCellMesh();
		self.loadFlagMesh();
		self.loadBombMesh();
		
		self.NewGame(10, 10);

		
		pass
	def NewGame(self, boardDimWidth, boardDimHeight):
		self._boardDimWidth = boardDimWidth
		self._boardDimHeight = boardDimHeight
		self._state = Game.State.Playing
		self._board = [Game.Cell() for x in xrange(0,self._boardDimHeight*self._boardDimWidth,1)]
		self._root.RemoveChildren()
		# init board
		r = Random()
		for j in xrange(0,self._boardDimHeight,1):
			for i in xrange(0,self._boardDimWidth,1):
				c = Game.Cell()
				c.i = i
				c.j = j
				c.number = -1 if (r.Next() % 6) == 0 else 0
				c.flagged = False
				c.revealed = False
				self._board[i + j * self._boardDimWidth] = c
				n = self._device.SceneManager.AddMeshSceneNode(self._meshCell, self._root, 0x10000 + i + j * self._boardDimWidth)
				n.Position = Vector3Df(i * Game.SIZE_OF_CELL, 0, j * Game.SIZE_OF_CELL)
				# n must have at least 2 children, where #0 is a flag node and #1 is a bomb node
				# (that's why we add shadow volume nodes at the very end)
				f = self._device.SceneManager.AddMeshSceneNode(self._meshFlag, n, 0)
				f.Position = Vector3Df((n.BoundingBox.MaxEdge.X - self._meshFlag.BoundingBox.MaxEdge.X) / 2, n.BoundingBox.MaxEdge.Y, (n.BoundingBox.MaxEdge.Z - self._meshFlag.BoundingBox.MaxEdge.Z) / 2 + Game.SIZE_OF_CELL / 6)
				f.Visible = False
				b = self._device.SceneManager.AddMeshSceneNode(self._meshBomb, n, 0)
				b.Position = Vector3Df(0, n.BoundingBox.MaxEdge.Y, 0)
				b.Visible = False
				n.AddShadowVolumeSceneNode(None, 0)
				f.AddShadowVolumeSceneNode(None, 0)
				b.AddShadowVolumeSceneNode(None, 0)
		# calc board numbers
		for j in xrange(0,self._boardDimHeight,1):
			for i in xrange(0,self._boardDimWidth,1):
				if not self._board[i + j * self._boardDimWidth].IsBomb:
					continue
				if i - 1 >= 0 and not self._board[i - 1 + j * self._boardDimWidth].IsBomb: # left
					self._board[i - 1 + j * self._boardDimWidth].number += 1
				if i + 1 < self._boardDimWidth and not self._board[i + 1 + j * self._boardDimWidth].IsBomb: # right
					self._board[i + 1 + j * self._boardDimWidth].number += 1
				if j - 1 >= 0 and not self._board[i + (j - 1) * self._boardDimWidth].IsBomb: # top
					self._board[i + (j - 1) * self._boardDimWidth].number += 1
				if j + 1 < self._boardDimHeight and not self._board[i + (j + 1) * self._boardDimWidth].IsBomb: # bottom
					self._board[i + (j + 1) * self._boardDimWidth].number += 1
				if j - 1 >= 0 and i - 1 >= 0 and not self._board[i - 1 + (j - 1) * self._boardDimWidth].IsBomb: # top left
					self._board[i - 1 + (j - 1) * self._boardDimWidth].number += 1
				if j - 1 >= 0 and i + 1 < self._boardDimWidth and not self._board[i + 1 + (j - 1) * self._boardDimWidth].IsBomb: # top right
					self._board[i + 1 + (j - 1) * self._boardDimWidth].number += 1
				if j + 1 < self._boardDimHeight and i + 1 < self._boardDimWidth and not self._board[i + 1 + (j + 1) * self._boardDimWidth].IsBomb: # bottom right
					self._board[i + 1 + (j + 1) * self._boardDimWidth].number += 1
				if j + 1 < self._boardDimHeight and i - 1 >= 0 and not self._board[i - 1 + (j + 1) * self._boardDimWidth].IsBomb: # bottom left
					self._board[i - 1 + (j + 1) * self._boardDimWidth].number += 1

	def MouseClick(self, x, y, isRight):
		if self._state != Game.State.Playing:
			return 
		m = Vector2Di(x, y)
		l = self._device.SceneManager.SceneCollisionManager.GetRayFromScreenCoordinates(m)
		n = self._device.SceneManager.SceneCollisionManager.GetSceneNodeFromRayBB(l, 0x10000, self._root)
		if n != None and n.ID >= 0x10000:
			i = n.ID - 0x10000
			if isRight:
				self.flagCell(self._board[i])
			else:
				self.revealCell(self._board[i])

	def checkVictory(self):
		f = True
		for i in xrange(0,len(self._board),1):
			c = self._board[i]
			if c.IsBomb and not c.flagged: # each bomb should be flagged
				f = False
				break
			if not c.IsBomb and not c.revealed: # each number shoud be revealed
				f = False
				break
		if f:
			self._state = Game.State.Won
			self._device.Logger.Log("game won")

	def flagCell(self, cell):
		if cell.revealed:
			return 
		cell.flagged = not cell.flagged
		self._root.Children[cell.i + cell.j * self._boardDimWidth].Children[0].Visible = cell.flagged
		self._device.Logger.Log("flagCell: (" + str(cell.i) + "," + str(cell.j) + ") now " + ("flagged" if cell.flagged else "unflagged"))
		self.checkVictory()

	def revealCell(self, cell):
		if cell.revealed or cell.flagged:
			return 
		cell.revealed = True
		self._device.Logger.Log("revealCell: (" + str(cell.i) + "," + str(cell.j) + ") now revealed, the number is " + str(cell.number))
		# if its a bomb - end the game
		if cell.IsBomb:
			self._root.Children[cell.i + cell.j * self._boardDimWidth].Children[1].Visible = True
			self._state = Game.State.Lost
			self._device.Logger.Log("game lost")
			for i in xrange(0,len(self._board),1):
				self._board[i].revealed = True
			return 
		# this is normal cell
		self._root.Children[cell.i + cell.j * self._boardDimWidth].SetMaterialTexture(0, self._device.VideoDriver.GetTexture("TEXTURE-num-" + str(cell.number) + ".jpg"))
		if cell.number == 0:
			if cell.i - 1 >= 0: # left
				self.revealCell(self._board[cell.i - 1 + cell.j * self._boardDimWidth])
			if cell.i + 1 < self._boardDimWidth: # right
				self.revealCell(self._board[cell.i + 1 + cell.j * self._boardDimWidth])
			if cell.j - 1 >= 0: # top
				self.revealCell(self._board[cell.i + (cell.j - 1) * self._boardDimWidth])
			if cell.j + 1 < self._boardDimHeight: # bottom
				self.revealCell(self._board[cell.i + (cell.j + 1) * self._boardDimWidth])
			if cell.j - 1 >= 0 and cell.i - 1 >= 0: # top left
				self.revealCell(self._board[cell.i - 1 + (cell.j - 1) * self._boardDimWidth])
			if cell.j - 1 >= 0 and cell.i + 1 < self._boardDimWidth: # top right
				self.revealCell(self._board[cell.i + 1 + (cell.j - 1) * self._boardDimWidth])
			if cell.j + 1 < self._boardDimHeight and cell.i + 1 < self._boardDimWidth: # bottom right
				self.revealCell(self._board[cell.i + 1 + (cell.j + 1) * self._boardDimWidth])
			if cell.j + 1 < self._boardDimHeight and cell.i - 1 >= 0: # bottom left
				self.revealCell(self._board[cell.i - 1 + (cell.j + 1) * self._boardDimWidth])
		self.checkVictory()

	def loadCellMesh(self):
		s = self._device.SceneManager.MeshManipulator
		d = self._device.VideoDriver
		self._meshCell = self._device.SceneManager.GetMesh("cell.obj")
		s.FlipSurfaces(self._meshCell) # i don't know why, but somehow this one OBJ exported by Blender has flipped faces when opened by Irrlicht
		self.fitMesh(self._meshCell)
		s.SetVertexColors(self._meshCell, Color.OpaqueWhite)
		s.MakePlanarTextureMapping(self._meshCell, Single(0.1))
		m = Material()
		m.Type = MaterialType.Reflection2Layer
		m.SetTexture(0, d.GetTexture("TEXTURE-unk.jpg"))
		m.SetTexture(1, d.GetTexture("TEXTURE-ref.jpg"))
		self._meshCell.MeshBuffers[0].SetMaterial(m)
		s.Transform(self._meshCell, Matrix(Vector3Df(0), Vector3Df(0, -90, 180)))
		s.RecalculateNormals(self._meshCell)

	def loadFlagMesh(self):
		self._meshFlag = self._device.SceneManager.GetMesh("flag.obj")
		self.fitMesh(self._meshFlag)

	def loadBombMesh(self):
		self._meshBomb = self._device.SceneManager.GetMesh("bomb.obj")
		self.fitMesh(self._meshBomb)

	def fitMesh(self, mesh):
		""" <summary>
		 Prepares mesh to be "cell fit":
		 1) uniform scale the mesh to fit to Game.SIZE_OF_MESH x Game.SIZE_OF_MESH on XZ plane;
		 2) translates mesh to align its bounding box to center of coordiantes (0,0,0);
		 </summary>
		"""
		s = self._device.SceneManager.MeshManipulator
		f = Math.Max(mesh.BoundingBox.Extent.X, mesh.BoundingBox.Extent.Z)
		s.Scale(mesh, Vector3Df(Game.SIZE_OF_MESH / f))
		s.Transform(mesh, Matrix(mesh.BoundingBox.MinEdge * -1))
		s.RecalculateNormals(mesh)