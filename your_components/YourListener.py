"""
Listen to realtime robot data  
Vers:20140307
Input:
	listen (in) [Generic Data] - True to listen to robot
	datatype (in, optional) [Generic Data] - Data to listen to e.g. "actual_joints_pos", "tool_pose"
	id (in) [Generic Data] - Robot ID: 1/2/3
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import comm
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

error_inputs = []
if listen is None: error_inputs.append('listen')
if not id: error_inputs.append('id')

if not error_inputs:
    ip = '192.168.10.%d'%(10 * int(id) + 3)
    if listen:
        if datatype == 0:
            a = comm.listen(ip)['tool_pose']
        elif datatype == 1:
            a = comm.listen(ip)['actual_joints_pos']
        else:
            a = ["{0} {1}".format(k,v) for k,v in comm.listen(ip).iteritems()]
else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)