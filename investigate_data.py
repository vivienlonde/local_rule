import numpy as np 
import matplotlib.pyplot as plt

# physical_error_rate = 0.01
# train_size = 100000
# s = str(int(100*physical_error_rate))
# train_set = np.load('data/train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')

# physical_error, syndrome = train_set[0]
# print(len(physical_error))
# print(len(syndrome))

def write_with_and_without_error_train_set(physical_error_rate,train_size):

	s = str(int(100*physical_error_rate))
	train_set = np.load('data/train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')

	with_error = []
	without_error = []

	for physical_error, syndrome in train_set:
		if len(physical_error)!=0 and physical_error[0]==0:
			with_error.append(syndrome)
		else: 
			without_error.append(syndrome)

	print(len(with_error))
	print(len(without_error))

	np.save('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy',with_error)
	np.save('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy',without_error)



def plot_histogram(syndrome_set_1,syndrome_set_2):

	syndrome_counts_1 = np.zeros(116)
	syndrome_counts_2 = np.zeros(116)

	for syndrome in syndrome_set_1:
		for c in syndrome:
			syndrome_counts_1[c] += 1
	normalised_syndrome_counts_1 = syndrome_counts_1/len(syndrome_set_1)

	for syndrome in syndrome_set_2:
		for c in syndrome:
			syndrome_counts_2[c] += 1
	normalised_syndrome_counts_2 = syndrome_counts_2/len(syndrome_set_2)

	plt.plot(normalised_syndrome_counts_1,'b.')
	plt.plot(normalised_syndrome_counts_2,'r.')
	plt.show()




def compute_syndrome_density(physical_error_rate,train_size):

	with_error = np.load('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
	without_error = np.load('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')

	nb_unsatisfied_checks = 0

	for syndrome in with_error:
		nb_unsatisfied_checks += len(syndrome)

	for syndrome in without_error:
		nb_unsatisfied_checks += len(syndrome)

	nb_checks = 116*train_size

	return nb_unsatisfied_checks/nb_checks

# print(compute_syndrome_density(physical_error_rate,train_size))

def probability_unsatisfied_check(p,d):

	return 1/2*(1-(1-2*p)**d)

def frange(start, stop, step):
	result = []
	i = start
	while i <= stop:
		result.append(i)
		i += step
	return result

def plot_probability_unsatisfied_check():

	physical_error_rates = frange(0,1,0.001)
	for d in range(20):
		probabilities_unsatisfied_check = np.array([probability_unsatisfied_check(p,d) for p in physical_error_rates])
		plt.plot(physical_error_rates,probabilities_unsatisfied_check)
	plt.show()

# plot_probability_unsatisfied_check()


# physical_error_rate = 0.01
# s = str(int(100*physical_error_rate))
# train_size = 100000

# write_with_and_without_error_train_set(physical_error_rate,train_size)

# with_error = np.load('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# without_error = np.load('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')

# plot_histogram(with_error,without_error)


# train_set = np.load('data/train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
# print(train_set[0])


def write_level_1_checks():
	level_1_checks = [0,1,2,3]
	np.save('data/level_1_checks.npy',level_1_checks)

# write_level_1_checks()

def write_level_2_qubits():

	subset_Hx_as_checks = np.load('data/subset_Hx_as_checks.npy')
	
	level_0_qubits = [0]
	level_1_checks = [0,1,2,3]

	level_2_qubits = []
	for check in level_1_checks:
		incident_qubits = subset_Hx_as_checks[check]
		for q in incident_qubits:
			if q not in level_0_qubits: level_2_qubits.append(q)

	print(len(level_2_qubits))

	np.save('data/level_2_qubits.npy',level_2_qubits)

# write_level_2_qubits()

def write_children():

	subset_Hx_as_qubits = np.load('data/subset_Hx_as_qubits.npy')
	subset_Hx_as_checks = np.load('data/subset_Hx_as_checks.npy')

	nb_qubits = len(subset_Hx_as_qubits)
	nb_checks = len(subset_Hx_as_checks)

	level_0_qubits = np.array([0])
	level_1_checks = np.load('data/level_1_checks.npy')
	level_2_qubits = np.load('data/level_2_qubits.npy')

	qubits_children = []
	checks_children = []

	for q in range(nb_qubits):
		if q in level_0_qubits:
			qubits_children.append(subset_Hx_as_qubits[q])
		elif q in level_2_qubits:
			children = []
			for c in subset_Hx_as_qubits[q]:
				if c not in level_1_checks:
					children.append(c)
			qubits_children.append(children)
		else:
			qubits_children.append([])

	for c in range(nb_checks):
		if c in level_1_checks:
			children = []
			for q in subset_Hx_as_checks[c]:
				if q not in level_0_qubits:
					children.append(q)
			checks_children.append(children)
		else:
			children = []
			for q in subset_Hx_as_checks[c]:
				if q not in level_2_qubits:
					children.append(q)
			checks_children.append(children)

	np.save('data/qubits_children.npy',qubits_children)
	np.save('data/checks_children.npy',checks_children)

# write_children()

# qubits_children = np.load('data/qubits_children.npy')
# for children in qubits_children:
# 	print(children)

# checks_children = np.load('data/checks_children.npy')
# counter=0
# for children in checks_children:
# 	if len(children)==10: counter+=1
# print(counter)


def write_parents():

	qubits_children = np.load('data/qubits_children.npy')
	checks_children = np.load('data/checks_children.npy')

	subset_Hx_as_qubits = np.load('data/subset_Hx_as_qubits.npy')
	subset_Hx_as_checks = np.load('data/subset_Hx_as_checks.npy')

	nb_qubits = len(subset_Hx_as_qubits)
	nb_checks = len(subset_Hx_as_checks)

	print(nb_qubits)
	print(nb_checks)

	qubits_parent = ['the root has no parent']
	checks_parent = []

	for q in range(nb_qubits):
		children = qubits_children[q]
		for c in subset_Hx_as_qubits[q]:
			if c not in children:
				qubits_parent.append(c)
				break

	for c in range(nb_checks):
		children = checks_children[c]
		for q in subset_Hx_as_checks[c]:
			if q not in children: checks_parent.append(q)

	np.save('data/qubits_parent.npy', qubits_parent)
	np.save('data/checks_parent.npy', checks_parent)
	
write_parents()

# physical_error_rate = 0.06
# s = str(int(100*physical_error_rate))
# train_size = 10000
# write_with_and_without_error_train_set(physical_error_rate,train_size)









