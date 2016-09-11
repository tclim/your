"""
Generate UR Script set_dig_out command 
Vers:20140307
Input:
	id [Generic Data] - ID number of digital output port
	signal [Generic Data] - Digital output value as True/False
Returns:
	out [Text] - The execution information, as output and error streams
	a [Generic Data] - Script variable Python
"""
import urscript as ur
from Grasshopper.Kernel import GH_RuntimeMessageLevel as gh_msg

error_inputs = []
if not id: error_inputs.append('id')
if not signal: error_inputs.append('signal')

if not error_inputs:
    a = ur.set_digital_out(int(id), signal)
else:
    error_message = 'Failed to collect data for {0} required input(s): {1}'.format(len(error_inputs), ','.join(error_inputs))
    ghenv.Component.AddRuntimeMessage(gh_msg.Warning, error_message)