#!/usr/bin/python3


from math import log2, ceil
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

    src_original = src
    for n in range(k-1):
        src_extended = []
        for x,y in src:
            for w,z in src_original:
                src_extended.append((x+w,round(y*z,10)))
        src = src_extended

    return src

def plus1(bit,string):
    aux = list(string)
    bitAux = len(aux)-1-bit
    if aux[bitAux] == '0':
        aux[bitAux] = '1'
        return "".join(aux)
    else:
        aux[bitAux] = '0'
        return plus1(bit+1,"".join(aux))


def shannon_code(src):
    if len(src) == 0:
        return [],0

    lengthSrc = []
    c = Counter()
    for x,y in src:
        lengthSrc.append((x,ceil(log2(1.0/y))))
        c[x] = ceil(log2(1.0/y))

    
    mostCommon = c.most_common()
    firstLetter, firstLength = mostCommon[len(mostCommon)-1]
    current = '0'*firstLength
    orderedList = [current]
    for x in range(len(mostCommon)-2,-1,-1):
        letter, length = mostCommon[x]
        
        current = plus1(0,current)
        # if (length == len(current)):
        # else:
        
        diff = length - len(current)
        current += '0'*diff

        orderedList.append(current)

    orderedList.reverse()

    result = []
    mean_length = 0
    for x in range(len(src)):
        letter,p=src[x]
        for y in range(len(mostCommon)):
            w,_ = mostCommon[y]
            if letter == w:
                result.append(orderedList[y])
                mean_length += p*len(orderedList[y])
                break

    return result, round(mean_length,10)




def shannon_fano_code_r(src):
    if len(src) <= 1:
        return [""]

    c = Counter()
    total = 0.0
    for x,y in src:
        c[x] = y
        total += y



    mostCommon = c.most_common()
    
    # print ("LAAAAAAAA")
    # print (mostCommon)

    x,y = mostCommon[0]
    current = y
    src1 = [(x,y)]
    src2 = []

    for n in range(1,len(mostCommon)):
        x,y = mostCommon[n]
        last = current
        current += y
        # print (x, y, current, total/2.0)
        if current < total/2.0:
            src1.append((x,y))
        elif current > total/2.0 and last < total/2.0:
            if total/2 - last < current - total/2:
                src2.append((x,y))
            else:
                src1.append((x,y))
        else:
            src2.append((x,y))

    # print("src1", src1,"src2", src2)

    shannon_fano1 = shannon_fano_code_r(src1)
    shannon_fano2 = shannon_fano_code_r(src2)
    # print("sha 1",shannon_fano1, "sha 2", shannon_fano2)

    shannon_fano = []

    for x in shannon_fano1:
        shannon_fano.append('0'+x)
    for x in shannon_fano2:
        shannon_fano.append('1'+x)

    return shannon_fano


def shannon_fano_code(src):

    shannon_fano = shannon_fano_code_r(src)

    c = Counter()
    for x,y in src:
        c[x] = y
    mostCommon = c.most_common()
    mean_length = 0

    result = []
    for n in range(len(src)):
        x, y = src[n]
        for n2 in range(len(mostCommon)):
            w,z = mostCommon[n2]
            if x == w:
                result.append(shannon_fano[n2])
                mean_length += z*len(shannon_fano[n])
                break

    return result, round(mean_length,10)

class Tree(object):
    def __init__(self, letter, probability):
        self.left = None
        self.right = None
        self.letter = letter
        self.probability = probability
        self.depth = 0

    def __repr__(self):
        return "Letter: \""+self.letter+"\" w/ Probability: "+str(round(self.probability,10))+(' Left '+self.left.letter if self.left != None else '')+(' Right '+self.right.letter if self.right != None else '')+ '\n'

    def __str__(self):
        return self.letter+' '+str(round(self.probability,10))

def printTree(root,n):
    print ((' '*n)+str(root))
    if root.left != None:
        print (' '*n+'left')
        printTree(root.left,n+1)
    if root.right != None:
        print (' '*n+'right')
        printTree(root.right,n+1)


def huffman_tree(tree):
    if tree.left == None and tree.right == None:
        return [('',tree.probability, tree.letter)]

    l = []
    if tree.right != None:
        tl = huffman_tree(tree.right)
        for word,probability,letter in tl:
            l.append(('0'+word, probability, letter))
    if tree.left != None:
        tl = huffman_tree(tree.left)
        for word,probability,letter in tl:
            l.append(('1'+word, probability, letter))

    return l

def huffman_code(src):
    c = Counter()
    for x,y in src:
        c[x] = y
    mostCommon = c.most_common()
    treeList = []
    for n in range(len(mostCommon)-1,-1,-1):
        x, y = mostCommon[n]
        t = Tree(x,y)
        treeList.append(t)

    i = 0
    while i+1 < len(treeList):
        p = treeList[i].probability+treeList[i+1].probability
        t = Tree('-'+treeList[i].letter+'+'+treeList[i+1].letter,p)
        if treeList[i].depth >= treeList[i+1].depth:
            t.left = treeList[i]
            t.right = treeList[i+1]
        else:
            t.left = treeList[i+1]
            t.right = treeList[i]
        t.depth = max(t.left.depth,t.right.depth)+1
        if p >= 1:
            treeList.insert(len(treeList),t)
            break
        inserted = False
        for x in range(i,len(treeList)):
            if p < treeList[x].probability:
                treeList.insert(x, t)
                inserted = True
                break
        if not inserted:
            treeList.insert(len(treeList),t)
        # print(treeList)
        i += 2

    # print (treeList)
    # print()
    # printTree(treeList[len(treeList)-1],0)

    ht = huffman_tree(treeList[len(treeList)-1])

    huffman_c = []
    mean_length = 0
    for x,y in src:
        for w,p,l in ht:
            if x == l:
                mean_length += len(w)*p
                huffman_c.append(w)

    return huffman_c, round(mean_length,10)

def translate(src,funcs,string):
    print()
    print("Source:", src)
    print("String:",string)

    for func in funcs:
        print()
        print("---------------",func.__name__,"--------------")
        output = []
        code,mean_len = func(src)
        offset = 0
        for i in range(len(string)):
            i = i+offset
            if i >= len(string):
                break
            for j in range(len(src)):
                letter,_ = src[j]
                b = True
                for n in range(len(letter)):
                    if string[i+n] != letter[n]:
                        b = False
                        break
                if b:
                    offset += len(letter)-1
                    output.append((letter,code[j]))
                    break

        solution1 = []
        solution2 = []
        for x in range(len(output)):
            solution1.append([])
            solution2.append([])
            for i in range(len(output)):
                letter, code = output[i]
                if x != i:
                    solution1[x].append(letter)
                    solution2[x].append(code)
                else:
                    solution1[x].append('['+letter+']')
                    solution2[x].append('['+code+']')


        for x in range(len(solution1)):
            print ()
            print ("Letter", x,"-th")
            print("".join(solution1[x]))
            print("".join(solution2[x]))

        # print(output)


src_code = [("0",0.9), ("1",0.1)]
src_code = source_extension(src_code,3)

# print ("source_extension 3" ,src_code)

# src_code = [("a",3), ("1",5), ("2",9), ("3",11), ("4",14), ("5",19), ("6",33), ("7",44), ("8",62)]

# src_code = [("a",0.05), ("d",0.05), ('e',0.2), ('f',0.025), ('h',0.075), ('j',0.1),('m',0.025),('n',0.125),('p',0.025),('s',0.05),('t',0.15),('u',0.1),('z',0.025)]

# src_code = [("a1",0.36),("a2",0.18),("a3",0.18),("a4",0.12),("a5",0.09),("a6",0.07)]

# src_code = [("A",15),("B",7),("C",6),("D",6),("E",5)]

translate(src_code,[shannon_code,shannon_fano_code,huffman_code],"111110111") # si el string no se puede descodificar, el programa peta

translate(src_code,[shannon_code,shannon_fano_code,huffman_code],"000001000")

print ()

print (src_code)

print("Shannon     ",shannon_code(source_extension(normalize_src(src_code),1)))

print("Shannon Fano",shannon_fano_code(source_extension(normalize_src(src_code),1)))

print("Huffman     ", huffman_code(source_extension(normalize_src(src_code),1)))


# print (normalize_src(src_code))

# print(huffman_code(normalize_src(src_code)))

# print (entropy (source_extension(normalize_src(([("0",18), ("1",2)])),2)))

# print (entropy (source_fromstring("00000010000000000100")))

# print ((source_extension(normalize_src([("0",0.9), ("1",0.1)]), 2)))
