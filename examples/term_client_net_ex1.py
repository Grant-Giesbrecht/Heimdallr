from heimdallr.all import *
from heimdallr.networking.network import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--local', help="Use localhost instead of intranet address.", action='store_true')
args = parser.parse_args()

# Create socket - this is not protected by a mutex and should only ever be used by the main thread
if args.local:
	ip_address = "localhost"
else:
	ip_address = "192.168.1.116"

if __name__ == '__main__':
	
	log = LogPile()
	
	# Create client agent
	ca = HeimdallrClientAgent(log)
	ca.set_addr(ip_address, 5555)
	ca.connect_socket()
	
	# login to server with default admin password
	ca.login("admin", "password")
	
	# Create client options
	copt = ClientOptions()
	
	ca.get_network_instrument_list(print_ids=True)
	
	# Create remote instruments from address
	# rem_osc1 = RemoteInstrument(ca, log, remote_address="192.168.1.117|TCPIP0::192.168.1.20::INSTR")
	rem_osc1 = RemoteInstrument(ca, log, remote_id="Scope1")
	
	# TODO: Change current register_instrument to something like find instrument
	# TODO: Make register_instrument accept an Instrument object
	# rem_osc1.locate_instrument(rem_osc1)
	
	if rem_osc1.connected:
		log.info(f"Successfully connected rem_osc1 to remote instrument!")
		print(f"IDN provided by network server:")
		print(f"{Fore.YELLOW}{rem_osc1.id}{Style.RESET_ALL}")
	else:
		log.error(f"Failed to connect rem_osc1 to remote instrument!")
	
	#TODO: Do things with rem_osc1 like set the voltage or whatever
	while True:
		
		time.sleep(1)