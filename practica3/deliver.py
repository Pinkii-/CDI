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

# if the number k < 3, the underflow prevent will crash
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
            print("This string cant be enconded with this src")
            pass
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

        betaInt = binaryStringToInt(beta)
        alfaInt = binaryStringToInt(alfa)
        delta = betaInt - alfaInt + 1
        newAlfa = alfaInt + floor(delta*piLeft)
        newBeta = alfaInt + floor(delta*piRight) -1

        beta = intToBinaryString(newBeta,k)
        alfa = intToBinaryString(newAlfa,k)

        # reescaling Step
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

src_code = [("0",0.9), ("1",0.1)]
k = 6
string = '1010000000'

print (arithmetic_encode(string,src_code,k))

