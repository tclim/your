"""
Generate a UR Script program and send it to the robot 
Vers:20140307
Input:
	send [Generic Data] - True to send to robot
	robot id [Generic Data] - Robot ID: 1/2/3
	commands [Generic Data] - A list of UR Script commands
	functions (in, optional) [Generic Data] - Optional. Custom UR Script functions to include in the program
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import comm
import urscript as ur
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

error_inputs = []
if not send: error_inputs.append('send')
if not id: error_inputs.append('id')
if not commands: error_inputs.append('commands')

if not error_inputs:
    ip = '192.168.10.%d'%(10 * int(id) + 3)
    script = ""
    statements = statements if hasattr(commands, '__iter__') else list(commands) 
    statements.insert(0,ur.popup('Running script'))
    if functions and not None in functions:
        script += ur.create_function('main',statements,functions)
    else:
        script += ur.create_function('main',statements)  
    a = script
    if _send:
        comm.send_script(script,ip)
else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)