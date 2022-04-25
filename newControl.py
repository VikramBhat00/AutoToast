import serial
import time



import communicate
import CV
import kalman_filter
import models
import ML



#Connect to arduino
arduino = serial.Serial(port = '/dev/cu.usbmodem101', baudrate=115200, timeout = 0.1)


kalman_filter.initialize_filter()
capture = CV.init_camera() #open camera and adjust to light

counter = 0
donesness_store = []


#Get First Image
model = ML.get_model_from_image(capture)





#model = models.white_bread_model_1 #Choose based on ML model

while(1):

	done_num = CV.get_doneness(capture)
	print("Done num: ", done_num)
	donesness_store.append(done_num)

	state_est, state_var = kalman_filter.do_kalman_filter_step(donesness_store, counter, model)


	print("KALMAN STATE EST: ", state_est)
	print()
	if state_est >= 0.99: #Reached done state
		for i in range(3):
			communicate.write_message(arduino, 0, True)
			time.sleep(0.5)
		break

	counter += 1
	time.sleep(1) 


CV.close_camera(capture) #Close camera



textfile = open("doneness_log.txt", "w")
for element in donesness_store:
    textfile.write(str(element) + "\n")
textfile.close()
