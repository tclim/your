"""
Generate a list of UR script commands for a local motion (linear in toolspace) 
Vers:20140307
Input:
	target plane [Generic Data] - Target plane to move towards
	acceleration (in, optional) [Generic Data] - Optional. Tool accel in m/s^2
	velocity (in, optional) [Generic Data] - Optional. Tool speed in m/s
	time (in, optional) [Generic Data] - Optional. Time in s (it overrides accel and vel)
	radius (in, optional) [Generic Data] - Optional. Blend radius in m
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import scriptcontext as sc
import urscript as ur
import Rhino.Geometry as rg
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

if not target:
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning,'Failed to collect data for required input: plane')
else:
    target_plane = rg.Plane(target)
    accel = float(accel) if accel else 1.2
    vel = float(vel) if vel else 0.3
    time = float(time) if time else 0.0
    blend = float(radius) if radius else 0.0
    target_pose = ur.pose_by_plane(target_plane)
    
    a = ur.move_local(target_pose, accel, vel, time, blend)