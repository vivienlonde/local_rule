import numpy as np 
import matplotlib.pyplot as plt 

def compute_incident_syndrome_weight(syndrome):
	incident_syndrome_weight = 0
	for c in syndrome:
		if c==0 or c==1 or c==2 or c==3: incident_syndrome_weight+=1
	return incident_syndrome_weight


def plot_histogram(physical_error_rate,train_size,syndrome_set_1,syndrome_set_2):

	incident_syndrome_weights_1 = np.zeros(5)
	incident_syndrome_weights_2 = np.zeros(5)

	for syndrome in syndrome_set_1:
		incident_syndrome_weight = compute_incident_syndrome_weight(syndrome)
		incident_syndrome_weights_1[incident_syndrome_weight]+=1
	normalised_incident_syndrome_weights_1 = incident_syndrome_weights_1/len(syndrome_set_1)

	for syndrome in syndrome_set_2:
		incident_syndrome_weight = compute_incident_syndrome_weight(syndrome)
		incident_syndrome_weights_2[incident_syndrome_weight]+=1
	normalised_incident_syndrome_weights_2 = incident_syndrome_weights_2/len(syndrome_set_2)

	# plt.plot(normalised_incident_syndrome_weights_1,'b.')
	# plt.plot(normalised_incident_syndrome_weights_2,'r.')
	plt.plot(incident_syndrome_weights_1,'b.', label= 'error on central qubit')
	plt.plot(incident_syndrome_weights_2,'r.', label= 'no error on central qubit')

	plt.title('$p_{physical}$ = '+str(int(100*physical_error_rate))+'%.       '+str(train_size)+' trials.')
	plt.xlabel('number of unsatisfied incident checks')
	plt.ylabel('counts')
	plt.legend()

	plt.savefig('data/incident_checks_plots/number_of_unsatisfied_incident_checks_error_rate_'+s+'_size_'+str(train_size)+'.png')
	plt.show()





def compute_classification_frequencies(syndrome_set_with_error,syndrome_set_without_error):

	nb_true_positive = 0
	nb_true_negative = 0

	nb_false_positive = 0
	nb_false_negative = 0

	nb_trials = len(syndrome_set_with_error)+len(syndrome_set_without_error)


	for syndrome in syndrome_set_with_error:
		w = compute_incident_syndrome_weight(syndrome)
		if w==0 or w==1 or w==2: nb_true_negative+=1
		# if w==3: nb_true_negative+=0.5; nb_true_positive+=0.5
		if w==4 or w==3: nb_true_positive+=1

	for syndrome in syndrome_set_without_error:
		w = compute_incident_syndrome_weight(syndrome)
		if w==0 or w==1 or w==2: nb_false_negative+=1
		# if w==3: nb_false_negative+=0.5; nb_false_positive+=0.5
		if w==4 or w==3: nb_false_positive+=1

	true_positive_frequency = nb_true_positive/nb_trials
	true_negative_frequency = nb_true_negative/nb_trials
	false_positive_frequency = nb_false_positive/nb_trials
	false_negative_frequency = nb_false_negative/nb_trials

	return true_positive_frequency, true_negative_frequency, false_positive_frequency, false_negative_frequency




physical_error_rate = 0.05
train_size = 10000
s = str(int(100*physical_error_rate))

with_error = np.load('data/with_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')
without_error = np.load('data/without_error_train_set_error_rate_'+s+'_size_'+str(train_size)+'.npy')

# true_positive_frequency, true_negative_frequency, false_positive_frequency, false_negative_frequency= compute_classification_frequencies(with_error,without_error)

# print('true positive frequency:',true_positive_frequency)
# print('true negative frequency:',true_negative_frequency)
# print('false positive frequency:',false_positive_frequency)
# print('false negative frequency:',false_negative_frequency)

plot_histogram(physical_error_rate,train_size,with_error,without_error)




