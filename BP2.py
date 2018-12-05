import numpy as np 
import matplotlib.pyplot as plt


def message_from_check_to_qubit(physical_error_rate, check_is_on, belief_list):
	
	# belief_list has length 11 (or 10) and corresponds to the error beliefs (for themselves) of the eleven other qubits.

	q = 1
	for b in belief_list:
		q = q*(1-2*b)
	q = 1/2*(1-q)

	error_belief = 0
	if check_is_on==0: error_belief = q
	if check_is_on==1: error_belief = 1-q

	return error_belief

# belief_list = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,]
# print(message_from_check_to_qubit(0.01, 1, belief_list))

def message_from_qubit_to_check(physical_error_rate, belief_list):

	# belief_list has length 3 and corresponds to the error beliefs (for this qubit) coming from the three input checks.

	unnormalised_error_belief = physical_error_rate
	unnormalised_no_error_belief = 1-physical_error_rate

	for b in belief_list:
		unnormalised_error_belief = unnormalised_error_belief*b
		unnormalised_no_error_belief = unnormalised_no_error_belief*(1-b)

	normalisation_constant = unnormalised_error_belief + unnormalised_no_error_belief
	error_belief = unnormalised_error_belief / normalisation_constant

	# print(unnormalised_error_belief,unnormalised_no_error_belief)

	return error_belief

# print(message_from_qubit_to_check(0.01,[0.9,0.9,0.1]))



def compute_level_2_qubits_beliefs(physical_error_rate,syndrome):

	level_2_qubits = np.load('data/level_2_qubits.npy')
	qubits_children = np.load('data/qubits_children.npy')

	level_4_belief_list = []
	for i in range(11):
		level_4_belief_list.append(physical_error_rate) 

	error_belief = [0] # we don't compute the belief of the central qubit (indexed 0). Hence this initialisation.
	for q in level_2_qubits:
		belief_list = []
		for c in qubits_children[q]:
			belief_list.append(message_from_check_to_qubit(physical_error_rate, c in syndrome, level_4_belief_list))
			# if message_from_check_to_qubit(physical_error_rate, c in syndrome, level_4_belief_list) > 0.2: print(c)
		error_belief.append(message_from_qubit_to_check(physical_error_rate, belief_list))
		# m = message_from_qubit_to_check(physical_error_rate, belief_list)
		# if m > 0.0001: print(qubits_children[q],m)
	# print(error_belief)

	return error_belief

# physical_error_rate = 0.05
# s = str(int(100*physical_error_rate))
# train_size = 100000
# with_error = np.load('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# without_error = np.load('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# syndrome = without_error[0]
# print(syndrome)
# compute_level_2_qubits_beliefs(physical_error_rate,syndrome)



def compute_central_qubit_belief(physical_error_rate,syndrome):

	belief_list = compute_level_2_qubits_beliefs(physical_error_rate,syndrome)

	level_1_checks = np.load('data/level_1_checks.npy')
	checks_children = np.load('data/checks_children.npy')

	very_new_belief_list = []
	for c in level_1_checks:
		new_belief_list = []
		for q in checks_children[c]:
			new_belief_list.append(belief_list[q])
		very_new_belief_list.append(message_from_check_to_qubit(physical_error_rate, c in syndrome, new_belief_list))

	return message_from_qubit_to_check(physical_error_rate, very_new_belief_list)

# physical_error_rate = 0.05
# s = str(int(100*physical_error_rate))
# train_size = 100000
# with_error = np.load('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# without_error = np.load('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# syndrome = without_error[0]
# print(syndrome)
# print(compute_central_qubit_belief(physical_error_rate,syndrome))

# for i in range(10):
# 	syndrome = with_error[i]
# 	print(compute_central_qubit_belief(physical_error_rate,syndrome))

# print('\n')

# for i in range(10):
# 	syndrome = without_error[i]
# 	print(compute_central_qubit_belief(physical_error_rate,syndrome))


def write_central_qubit_beliefs(physical_error_rate,syndrome_set,with_error,train_size):

	print('physical error rate',physical_error_rate)
	print('number of syndromes',len(syndrome_set))

	filename = 'data/central_qubit_beliefs_'
	if with_error==0: filename = filename + 'without_error_'; print('without error')
	elif with_error==1: filename = filename + 'with_error_'; print('with error')
	else: 'ERROR (problem)'
	filename = filename + 'physical_error_rate_' + str(int(100*physical_error_rate))
	filename = filename + '_size_' + str(train_size) + '.npy'

	beliefs = []
	counter = 0
	for syndrome in syndrome_set:
		beliefs.append(compute_central_qubit_belief(physical_error_rate,syndrome))
		if counter%1000==0: print(counter)
		counter+=1

	np.save(filename,beliefs)


# physical_error_rate = 0.05
# s = str(int(100*physical_error_rate))
# train_size = 10000
# with_error = np.load('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# without_error = np.load('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# write_central_qubit_beliefs(physical_error_rate,with_error,1,train_size)
# write_central_qubit_beliefs(physical_error_rate,without_error,0,train_size)



def plot_beliefs(physical_error_rate,train_size):

	central_qubit_beliefs_with_error = np.load('data/central_qubit_beliefs_with_error_physical_error_rate_'+str(int(100*physical_error_rate))+'_size_'+str(train_size)+'.npy')
	central_qubit_beliefs_without_error = np.load('data/central_qubit_beliefs_without_error_physical_error_rate_'+str(int(100*physical_error_rate))+'_size_'+str(train_size)+'.npy')
	plt.hist([central_qubit_beliefs_with_error,central_qubit_beliefs_without_error])

	plt.title('$p_{physical}$ = '+str(int(100*physical_error_rate))+'%.       '+str(train_size)+' trials.')
	plt.xlabel('central qubit belief')
	plt.ylabel('counts')

	plt.savefig('plots/BP_plots/central_qubit_beliefs_physical_error_rate_'+str(int(100*physical_error_rate))+'_size_'+str(train_size)+'.png')
	plt.show()


physical_error_rate = 0.01
train_size = 10000

plot_beliefs(physical_error_rate,train_size)



















