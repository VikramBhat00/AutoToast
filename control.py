
import serial
import time

import communicate

import CV

import kalman_filter

import models
#Connect to arduino
arduino = serial.Serial(port = '/dev/cu.usbmodem101', baudrate=115200, timeout = 0.1)


kalman_filter.initialize_filter()
capture = CV.init_camera() #open camera and adjust to light

target_done = 103


currentMax = 0
maxCounter = 0

whitest_bread = 255

ready_to_stop = False

percentage_of_perfect_toast = 0.9

counter = 0
decreasing_counter = 0

doneness_readings = {}

donesness_store = []
model = models.white_bread_model_1 #Choose based on ML model
while(1):

	done_num = CV.get_doneness(capture)
	print("Done num: ", done_num)
	donesness_store.append(done_num)
	done_num_int = int(done_num)

	state_est, state_var = kalman_filter.do_kalman_filter_step(donesness_store, counter, model)


	print("KALMAN STATE EST: ", state_est)
	if done_num_int > currentMax:
		currentMax = done_num_int

	if done_num_int not in doneness_readings.keys():
		doneness_readings[(done_num_int)] = 1
	else:
		doneness_readings[(done_num_int)] += 1

	if counter >= 30 and doneness_readings[(currentMax)] >= 2 and currentMax > done_num_int:
		decreasing_counter += 1

	if decreasing_counter >= 10:
		whitest_bread = currentMax
		ready_to_stop = True

	if ready_to_stop and done_num_int <= whitest_bread*percentage_of_perfect_toast:
		for i in range(3):
			communicate.write_message(arduino, 0, True)
			time.sleep(0.5)
		break	

	print("current Max: ", currentMax)
	print("ready? ", ready_to_stop)
	print("whitest_bread: ", whitest_bread)
	print("counter: ", counter)
	print("Target: ", whitest_bread*percentage_of_perfect_toast)
	print("doneness readings of max: ", doneness_readings[(currentMax)])
	print("decreasing_counter: ", decreasing_counter)
	print()
	

	#If the toast has hit the target
	# if abs(done_num - target_done) <= 1:
	# 	#Tell arduino to stop the toaster (send a few messages just in case)
		# for i in range(3):
		# 	communicate.write_message(arduino, 0, True)
		# 	time.sleep(0.5)
		# break
	counter += 1
	time.sleep(1) 


CV.close_camera(capture) #Close camera



textfile = open("doneness_log.txt", "w")
for element in donesness_store:
    textfile.write(str(element) + "\n")
textfile.close()


