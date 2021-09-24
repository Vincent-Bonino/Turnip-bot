# ======================
# Early python script drafted, rewritten in tools.py
# ======================


import matplotlib.pyplot as plt
import numpy as np
#import scipy.stats as stats
import math


bold = "\033[1m"
reset = "\033[0m"
sure = 1
veryLikely = 0.90
likely = 0.75
average = 0.50
unlikely = 0.25
veryUnlikely = 0.10
no = 0
limit = 180

# Usefull functions

def moyenne(v):
	res = 0
	for e in v:
		res+=e
	return res/len(v)


def analyse(v):
	'''
	Depending on the previous week and the current one,
	calculate probabilities for each pattern.
	1. Random 2. big spike 3. small spike 4. decreasing

	Input : array with all your prices, from the oldest day to now
	Output : array of the probability of each of the four patterns
	>>> analyse([92,89,91,85,81,98,133,250,142,107,82])
	[veryUnlikely,veryLikely,no,no]
	'''

	# Define the variables
	patterns = [unlikely,unlikely,unlikely,unlikely]
	random, bigSpike, smallSpike, decr = patterns[0],patterns[1],patterns[2],patterns[3]
	spike = False
	passedSpike = False

	week = len(v)//14;
	curr_week = v[14*week:min(14*(week+1),len(v))]


	# Use previous week
	if week>0:
		patterns = analyse(v[:2*week])


	# Try to find a pattern
	# Decreasing
	if curr_week[0]<100:
		test_decr = True
		for i in range(1,len(curr_week)):
			test_decr = test_decr and (curr_week[i]<=curr_week[i-1])
		if test_decr:
			decr*= sure
			random*=veryUnlikely
			# Can't be large spike
			if (14-len(curr_week)<5):
				bigSpike = no
			if (14-len(curr_week)<3):
				smallSpike = no

	# Spike
	count_big = 2
	count_small = 3

	for i in range(1,len(curr_week)):
		if curr_week[i]>curr_week[i-1]:
			count_big-=1
			count_small-=1
			if curr_week[i]>limit:
				bigSpike*=veryLikely
				smallSpike*=veryUnlikely
		else:
			count_big = 2
			count_small = 3

	# Large
	if count_big==1:
		bigSpike*=likely
	elif count_big==0:
		spike = True
		bigSpike*=veryLikely
	elif count_big<0:
		spike = True
		passedSpike = True
		bigSpike*=veryLikely        

	# Small
	if count_small<2:
		smallSpike*=likely
	elif count_small==0:
		spike = True
		smallSpike*=veryLikely
	elif count_small<0:
		spike = True
		passedSpike = True
		smallSpike*=veryLikely

	# Random
	if curr_week[0]>=100:
		decr*=veryUnlikely
		random*=sure

	# Other rules
	if curr_week[0]<80:
		decr*=veryUnlikely


	# Print pattern (and prediction)
	if np.max(patterns)==random:
		print("Random pattern (%.3f)" %random)
		print("You should : look at maths\n")
	if np.max(patterns)==bigSpike or np.max(patterns)==smallSpike:
		if bigSpike==smallSpike:
			print("Undetermined spike pattern (%.3f)" %smallSpike)
			print("You should : wait %.1f or %.1f days before selling\n" %(count_big/2,count_small/2))
		elif bigSpike>smallSpike:
			print("Large spike pattern (%.3f)" %bigSpike)
			if passedSpike:
				print("The best day to sell was %.1f day(s) ago\n" %abs(count_big)/2)
			else:
				print("The best day to sell is in %.1f day(s)\n" %abs(count_big)/2)
		else:
			print("Small spike pattern (%.3f)" %smallSpike)
			if passedSpike:
				print("The best day to sell was %.1f day(s) ago\n" %(count_small/2))
			else:
				print("The best day to sell is in %.1f day(s)\n" %(count_small/2))
	if np.max(patterns)==decr:
		print("Decreasing pattern (%.3f)" %decr)
		print("You should : sell now\n")
	# Return 
	return patterns

def show_data():
	# Show the data

	plt.plot(range(1,len(X)+1),X,label="X")
	plt.plot(range(1,len(XX)+1),XX,label="XX")
	plt.plot(range(1,len(Vincent)+1),Vincent,label="Vincent")
	plt.plot(range(1,len(XXX)+1),XXX,label="XXX")
	for i in range(0,l_max//7):
		plt.vlines(7*(i+1),min(allOfUS),max(allOfUs),label="Semaine %d" %(i+1))

	#plt.xticks(x, jours)

	plt.title("Prix de vente des navets")
	plt.xlabel("Jours")
	plt.ylabel("Clochettes")
	plt.legend()

	print("X :     Moyenne : %.2f  ecart type : %.2f" %(tab_moys[0],tab_ecartTypes[0]))
	print("XX :     Moyenne : %.2f  ecart type : %.2f" %(tab_moys[1],tab_ecartTypes[1]))
	print("Vincent :  Moyenne : %.2f  ecart type : %.2f" %(tab_moys[2],tab_ecartTypes[2]))
	print("XXX :     Moyenne : %.2f  ecart type : %.2f" %(tab_moys[3],tab_ecartTypes[3]))
	print("\nGeneral :  Moyenne : %.2f  ecart type : %.2f\n" %(moy,ecartType))
	plt.show()

def show_probabilities():
	# Probabilities

	# Set up
	x = np.linspace(moy - 3*ecartType, moy + 3*ecartType, 100)

	# matplotlib histogram
	pas = 10
	plt.hist(allData, color = 'springgreen', edgecolor = 'black', bins = (max(allData)-min(allData))//pas)

	# normal distribution
	#plt.plot(x, 4*stats.norm.pdf(x, moy, ecartType))

	plt.title('Histogramme des prix')
	plt.xlabel('Prix')
	plt.ylabel('Nombre')
	plt.show()

def show_analysis():
	# Analyse et prediction

	print(bold+"Analyse X :"+reset)
	analyse(X)

	print(bold+"Analyse XX :"+reset)
	analyse(XX)

	print(bold+"Analyse Vincent :"+reset)
	analyse(Vincent)

	print(bold+"Analyse XXX :"+reset)
	analyse(XXX)


# Data
Autres = [95]
X = [81,120,200,408]
XX = [59,131,105,148]
Vincent = [105,95,133,101]
XXX = [65,55,120,104]

# Probably useful at sometime
allOfUs = X+XX+Vincent+XXX
allData = X+XX+Vincent+XXX+Autres
l_max = max(len(X),len(XX),len(Vincent),len(XXX))
jours = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche",""]


tab_moys = [moyenne(X), moyenne(XX), moyenne(Vincent), moyenne(XXX)]
tab_ecartTypes = [np.std(X), np.std(XX), np.std(Vincent), np.std(XXX)]

moy = moyenne(tab_moys)
ecartType = moyenne(tab_ecartTypes)


# Execution

show_analysis()
show_data()