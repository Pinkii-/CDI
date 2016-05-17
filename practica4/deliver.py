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

        print("searchBuffer" ,searchBuffer, "lookaheadBuffer", lookaheadBuffer)

        for rSearchBuffer in range(len(searchBuffer)):
            if searchBuffer[rSearchBuffer] == lookaheadBuffer[0]:
                offset = len(searchBuffer) - rSearchBuffer
                length = 1
                window = searchBuffer + lookaheadBuffer
                while length < len(lookaheadBuffer) and window[rSearchBuffer+length] == lookaheadBuffer[length]:
                    length += 1
                if length == len(lookaheadBuffer):
                    length -= 1
                letter = lookaheadBuffer[length]
                incr += length
                break

        
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

        for rSearchBuffer in range(len(searchBuffer)):
            if searchBuffer[rSearchBuffer] == lookaheadBuffer[0]:
                offset = len(searchBuffer) - rSearchBuffer
                length = 1
                window = searchBuffer + lookaheadBuffer
                while length < len(lookaheadBuffer) and window[rSearchBuffer+length] == lookaheadBuffer[length]:
                    length += 1
                if length == len(lookaheadBuffer):
                    length -= 1
                letter = lookaheadBuffer[length]
                break

        
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


txt1 = open("yourfilename.txt","r",encoding="utf-8").read()

txt2 = "setzejutgesdunjutjatmengenfetgedunpenjat"

txt3 = 10*"0000000001"

txt4 = "aaaaaaaaba"
# txt4 = "abac"

txt = "1234123412323123"
txt = txt3

# _, tok = LZ77_encode(txt,8,16)

# print (tok)

# print (txt)
# print(LZ77_decode(tok))

_, tok = LZSS_encode(txt,16,8,2)

print (tok)

print (txt)
print(LZSS_decode(tok))