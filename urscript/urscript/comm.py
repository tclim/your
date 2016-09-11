""" comm.py module manages Robot communication using sockets.
It contains functions for sending and listening to the robot
"""

import socket
from struct import unpack

PORT_DASH = 29999
PORT = 30002
PORT_RT = 30003

def send_script(ur_program, robot_ip) :
    """Send a script to robot via a socket
    Args:
    ur_program: Formatted UR Script program to send (string)
    robot_ip: IP address of robot (string)        
    """
       
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        # add an extra new line
        ur_program += '\n'
        s.connect((robot_ip, PORT))
        s.send(ur_program)
    except socket.timeout:
        print "Time out connecting to {0} Port:{1}".format(robot_ip,PORT)
    except socket.error, e:
        print e  
    s.close()

def stop_program(robot_ip):
    """ Pauses a running program by sending a command to the Dashboard
    Args:
    robot_ip: IP address of robot (string) 
    """
    send_script('pause', robot_ip,PORT_DASH)

def listen(robot_ip):
    """Returns robot data received through a socket in dictionary format.
    Args:
    robot_ip: IP address of robot (string)
    Returns:
    dict_data: A dictionary containing robot data in readable format      
    """
    data = _receive_data(robot_ip)
    dict_data = _format_data(data)
    return dict_data

def _receive_data(robot_ip):
    """Receives unformatted data from robot using the realtime interface (Port 30003)
    Args:
    robot_ip: ip address of robot (string)
    Returns:
    data: Robot data (byte[])
    """    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(.1)
    try:
        s.connect((robot_ip, PORT_RT))
    except socket.timeout:
        print "Time out connecting to {0} Port:{1}".format(robot_ip,PORT_RT)
    except socket.error, e:
        print e  
    data = s.recv(1024)
    s.close()
    return data

def _format_data(data):
    """Formats robot data into dictionary   
    Received byte array is formatted as a dictionary. For added into on data: see 
    Args:
    data: Raw data from robot (byte[])
    Returns:
    dict_data: A dictionary containing data in readable format
    """ 
    dict_data = {}

    fmt_int = "!i"
    #fmt_uInt = "!Q"
    fmt_double1 = "!d"
    fmt_double3 = "!ddd"
    fmt_double6 = "!dddddd"
    
    dict_data["message_length"] = unpack(fmt_int, data[0:4])
    dict_data["time"] = unpack(fmt_double1, data[4:12])
    dict_data["target_joints_pos"] = unpack(fmt_double6, data[12:60])
    dict_data["target_joints_vel"] = unpack(fmt_double6, data[60:108])
    dict_data["target_joints_accel"] = unpack(fmt_double6, data[108:156])
    dict_data["target_joints_current"] = unpack(fmt_double6, data[156:204])
    dict_data["target_joints_torque"] = unpack(fmt_double6, data[204:252])
    dict_data["actual_joints_pos"] = unpack(fmt_double6, data[252:300])
    dict_data["actual_joints_vel"] = unpack(fmt_double6, data[300:348])
    dict_data["actual_joints_current"] = unpack(fmt_double6, data[348:396])
    dict_data["xyz_accelerometer"] = unpack(fmt_double3, data[396:420])
    dict_data["tcp_force"] = unpack(fmt_double6, data[540:588])
    dict_data["tool_pose"] = unpack(fmt_double6, data[588:636])
    dict_data["tool_speed"] = unpack(fmt_double6, data[636:684])
    #dict_data["digital_input"] = unpack(fmt_double6, data[636:684])
    dict_data["joint_temperatures"] = unpack(fmt_double6, data[692:740])

    return dict_data