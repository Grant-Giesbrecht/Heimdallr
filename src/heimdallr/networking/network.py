
from pyfrost.base import *
from pyfrost.pf_client import *

# def client_handler(ca:ClientAgent, opt:ClientOptions, words:list) -> bool:
# 	''' Handles commands on the client side'''
	
# 	# This function would only be needed if commandline_main() were going to be called, rather than just direct function calls.
	
# 	return False

# class HeimdallrClientAgent(ClientAgent):
# 	''' Custom version of ClientAgent with functions specialized for Heimdallr.
# 	'''
	
# 	def __init__(self, **kwargs):
# 		super().__init__(**kwargs)
	
# 	def register

class RemoteInstrument:
	''' Class to represent an instrument driven by another host on this network. This
	class allows remote clients to control the instrument, despite not having a 
	connection or driver locally.
	'''
	
	def __init__(self, ca:ClientAgent, remote_id:str=None, remote_address:str=None):
		
		# Save values
		self.remote_id = remote_id
		self.remote_address = remote_address
		self.client_agent = ca
		
		self.connected = False # True if sucessfully connected to a remote instrument via server.
		
		# Register with server - this will populate
		self.register_instrument(remote_id=self.remote_id, remote_address=self.remote_address)
	
	def register_instrument(self, remote_id:str=None, remote_address:str=None):
		
		#TODO: Verify that remote_id or remote_address are valid
		
		# Tell server you wish to connect to this instrument
		gc = GenCommand("REG-INST", {"REMOTE-ID":remote_id, "REMOTE-ADDR":remote_address })
		
		data_packet = self.client_agent.send_query(gc)
		
		# Check for missing packet
		if data_packet is None:
			self.connected = False
			return
		
		# Check for error in packet
		if not data_packet.validate_reply(['REMOTE_ID', 'REMOTE_ADDRESS'], self.log):
			self.connected = False
			return
		
		# Update data
		self.remote_id = data_packet.data['REMOTE_ID']
		self.remote_address = data_packet.data['REMOTE_ADDRESS']
		self.connected = True
	
	def remote_call(self, func_name:str, *args, **kwargs):
		''' Calls the function 'func_name' of a remote instrument '''
		
		arg_str = ""
		for a in args:
			arg_str = arg_str + f"{a} "
		for key, value in kwargs.items():
			arg_str = arg_str + f"{key}:{value} "
		
		print(f"Initializing remote call: function = {func_name}, arguments = {arg_str} ")
		
		#TODO: Send command to server
	
def RemoteFunction(func):
	'''Decorator to allow empty functions to call
	their remote counterparts'''
	
	def wrapper(self, *args, **kwargs):
		self.remote_call(func.__name__, *args, **kwargs)
		func(self, *args, **kwargs)
	return wrapper
