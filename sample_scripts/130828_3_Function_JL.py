"""
Sample 3 : Create a program 1
Take note: Units are in m
"""

#1) Import 
import urscript as ur
import comm 
import Rhino
import rhinoscriptsyntax as rs

pick_target = (0.3,0.3,0.45,0,0,0)
place_target = (0.3,0.5,0.55,0,0,0)
ip = '192.168.10.13'

# Return a pick function
def pick_script(target):
    pick_pose = ur.pose(*target)
    pick = ur.statements(ur.comment('picking now'),
                         ur.action(pick_pose, 1, True))
    return ur.create_function('pick',pick)

# Return a place function
def place_script(target):
    place_pose = ur.pose(*target),
    place = ur.statements(ur.comment('placing now'),
                          ur.action(place_pose, 1, False))
    return ur.create_function('place',place)

# Listen to robot
safety = comm.listen(ip)['actual_joints_pos']

# Create body of main program
main_statements = ur.statements(ur.popup("starting now"),
                  ur.movej(safety),
                  ur.custom_function('pick'),
                  ur.movej(safety),
                  ur.custom_function("place"),
                  ur.movej(safety)
                  )

# Create pick and place functions
pick_function = pick_script(pick_target)
place_function = place_script(place_target)

main_script = ur.create_function("main",main_statements, [pick_script(),place_script()])
print main_script
#comm.send_script(main_script,ip)

