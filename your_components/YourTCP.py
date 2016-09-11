"""
Generate UR Script set_tcp (Tool Center Point) command 
Vers:20140307
Input:
	tool plane [Generic Data] - Plane that describes tool pose
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import urscript as ur
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

if not plane:
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning,'Failed to collect data for required input: plane')
else:
    tool_pose = ur.pose_by_plane(plane)
    a = ur.set_tcp(tool_pose)
