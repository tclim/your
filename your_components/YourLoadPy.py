"""
Loads python modules for use in Grasshopper 
Vers:20140307
Input:
	folder path [Generic Data] - Path of folder python modules are located in
	unload [Generic Data] - Unload modules in folder from system True/False
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import sys
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

if not folder:
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning,'Failed to collect data from required input - folder')
if not folder in sys.path:
    sys.path.append(folder)

def unload_modules():
    """unloads modules in folder"""
    import os
    import glob
    # filter only .py files from the directory folder
    files = os.listdir(folder) 
    filtered_files = filter(lambda x: x.endswith(".py"), files) # filter(function,sequence) 
    # remove .py from filenames
    filenames = [file.split(".")[0] for file in filtered_files]
    # pop modules 
    for fn in filenames: 
        if sys.modules.has_key(fn):
            sys.modules.pop(fn)

if unload:
    unload_modules()

