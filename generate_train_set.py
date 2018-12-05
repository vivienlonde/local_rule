import numpy as np


def write_four_depth_levels():
	Hx_as_checks = np.loadtxt('data/Hx_as_checks_space_separated.txt', dtype=int)
	print(Hx_as_checks[0])

	Hx_as_qubits = np.loadtxt('data/Hx_as_qubits_space_separated.txt', dtype=int)
	print(Hx_as_qubits[0])

	depth_levels = [[0]]

	def not_in(new_node,depth_levels):
		l_max = len(depth_levels)
		for backwards_level in range(l_max):
			# print(backwards_level)
			if backwards_level%2==1:
				# print(depth_levels[l_max-1-backwards_level])
				if new_node in depth_levels[l_max-1-backwards_level]:
					return 0
		return 1

	# not_in('ba',['a','b','c'])

	def add_one_depth_level(previous_level_type):

		new_level = []

		previous_level = depth_levels[-1]
		# print(previous_level)

		H = []
		if previous_level_type=='qubits':
			H = Hx_as_qubits
		elif previous_level_type=='checks':
			H = Hx_as_checks
		else:
			print('ERROR')

		for node in previous_level:
			neighbours = H[node]
			for new_node in neighbours:
				if new_node not in new_level and not_in(new_node,depth_levels):
					new_level.append(new_node)

		depth_levels.append(new_level)


	print(depth_levels[-1])
	add_one_depth_level('qubits')
	print(depth_levels[-1])
	add_one_depth_level('checks')
	print(depth_levels[-1])
	add_one_depth_level('qubits')
	add_one_depth_level('checks')
	# add_one_depth_level('qubits')
	# add_one_depth_level('checks')

	for i, level in enumerate(depth_levels):
		print(i, len(level))

	np.save('data/four_depth_levels.npy',depth_levels)

# write_four_depth_levels()


def compute_qubits_and_checks():
	
	four_depth_levels = np.load('data/four_depth_levels.npy')

	qubits = []
	checks = []
	level_index = 0
	for level in four_depth_levels:
		if level_index%2==0: qubits += level
		else: checks += level
		level_index += 1

	return qubits, checks


def inv_qubits(qubits,qub):
	subset_index = 0
	for q in qubits:
		if q==qub : return subset_index
		subset_index += 1
	# print('not in the subset')
	return -1	

def inv_checks(checks,che):
	subset_index = 0
	for c in checks:
		if c==che : return subset_index
		subset_index += 1
	# print('not in the subset')
	return -1

def write_subset_parity_check(side,as_smthg):
	if side=='X' and as_smthg=='as_qubits':
		H = np.loadtxt('data/Hx_as_qubits_space_separated.txt', dtype=int)
		I = qubits
		J = checks
		inv = inv_checks
		filename = 'data/subset_Hx_as_qubits.npy'

	elif side=='X' and as_smthg=='as_checks':
		H = np.loadtxt('data/Hx_as_checks_space_separated.txt', dtype=int)
		I = checks
		J = qubits
		inv = inv_qubits
		filename = 'data/subset_Hx_as_checks.npy'

	elif side=='Z' and as_smthg=='as_qubits':
		H = np.loadtxt('data/Hz_as_qubits_space_separated.txt', dtype=int)
		I = qubits
		J = checks
		inv = inv_checks
		filename = 'data/subset_Hz_as_qubits.npy'

	elif side=='Z' and as_smthg=='as_checks':
		H = np.loadtxt('data/Hz_as_checks_space_separated.txt', dtype=int)
		I = checks
		J = qubits
		inv = inv_qubits
		filename = 'data/subset_Hz_as_checks.npy'

	else: print('ERROR')


	subset_H = []

	for row in H[I]:
		subset_row =[]
		for j in row:
			subset_j = inv(J,j)
			if subset_j!=-1 : subset_row.append(subset_j)
		subset_H.append(subset_row)

	np.save(filename,subset_H)

# write_subset_parity_check('X','as_checks')



def weight(binary_vector):
	result = 0
	for b in binary_vector:
		if b==1: result += 1
	return result

def compute_physical_error(physical_error_rate,nb_qubits):

	one_hot_physical_error = np.random.binomial(1,physical_error_rate,nb_qubits)
	physical_error = []

	qubit_index = 0
	for q in one_hot_physical_error:
		if q==1: physical_error.append(qubit_index)
		qubit_index += 1

	return physical_error


def compute_partial_syndrome(physical_error,subset_H):

	syndrome = []
	# print(subset_H)

	check_index = 0
	for row in subset_H:
		check = 0
		for qubit in row:
			# print(qubit)
			if qubit in physical_error: check = (check+1)%2
		if check==1: syndrome.append(check_index)
		check_index += 1

	return syndrome 




# qubits, checks = compute_qubits_and_checks()
# nb_qubits = len(qubits)
# nb_checks = len(checks)
# print(nb_qubits,'qubits;', nb_checks, 'checks')

# physical_error_rate = 0.05
# print('physical error rate: ',physical_error_rate)
# physical_error = compute_physical_error(physical_error_rate,nb_qubits)

# subset_H = np.load('data/subset_Hx_as_checks.npy')
# syndrome = compute_partial_syndrome(physical_error,subset_H)

# print(len(physical_error), 'physical errors out of 1038 qubits')
# print(len(syndrome), 'checks unsatisfied out of 116 checks')

# print(physical_error)
# print(syndrome)

def write_train_set(physical_error_rate,train_size):

	print('physical error rate:',physical_error_rate)
	print('train_size:',train_size)
	qubits, checks = compute_qubits_and_checks()
	nb_qubits = len(qubits)
	nb_checks = len(checks)
	print(nb_qubits,'qubits;', nb_checks, 'checks')

	subset_H = np.load('data/subset_Hx_as_checks.npy')

	train_set = []
	for t in range(train_size):
		physical_error = compute_physical_error(physical_error_rate,nb_qubits)
		syndrome = compute_partial_syndrome(physical_error,subset_H)
		train_set.append([physical_error,syndrome])
		if t%1000==0: print(int(t/1000),'over',int(train_size/1000))

	s = str(int(100*physical_error_rate))
	np.save('data/train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy',train_set)


write_train_set(0.06,10000)


# train_set = np.load('data/training_set_error_rate_5.npy')

# physical_error, syndrome = train_set[0]
# print(physical_error)
# print(syndrome)









