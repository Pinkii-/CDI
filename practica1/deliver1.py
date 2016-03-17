# from scipy import misc
# lena = misc.lena()
# import matplotlib.pyplot as plt
# plt.imshow(lena,cmap=clt.cm.gray)



import glob
import unicodedata
from math import log2
import random
import zipfile
import os

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

	if type(txt[0]) == type('str'):
		for x in range(1,len(txt)):
			last = txt[x-1]
			current = txt[x]
			if last == ltr:
				total += 1.0
				countLeters[current] += 1.0
	else:
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


def get_compressed_file_size(key):
	global datas
	txtRand = new_text(datas[key]);
	txtRand2 = new_text_join(datas[key]);

	txt = str(datas[key])
	with open(resultsPath+str(key)+'.txt_procesado', 'w+') as f: 
		f.write(txt)
	with zipfile.ZipFile(resultsPath+str(key)+'.txt_procesado.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
	 	myzip.write(resultsPath+str(key)+'.txt_procesado');

	with open(resultsPath+str(key)+'_rand.txt_procesado', 'w+') as f: 
		f.write(txtRand)
	with zipfile.ZipFile(resultsPath+str(key)+'_rand.txt_procesado.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
	 	myzip.write(resultsPath+str(key)+'_rand.txt_procesado');

	with open(resultsPath+str(key)+'_randJoint.txt_procesado', 'w+') as f: 
		f.write(txtRand2)
	with zipfile.ZipFile(resultsPath+str(key)+'_randJoint.txt_procesado.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
	 	myzip.write(resultsPath+str(key)+'_randJoint.txt_procesado');


	txt_procesado_size = os.stat(resultsPath+str(key)+'.txt_procesado').st_size;
	txt_procesado_zip_size = os.stat(resultsPath+str(key)+'.txt_procesado.zip').st_size;
	txt_rand_size = os.stat(resultsPath+str(key)+'_rand.txt_procesado').st_size;
	txt_rand_zip_size = os.stat(resultsPath+str(key)+'_rand.txt_procesado.zip').st_size;
	txt_randJoint_size = os.stat(resultsPath+str(key)+'_randJoint.txt_procesado').st_size;
	txt_randJoint_zip_size = os.stat(resultsPath+str(key)+'_randJoint.txt_procesado.zip').st_size;

	print("text processed:           ",txt_procesado_size,  "B  text processed zip          ", txt_procesado_zip_size, "B", "ratio of compression", txt_procesado_zip_size/txt_procesado_size)
	print("text same entropy:        ",txt_rand_size,	    "B  text same entropy zip       ", txt_rand_zip_size,      "B", "ratio of compression", )
	print("text same joint entropy:  ",txt_randJoint_size,  "B  text same joint entropy zip ", txt_randJoint_zip_size, "B", "ratio of compression", )
	print("--------------------------")


def print_all(funct):
	global datas
	for txtName in sorted(datas.keys()):
		print (funct(datas[txtName]), txtName)

def print_all_key(funct):
	global datas
	for txtName in sorted(datas.keys()):
		print (txtName,":")
		funct(txtName)


# MAIN

# txt = "00001"*1000

# print (joint_entropy(txt))
# print (1/5*conditional_entropy1(txt,'1')+4/5*conditional_entropy1(txt,'0'))
# print (conditional_entropy(txt))

# exit(0)

filepath = "./*.txt"

resultsPath = "Results/"

datas = {}

for i in range(len(glob.glob(filepath))):
	datas[glob.glob(filepath)[i].replace('./','').replace('.txt','')] = (clean_text(open(glob.glob(filepath)[i],'r').read()))

print ("	Entropies:")
print_all(entropy)
print ("\n	Joint Entropies:")
print_all(joint_entropy)
print ("\n	Condition Entropies:")
print_all(conditional_entropy)
print ("\n  Size of the files")
print_all_key(get_compressed_file_size)

exit(0)

# We can see that the aleatory text made with the same joint entropy have the exactaly same size when is compressed with zip than the original.
# We can also appreciate that when we made a text with the same entropy, as the entropy is greater than the joint entropy, the zip made with that text is greater.


# 	Entropies:
# 4.040598102961624 DE_Kafka_Metamorphosis
# 4.083822097557767 EN_CaptainsCourageous
# 4.058186751934843 EN_Kafka_Metamorphosis
# 4.067542780122727 EN_Kafka_TheTrial
# 3.967862196576073 ES_AlonsoDeVillegasSelvago_ComediaSerafina
# 3.9687994956241908 ES_Cervantes_DonQuijote
# 3.9767033188144327 ES_Cervantes_ViajeAlParnaso
# 3.9612257160034 FR_PaulDesjardins_LaDemocratieSpiritualiste
# 3.9688384340255256 IT_PaoloMantegazza_ASediciAnni
# 3.9703099397607744 IT_Various_LaVitaItalianaNelRisorgimientoIII

# 	Joint Entropies:
# 3.5946299404092454 DE_Kafka_Metamorphosis
# 3.6989527052916515 EN_CaptainsCourageous
# 3.6274865402235106 EN_Kafka_Metamorphosis
# 3.6547644610702563 EN_Kafka_TheTrial
# 3.519086455952491 ES_AlonsoDeVillegasSelvago_ComediaSerafina
# 3.502408092985971 ES_Cervantes_DonQuijote
# 3.5374260254501433 ES_Cervantes_ViajeAlParnaso
# 3.5688315884157835 FR_PaulDesjardins_LaDemocratieSpiritualiste
# 3.575126918655189 IT_PaoloMantegazza_ASediciAnni
# 3.5741291345913537 IT_Various_LaVitaItalianaNelRisorgimientoIII

# 	Condition Entropies:
# 3.1486512229739034 DE_Kafka_Metamorphosis
# 3.3140805673456883 EN_CaptainsCourageous
# 3.1968044525022963 EN_Kafka_Metamorphosis
# 3.2419899139033683 EN_Kafka_TheTrial
# 3.070307090346807 ES_AlonsoDeVillegasSelvago_ComediaSerafina
# 3.0360167875860364 ES_Cervantes_DonQuijote
# 3.098146412109047 ES_Cervantes_ViajeAlParnaso
# 3.1764361252505036 FR_PaulDesjardins_LaDemocratieSpiritualiste
# 3.181413477829422 IT_PaoloMantegazza_ASediciAnni
# 3.1779464383324845 IT_Various_LaVitaItalianaNelRisorgimientoIII

#   Size of the files
# DE_Kafka_Metamorphosis :
# text processed:            117360 B  text processed zip           40669 B
# text same entropy:         117357 B  text same entropy zip        68374 B
# text same joint entropy:   117357 B  text same joint entropy zip  40669 B
# --------------------------
# EN_CaptainsCourageous :
# text processed:            276592 B  text processed zip           104628 B
# text same entropy:         276589 B  text same entropy zip        161585 B
# text same joint entropy:   276589 B  text same joint entropy zip  104628 B
# --------------------------
# EN_Kafka_Metamorphosis :
# text processed:            115391 B  text processed zip           39138 B
# text same entropy:         115388 B  text same entropy zip        67444 B
# text same joint entropy:   115388 B  text same joint entropy zip  39138 B
# --------------------------
# EN_Kafka_TheTrial :
# text processed:            432819 B  text processed zip           143087 B
# text same entropy:         432816 B  text same entropy zip        251640 B
# text same joint entropy:   432816 B  text same joint entropy zip  143087 B
# --------------------------
# ES_AlonsoDeVillegasSelvago_ComediaSerafina :
# text processed:            433454 B  text processed zip           153330 B
# text same entropy:         433451 B  text same entropy zip        247018 B
# text same joint entropy:   433451 B  text same joint entropy zip  153330 B
# --------------------------
# ES_Cervantes_DonQuijote :
# text processed:            2021951 B  text processed zip           693016 B
# text same entropy:         2021948 B  text same entropy zip        1149575 B
# text same joint entropy:   2021948 B  text same joint entropy zip  693016 B
# --------------------------
# ES_Cervantes_ViajeAlParnaso :
# text processed:            285893 B  text processed zip           105126 B
# text same entropy:         285890 B  text same entropy zip        163534 B
# text same joint entropy:   285890 B  text same joint entropy zip  105126 B
# --------------------------
# FR_PaulDesjardins_LaDemocratieSpiritualiste :
# text processed:            44178 B  text processed zip           17174 B
# text same entropy:         44175 B  text same entropy zip        25815 B
# text same joint entropy:   44175 B  text same joint entropy zip  17174 B
# --------------------------
# IT_PaoloMantegazza_ASediciAnni :
# text processed:            119953 B  text processed zip           44766 B
# text same entropy:         119950 B  text same entropy zip        68792 B
# text same joint entropy:   119950 B  text same joint entropy zip  44766 B
# --------------------------
# IT_Various_LaVitaItalianaNelRisorgimientoIII :
# text processed:            269059 B  text processed zip           99408 B
# text same entropy:         269056 B  text same entropy zip        153618 B
# text same joint entropy:   269056 B  text same joint entropy zip  99408 B
# --------------------------
