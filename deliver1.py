# from scipy import misc
# lena = misc.lena()
# import matplotlib.pyplot as plt
# plt.imshow(lena,cmap=clt.cm.gray)



import glob
import unicodedata
from math import log2

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

filepath = "./*.txt"

datas = []

for i in range(len(glob.glob(filepath))):
	datas.append(clean_text(open(glob.glob(filepath)[i],'r').read()))


def entropy(txt):

	for x in set(txt):
		print (chr(x),end=' ')

	print ('')	

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
	for x in set(txt):
		print (chr(x),end=' ')

	print('')

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
	for x in set(txt):
		print (chr(x),end=' ')

	print('')

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


# print (datas[0])



# print (joint_entropy(datas[0]))

print (conditional_entropy(datas[0]))
print (joint_entropy(datas[0])*2 - entropy(datas[0]))
