"""
Generate UR Script movej motion (linear in joint-space) command 
Vers:20140307
Input:
	target [Generic Data] - Target. A list of joint angles (radians). Alternatively a plane can be used
	base (in, optional) [Generic Data] - Optional. A reference plane used as the basis for calculating  pose if a target plane was given instead of angles
	acceleration (in, optional) [Generic Data] - Optional. Joint acceleration of leading axis in rad/s^2
	velocity (in, optional) [Generic Data] - Optional. Joint speed of leading axis in rad/s
	time (in, optional) [Generic Data] - Optional. Time in s (it overrides accel and vel)
	radius (in, optional) [Generic Data] - Optional. Blend radius in m
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import urscript as ur
import Rhino.Geometry as rg
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

error_inputs = []
if not joints and (target and base):
    break
else:
    error_inputs.append('joints')
    if not target:
        error_inputs.append('target')
    if not base:
        error_inputs.append('base')

if not error_inputs:
    accel = float(accel) if accel else 3.0
    vel = float(vel) if vel else 0.75
    time = float(time) if time else 0.0
    blend = float(radius) if radius else 0.0
    if joints:
        a= ur.movej([float(j) for j in target],accel, vel, time, blend)
    else:
        target_plane = rg.Plane(target)
        matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,base)
        target_plane.Transform(matrix)
        target_pose = ur.pose_by_plane(target_plane)
        a = ur.movej(target_pose, accel, vel,time, blend)
else:
    error_message = 'Failed to collect data for input(s): {0}'.format(','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message) 