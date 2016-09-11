"""
Generate a list of UR script commands for a sequential cutting action (servo based). 
Vers:20140309
Input:
	targets (in, optional) [Generic Data] - A list of target plane to move through
	base (in, optional) [Generic Data] - A reference plane used as the basis for calculating target poses
	start (in, optional) [Generic Data] - A list of joint angles specifying start position
	end (in, optional) [Generic Data] - A list of joint angles specifying end position
	accel (in, optional) [Generic Data] - Optional. Tool accel in m/s^2
	vel (in, optional) [Generic Data] - Optional. Tool speed in m/s
	radius (in, optional) [Generic Data] - Optional. Blend radius in m
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""

import urscript as ur
import Rhino.Geometry as rg
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg


error_inputs = []
if not targets: error_inputs.append('targets')
if not base: error_inputs.append('base')
if not start: error_inputs.append('start')
if not end: error_inputs.append('end')

if not error_inputs:
    cut_accel = float(accel) if accel else 0.01
    cut_vel = float(vel) if vel else 0.0085
    cut_blend = float(radius) if radius else 0.01
    start_joints = [float(sj) for sj in start_joints]
    end_joints = [float(ej) for ej in end_joints]
    
    # Orient the cut planes with reference to robot base and create poses
    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, base)
    print type(targets[0])
    initial_cut_plane = rg.Plane(targets[0])
    initial_cut_plane.Transform(matrix)
    initial_cut_pose = ur.pose_by_plane(initial_cut_plane)
    
    cut_planes = targets[1:]
    [cp.Transform(matrix) for cp in cut_planes]
    cut_poses = [ur.pose_by_plane(cp) for cp in cut_planes]
    
    commands = ur.statements(#1) Approach start position
                             ur.movej(start_joints,3.0, 3.0),
                             #2) Approach first cut pose
                             ur.movel(initial_cut_pose, 0.1, 0.1),
                             #3) Move through rest of cut poses
                             [ur.servoc(cp, cut_accel, cut_vel, cut_blend) for cp in cut_poses],
                             #4) Move to end position
                             ur.movej(end_joints, 0.1, 0.15))      
    
    a = commands

else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)
