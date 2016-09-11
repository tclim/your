""" script.py module contains classes and functions for generating UR Script programs

It contains:
    1) Functions for generating, loading and saving UR Script programs/functions
    2) Functions for generating UR Script statements (commands,comments, expressions)
    3) Functions for generating Pose type that is specific to UR script.

"""

#----- Functions for creating, loading and saving UR Script programs/functions -----

import string
import os.path

def create_function(name, statements, inner_functions = (), arguments = ()):
    """Returns a UR script formatted program/function
    A UR program is a function without arguments. It contains a list of statements (commands) and may contain
    inner functions.
    Args:
    name: Name of function (string)
    statements: A list of UR script formatted statements (string collection)
    inner_functions: Optional. A list of inner functions (string collection) 
    """
    # create header
    arg_list = ','.join(['{}'.format(arg) for arg in arguments])
    header = 'def {0}({1}):'.format(name, arg_list)
    # inner_functions body
    indented_functions = [_indent_body(f) for f in inner_functions]
    function_body = ('\n').join(indented_functions)
    #command body
    statement_body ='\t' + '\n\t'.join(statements)
    #footer
    footer = 'end\n'
    return '\n'.join([ txt for txt in (header,function_body, statement_body, footer) if txt])

def statements(*ur_statement):
    """Convenience function to combine UR Script formatted statements(single or sequence) into one list
    """
    _statements = []
    for urs in ur_statement:
        if hasattr(urs, 'strip'):      #assume urscript formatted string
            _statements.append(urs)
        elif hasattr(urs, '__iter__'):
            _statements.extend(urs)
    return _statements

def _indent_body(text_body):
    """Private function that indents each line of a text string
    Args:
    text_body: Text to indent which spans multiple lines (string)
    Returns:
    Indented text as string
    """
    lines = text_body.split('\n')
    body = [('\t' + l) for l in lines]
    return '\n'.join(body)

def save_function(save_path, file_name, text):
    """Saves text to file
    Args:
    save_path: The path pointing to directory to save in (string)
    file_name: Name of file (string)
    function_text: Text to write (string)
    Raises:
    IO error on write failure
    """
    full_name = os.path.join(save_path, file_name+".txt")
    try:
        f = open(full_name, "w")
        try:
            f.write(text) # Write a string to a file
        finally:
            print("file saved")
            f.close()
    except IOError,e:
        print e

def load_function(load_path, file_name):
    """Loads a text from file. Should be used to load already formatted UR script programs
    Args:
    load_path: The path pointing to directory where UR script program is saved
    file_name: Name of file (string)
    Raises:
    IO error on read failure
    """
    full_name = os.path.join(load_path, file_name+".txt")
    try:
        f = open(full_name)
        return "".join([line for line in f])
    except IOError, e:
        print e.strerror

#----- Functions for Generating UR Script commands (Interfaces, Motion and Internals modules), custom operations and miscellaneous statements -----

def get_analog_in(id):
    """Returns UR script for get_analog_in(n) - Get analog input level    
    Args:
    id: The number (id) of the input. (int)
    Returns:
    Formatted get_analog_in UR Script function
    """
    return 'get_analog_in({})'.format(id)
   
def get_analog_out(id):
    """Returns UR script for get_analog_out(n) - Get analog output level  
    Args:
    id: The number (id) of the output. (int)
    Returns:
    Formatted get_analog_out UR Script function
    """
    return 'get_analog_out({})'.format(id)

def get_digital_in(id):
    """Returns UR script for get_digital_in(n) - Get digital input level   
    Args:
    id: The number (id) of the input. (int)
    Returns:
    Formatted get_digital_in UR Script function
    """
    return 'get_digital_in({})'.format(id)
   
def get_digital_out(id):
    """Returns UR script for get_digital_in(n) - Get digital output level  
    Args:
    id: The number (id) of the output. (int)
    Returns:
    Formatted get_digital_out UR Script function
    """
    return 'get_digital_out({}'.format(id)

def get_inverse_kin(pose):
    """
    Returns UR script for get_inverse_kin(x) - Inverse kinematic transformation (tool space -> joint space).   
    Args:
    pose: Tool pose (Pose)
    Returns:
    Formatted get_inverse_kin UR Script function
    """
    return 'get_inverse_kin({0})'.format(pose)

def popup(message, title = "Popup", warning = False, error = False):
	"""Returns UR Script for popup(s,title, warning,error) - Display popup on GUI  
    Args:
    message: Message string
    title: Optional. Popup title string
    warning: Optional. Warning message (boolean)
    error: Optional. Error message (boolean)      
    Returns:
    Formatted popup UR Script function
    """
	return 'popup("%s",title = "%s", warning = %s, error = %s)'%(message, title, warning, error)

def movec(pose_via, pose_to, accel = 1.2, vel = 0.3, blend = 0.0):
    """Returns UR script for movec - Move to position (circular in tool-space)   
    Args:
	pose via: Path point (note: only position is used, pose via can also be specified as joint positions)
	pose to: Target pose (pose to can also be specified as joint positions)
	accel: Optional. Tool acceleration [m/s^2]
	vel: Optional. Tool speed [m/s]
	blend: Optional. Blend radius (of target pose) [m]       
    Returns:
    Formatted movec UR Script function
    """
    return 'movec({0}, {1}, a = {2:.2f}, v = {3:.2f}, r = {4:.2f})'.format(pose_via, pose_to, accel , vel , blend)
   
def movej(joints, accel = 3.0, vel = 0.75, time = 0.0, blend = 0.0):
    """Returns UR script for movej - Move to position (linear in joint-space)    
    Args:
    joints: Joint positions - can also be specified in pose (list of float)
    accel: Optional. Joint acceleration of leading axis [rad/s^2]
    vel: Optional. Joint speed of leading axis [rad/s]
    time: Optional. Time [s]
    blend: Optional. Blend radius [m]        
    Returns:
    Formatted movej UR Script function
    """
    if not hasattr(joints, 'strip'):
        joints = list(joints)
    return 'movej({0}, a = {1:.2f}, v = {2:.2f}, t = {3:.4f}, r = {4:.2f})'.format(joints, accel, vel, time, blend)

def movel(pose, accel = 1.2, vel = 0.3, time = 0.0, blend = 0.0):
    """Returns UR script for movel - Move to position (linear in joint-space)    
    Args:
	pose: Target pose (can also be specified as joint positions)
	accel: Optional. Tool acceleration [m/s^2]
	vel: Optional. Tool speed [m/s]
	time: Optional. Time [s]
	blend: Optional. Blend radius [m]        
    Returns:
    Formatted movel UR Script function
    """
    return 'movel({0}, a = {1:.2f}, v = {2:.2f}, t = {3:.4f}, r = {4:.2f})'.format(pose, accel, vel, time, blend)
 
def movep(pose, accel = 1.2, vel = 0.3, blend = 0.0):
    """Returns UR script for movep - Blend circular (in tool-space) and move linear (in tool-space) to position    
    Args:
	pose: Target pose (can also be specified as joint positions)
	accel: Optional. Tool acceleration [m/s^2]
	vel: Optional. Tool speed [m/s]
	blend: Optional. Blend radius [m]        
    Returns:
    Formatted movep UR Script function
    """
    return 'movep({0}, a = {1:.2f}, v = {2:.2f}, r = {3:.2f})'.format(pose, accel, vel, blend)

def request_boolean_from_client(message):
    """ Returns UR Script for request_boolean_from_client - Useful for introducing a pause
    Args:
    message: String message to show on request screen.
    Returns:
    Formatted UR Script function
    """
    return 'request_boolean_from_primary_client("%s")'%message

def servoc(pose, accel = 1.2, vel = 0.3, blend = 0.0):
    """Returns UR script for servoc - Servo to position (circular in tool-space)   
    Args:
	pose: Target pose (can also be specified as joint positions)
	accel: Optional. Tool acceleration [m/s^2]
	vel: Optional. Tool speed [m/s]
	blend: Optional. Blend radius (of target pose) [m]    
    Returns:
    Formatted servoc UR Script function
    """
    return 'servoc({0}, a = {1:.2f}, v = {2:.2f}, r = {3:.2f})'.format(pose, accel, vel, blend)

def servoj(joints, time = 0.0):
    """Returns UR script for servoj - Servo to position (linear in joint-space)    
    Args:
	joints: Joint positions (can also be specified as a pose)
	time: Optional. Time [s]       
    Returns:
    Formatted servoj UR Script function
    """
    return 'servoc({0},  t = {1:.4f})'%(joints, time)

def set_analog_out(id, signal):
    """Returns UR script for set_analog_out(n,f) - Set analog output level   
    Args:
    id: int. The number (id) of the output. (int)
    signal: The signal level [0;1] (float) 
    Returns:
    Formatted set_analog_out UR Script function
    """
    return 'set_analog_out(%s,%s)'%(id,signal)

def set_digital_out(id, signal):
    """Returns UR script for set_digital_out(n,b) - Set digital output level   
    Args:
    id: int. The number (id) of the output. (int)
    signal: The signal level (boolean)  
    Returns:
    Formatted set_digital_out UR Script function
    """
    return 'set_digital_out(%s,%s)'%(id,signal)

def set_gravity(direction):	
	"""Returns UR Script for set_gravity(d)- Set the direction of gravity  
    Args:
	direction: 3D vector, describing the direction of the gravity, relative to robot's base.      
    Returns:
    Formatted set_gravity UR Script function
    """
	return 'set_gravity{0}'.format(direction,)

def set_payload(mass, center_of_gravity = None):
    """Returns UR Script for set_payload(m, CoG)- Set payload mass and center of gravity    
    Args:
    mass: mass in kilograms
    center_of_gravity: Optional. Center of Gravity [CoGx, CoGy, CoGz] - displacement from the toolmount. [m]
    Returns:
    Formatted set_gravity UR Script function
    """
    if center_of_gravity:
        return 'set_payload({0},{1})'.format(mass, center_of_gravity)
    else:
        return 'set_payload({0})'.format(mass)

def set_tcp(pose):
    """	 
    Returns UR Script for set_tcp(pose) - Set the Tool Centre Point   
    Args:
	pose: A pose describing the transformation from the output flange coordinate system to the TCP. (Pose)
    Returns:
    Formatted set_tcp UR Script function
    """
    return 'set_tcp({0})'.format(pose)

def sleep(time):
    """
    Returns UR script for sleep(t) - Sleep for an amount of time   
    Args:
    time: time [s]               
    Returns:
    Formatted set_tcp UR Script function
    """
    return 'sleep({0})'.format(time)

def socket_close(socket_name):
    """
    Returns UR script for socket_close(address,port,socket_name) - Closes ethernet communication    
    Args:
	socket name: Name of socket (string)   
    Returns:
    Formatted socket_close UR Script function
    """
    return 'socket_close(socket_name = "{}")'.format(socket_name)

def socket_get_var(name, socket_name):
	"""
	Returns UR script for socket_get_var(name,socket_name) - Reads an integer from the server   
    Args:
	name: Variable name (string)
	socket name: Name of socket (string)   
    Returns:
    Formatted socket_get_var UR Script function
	"""
	return 'socket_get_var({0},socket_name = "{1}")'.format(name,socket_name)
	
def socket_open(address, port, socket_name):
    """
    Returns UR script for socket_open(address,port,socket_name) - Open ethernet communication    
    Args:
	address: Server address (string)
	port: Port number (int)
	socket name: Name of socket (string)   
    Returns:
    Formatted socket_open UR Script function
    """
    return 'socket_open({0}, {1},socket_name = "{2}")'.format(address,port,socket_name)

def socket_send_line(str, socket_name):
    """
    Returns UR script for socket_send_string(str,socket_name) - Sends a string with a newline character to the server  
    Args:	
	str: The string to send (ascii)
	socket name: Name of socket (string) 
    Returns:
    Formatted socket_send_line UR Script function
    """  
    return 'socket_send_line("{0}",socket_name = "{1}")'.format(str,socket_name)

def socket_send_string(str, socket_name):
    """
    Returns UR script for socket_send_string(str,socket_name) - Sends a string to the server
    Args:	
	str: The string to send (ascii)
	socket name: Name of socket (string)   
    Returns:
    Formatted socket_send_string UR Script function
    """  
    return 'socket_send_string("{0}",socket_name = "{1}")'.format(str,socket_name)

def socket_set_var(name, value, socket_name):
    """
    Returns UR script for socket_send_string(str,socket_name)
    Sends the message "set <name> <value>" through the socket.Sends a string to the server   
    Args:	
	name: Variable name (string)
	value: The number to send (int)
	socket name: Name of socket (string)	    
    Returns:
    Formatted socket_set_var UR Script function
    """  
    return 'socket_set_var({0},{1},socket_name = "{2}")'.format(str,socket_name)
   
def stopj(accel):
	"""Returns UR Script for stopj - Decellerate joint speeds to zero	
	Args:
	accel: Joint acceleration of leading axis [rad/s^2]	
	Returns:
    Formatted stopj UR Script function
	"""
	return 'stopj({0})'.format(accel)

def stopl(accel):	    	
	"""
	Returns UR Script for stopl - Decellerate tool speed to zero	
	Args:
	accel: Tool acceleration [m/s^2]		
	Returns:
	Formatted stopl UR Script function
	"""
	return 'stopl({0})'.format(accel)

def textmsg(message):
    """
    Returns UR script for testmsg(s) - Sends text message to be shown on GUI log tab   
    Args:
    message: message string          
    Returns:
    Formatted textmsg UR Script function
    """
    return 'textmsg("%s")'%message

### ---- Custom Actions (sequences of URscript commands) ----
 
def action(pose, id, on, sleep_time = 0.5, retract = 0.0, accel = 1.2, vel = 0.3):
    """Returns a tuple of UR script commands for a motion-digital out compound action     
    Robot moves to target pose and sets digital out. An optional retraction motion is added at the end. For example, this is used for pick/place operations.
    Args:
    pose: Target pose (can also be specified as joint positions)
    id: The number (id) of the digital output. (int)
    on: The signal level. (boolean)
    sleep_time: Optional. Wait time following digital_out [s]
    retract: Optional. Distance to retract in TCP's -z direction after sleep. [m]    
    accel: Optional. Tool accel [m/s^2]
    vel: Optional. Tool speed [m/s] 
    Returns:
    Tuple of UR script commands
    """
    commands = []
    # Move to target pose
    commands.append(movel(pose,accel,vel))
    # Set digital out
    commands.append(set_digital_out(id,on))
    # Sleep
    commands.append(sleep(sleep_time))
    # Retract
    if retract:
        _retract_pose = pose_by_vectors((0,0,-retract),(0,0,0))
        commands.extend(move_local(_retract_pose,accel/3, vel/3))
    return tuple(commands)
 
def move_local(pose, accel = 1.2, vel = 0.3, time = 0.0, blend = 0.0):	
    """
    Returns a tuple of UR script commands that describes a local linear motion.  
    Args:
    pose:  Pose with reference to tool. [X,Y,Z,Rx,Ry,Rz] 
    accel: Optional. Tool accel [m/s^2]
    vel: Optional. Tool speed [m/s] 
	time: Optional. Time [s]
	blend: Optional. Blend radius [m]     
    Returns:
    Tuple of UR script commands
    """
    command1 = "cur_pose = get_forward_kin()"
    command2 = 'target_pose = pose_trans(cur_pose, {})'.format(pose)
    command3 = 'movel(target_pose, a = {0:.2f}, v = {1:.2f}, t = {2:.4f}, r = {3:.2f})'.format(accel,vel,time, blend)
    return (command1, command2, command3)

def comment(comment_text):
    """Returns a formatted comment statement
    Args:
    comment_text: Comment text (string)
    Returns:
    A comment statement
    """
    return '# {0}'.format(comment_text)

def expression(variable_name, variable_value):
    """Set a variable by formatting a statement in the form "variable = value"
    Args:
    variable_name: Name of variable (string)
    variable_value: Value of variable
    Returns:
    A variable statement
    """
    return "{0} = {1}".format(variable_name, variable_value)

def custom_function(function_name, args = None):
    """ Formats a statement for calling a function
    Args:
    function_name: Name of function to call (string)
    args: Optional. Arguments for the function
    Returns:
    A function call statement 
    """
    if not args:
        return '{0}()'.format(function_name)
    elif hasattr(args, '__iter__') and not isinstance(args,basestring):
        return '{0}({1})'.format(function_name,','.join([str(a) for a in args]))
    else:
        return '{0}({1})'.format(function_name,args)

### ----- Functions related to UR Script Pose type -----

import math
from collections import namedtuple

def pose(x,y,z,ax,ay,az):
    """Returns pose as a string in format p[x,y,z,ax,ay,az]
    Args:
    x: X value of position vector [m]
    y: Y value of position vector [m]
    z: Z value of position vector [m]
    ax: X value of rotation vector 
    ay: Y value of rotation vector
    az: Z value of rotation vector
    Returns:
    Formatted pose
    """     
    return "p[{0:f}, {1:f}, {2:f}, {3:f}, {4:f}, {5:f}]".format(x,y,z,ax,ay,az) 

def pose_by_vectors(position,orientation):
    """Returns pose as a string in format p[x,y,z,ax,ay,az]
    Args:
    position: Vector (x,y,z) [m]
    orientation: Rotation vector based on axis-angle format
    Returns:
    Formatted pose
    """     
    return "p[{0:f}, {1:f}, {2:f}, {3:f}, {4:f}, {5:f}]".format(*(tuple(position) + tuple(orientation)))

def pose_by_plane(plane):
    """Returns pose as a string in format p[x,y,z,ax,ay,az] using plane argument
    Use this with Rhino planes
    Args:
    plane: Plane object that has attributes "XAxis", "YAxis", "ZAxis", "Origin"
    Returns:
    Formatted pose
    Raises:
    Attribute error if argument has no plane attributes
    """
    try:
        origin = getattr(plane, "Origin")
        xaxis = getattr(plane, "XAxis")
        yaxis = getattr(plane, "YAxis")
        zaxis = getattr(plane, "Normal")           
    except AttributeError, e:
        print "Handling attribute error:",e
    else:
        position = (origin.X, origin.Y, origin.Z)
        axis_angle = axisangle_from_vectors((xaxis, yaxis, zaxis))
        orientation = tuple([axis_angle.angle * item for item in axis_angle.axis])
        return "p[{0:f}, {1:f}, {2:f}, {3:f}, {4:f}, {5:f}]".format(*(position + orientation))

def pose_by_origin_axis(origin, xaxis, yaxis):
    """Returns pose as a string in format p[x,y,z,ax,ay,az] 
    Uses information from a plane
    Args:
    origin: Vector (x,y,z) [m]
    xaxis: Xaxis of plane
    yaxis: Yaxis of plane
    Returns:
    Formatted pose
    """
    assert len(origin) == 3, "Please ensure origin vector has 3 values"
    assert len(xaxis) == 3, "Please ensure xaxis vector has 3 values"
    assert len(yaxis) == 3, "Please ensure yaxis vector has 3 values"
    # Cross product 
    zaxis =  (xaxis[1] * yaxis[2] - xaxis[2] * yaxis[1], 
                -xaxis[0] * yaxis[2] + xaxis[2] * yaxis[0], 
                xaxis[0] * yaxis[1] - xaxis[1] * yaxis[0])  
    axis_angle = axisangle_from_vectors((xaxis, yaxis, zaxis))
    orientation = tuple([axis_angle.angle * item for item in axis_angle.axis])
    return "p[{0:f}, {1:f}, {2:f}, {3:f}, {4:f}, {5:f}]".format(*(tuple(origin) + orientation))


        
def axisangle_from_vectors(vectors):
    """ Returns an Axis_angle named_tuple using three orthonormal vectors as arguments  
    References Martin Baker's implementation of matrix to axis angle function at www.euclideanspace.com    
    Args:
    vectors: A list of three orthonormal vectors.  
    Returns:
    Axis_angle named_tuple that defines an orientation representation  
    """ 
    Axis_angle = namedtuple('Axis_angle','angle axis')
        
    epsilon = 0.01
    epsilon2 = 0.1   
    if (math.fabs(vectors[1].X - vectors[0].Y) < epsilon) and \
        (math.fabs(vectors[2].X - vectors[0].Z) < epsilon) and \
        (math.fabs(vectors[2].Y - vectors[1].Z) < epsilon):
    #singularity found
    #first check for identity matrix which must have +1 for all terms in leading diagonal and zero in other terms
        if (math.fabs(vectors[1].X + vectors[0].Y) < epsilon2) and \
            (math.fabs(vectors[2].X + vectors[0].Z) < epsilon2) and \
            (math.fabs(vectors[2].Y + vectors[1].Z) < epsilon2) and \
            (math.fabs(vectors[0].X + vectors[1].Y + vectors[2].Z - 3) < epsilon2):
            # Identity matrix. Singularity found: angle = 0. 
            # Set zero angle and arbitrary axis
            return Axis_angle(0, (1,0,0))
        else:
            # Singularity found: angle = 180
            xx = (vectors[0].X + 1)/2
            yy = (vectors[1].Y + 1)/2
            zz = (vectors[2].Z + 1)/2
            xy = (vectors[1].X + vectors[0].Y)/4
            xz = (vectors[2].X + vectors[0].Z)/4
            yz = (vectors[2].Y + vectors[1].Z)/4            
            root_half = math.sqrt(0.5)
            if ((xx > yy) & (xx > zz)):
                # vectors[0][0] is the largest diagonal term
                if (xx < epsilon):
                    axis = (0, root_half, root_half)
                else:
                    x = math.sqrt(xx)
                    axis = (x, xy/x, xz/x)
            elif (yy > zz): 
                # vectors[1].Y is the largest diagonal term
                if (yy < epsilon):
                    axis = (root_half, 0, root_half)
                else:
                    y = math.sqrt(yy)
                    axis = (xy/y, y, yz/y) 
            else: 
                # vectors[2].Z is the largest diagonal term so base result on this
                if (zz < epsilon):
                    axis = (root_half, root_half, 0)
                else:
                    z = math.sqrt(zz)
                    axis = (xz/z, yz/z, z)
            return Axis_angle(math.pi,axis)            
    else:
        #no singularities
        s = math.sqrt(\
            (vectors[1].Z - vectors[2].Y) * (vectors[1].Z - vectors[2].Y) + \
            (vectors[2].X - vectors[0].Z) * (vectors[2].X - vectors[0].Z) + \
            (vectors[0].Y - vectors[1].X) * (vectors[0].Y - vectors[1].X))
        if (math.fabs(s) < 0.001):
            #prevent divide by zero, should not happen if vectors are orthonormal
            s = 1
        angle = math.acos((vectors[0].X + vectors[1].Y + vectors[2].Z - 1) / 2)
        axis = ((vectors[1].Z - vectors[2].Y)/s, (vectors[2].X - vectors[0].Z)/s, (vectors[0].Y - vectors[1].X)/s)
        return Axis_angle(angle, axis)