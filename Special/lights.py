import serial
from time import sleep

# Communicates with the Arduino to control the LEDs. Not strictly necessary, but a convenient abstraction.
class Lights:
	def __init__(self, port):
		self.serial = serial.Serial(port, 1000000, timeout=1)
		sleep(1) # This is a gross hack, but there doesn't seem to be a better way to wait for the Arduino to be ready

	def set(self, port, level):
		payload = '>' + str(port) + ':' + str(level) + ';'
		# print(payload)
		payload = payload.encode('ascii')
		# print(payload)
		self.serial.write(payload)
		# self.serial.flush()