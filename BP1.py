import numpy as np 

# this approach is the same as an incident check vote.

def message_from_check_to_qubit(physical_error_rate, check_is_on):
	
	# We consider that the eleven other qubits have an error with probability physical_error_rate.

	q = 1/2*(1-(1-2*physical_error_rate)**11)

	if check_is_on==0: error_belief = q
	if check_is_on==1: error_belief = 1-q

	return error_belief


def belief(physical_error_rate, error_belief_1, error_belief_2, error_belief_3, error_belief_4):

	unnormalised_error_belief = physical_error_rate*error_belief_1*error_belief_2*error_belief_3*error_belief_4
	unnormalised_no_error_belief = (1-physical_error_rate)*(1-error_belief_1)*(1-error_belief_2)*(1-error_belief_3)*(1-error_belief_4)

	normalisation_constant = unnormalised_error_belief + unnormalised_no_error_belief
	error_belief = unnormalised_error_belief / normalisation_constant

	return error_belief


def compute_final_belief(physical_error_rate,incident_syndrome_weight):

	error_belief_list = []

	for i in range(incident_syndrome_weight):
		error_belief_list.append(message_from_check_to_qubit(physical_error_rate,1))

	for i in range(4-incident_syndrome_weight):
		error_belief_list.append(message_from_check_to_qubit(physical_error_rate,0))

	error_belief = belief(physical_error_rate,error_belief_list[0],error_belief_list[1],error_belief_list[2],error_belief_list[3])

	return error_belief


for w in range(5):
	print(w,compute_final_belief(0.1,w))









