"""
Generate a list of UR script commands for a motion-digital out compound action.     Robot moves to target pose and sets digital out. An optional retraction motion is added at the end. 
Vers:20140307
Input:
	target plane [Generic Data] - Target plane to move towards
	base [Generic Data] - A reference plane used as the basis for calculating target pose
	id [Generic Data] - ID number of digital output port
	signal [Generic Data] - Digital output value as True/False
	sleep (in, optional) [Generic Data] - Optional. Wait time following digital_out action in s (default 0.5s)
	retraction (in, optional) [Generic Data] - Optional. Distance to retract in m (default 1mm)
	acceleration (in, optional) [Generic Data] - Optional. Tool accel in m/s^2
	velocity (in, optional) [Generic Data] - Optional. Tool speed in m/s
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import scriptcontext as sc
import urscript as ur
import Rhino.Geometry as rg
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

error_inputs = []
if not target: error_inputs.append('target')
if not base: error_inputs.append('base')
if not id: error_inputs.append('id')

if not error_inputs:
    target_plane = rg.Plane(target)
    if signal is None: signal = True
    sleep = float(sleep) if sleep else 0.5
    retract = float(retract) if retract else 0.01
    accel = float(accel) if accel else 1.2
    vel = float(vel) if vel else 0.3
    
    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, base)
    target_plane.Transform(matrix)
    target_pose = ur.pose_by_plane(target_plane)   
    a = ur.action(target_pose,id,signal,sleep,retract,accel,vel)

else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)