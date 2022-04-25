



#Toast State in percentage Done
toastState = 0
#How certain we are
toastVariance = 1





#Initialize variables
def initialize_filter():
	global toastState, toastVariance
	toastState = 0
	toastVariance = 0.1

#Gets total error between 2 arrays of same length
def get_error(l1, l2):
	totalE = 0
	for i in range(len(l1)):

		e = (l1[i] - l2[i]) ** 2
		totalE += e

	return totalE

def fitting_function(toast_doneness_arr, model):
	offset = 0
	num_data = len(toast_doneness_arr)

	errorArr = []

	if num_data >= len(model):
		return -1

	while num_data + offset < len(model):

		model_subset = model[offset:num_data+offset]

		err = get_error(toast_doneness_arr, model_subset)
		offset += 1
		errorArr.append(err)

	#Get offset with smallest err
	minErr = min(errorArr)
	minErrOffset = errorArr.index(minErr)

	return minErrOffset





def do_kalman_filter_step(toast_doneness_arr, num_iterations, model):

	global toastState, toastVariance

	#Measurements - get estimates for toast state based on the 2 different measurements


	#Feature matching with model

	offset = fitting_function(toast_doneness_arr, model)
	if offset == -1:
		currentIdxEst = len(model)
	else:
		currentIdxEst = offset+len(toast_doneness_arr)

	featureMeasure = currentIdxEst/len(model) #Estimate of where it is within model
	featureMeasureVar = (1-0.9)

	#Just using time
	timeMeasure = num_iterations/len(model)
	timeMeasureVar = (1-0.3)


	#Fuse the two
	measuredStateEstimate = featureMeasure * featureMeasureVar + timeMeasure * timeMeasureVar / (featureMeasureVar + timeMeasureVar)
	measuredStateVar = (featureMeasureVar + timeMeasureVar) / 2 #Average of the 2 


	#State Update - Figure out current toast done-ness based on measurement and last state
	Kalman_gain = toastVariance/(toastVariance + measuredStateVar)
	toastState = toastState + Kalman_gain * (measuredStateEstimate - toastState) 
	toastVariance = (1 - Kalman_gain) * toastVariance

	#Prediction - Use feature-matched position to predict next state

	toastState = (currentIdxEst + 1) / len(model) #Move 1 index forward
	#Keep toast variance the same (for now)
	return (toastState, toastVariance)



