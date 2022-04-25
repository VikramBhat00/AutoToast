

import serial
import time
from copy import deepcopy






#Message Format  Start byte    Rotation Degrees  Toast Stop indicator  End Byte
#									(0-180)			    (0, 1)
msg = bytearray([	254, 		       0,               0, 			     255])

def write_message(arduino, rotate, stop):
	msg_to_write = deepcopy(msg)
	msg_to_write[1] = rotate	
	if stop == True:
		msg_to_write[2] = 1

	arduino.write(msg_to_write)

# arduino = serial.Serial(port = '/dev/cu.usbmodem101', baudrate=115200, timeout = 0.1)



# switcher = 1
# # for i in range(3):
# # 	write_message(arduino, 100, True)
# # 	time.sleep(0.5)
# while(1):
# 	write_message(arduino, 100,switcher)
	

# 	if switcher == 1:
# 		switcher = 0
# 	else:
# 		switcher = 1
# 	data = arduino.readline().hex()
# 	if data:
# 		print(data)
# 	time.sleep(1)