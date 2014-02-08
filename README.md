Irrlicht-LimePy
===============

IronPython examples for Irrlicht Lime .NET wrapper around the Irrlicht Engine 

==========================================================================
1. How to Start
==========================================================================
  
  Prerequisites IronPython 2.7.4 or higher must be installed.  A 
    precompiled compatible version is available in the external folder.
  
  Note that there are bugs in IronPython regarding Protected Events 
	that are fixed in the external files provided.  These changes are 
	pending and unreleased at the time of authoring of this file so
	use of the bundled version is required for now.

  To see Lime wrapper in action with python, go to \bin folder and run 
    the example .bat files.
     
  When running your application, make sure that IrrlichtLime.dll and 
    Irrlicht.dll are referenced in the PATH or IRONPYTHONPATH or sys.path
    in IronPython.

==========================================================================
2. Directory Structure Overview
==========================================================================

  \bin         Prcompiled Lime and Irrlicht binaries and batch scripts
               to launch examples.
  \examples    Directory with examples of usage. These examples are ports
               from Lime which were ports from the Irrlicht Engine SDK 
			   examples written on C++.
  \media       Media resources for the examples.
  \external    Precompiled IronPython binaries and libraries which work
               with the examples.
			   
==========================================================================
3. Release Notes
==========================================================================

  Please note that the textures, 3D models and levels are copyright
  by their authors and not covered by the Irrlicht LimePy license or
  the Irrlicht Lime license.
  
  All of the Examples were converted using SharpDevelop Python converter
  and the bundled projects are SharpDevelop 4.x projects.  The inbuilt
  python converter has a number of bugs that were fixed but not included
  in the official release at this time.

==========================================================================
4. Contact
==========================================================================

  The examples are offered as-is for demonstration purposes.
  
  The author does not have time to support the examples at this time.

  The official LimePy homepage:
    https://github.com/figment/Irrlicht-LimePy
  
  Additional information:
	The official Lime homepage:
	http://irrlichtlime.sourceforge.net

