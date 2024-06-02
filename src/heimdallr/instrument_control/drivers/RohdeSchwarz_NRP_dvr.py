''' Driver for Rohde & Schwarz NRX Power Meter 

Manual: https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/pdm/cl_manuals/user_manual/1178_5566_01/NRX_UserManual_en_10.pdf
'''

from heimdallr.base import *
from heimdallr.instrument_control.categories.rf_power_sensor_ctg import *

class RohdeSchwarzNRP(RFPowerSensor):
	
	def __init__(self, address:str, log:LogPile):
		super().__init__(address, log, expected_idn="Rohde&Schwarz,NRP") # Example string:  ''
		
	# def set_meas_frequency(self, f_Hz:float):
	# 	self.write(f"SENSE:FREQ:CW {f_Hz}")
	# def get_meas_frequency(self):
	# 	return float(self.query(f"SENSE:FREQ:CW?"))
	
	# def send_autoscale(self):
	# 	print("Should this be send or enable? Is it one time?")
	# 	self.write(f":SENS:POW:RANGE:AUTO ON")
	
	def send_trigger(self, wait:bool=False):
		
		self.write(f"*CLS") # Clear status register so can determine when ready
		
		# Maybe should be :INIT:ALL? I think this just triggers all sensors vs one
		# Send trigger
		self.write(f":INIT:IMM")
		
		# Wait for operation to complete if requested
		if wait:
			self.wait_ready()
		
	
	def get_measurement(self):
		
		self.write("UNIT:POW DBM")
		
		data = float(self.query(f"FETCH?"))
		return data
	
	def set_averaging_count(self, counts:int, meas_no:int=1):
		
		 # Enforce bounds - counts
		counts = max(1, min(counts, 1048576))
		if counts != counts:
			self.log.error(f"Did not apply command. Instrument limits number of counts from 1 to 1048576 and this range was violated.")
			return
		
		# Enforce bounds - meas_no
		meas_no = max(1, min(meas_no, 8))
		if meas_no != meas_no:
			self.log.error(f"Did not apply command. Instrument limits measurement-number values from 1 to 8 and this range was violated.")
			return
		
		# Legacy version, works for R&S but deprecated
		#  [SENSe<Sensor>:]AVERage:COUNt[:VALue]
		
		self.write(f"CALC{meas_no}:CHAN1:AVER:COUN:VAL {counts}")

