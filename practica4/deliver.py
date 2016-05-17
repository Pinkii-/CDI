#!/usr/bin/python3

from math import log2, ceil

def LZ77_encode(txt,s,t):
    tokens = []
    incr = 0
    for r in range(len(txt)):
        # print(tokens)
        r = r + incr
        if (r >= len(txt)):
            break

        if r-s < 0:
            searchBuffer = txt[0:r]
        else:
            searchBuffer = txt[r-s:r]    
        lookaheadBuffer = txt[r:r+t]

        offset = 0
        length = 0
        letter = lookaheadBuffer[0]

        if len(lookaheadBuffer) == 1:
            tokens.append((offset,length,letter))
            continue

        # print("searchBuffer" ,searchBuffer, "lookaheadBuffer", lookaheadBuffer)

        window = searchBuffer + lookaheadBuffer
        for rSearchBuffer in range(len(searchBuffer)):
            if searchBuffer[rSearchBuffer] == lookaheadBuffer[0]:
                offsetAux = len(searchBuffer) - rSearchBuffer
                lengthAux = 1
                while lengthAux < len(lookaheadBuffer) and window[rSearchBuffer+lengthAux] == lookaheadBuffer[lengthAux]:
                    lengthAux += 1
                if lengthAux == len(lookaheadBuffer):
                    lengthAux -= 1
                letterAux = lookaheadBuffer[lengthAux]
                
                if lengthAux > length:
                    length = lengthAux
                    offset = offsetAux
                    letter = letterAux

        incr += length
        tokens.append((offset,length,letter))

    print(ceil(log2(s+1)),ceil(log2(t)),ceil(log2(len(set(txt)))))

    bs = ceil(log2(s+1)) + ceil(log2(t)) + ceil(log2(len(set(txt))))

    return bs,tokens

def LZ77_decode(tok):
    x = ""
    for offset, length, letter in tok:
        if offset == 0:
            x += letter
        else:
            for l in range(length):
                x+= x[-offset]
            x += letter
    return x

def LZSS_encode(txt,s,t,m):
    tokens = []
    incr = 0
    for r in range(len(txt)):
        # print(tokens)
        r = r + incr
        if (r >= len(txt)):
            break

        if r-s < 0:
            searchBuffer = txt[0:r]
        else:
            searchBuffer = txt[r-s:r]    
        lookaheadBuffer = txt[r:r+t]

        offset = 0
        length = 0
        letter = lookaheadBuffer[0]

        if len(lookaheadBuffer) == 1:
            tokens.append((0,letter))
            continue

        print("searchBuffer" ,searchBuffer, "lookaheadBuffer", lookaheadBuffer)
        window = searchBuffer + lookaheadBuffer
        for rSearchBuffer in range(len(searchBuffer)):
            if searchBuffer[rSearchBuffer] == lookaheadBuffer[0]:
                offsetAux = len(searchBuffer) - rSearchBuffer
                lengthAux = 1
                while lengthAux < len(lookaheadBuffer) and window[rSearchBuffer+lengthAux] == lookaheadBuffer[lengthAux]:
                    lengthAux += 1
                if lengthAux == len(lookaheadBuffer):
                    lengthAux -= 1
                letterAux = lookaheadBuffer[lengthAux]
                
                if lengthAux > length:
                    length = lengthAux
                    offset = offsetAux
                    letter = letterAux

        
        if length < m:
            letter = lookaheadBuffer[0]
            tokens.append((0,letter))
        else:
            incr += length-1
            tokens.append((1,offset,length))
            

    # print(ceil(log2(s+1)),ceil(log2(t)),ceil(log2(len(set(txt)))))

    bs = ceil(log2(s+1)) + ceil(log2(t)) + ceil(log2(len(set(txt)))) # Cambiar esto porque seguramente el enunciado está mal

    return bs,tokens


def LZSS_decode(tok):
    x = ""
    for t in tok:
        if t[0] == 0:
            x += t[1]
        else:
            offset = t[1]
            length = t[2]
            for l in range(length):
                x+= x[-offset]
    return x


def LZ78_encode(txt):
    tokens = []
    dic = list(sorted(set(txt)))
    lastPosition = len(dic)-1
    dic += [None]*((2**max((ceil(log2(len(dic)))),4) - len(dic)))
   
    # print(dic, len(dic))
    print(lastPosition, dic)

    incr = 0
    for r in range(len(txt)):
        r = r + incr
        if (r >= len(txt)):
            break

        length = 0
        i = -1
        print(txt, "buclee")
        print(txt[:r], txt[r:])
        for x in range(lastPosition+1):
            print ("   ",x, len(dic), dic[x])
            if len(dic[x]) != 1 and (len(dic[x]) < length or len(dic[x]) + r > len(txt)-1):
                continue
            print("    ha entrado")
            lengthAux = 0
            util = True
            for p in range(len(dic[x])):
                if txt[r+p] == dic[x][p]:
                    lengthAux += 1
                else:
                    util = False
                    break
            if util and lengthAux > length:
                print (lengthAux)
                length = lengthAux
                a = txt[r+length:r+length+1]
                i = x

        print (" la a es ", a)

        incr += length
        lastPosition += 1
        if lastPosition >= len(dic):
            dic += [None]*len(dic)
        dic[lastPosition] = txt[r:r+length+1]
        print (dic)
        tokens.append((i,a))
        print (tokens)

    return tokens

def LZW_encode(txt):
    tokens = []
    dic = list(sorted(set(txt)))
    lastPosition = len(dic)-1
    dic += [None]*((2**max((ceil(log2(len(dic)))),4) - len(dic)))
   
    # print(dic, len(dic))
    # print(lastPosition, dic)

    incr = 0
    for r in range(len(txt)):
        r = r + incr
        if (r >= len(txt)):
            break

        length = 0
        i = -1
        # print(txt, "buclee")
        # print(txt[:r], txt[r:])
        for x in range(lastPosition+1):
            # print ("   ",x, len(dic), dic[x])
            if len(dic[x]) != 1 and (len(dic[x]) < length or len(dic[x]) + r > len(txt)-1):
                continue
            # print("    ha entrado")
            lengthAux = 0
            util = True
            for p in range(len(dic[x])):
                if txt[r+p] == dic[x][p]:
                    lengthAux += 1
                else:
                    util = False
                    break
            if util and lengthAux > length:
                # print (lengthAux)
                length = lengthAux
                a = txt[r+length:r+length+1]
                i = x

        # print (" la a es ", a)

        incr += length-1
        lastPosition += 1
        if lastPosition >= len(dic):
            dic += [None]*len(dic)
        dic[lastPosition] = txt[r:r+length+1]
        # print (dic)
        tokens.append((i))
        # print (tokens)

    return tokens

def LZW_decode(dic,tok):
    x = dic[tok[0]] 
    dic += dic[tok[0]]
    # print (dic)
    for r in range(1,len(tok)):
        # print ("tok", tok[r], "dic", dic[tok[r]])
        # print (dic[len(dic)-1])
        dic[len(dic)-1] += dic[tok[r]][0]
        # print (dic[len(dic)-1])
        x += dic[tok[r]]
        dic.append(dic[tok[r]])
        # print (dic)

    return x
    


txt1 = open("yourfilename.txt","r",encoding="utf-8").read()

txt2 = "setzejutgesdunjutjatmengenfetgedunpenjat"

txt3 = 10*"0000000001"

txt4 = "aaaaaaaaba"
# txt4 = "abac"

# txt = "1234123412323123987"
# txt = "AABCBBABC"
txt = txt1

## LZ77

# _, tok = LZ77_encode(txt,4096,16)

# print (tok)

# print (txt)
# print(LZ77_decode(tok))

## LZSS

# _, tok = LZSS_encode(txt,16,8,2)

# print (tok)

# print (txt)
# print(LZSS_decode(tok))

## LZ78

# print(LZ78_encode(txt))

## LZW

# print()
print("decoded ",LZW_decode(list(sorted(set(txt))),LZW_encode(txt)) == txt)
# print("original",txt)