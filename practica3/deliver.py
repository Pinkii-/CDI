#!/usr/bin/python3

from math import log2, ceil, floor

def binaryStringToInt(string):
    val = 0
    for x in range(len(string)):
        val += pow(2,len(string)-x-1) * (0 if string[x] == '0' else 1)

    return val

def intToBinaryString(number,k):
    string = ""
    for x in range(k):
        string += str(number//pow(2,k-x-1))
        number = number%pow(2,k-x-1)
    return string


def arithmetic_encode(string,src,k):
    alfa = "0"*k
    beta = "1"*k
    c = ""

    u = 0
    # if the letters of the source have more than one symbol. Example: ('00','01','10','11')
    offset = 0
    for i in range(len(string)):
        i = i+offset
        if i >= len(string):
            if i != len(string):
                print("This string cant be enconded with this src")
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
                index = j
                break

        # Generating the subInterval that I need and updating to it
        piLeft = 0
        for j in range(index):
            _, prob = src[j]
            piLeft += prob
        _, prob = src[index]
        piRight = piLeft + prob

        alfaInt = binaryStringToInt(alfa)
        betaInt = binaryStringToInt(beta)
        delta = betaInt - alfaInt + 1
        newAlfa = alfaInt + floor(delta*piLeft)
        newBeta = alfaInt + floor(delta*piRight) -1

        alfa = intToBinaryString(newAlfa,k)
        beta = intToBinaryString(newBeta,k)

        # rescaling Step
        while beta[0] == alfa[0]:
            c += alfa[0]
            alfa = alfa[1:]+'0'
            beta = beta[1:]+'1'
            c += ('1' if alfa[0] == '0' else '0') * u
            u = 0

        # underflow prevent
        while alfa[1] == '1' and beta[1] == '0':
            u += 1
            alfa = alfa[0] + alfa[2:] + '0'
            beta = beta[0] + beta[2:] + '1'

    return c + '1'

def arithmetic_decode(bin,src,k,l):
    alfa = '0'*k
    beta = '1'*k
    bin += '0'*1000
    gama = bin[:k]

    x = ''

    offset = 0
    offsetTop = 0
    while (True):
        # finding gama
        piLeft = 0
        gamaInt = binaryStringToInt(gama)
        alfaInt = binaryStringToInt(alfa)
        betaInt = binaryStringToInt(beta)
        # print (alfaInt, gamaInt, betaInt)
        # print (alfa,'0'*(k-len(gama)) +gama,beta)
        delta = betaInt - alfaInt + 1
        for letter, prob in src:
            piRight = piLeft + prob
            newAlfa = alfaInt + floor(delta*piLeft)
            newBeta = alfaInt + floor(delta*piRight)-1
            if (newAlfa <= gamaInt and gamaInt <= newBeta):
                x += letter
                alfa = intToBinaryString(newAlfa,k)
                beta = intToBinaryString(newBeta,k)
                # print (x)
                if len(x) == l:
                    return x
                break
            piLeft = piRight

        # unused = input()

        # print ("alfaBeta: ", alfa,gama,beta)
        # Rescaling
        while beta[0] == alfa[0]:
            offset += 1
            alfa = alfa[1:]+'0'
            beta = beta[1:]+'1'
            gama = bin[offset:k+offset]
            # print ("Rescaling:",alfa,gama,beta, offset)


        #underflow
        while alfa[1] == '1' and beta[1] == '0':
            alfa = alfa[0] + alfa[2:] + '0'
            beta = beta[0] + beta[2:] + '1'
            bin = bin[:offset+1] + bin[offset+2:]
            gama = bin[offset:k+offset]
            # print ("underflow:",alfa,gama,beta, offset)

        


    return None # If this happens, you are like a magician... A great magician.




src_code = [("0",0.9), ("1",0.1)]
k = 6
string = '1010010100'
print ("String to encode and decode:",string)
print ("Encoded:",arithmetic_encode(string,src_code,k))
print ("Decoded:",arithmetic_decode(arithmetic_encode(string,src_code,k),src_code,k, len(string)), "==", string,"->",arithmetic_decode(arithmetic_encode(string,src_code,k),src_code,k, len(string))==string)
# print (arithmetic_decode('11111011',src_code,k, len(string)))

