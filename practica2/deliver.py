#!/usr/bin/python3


from math import log2
from collections import Counter

def normalize_src(src):
    total = 0;
    for x,y in src:
        total += y

    src_normalized = [];
    for x,y in src:
        src_normalized.append((x,y/total))

    return src_normalized

def entropy(src):
    ent = 0.0;
    for x,y in src:
        ent += y * log2(1.0/y)

    return ent

def source_fromstring(mystr):
    aux = {}
    for x in mystr:
        if x in aux.keys():
            aux[x] += 1
        else:
            aux[x] = 1

    src = []
    for x in aux:
        src.append((x, aux[x]))

    return normalize_src(src)

def source_extension(src, k):
    if k == 1:
        return src

    src_extended = []
    for x,y in src:
        for w,z in src:
            src_extended.append((x+w,round(y*z,10)))

    return source_extension(src_extended,k-1)

def shannon_fano_code_r(src):
    if len(src) <= 1:
        return [""]

    c = Counter()
    total = 0
    for x,y in src:
        c[x] = y
        total += y

    current = 0
    src1 = []
    src2 = []
    for x in c:
        print (x, c[x])
        current += c[x]
        if current < total/2.0:
            src1.append((x,c[x]))
        else:
            src2.append((x,c[x]))

    shannon_fano1 = shannon_fano_code_r(src1)
    shannon_fano2 = shannon_fano_code_r(src2)

    shannon_fano = []

    for x in shannon_fano1:
        shannon_fano.append('0'+x)
    for x in shannon_fano2:
        shannon_fano.append('1'+x)

    return shannon_fano


def shannon_fano_code(src):

    shannon_fano = shannon_fano_code_r(src)

    return shannon_fano


    

src_code = [("0",18), ("1",2)]

print(shannon_fano_code(source_extension(normalize_src(src_code),2)))


# print (entropy (normalize_src(([("0",18), ("1",2)]))))

# print (entropy (source_fromstring("00000010000000000100")))

# print ((source_extension(normalize_src([("0",0.9), ("1",0.1)]), 2)))