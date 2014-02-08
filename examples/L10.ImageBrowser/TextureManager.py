import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Threading import *
from IrrlichtLime import *
from IrrlichtLime.Scene import *
from IrrlichtLime.Video import *
from IrrlichtLime.Core import *
import pyevent

class ThreadCommandType(object):
	Stop = 0 # Params = null 
	LoadTexture = Stop + 1 # Params = [SceneNode] the node witch will get SetMaterialTexture() call, [string] path to the texture, [Dimension2Di] resize loaded texture to this size 
	UnloadTexture = LoadTexture + 1 # Params = [string] name of the texture

class ThreadCommand(object):
	def __init__(self):
		Type = ThreadCommandType.Stop
		Params = None

class TextureManager(object):
	
	def __init__(self, irrDevice):
		self._irrDevice = None
		self._noPreviewTexture = None
		self._threads = None
		self._threadCommands = None
		self._loadedTextures = None
		
		# TextureLoadedDelegate(SceneNode node, Texture texture, Dimension2Di sourceDimension)
		self.OnTextureLoaded, self._FireTextureLoaded= pyevent.make_event()
		
		self._irrDevice = irrDevice
		self._threadCommands = Queue[ThreadCommand]()
		self._loadedTextures = List[str]()
		# generate "no preview" texture
		h = 256
		i = irrDevice.DriverNoCheck.CreateImage(ColorFormat.A8R8G8B8, Dimension2Di(h))
		i.Fill(Color(0x112233))
		for a in xrange(0,h,1):
			i.SetPixel(a, 0, Color(0x557799))
			i.SetPixel(a, h - 1, Color(0x557799))
			i.SetPixel(0, a, Color(0x557799))
			i.SetPixel(h - 1, a, Color(0x557799))
			if a > 16 and a < h - 16:
				i.SetPixel(a, a, Color(0x557799))
				i.SetPixel(h - a - 1, a, Color(0x557799))
		irrDevice.Lock()
		self._noPreviewTexture = irrDevice.Driver.AddTexture("NoPreviewTexture", i)
		irrDevice.Unlock()
		i.Drop()

	def Start(self, threadCount):
		self._threads = Array.CreateInstance(Thread, threadCount)
		for i in xrange(0,threadCount,1):
			self._threads[i] = Thread(ThreadStart(self.thread_Main))
			self._threads[i].Name = self.GetType().Name + "/Thread#" + str(i + 1)
			self._threads[i].Start()

	def Stop(self):
		if self._threads == None:
			return 
		self.addThreadCommand(ThreadCommandType.Stop, False)
		for t in self._threads:
			t.Join()
		System.Diagnostics.Debug.Assert(self._threadCommands.Count == 1)
		self._threadCommands.Dequeue()

	def LoadTexture(self, node, path, size, topPriority=False):
		node.Grab()
		self.addThreadCommand(ThreadCommandType.LoadTexture, topPriority, node, path, size)

	def UnloadTexture(self, path):
		self.addThreadCommand(ThreadCommandType.UnloadTexture, False, path)

	def EnqueueUnloadingOfAllLoadedTextures(self):
		Monitor.Enter(self._loadedTextures)
		try:
			for t in self._loadedTextures:
				self.addThreadCommand(ThreadCommandType.UnloadTexture, False, t)
			self._loadedTextures.Clear()
		finally:
			Monitor.Exit(self._loadedTextures)

	def GetCommandQueueLength(self):
		Monitor.Enter(self._threadCommands)
		try:
			return self._threadCommands.Count
		finally:
			Monitor.Exit(self._threadCommands)

	def addThreadCommand(self, command, topPriority, *args):
		cmd = ThreadCommand()
		cmd.Type = command
		cmd.Params = args
		Monitor.Enter(self._threadCommands)
		try:
			if cmd.Type == ThreadCommandType.Stop:
				for c in self._threadCommands:
					if c.Type == ThreadCommandType.LoadTexture:
						(c.Params[0]).Drop()
				self._threadCommands.Clear()
			if topPriority and self._threadCommands.Count > 0:
				a = self._threadCommands.ToArray()
				self._threadCommands.Clear()
				self._threadCommands.Enqueue(cmd)
				for i in xrange(0,a.Length,1):
					self._threadCommands.Enqueue(a[i])
			else:
				self._threadCommands.Enqueue(cmd)
		finally:
			Monitor.Exit(self._threadCommands)

	def thread_Main(self):
		self._irrDevice.Logger.Log(Thread.CurrentThread.Name, "Started", LogLevel.Information)
		while True:
			cmd = self.thread_GetNextCommand()
			if cmd == None:
				Thread.Sleep(1)
				continue
			if cmd.Type == ThreadCommandType.Stop:
				self._irrDevice.Logger.Log(Thread.CurrentThread.Name, "Finished", LogLevel.Information)
				return 
			elif cmd.Type == ThreadCommandType.LoadTexture:
				self._irrDevice.Logger.Log(Thread.CurrentThread.Name, "Loading " + str(cmd.Params[1]) + "|" + str(cmd.Params[2]), LogLevel.Information)
				self.thread_LoadTexture(cmd.Params[0], cmd.Params[1], cmd.Params[2])
			elif cmd.Type == ThreadCommandType.UnloadTexture:
				self._irrDevice.Logger.Log(Thread.CurrentThread.Name, "Unloading " + str(cmd.Params[0]), LogLevel.Information)
				self.thread_UnloadTexture(cmd.Params[0])

	def thread_GetNextCommand(self):
		cmd = None
		Monitor.Enter(self._threadCommands)
		try:
			if self._threadCommands.Count > 0:
				# We do first Peek and only then Dequeue, because we do not want Stop command to be processed only by one thread (so other will not get this command)
				cmd = self._threadCommands.Peek()
				if cmd.Type != ThreadCommandType.Stop:
					self._threadCommands.Dequeue()
		finally:
			Monitor.Exit(self._threadCommands)
		return cmd

	def thread_LoadTexture(self, node, path, size):
		i = self._irrDevice.DriverNoCheck.CreateImage(path)
		if i != None:
			j = self._irrDevice.DriverNoCheck.CreateImage(ColorFormat.A8R8G8B8, size)
			i.CopyToScaling(j)
			self._irrDevice.Lock()
			t = self._irrDevice.Driver.AddTexture(path + "|" + size.ToString(), j)
			self._irrDevice.Unlock()
			si = i.Dimension
			i.Drop()
			j.Drop()
			Monitor.Enter(self._loadedTextures)
			try:
				self._loadedTextures.Add(t.Name.Path)
			finally:
				Monitor.Exit(self._loadedTextures)
		else:
			t = self._noPreviewTexture
			si = self._noPreviewTexture.Size
		self._irrDevice.Lock()
		node.SetMaterialTexture(0, t)
		self._irrDevice.Unlock()
		if self._FireTextureLoaded != None:
			self._FireTextureLoaded(node, t, si)
		node.Drop()

	def thread_UnloadTexture(self, path):
		self._irrDevice.Lock()
		t = self._irrDevice.Driver.FindTexture(path)
		if t != None:
			self._irrDevice.Driver.RemoveTexture(t)
		self._irrDevice.Unlock()

