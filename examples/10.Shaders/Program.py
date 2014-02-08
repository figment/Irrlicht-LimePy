import clr
clr.AddReferenceByPartialName("System.Core")
clr.AddReferenceByPartialName("IrrlichtLime")
import System
from System import *
from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from IrrlichtLime import *
from IrrlichtLime.Core import *
from IrrlichtLime.Video import *
from IrrlichtLime.Scene import *
from IrrlichtLime.GUI import *

class Program(object):
	device = None
	useHighLevelShaders = False
	useCgShaders = False
	shaderFirstUpdate = True
	shaderInvWorldId = 0
	shaderWorldViewProjId = 0
	shaderLightPosId = 0
	shaderLightColorId = 0
	shaderTransWorldId = 0
	shaderTextureId = 0
	def __init__(self):
		pass
	def Main(args):
		ok, driverType = Program.AskUserForDriver()
		if not ok:
			return 
		Program.useHighLevelShaders = Program.AskUserForHighLevelShaders(driverType)
		if Program.useHighLevelShaders:
			Program.useCgShaders = Program.AskUserForCgShaders(driverType)
		Program.device = IrrlichtDevice.CreateDevice(driverType, Dimension2Di(640, 480))
		if Program.device == None:
			return 
		driver = Program.device.VideoDriver
		smgr = Program.device.SceneManager
		vsFileName = None # filename for the vertex shader
		psFileName = None # filename for the pixel shader
		if driverType == DriverType.Direct3D8:
			psFileName = "../../media/d3d8.psh"
			vsFileName = "../../media/d3d8.vsh"
		elif driverType == DriverType.Direct3D9:
			if Program.useHighLevelShaders:
				# Cg can also handle this syntax
				psFileName = "../../media/d3d9.hlsl"
				vsFileName = psFileName
			else: # both shaders are in the same file
				psFileName = "../../media/d3d9.psh"
				vsFileName = "../../media/d3d9.vsh"
		elif driverType == DriverType.OpenGL:
			if Program.useHighLevelShaders:
				if Program.useCgShaders:
					# Use HLSL syntax for Cg
					psFileName = "../../media/d3d9.hlsl"
					vsFileName = psFileName
				else: # both shaders are in the same file
					psFileName = "../../media/opengl.frag"
					vsFileName = "../../media/opengl.vert"
			else:
				psFileName = "../../media/opengl.psh"
				vsFileName = "../../media/opengl.vsh"
		if not driver.QueryFeature(VideoDriverFeature.PixelShader_1_1) and not driver.QueryFeature(VideoDriverFeature.ARB_FragmentProgram_1):
			Program.device.Logger.Log("WARNING: Pixel shaders disabled because of missing driver/hardware support.")
		if not driver.QueryFeature(VideoDriverFeature.VertexShader_1_1) and not driver.QueryFeature(VideoDriverFeature.ARB_VertexProgram_1):
			Program.device.Logger.Log("WARNING: Vertex shaders disabled because of missing driver/hardware support.")
		# create materials
		gpu = driver.GPUProgrammingServices
		newMaterialType1 = MaterialType.Solid
		newMaterialType2 = MaterialType.TransparentAddColor
		if gpu != None:
			gpu.OnSetConstants += Program.gpu_OnSetConstants
			# create the shaders depending on if the user wanted high level or low level shaders
			if Program.useHighLevelShaders:
				shadingLanguage = GPUShadingLanguage.Cg if Program.useCgShaders else GPUShadingLanguage.Default
				newMaterialType1 = gpu.AddHighLevelShaderMaterialFromFiles(vsFileName, "vertexMain", VertexShaderType.VS_1_1, psFileName, "pixelMain", PixelShaderType.PS_1_1, MaterialType.Solid, 0, shadingLanguage)
				newMaterialType2 = gpu.AddHighLevelShaderMaterialFromFiles(vsFileName, "vertexMain", VertexShaderType.VS_1_1, psFileName, "pixelMain", PixelShaderType.PS_1_1, MaterialType.TransparentAddColor, 0, shadingLanguage)
			else:
				# create material from low level shaders (asm or arb_asm)
				newMaterialType1 = gpu.AddShaderMaterialFromFiles(vsFileName, psFileName, MaterialType.Solid)
				newMaterialType2 = gpu.AddShaderMaterialFromFiles(vsFileName, psFileName, MaterialType.TransparentAddColor)
		if newMaterialType1 == -1:
			newMaterialType1 = MaterialType.Solid
		if newMaterialType2 == -1:
			newMaterialType2 = MaterialType.TransparentAddColor
		# create test scene node 1, with the new created material type 1
		node = smgr.AddCubeSceneNode(50)
		node.Position = Vector3Df(0)
		node.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
		node.SetMaterialFlag(MaterialFlag.Lighting, False)
		node.SetMaterialType(newMaterialType1)
		smgr.AddTextSceneNode(Program.device.GUIEnvironment.BuiltInFont, "PS & VS & EMT_SOLID", Color(255, 255, 255), node)
		anim = smgr.CreateRotationAnimator(Vector3Df(0, Single(0.3), 0))
		node.AddAnimator(anim)
		anim.Drop()
		# create test scene node 2, with the new created material type 2
		node = smgr.AddCubeSceneNode(50)
		node.Position = Vector3Df(0, -10, 50)
		node.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
		node.SetMaterialFlag(MaterialFlag.Lighting, False)
		node.SetMaterialFlag(MaterialFlag.BlendOperation, True)
		node.SetMaterialType(newMaterialType2)
		smgr.AddTextSceneNode(Program.device.GUIEnvironment.BuiltInFont, "PS & VS & EMT_TRANSPARENT", Color(255, 255, 255), node)
		anim = smgr.CreateRotationAnimator(Vector3Df(0, Single(0.3), 0))
		node.AddAnimator(anim)
		anim.Drop()
		# create test scene node 3, with no shader
		node = smgr.AddCubeSceneNode(50)
		node.Position = Vector3Df(0, 50, 25)
		node.SetMaterialTexture(0, driver.GetTexture("../../media/wall.bmp"))
		node.SetMaterialFlag(MaterialFlag.Lighting, False)
		smgr.AddTextSceneNode(Program.device.GUIEnvironment.BuiltInFont, "NO SHADER", Color(255, 255, 255), node)
		# add a nice skybox
		driver.SetTextureCreationFlag(TextureCreationFlag.CreateMipMaps, False)
		skybox = smgr.AddSkyBoxSceneNode("../../media/irrlicht2_up.jpg", "../../media/irrlicht2_dn.jpg", "../../media/irrlicht2_lf.jpg", "../../media/irrlicht2_rt.jpg", "../../media/irrlicht2_ft.jpg", "../../media/irrlicht2_bk.jpg")
		driver.SetTextureCreationFlag(TextureCreationFlag.CreateMipMaps, True)
		# add a camera and disable the mouse cursor
		cam = smgr.AddCameraSceneNodeFPS()
		cam.Position = Vector3Df(-100, 50, 100)
		cam.Target = Vector3Df(0)
		Program.device.CursorControl.Visible = False
		# draw everything
		lastFPS = -1
		while Program.device.Run():
			if Program.device.WindowActive:
				driver.BeginScene(True, True, Color(0))
				smgr.DrawAll()
				driver.EndScene()
				fps = driver.FPS
				if lastFPS != fps:
					Program.device.SetWindowCaption(String.Format("Vertex and pixel shader example - Irrlicht Engine [{0}] fps: {1}", driver.Name, fps))
					lastFPS = fps
		Program.device.Drop()

	Main = staticmethod(Main)

	def gpu_OnSetConstants(services, userData):
		driver = services.VideoDriver
		if Program.useHighLevelShaders and Program.shaderFirstUpdate:
			Program.shaderWorldViewProjId = services.GetVertexShaderConstantID("mWorldViewProj")
			Program.shaderTransWorldId = services.GetVertexShaderConstantID("mTransWorld")
			Program.shaderInvWorldId = services.GetVertexShaderConstantID("mInvWorld")
			Program.shaderLightPosId = services.GetVertexShaderConstantID("mLightPos")
			Program.shaderLightColorId = services.GetVertexShaderConstantID("mLightColor")
			# textures id are important only for OpenGL interface
			if driver.DriverType == DriverType.OpenGL:
				Program.shaderTextureId = services.GetVertexShaderConstantID("myTexture")
			Program.shaderFirstUpdate = False
		# set inverted world matrix
		# if we are using highlevel shaders (the user can select this when
		# starting the program), we must set the constants by name
		invWorld = driver.GetTransform(TransformationState.World)
		invWorld.MakeInverse()
		if Program.useHighLevelShaders:
			services.SetVertexShaderConstant(Program.shaderInvWorldId, invWorld.ToArray())
		else:
			services.SetVertexShaderConstant(0, invWorld.ToArray())
		# set clip matrix
		worldViewProj = driver.GetTransform(TransformationState.Projection)
		worldViewProj *= driver.GetTransform(TransformationState.View)
		worldViewProj *= driver.GetTransform(TransformationState.World)
		if Program.useHighLevelShaders:
			services.SetVertexShaderConstant(Program.shaderWorldViewProjId, worldViewProj.ToArray())
		else:
			services.SetVertexShaderConstant(4, worldViewProj.ToArray())
		# set camera position
		pos = Program.device.SceneManager.ActiveCamera.AbsolutePosition
		if Program.useHighLevelShaders:
			services.SetVertexShaderConstant(Program.shaderLightPosId, pos.ToArray())
		else:
			services.SetVertexShaderConstant(8, pos.ToArray())
		# set light color
		col = Colorf(0, 1, 1, 0)
		if Program.useHighLevelShaders:
			services.SetVertexShaderConstant(Program.shaderLightColorId, col.ToArray())
		else:
			services.SetVertexShaderConstant(9, col.ToArray())
		# set transposed world matrix
		transpWorld = driver.GetTransform(TransformationState.World).Transposed
		if Program.useHighLevelShaders:
			services.SetVertexShaderConstant(Program.shaderTransWorldId, transpWorld.ToArray())
			services.SetPixelShaderConstant(Program.shaderTextureId, Array[int]((0,)))
		else:
			services.SetVertexShaderConstant(10, transpWorld.ToArray())

	gpu_OnSetConstants = staticmethod(gpu_OnSetConstants)

	def AskUserForCgShaders(driverType):
		if driverType != DriverType.Direct3D9 and driverType != DriverType.OpenGL:
			return False
		Console.WriteLine("\nPlease press 'y' if you want to use Cg shaders.")
		return Console.ReadKey().Key == ConsoleKey.Y

	AskUserForCgShaders = staticmethod(AskUserForCgShaders)

	def AskUserForHighLevelShaders(driverType):
		if driverType != DriverType.Direct3D9 and driverType != DriverType.OpenGL:
			return False
		Console.WriteLine("\nPlease press 'y' if you want to use high level shaders.")
		return Console.ReadKey().Key == ConsoleKey.Y

	AskUserForHighLevelShaders = staticmethod(AskUserForHighLevelShaders)

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