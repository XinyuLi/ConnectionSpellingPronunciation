from __future__ import division          #integer division
from collections import defaultdict
import codecs          #to read and write unicode
import math
import re
import sys
from string import punctuation

#File Name
FileName = "cmudict.0.7a"
Vs = {"A","E","I","O","U"}

emiP2S = "emiP2S.txt"
tranP2S = "tranP2S.txt"
emiS2P = "emiS2P.txt"
tranS2P = "tranS2P.txt"
claP = "claP.txt"
claS = "claS.txt"

cP = list()
cS = list()

MIN_F = -10000000

def getProbSP():
    tran = defaultdict(float)
    tranT = codecs.open(tranS2P,'r','utf8')
    for line in tranT:
        w = line.split(',')
        tran[w[0]] = float(w[1])
    emi = defaultdict(float)
    emiT = codecs.open(emiS2P,'r','utf8')
    for line in emiT:
        w = line.split(',')
        emi[w[0]] = float(w[1])
    clPT = codecs.open(claP,'r','utf8')
    for line in clPT:
        #print ("R")
        cP.append(line[0:len(line)-1])
    clST = codecs.open(claS,'r','utf8')
    for line in clST:
        #print ("T")
        cS.append(line[0:len(line)-1])
    return tran,emi

def parsing(obs):
    i = 0
    l = len(obs)
    boLi = list()
    while i < l:
        boLi.append(obs[i])
        i += 1
    return boLi

def Viterbi(ClaList,transDict,emiDict,observ): # run Viterbi algorithm
    c = len(observ)
    r = len(ClaList)
    mtrx = [[0 for col in range(c)] for row in range(r)]
    Vtag = [" "]*c
    mVT = ""
    mValue = 0
    for i in range(0,r):
        mtrx[i][0] = float(transDict["#"+ClaList[i]])*float(emiDict[ClaList[i]+"#"+observ[0]])
        
        if mtrx[i][0] > mValue:
            mValue = mtrx[i][0]
            mVT = ClaList[i]
    if len(mVT) > 2:
        Vtag[0] = mVT[0:-1]
    else:
        Vtag[0] = mVT
    for i in range(1,c):
        mValue = MIN_F
        mVT = 0
        for j in range(0,r):
            mtrx[j][i] = MIN_F
            for k in range(0,r):
                t = mtrx[k][i-1]*float(transDict[ClaList[k]+"#"+ClaList[j]])*float(emiDict[ClaList[j]+"#"+observ[i]])
                if mtrx[j][i] < t:
                    mtrx[j][i] = t
            if mtrx[j][i] > mValue:
                mValue = mtrx[j][i]
                mVT = ClaList[j]
        if len(mVT) > 2:
            Vtag[i] = mVT[0:-1]
        else:
            Vtag[i] = mVT
    return [mtrx,Vtag]

        
if __name__=='__main__':   #main function
    [tra,emi] = getProbSP()
    while 1:
        word = input('Enter the pronunciation: ')
        obs = parsing(word.split())
        [m,V] = Viterbi(cS,tra,emi,obs)
        print ("The word is:")
        tw = ""
        for e in V:
            tw += e
        print (tw)
