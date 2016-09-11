"""
A python scriptable component
Input:
	path (in, optional) [Generic Data] - Local directory that contains python modules
	unload (in, optional) [Generic Data] - Script input unload.
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script output a.
"""
import sys
if not path in sys.path:
    sys.path.append(path)

def unload_modules():
    """unloads modules in folder"""

    import os
    import glob
    
    # filter only .py files from the directory folder
    files = os.listdir(path) 
    filtered_files = filter(lambda x: x.endswith(".py"), files) # filter(function,sequence) 
    # remove .py from filenames
    filenames = [file.split(".")[0] for file in filtered_files]
    # pop modules 
    for fn in filenames: 
        if sys.modules.has_key(fn):
            sys.modules.pop(fn)

if unload:
    unload_modules()

