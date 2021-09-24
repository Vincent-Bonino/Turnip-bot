# read data -> tool
# add value -> add
# print stats -> inside read
# plot proba -> proba
# plot data -> inside read
# plot all -> inside read
# change_last_value -> change
# prediction -> sell

def read_data(name):
	import numpy as np
	err = False # error value
	data_file = open("data.txt",'r')
	lines = data_file.readlines()
	data_file.close()

	names = lines[0].rstrip().split(",")
	line_number = 1

	data = ""

	if name=="all":
		data = lines[1]
		for e in lines[2:]:
			data = data+","+(e.rstrip())
		data = data.split(",")
		data = [int(i) for i in data] #from string to int
		for i in range(len(data)):
			if data[i]==-1:
				data[i]=np.inf

	else:
		# Find the number of the line
		for e in names:
			if e==name:
				break
			line_number+=1

		# This name is not in the list
		if line_number>len(names):
			err == True
			data = "No such name in the database"
		else:
			data = lines[line_number].rstrip().split(",")
			data = [int(i) for i in data] #from string to int
			for i in range(len(data)):
				if data[i]==-1:
					data[i]=np.inf

	return [err,data]

def get_all():
	import numpy as np
	data_file = open("data.txt",'r')
	lines = data_file.readlines()
	data_file.close()

	names = lines[0].rstrip().split(",")
	allData = []
	for i in range(1,len(lines)-1):
		aux = lines[i]
		aux = [int(i) for i in aux] #from string to int
		for i in range(len(aux)):
			if aux[i]==-1:
				aux[i]=np.inf
		allData.append(aux)
	return allData

def get_names():
	data_file = open("data.txt",'r')
	lines = data_file.readlines()
	data_file.close()

	names = lines[0].rstrip().split(",")
	return names

def add_value(value,name):
	err = False # error value
	if name!="all":
		data_file = open("data.txt",'r+')
		lines = data_file.readlines()
		data_file.close()

		names = lines[0].rstrip().split(",")
		line_number = 1

		for e in names:
			if e==name:
				break
			line_number+=1

		if line_number>len(names):
			err = True
		else:
			lines[line_number] = lines[line_number][:-1]+",%d\n" %value
			data_file = open("data.txt","w")
			data_file.writelines(lines)
			data_file.close()
	return err

def change_last_value(value,name):
	err = False # error value
	if name!="all":
		data_file = open("data.txt",'r+')
		lines = data_file.readlines()
		data_file.close()

		names = lines[0].rstrip().split(",")
		line_number = 1

		for e in names:
			if e==name:
				break
			line_number+=1

		if line_number>len(names):
			err = True
		else:
			aux = lines[line_number][:-1].rstrip().split(",")
			aux = aux[:-1]
			auxStr = ""

			if len(aux)>0:
				for e in aux:
					auxStr = auxStr + e + ","
			lines[line_number] = auxStr+"%d\n" %value
			data_file = open("data.txt","w")
			data_file.writelines(lines)
			data_file.close()
	return err

def print_stats(v, name):
	import numpy as np
	v = np.array(v)
	mask = np.isfinite(v)
	v = v[mask]
	#print(name+" : %d values\nAverage : %.2f  standard deviation : %.2f" %(len(v),np.average(v),np.std(v)))
	return(name+" : %d values\nAverage : %.2f  standard deviation : %.2f" %(len(v),np.average(v),np.std(v)))


def plot_data(v,name):
	import matplotlib.pyplot as plt
	import numpy as np

	if name=="all":
		plot_all()
	else:
		days=["M","","T","","W","","Th","","F","","S","","Su","","M","","T","","W","","Th","","F","","S","","Su",""]
		plt.clf()
		t = np.arange(0,(len(v))/2,0.5)
		v = np.array(v)
		mask = np.isfinite(v)

		plt.plot(t[mask],v[mask],label=name)
		for i in range(1,1+len(v)//14):
			print("week")
			plt.axvline(x=7*(i),color="black",label="Week n%d" %(i+1))

		plt.xticks(t,days)
		plt.title("Turnips selling price ("+name+")")
		plt.xlabel("Days")
		plt.ylabel("Bells")
		plt.legend()
		plt.grid()
		plt.savefig("data-"+name+".png",transparent=False)

def plot_all():
	import matplotlib.pyplot as plt
	import numpy as np

	data_file = open("data.txt",'r')
	lines = data_file.readlines()
	data_file.close()

	days=["M","","T","","W","","Th","","F","","S","","Su","","M","","T","","W","","Th","","F","","S","","Su",""]

	names = lines[0].rstrip().split(",")
	all_data = []

	plt.clf()
	count = 0
	max_len = 0
	for line in lines[1:-1]:
		data = line.rstrip().split(",")
		data = [int(i) for i in data] #from string to int
		for i in range(len(data)):
			if data[i]==-1:
				data[i]=np.inf
		max_len = max(max_len,len(data))
		all_data = all_data+data

		t = np.arange(0,(len(data))/2,0.5)
		data = np.array(data)
		mask = np.isfinite(data)
		plt.plot(t[mask],data[mask],label=names[count])
		count+=1

	for i in range(1,1+len(all_data)//(4*14)):
		print("week")
		plt.axvline(x=7*(i),color="black",label="Week n%d" %(i+1))

	plt.xticks(t,days[:max_len])
	plt.title("Turnips selling price (all)")
	plt.xlabel("Days")
	plt.ylabel("Bells")
	plt.legend()
	plt.grid()
	plt.savefig("data-all.png",transparent=False)

def plot_proba():
	# Probabilities
	import numpy as np
	import matplotlib.pyplot as plt

	data = read_data("all")
	allData = data[1]
	allData = np.array(allData)
	mask = np.isfinite(allData)
	allData = allData[mask]

	# Set up
	moy = np.average(allData)
	stanDev = np.std(allData)
	pas = 10
	x = np.linspace(moy - 3*stanDev, moy + 3*stanDev, 100)

	# matplotlib histogram
	pas = 10

	plt.clf()
	plt.hist(allData, color = 'springgreen', edgecolor = 'black', bins = int((max(allData)-min(allData))//pas))

	# normal distribution
	#plt.plot(x, 4*stats.norm.pdf(x, moy, stanDev))

	plt.title('Prices histogram')
	plt.xlabel('Prices')
	plt.ylabel('Number of occurence')
	plt.savefig("proba.png",transparent=False)
	return "{} values".format(len(allData))

def impact_of_previous_week(v):
	print("[previous]",v)
	if v[0]==max(v):
		print("[previous] random")
		return [1/8,3/8,3/8,1/8]
	elif v[1]==max(v):
		print("[previous] bigSpike")
		return [5/8,1/8,1/8,1/8]
	elif v[2]==max(v):
		print("[previous] smallSpike")
		return [4/8,2/8,1/8,1/8]
	elif v[3]==max(v):
		print("[previous] decr")
		return [0.25,3/8,1/8,0.25]

def pattern(v,previous_week): # arg for back tracking ?
	import numpy as np
	# monday morning / buy price = x
	# 0.91 < x, random or small 
	# 0.85 <= x < 0.91, random, big, or small
	# 0.80 <= x < 0.85, big or small 
	# 0.60 <= x < 0.80, random or small
	# x < 0.60, usually small

	# Probalility changes are completly arbitrary !!!!

	# Set up
	
	week = len(v)//14;
	curr_week = v[14*week:min(14*(week+1),len(v))]
	limit = 190

	# Use previous week
	if previous_week or week<1:
		random, bigSpike, smallSpike, decr = 0.25, 0.25, 0.25, 0.25
	else:
		random, bigSpike, smallSpike, decr = impact_of_previous_week(pattern(v[:2*week],True)[0])


	# Try to find a pattern

	# Random
	if curr_week[0]>=100:
		bigSpike+=decr/6
		smallSpike+=decr/6
		random+=decr/6
		decr-=decr/2

	# Other rules
	if curr_week[0]<80:
		bigSpike+=decr/6
		smallSpike+=decr/6
		random+=decr/6
		decr-=decr/2


	# Decreasing
	if curr_week[0]<100:
		test_decr = True
		for i in range(1,len(curr_week)):
			test_decr = test_decr and (curr_week[i]<=curr_week[i-1])
		if test_decr:
			decr = 0.3
			bigSpike = 0.3
			smallSpike = 0.3
			random = 0.1
			# Can't be large spike
			if (14-len(curr_week)<5):
				smallSpike+= bigSpike/2
				decr+=bigSpike/2
				bigSpike = 0
			#Can't be small spike
			if (14-len(curr_week)<3):
				decr+=smallSpike
				smallSpike = 0

	# Spike
	count_big = 3
	count_small = 4
	found_higher = False

	# No value before the start of the spike
	if len(curr_week)>=2 and curr_week[1]>curr_week[0] and curr_week[0]>=100:
		count_small-=1
		count_big-=1

	for i in range(1,len(curr_week)):
		if curr_week[i]>curr_week[i-1] or curr_week[i-1]==np.inf:
			# Can't be decreasing
			bigSpike+=decr/2
			smallSpike+=decr/2
			decr=0

			#if there are some missing value
			# ??

			found_higher = True
			count_big-=1
			count_small-=1

			if curr_week[i]>limit:
				bigSpike+=smallSpike*2/3
				smallSpike-=smallSpike*2/3

		elif found_higher and count_big>0 and count_small>0:
			# random, no spike found
			random = 1
			bigSpike = 0
			smallSpike = 0
			decr = 0;
			return [[random, bigSpike, smallSpike, decr], [count_big,count_small,len(curr_week)]]
		elif count_big>0 and count_small>0:
			#currently decreasing, reset
			count_big = 3
			count_small = 4
		else :
			count_big-=1
			count_small-=1

	# Large or small ?
	if 0<=count_big<3 and max(curr_week)>limit:
		print("[spike] big")
		bigSpike+=smallSpike/2
		smallSpike-=smallSpike/2

	elif count_big<0 and max(curr_week)<=limit: # and count_small>=0
		print("[spike] small")
		smallSpike+=bigSpike
		bigSpike = 0

	return [[random, bigSpike, smallSpike, decr], [count_big,count_small,len(curr_week)]]

def advice(args):
	# Define variables
	proba,counters = args[0], args[1]
	str_advice = ""
	count_big = counters[0]
	count_small = counters[1]
	length = counters[2]
	passedSpike = count_big<0 and count_small<0

	print("[advice] proba: ",proba)

	if max(proba)==proba[0]:
		str_advice = "Random pattern (p={})\n".format(proba[0],".3f")
		str_advice += "**You should** : use !proba <price>\n"
	if max(proba)==proba[1] or max(proba)==proba[2]:
		if proba[1]==proba[2]:
			str_advice = "Undetermined spike pattern (p={})\n".format(proba[1],".3f")
			str_advice += "**You should** : wait {} or {} days before selling\n".format(count_big/2,count_small/2,".1f")
		elif proba[1]>proba[2]:
			str_advice = "Large spike pattern (p={})\n".format(proba[1],".3f")
			if passedSpike:
				str_advice += "The best day to sell was {} day(s) ago\n".format(abs(count_big)/2,".1f")
			elif count_big==0:
				str_advice += "You sould : **SELL NOW**"
			else:
				str_advice += "The best day to sell is in {} day(s)\n".format(abs(count_big)/2,".1f")
		else:
			str_advice = "Small spike pattern (p={})\n".format(proba[2],".3f")
			if passedSpike:
				str_advice += "The best day to sell was {} day(s) ago\n".format(abs(count_small)/2,".1f")
			elif count_small==0:
				str_advice += "You sould : **sell now**"
			else:
				str_advice += "The best day to sell is in {} day(s)\n".format(abs(count_small)/2,".1f")
	if max(proba)==proba[3]:
		str_advice = "Decreasing pattern (p={})\n".format(proba[3],".3f")
		str_advice += "You should : **sell now**\n"
	# Return 
	return str_advice

def chance(value):
	import numpy as np

	raw_allData = np.array(read_data("all")[1])
	mask = np.isfinite(raw_allData)
	allData = raw_allData[mask]

	proba = 0
	for i in range(value,int(max(allData))+1):
		proba+= np.count_nonzero(allData == i)

	proba = proba / len(allData)

	nb_of_player = 4
	remaining_half_days =  max(0,12 - (len(raw_allData)//4)%14)
	print(proba,len(allData),remaining_half_days)

	return 1-((1-proba)**(nb_of_player*remaining_half_days))