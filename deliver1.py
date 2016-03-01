# from scipy import misc
# lena = misc.lena()
# import matplotlib.pyplot as plt
# plt.imshow(lena,cmap=clt.cm.gray)



import glob
import unicodedata
from math import log2
import random

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def clean_text(txt):
	clean = txt.lower()
	clean = clean.replace('.',' ')
	clean = clean.replace(':',' ')
	clean = clean.replace(',',' ')
	clean = clean.replace(';',' ')
	clean = clean.replace('\'','')
	clean = clean.replace('\n',' ')
	clean = clean.replace('\"',' ')
	clean = clean.replace('!',' ')
	clean = clean.replace('¡',' ')
	clean = clean.replace('?',' ')
	clean = clean.replace('¿',' ')
	clean = clean.replace('&',' ')
	clean = clean.replace('-',' ')
	clean = clean.replace('_',' ')
	clean = clean.replace(']',' ')
	clean = clean.replace('[',' ')
	clean = clean.replace('(',' ')
	clean = clean.replace(')',' ')
	clean = clean.replace('·','')
	clean = ' '.join(clean.split())
	clean = ''.join([i for i in clean if not i.isdigit()])
	return remove_accents(clean)

def entropy(txt):
	# for x in set(txt):
	# 	print (chr(x),end=' ')

	# print ('')	

	countLeters = {};
	for x in set(txt):
		countLeters[x] = 0.0

	total = 0.0
	for x in txt:
		total += 1
		countLeters[x] += 1

	ent = 0.0;
	for x in countLeters:
		ent += (countLeters[x]/total) * log2(1.0/(countLeters[x]/total))

	return ent

def joint_entropy(txt):
	# for x in set(txt):
	# 	print (chr(x),end=' ')

	# print('')

	countLeters = {};
	for x in set(txt):
		countLeters[x] = {}
		for y in set(txt):
			countLeters[x][y] = 0.0

	total = 0.0
	for x in range(1,len(txt)):
		total += 1.0
		last = txt[x-1]
		current = txt[x]
		countLeters[last][current] += 1.0

	ent = 0.0
	for x in countLeters:
		for y in countLeters:
			if countLeters[x][y] != 0.0:
				ent += (countLeters[x][y]/total) * log2(1.0/(countLeters[x][y]/total))

	return ent/2


def conditional_entropy1(txt,ltr):
	countLeters = {};
	for x in set(txt):
		countLeters[x] = 0

	total = 0.0
	for x in range(1,len(txt)):
		last = txt[x-1]
		current = txt[x]
		if chr(last) == ltr:
			total += 1.0
			countLeters[current] += 1.0

	ent = 0.0
	for x in countLeters:
		if countLeters[x] != 0.0:
			ent += (countLeters[x]/total) * log2(1.0/(countLeters[x]/total))

	return ent

def conditional_entropy(txt):
	# for x in set(txt):
	# 	print (chr(x),end=' ')

	# print('')

	countLeters = {};
	total = 0.0
	totalCond = {};
	for x in set(txt):
		countLeters[x] = {}
		totalCond[x] = 0
		for y in set(txt):
			countLeters[x][y] = 0.0

	for x in range(1,len(txt)):
		total += 1.0
		last = txt[x-1]
		current = txt[x]
		countLeters[last][current] += 1.0
		totalCond[last] += 1

	ent = 0.0
	for x in countLeters:
		for y in countLeters:
			if countLeters[x][y] != 0.0:
				ent += (countLeters[x][y]/total) * log2(1.0/(countLeters[x][y]/totalCond[x]))

	return ent

def weighted_choice(choices, total):
	r = random.uniform(0, total)
	upto = 0
	for c in choices.keys():
		w = choices[c]
		if upto + w >= r:
			return c
		upto += w
	assert False, "Shouldn't get here"

def new_text(txt):
	countLeters = {};
	for x in set(txt):
		countLeters[x] = 0.0

	total = 0.0
	for x in txt:
		total += 1
		countLeters[x] += 1

	output = ""

	# while len(countLeters.keys()) > 0:
	for x in range(len(txt)):
		key = weighted_choice(countLeters, total)
		output += chr(key)
		countLeters[key] -= 1
		total -= 1
		if countLeters[key] == 0:
			countLeters.pop(key, None)

	return output

def new_text_join(txt):
	countLeters = {};
	total = 0.0
	totalCond = {};
	for x in set(txt):
		countLeters[x] = {}
		totalCond[x] = 0
		for y in set(txt):
			countLeters[x][y] = 0.0

	for x in range(1,len(txt)):
		total += 1.0
		last = txt[x-1]
		current = txt[x]
		countLeters[last][current] += 1.0
		totalCond[last] += 1

	output = ""
	output += chr(txt[0])

	for x in range(1, len(txt)):
		key = weighted_choice(countLeters[ord(output[x-1])], totalCond[ord(output[x-1])])
		output += chr(key)
		# countLeters[ord(output[x-1])][key] -= 1
		# total -= 1
		# if countLeters[ord(output[x-1])][key] == 0:
		# 	countLeters[ord(output[x-1])].pop(key, None)

	return output

def print_all(funct):
	global datas
	for txt in sorted(datas.keys()):
		print (funct(datas[txt]), txt)

# MAIN

filepath = "./*.txt"

datas = {}

for i in range(len(glob.glob(filepath))):
	datas[glob.glob(filepath)[i].replace('./','').replace('.txt','')] = (clean_text(open(glob.glob(filepath)[i],'r').read()))

print ("	Entropies:")
print_all(entropy)
print ("\n	Joint Entropies:")
print_all(joint_entropy)
print ("\n	Condition Entropies:")
print_all(conditional_entropy)

# print (datas[0])



# print (joint_entropy(datas[0]))

# print (conditional_entropy(datas[0]))
# print (joint_entropy(datas[0])*2 - entropy(datas[0]))

# print (new_text(datas[0]))

# print (joint_entropy(datas[0]))
# print (joint_entropy(new_text_join(datas[0])))