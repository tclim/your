"""
Sample 2 : Creating a Pose
Take note: Units
"""

#1) Import 
import urscript as urs
import comm 
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs

ip = '192.168.10.13'

def robot_script():
    
    sel_pt = rs.GetPoint("select point")

    #1) Use 6 values
    pose1 = urs.pose(sel_pt.X,sel_pt.Y,sel_pt.Z, 0,0,0)
    #2) Use two tuples - vector and orientation
    pose2_pos = (sel_pt.X, sel_pt.Y, sel_pt.Z + 0.15)
    pose2 = urs.pose_by_vectors(pose2_pos, (0,0,0))
    #3) Use a Rhino plane
    plane3 = rg.Plane(sel_pt, rg.Vector3d.ZAxis)
    pose3 = urs.pose_by_plane(plane3)
    #4) Use an origin and 2 vectors - same as a plane
    pose4_pos = (sel_pt.X, sel_pt.Y - 0.15, sel_pt.Z + 0.15)
    pose4 = urs.pose_by_origin_axis(pose4_pos, (1,0,0),(0,1,0))
    #5) Use a listened pose
    pose5_vals = comm.listen(ip)['tool_pose']
    pose5 = urs.pose(*pose5_vals)

    
    
    #Create a list of statements
    commands = []
    poses = (pose1,pose2,pose3,pose4)
    #Go through all poses 
    for i in range(len(poses)):
        #Add a comment
        commands.append(urs.comment("Movement {}".format(i)))
        #Add a command
        commands.append(urs.movel(poses[i]))
    # return to pose 5 via movej
    commands.append(urs.movej(pose5))
    
    #3) Create a program using commands as argument
    my_program = urs.create_function("main",commands)
    return my_program

script = robot_script()
print script
#comm.send_script(script,ip)
