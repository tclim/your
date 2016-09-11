"""
Generate a list of UR script commands for a custom crumpling action.     Robot grips, folds and crumples a strip using local motions only. 
Vers:20140309
Input:
	approach (in, optional) [Generic Data] - Approach distance to grip point
	rotation (in, optional) [Generic Data] - Specify fold point in tool coordinates system
	angle (in, optional) [Generic Data] - Folding angle in degrees
	c_dist (in, optional) [Generic Data] - Distance covered by crumpling action
	heat (in, optional) [Generic Data] - Wait time for heating in s)
	cool (in, optional) [Generic Data] - Wait time for cooling in s)
	f_accel (in, optional) [Generic Data] - Optional. Folding accel in m/s^2
	f_vel (in, optional) [Generic Data] - Optional. Folding speed in m/s
	c_accel (in, optional) [Generic Data] - Optional. Crumpling accel in m/s^2
	c_vel (in, optional) [Generic Data] - Optional. Crumpling speed in m/s
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import urscript as ur
import Rhino.Geometry as rg
import math
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

# Fixed variables
cool_io = 1
grip_io = 3
clamp_io = 4

error_inputs = []
if not approach: error_inputs.append('approach')
if not rotation: error_inputs.append('rotation')
if not angle: error_inputs.append('angle')
if not c_dist: error_inputs.append('c_dist')
if not heat:error_inputs.append('heat')
if not cool: error_inputs.append('cool')

if not error_inputs:
    # Ensure parameter typing
    approach = float(approach)
    angle = math.radians(float(angle))
    crumple = float(c_dist)
    heat = float(heat)
    cool = float(cool)
    fold_accel = float(f_accel) if f_accel else 0.1
    fold_vel = float(f_vel) if f_vel else 0.1
    crumple_accel = float(c_accel) if c_accel else 0.1
    crumple_vel = float(c_vel) if c_vel else 0.1

    # Local Motion 1 - Approach and grip
    v_approach = (0,0, approach)
    pose_approach = ur.pose_by_vectors(v_approach,(0,0,0))
    
    commands1 = ur.statements(ur.sleep(0.5),                             #1) Slight pause
                              ur.move_local(pose_approach,0.1, 0.1),    #2) Approach
                              ur.set_digital_out(grip_io, True))       #3) Close gripper
    
    # Local Motion 2 - Fold
    pose_tcp_offset = ur.pose_by_vectors(rotation, (0,0,0))
    pose_fold = ur.pose_by_vectors((0,0,0), (0,0, angle)) 
    
    commands2 = ur.statements(ur.sleep(heat),                                 #1) Heat
                              ur.set_tcp(pose_tcp_offset),                    #2) Set Rotation point
                              ur.move_local(pose_fold,fold_accel,fold_vel))   #3) Rotate 
    
    # Local Motion 3 - Crumple
    v_crumple = (-crumple,0, 0)    
    pose_crumple= ur.pose_by_vectors(v_crumple, (0,0,0)) 
    
    commands3 = ur.statements(ur.move_local(pose_crumple,crumple_accel,crumple_vel),   #1) Rotate
                              ur.set_digital_out(cool_io, True),                       #2) Switch on cooling
                              ur.sleep(cool),                                          #3) Sleep/wait - cooling
                              ur.set_digital_out(cool_io, False))                      #4) Switch off cooling
    
    # Local Motion 4 - Retract
    v_retract = (0,0,-approach)    
    pose_retract= ur.pose_by_vectors(v_retract,(0,0,0))
    
    commands4 = ur.statements(ur.set_digital_out(grip_io, False),      #1) Open clamp
                              ur.sleep(0.5),                            #2) Slight pause
                              ur.move_local(pose_retract),   #3) Retract
                              ur.set_digital_out(clamp_io, True))       #4) Open gripper
    
    commands_all = ur.statements(commands1, commands2, commands3, commands4)
    a = commands_all

else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)
