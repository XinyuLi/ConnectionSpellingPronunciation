from __future__ import division          #integer division
from collections import defaultdict
import codecs          #to read and write unicode
import math
import re
from string import punctuation

#File Name
FileName = "cmudict_SPHINX_40.txt"

emiP2S = "emiP2S.txt"
tranP2S = "tranP2S.txt"
emiS2P = "emiS2P.txt"
tranS2P = "tranS2P.txt"
claP = "claP.txt"
claS = "claS.txt"

Vs = {"A","E","I","O","U"}
Vv = {"W","Y"}

countsdict = defaultdict(int)
bidict = defaultdict(int)
bidictP = defaultdict(int)
cS = defaultdict(int)
cP = defaultdict(int)
fd = defaultdict(str)

def get_alignment(words):
    li = len(words[0])
    lj = len(words)
    i = 0
    j = 1
    LC = list()
    LS = list()
    #print (words)
    while i < li and j < lj:
        curS = ""
        #print (LC)
        #print (LS)
        if words[0][i] == "X" and (j < lj-1 and (words[j+1][0] == "S" or words[j+1][0] == "Z")):
            LC.append("X")
            LS.append(words[j]+" "+words[j+1])
            i += 1
            j += 2
            continue
        
        if j == lj-1:
            LC.append(words[0][i:])
            LS.append(words[j])
            break
        if i == li-1:
            LC.append(words[0][i])
            while j < lj:
                LS.append(words[j])
                j += 1
            break
        if i == 0 and words[0][0] == "M" and words[0][1] not in Vs:
            if words[j+1][0] in Vs:
                LC.append("M")
                LS.append(words[j]+" "+words[j+1])
                i += 1
                j += 2
                continue
        if i == 0 and words[0][0] == "U" and words[j] == "Y" and words[0][1] not in Vs and words[0][1] not in Vv:
            LC.append("U")
            LS.append(words[j]+" "+"Y")
            i += 1
            j += 2
            continue
        if words[j] == "ER" and words[0][i] == "R":
            LC.append("R")
            LS.append("ER")
            i += 1
            j += 1
            continue
        if words[0][i] == "C" and words[0][i+1] == "K" and words[j] == "T" and words[j+1] == "S":
            LC.append("C")
            LS.append("T S")
            i += 1
            j += 2
            continue
        if (words[0][i:i+2] == "ZM" or words[0][i:i+2] == "SM") and i == li-2:
            #print ("eeeeeeee")
            LC.append(words[0][i:])
            LS.append("Z AH M")
            break
        if words[0][i:] == "SMS" and i == li-3:
            LC.append(words[0][i+1:])
            LS.append("Z AH M")
            break
        if words[0][i:i+2] == "CC" and words[j+1][0] not in Vs:
            LC.append("CC")
            LS.append(words[j]+" "+words[j+1])
            i += 2
            j += 2
            continue
        if words[0][i+1] == "L" and words[j+1][0] in Vs:
            LC.append(words[0][i])
            LC.append("L")
            LS.append(words[j])
            LS.append(words[j]+" "+words[j+1])
            i += 2
            j += 3
            continue
        if ((words[0][i] == "T" or words[j] == "K" or words[j] == "P" or words[j] == "M" or words[j] == "G" or words[j] == "N" or words[j] == "B" or words[j] == "F" or words[j] == "D" or words[0][i] == "H") and words[0][i+1] in Vs) and words[j+1][0] == "Y":
            LC.append(words[0][i])
            LS.append(words[j]+" "+"Y")
            i += 1
            j += 2
            continue
        if words[0][i] in Vs and words[0][i+1] in Vv and words[j+1] != "W" and words[j+1] != "Y":
            LC.append(words[0][i:i+2])
            LS.append(words[j])
            i += 2
            j += 1
            continue
        if len(words[j]) == 2 and words[j][1] == "R":
            LC.append(words[0][i:i+2])
            LS.append(words[j])
            i += 2
            j += 1
            continue
        if j == lj-1:
            LC.append(words[0][i:])
            LS.append(words[j])
            break
        if words[j+1][0] in Vs or words[j+1][0] in Vv:
            while words[0][i+1] not in Vs and words[0][i+1] not in Vv:
                if words[0][i+1] == "J" and words[j+1][0] == "Y":
                    break
                if words[0][i+1] == "R" and words[j+1] == "ER":
                    break
                curS += words[0][i]
                i += 1
                if i >= li-1:
                    break
            curS += words[0][i]
            i += 1
            LC.append(curS)
            LS.append(words[j])
            j += 1
        else:
            while words[0][i+1] in Vs:
                curS += words[0][i]
                i += 1
                if i >= li-1:
                    break
            curS += words[0][i]
            i += 1
            LC.append(curS)
            LS.append(words[j])
            j += 1
    return LC,LS

def count_words(fileN):
    text = codecs.open(fileN,'r','utf8')
    ln = text.readline()
    
    corre = 0
    fal = 0
    for line in text:
        words = line.split()
        j = 1
        if len(words[0]) > len(words)-1 or "(" in words[0] or "'" in words[0]:
            continue
        if not re.match('^[A-Z]+$',words[0]):
            continue
        [LC,LS] = get_alignment(words)
        if len(LC) != len(LS):
            continue
        bidict["#"+LC[0]] += 1
        bidictP["#"+LS[0]] += 1
        for i in range(len(LC)):
            countsdict[LC[i]+"#"+LS[i]] += 1
            cS[LC[i]] += 1
            cP[LS[i]] += 1
            if i != 0:
                bidict[LC[i-1]+"#"+LC[i]] += 1
                bidictP[LS[i-1]+"#"+LS[i]] += 1
    text.close()
    return

def getProbSP():
    countT = 0
    emi2 = defaultdict(float)
    tra = defaultdict(float)
    traS = defaultdict(float)
    for l in cP:
        countT += bidictP["#"+l]
    for l in cP:
        tra["#"+l] = (float)(bidictP["#"+l])/(float)(countT)
    for i in cP:
        for j in cP:
            tra[i+"#"+j] = (float)(bidictP[i+"#"+j])/(float)(cP[i])
    for l in cS:
        countT += bidict["#"+l]
    for l in cS:
        traS["#"+l] = (float)(bidict["#"+l])/(float)(countT)
    for i in cS:
        for j in cS:
            traS[i+"#"+j] = (float)(bidict[i+"#"+j])/(float)(cS[i])
    emi = defaultdict(float)
    for i in cP:
        for j in cS:
            emi[i+"#"+j] = (float)(countsdict[j+"#"+i])/(float)(cP[i])
            emi2[j+"#"+i] = (float)(countsdict[j+"#"+i])/(float)(cS[j])
    return tra,traS,emi,emi2

        
if __name__=='__main__':   #main function
    count_words(FileName)
    #print (cS)
    #print (cP)
    [tra,traS,emi,emi2] = getProbSP()
    outcS = codecs.open(claS, 'w', 'utf8')
    for i in cS:
        if cS[i] < 10:
            continue
        outcS.write(i+"\n")
        #outcS.write("\n")
    outcS.close()
    outcP = codecs.open(claP,'w','utf8')
    for i in cP:
        if cP[i] < 10:
            continue
        outcP.write(i+"\n")
        #outcP.write("\n")
    outcP.close()
    outemiP2S = codecs.open(emiP2S,'w','utf8')
    for i in emi:
        if emi[i] == 0:
            continue
        outemiP2S.write(i+",")
        outemiP2S.write(str(emi[i]))
        outemiP2S.write("\n")
    outemiP2S.close()
    outemiS2P = codecs.open(emiS2P,'w','utf8')
    for i in emi2:
        if emi2[i] == 0:
            continue
        outemiS2P.write(i+",")
        outemiS2P.write(str(emi2[i]))
        outemiS2P.write("\n")
    outtranP = codecs.open(tranP2S,'w','utf8')
    for i in tra:
        if tra[i] == 0:
            continue
        outtranP.write(i+",")
        outtranP.write(str(tra[i]))
        outtranP.write("\n")
    outtranP.close()
    outtranS = codecs.open(tranS2P,'w','utf8')
    for i in traS:
        if traS[i] == 0:
            continue
        outtranS.write(i+",")
        outtranS.write(str(traS[i]))
        outtranS.write("\n")
    outtranS.close()
