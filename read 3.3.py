# -*- coding: utf-8 -*-
"""
Created on Thu May 11 20:46:30 2017

@author: chaoran
"""
#####################################################################
#read in iris data
#####################################################################
x0 = []
x1 = []
x2 = []
x3 = []
x = []
y = []
index=[]


with open("iris.data", "r") as file:
    data = file.readlines()[:-1]
    
    for line in data:
        words = line.split(",")
        #print(words)
        x0.append(float(words[0]))
        x1.append(float(words[1]))
        x2.append(float(words[2]))
        x3.append(float(words[3]))
        x.append([float(words[0]),float(words[1]),float(words[2]),float(words[3])])
        #Iris-setosa
        if((words[4])=="Iris-setosa\n"):           
            y.append(0)    
        #Iris-versicolor
        elif((words[4])=="Iris-versicolor\n"):          
            y.append(1)
        #Iris-virginica
        else:
            y.append(2)                                 
        #print("0",x0)
        #print("y",y)
                           
#print(len(x0))
#print(len(y))
##################################################################
#generating training and testing dataset                          
##################################################################

import random

index=list(range(0, 150))
#print(index)
random.shuffle(index)
#print("index",index)
nx0=[]
nx1=[]
nx2=[]
nx3=[]
ny=[]

for i in range(0,150):
    number=index[i]
    nx0.append(x0[number])
    nx1.append(x1[number])
    nx2.append(x2[number])
    nx3.append(x3[number])
    ny.append(y[number])
 
#print("y",ny)
                                         
##################################################################
#generating group instruction set
##################################################################                            
from random import randint, sample

modeM=[]
opM=[]
target1M=[]
target2M=[] 
instructionM=[]

for q in range(0,100): 
    #generate the mode, operator, gpr[target1],iris[target2]   
    modeA=[]
    opA=[]
    target1A=[]
    target2A=[] 
    instruction=[]
    
    for i in range(0,100): 
        mode = randint(0,1)
        op = randint(0,3) 
        target1 = randint(0,7)
        target2 = randint(0,7)
        #set the number target2 suit for gpr
        if (mode == 1):
            target2=target2%4
            
        modeA.append(mode)
        opA.append(op)
        target1A.append(target1)
        target2A.append(target2)
        instruction.append([mode,op,target1,target2])
 
    modeM.append(modeA)
    opM.append(opA)
    target1M.append(target1A)
    target2M.append(target2A)
    instructionM.append(instruction) 
    
 
#########################################################
#function to generate the validation
#########################################################

def signValid0(x, y, z):    
    if (min(x,y)==min(x,z)==x):
        valid0.append(0)
    elif(max(x,y)==max(x,z)==x):
        valid0.append(2)
    else:
        valid0.append(1)

##########################################################
#first 100 program population 0
##########################################################

#bestprogram to keep the best program(100 instructions)
bestprogram=[]
bestc=0

countA=[]#count for how many correct for each program

#counting how many right classification for 1000 program
total0=0
total1=0
total2=0

#arrays to stroe each programs correctness for each classification
countA0=[]
countA1=[]
countA2=[]
#this loop is for run 100 iterations of the whole 100 programs
for g in range(0,100):     
    count=0;
    valid0=[]
    
    #counting how many right classification for each program
    count0=0
    count1=0
    count2=0
    
    #this loop is for 105 lines of data
    for j in range(0,105):
        #reset gpr array with 8 element
        gpr = [1,1,1,1,1,1,1,1]        
        
        #decided which column of iris I sould use
        if (target2 == 0):
            source = nx0[j]
        elif (target2 == 1):
            source = nx1[j]
        elif (target2 == 2):
            source = nx2[j]
        else:
            source = nx3[j]
        #this loop is for 100 lines of instructions
        for i in range(0,100):
            
            mode = modeM[g][i]
            op = opM[g][i]
            target1 = target1M[g][i]
            target2 = target2M[g][i]        
                    
            #base on the mode decide the calculation            
            if (mode == 1):
                if (op == 0):
                    gpr[target1]=gpr[target1]+source
                elif (op == 1):
                    gpr[target1]=gpr[target1]-source
                elif (op == 2):
                    gpr[target1]=gpr[target1]%source
                else:
                    gpr[target1]=gpr[target1]*source
            else:
                if (op == 0):
                    gpr[target1]=gpr[target1]+gpr[target2]
                elif (op == 1):
                    gpr[target1]=gpr[target1]-gpr[target2]
                elif (op == 2):
                    try:
                        gpr[target1]=gpr[target1]%gpr[target2]
                    except ZeroDivisionError :
                        gpr[target1]=1
                else:
                    gpr[target1]=gpr[target1]*gpr[target2]

        signValid0(gpr[0],gpr[1],gpr[2])
            
        #compare valid with iris classification
        if(valid0[j]==ny[j]):
            count+=1
            if(ny[j]==0):
                count0+=1
                total0+=1
            if(ny[j]==1):
                count1+=1
                total1+=1
            if(ny[j]==2):
                count2+=1
                total2+=1
    countA.append([g,count])
    countA0.append(count0)
    countA1.append(count1)
    countA2.append(count2)
    #print(len(countA0))
    #print("c0", count0)
    #print("t0", total0)
    #print(countA)           

#for fitness sharing
countfs=[]
fittness=0
#get the fitness sharing
for g in range(0,100):
    number0 = (countA0[g])/total0
    number1 = (countA1[g])/total1
    number2 = (countA2[g])/total2           
    countA0[g] = number0
    countA1[g] = number1
    countA2[g] = number2
    fittness = number0+number1+number2
    countfs.append([g,fittness])
    
    if(fittness>bestc):
        bestc=fittness
        bestprogram=[]
        for i in range(0,100):
            mode = modeM[g][i]
            op = opM[g][i]
            target1 = target1M[g][i]
            target2 = target2M[g][i]
            bestprogram.append([mode,op,target1,target2])
#print(countfs)    
#print(countA0)

#############################################################
#mutation set population
#############################################################

countB=[]
bestA=[]
averageA=[]

import matplotlib.pyplot as plt
from operator import itemgetter
import numpy as np
#this loop is for run 100 iterations of the whole 100 programs
for k in range(0,100):
    total=0
    average=0    
    countB=sorted(countfs,key=itemgetter(1)) 
    #print("countB after sort",k,countB)
    best=countB[99][1]   
    #print("best",best)
    bestA.append(best)
    countB=countB[20:]
    #print("countB after delete",k,countB)   
    
    newlist=countB
    #print("new",k,newlist)     
    
    countB=[]
    #counting how many right classification for 1000 program
    total0=0
    total1=0
    total2=0

    #arrays to stroe each programs correctness for each classification
    countA0=[]
    countA1=[]
    countA2=[]
    

    #this loop is for 80 programs
    for m in range(0,80):
        indexn=newlist[m][0]
        count=0;
        valid0=[]

        count0=0
        count1=0
        count2=0
    
        #this loop is for 105 lines of data
        for j in range(0,105):
            #reset gpr array with 8 element
            gpr = [1,1,1,1,1,1,1,1]        
            
            #decided which column of iris I sould use
            if (target2 == 0):
                source = nx0[j]
            elif (target2 == 1):
                source = nx1[j]
            elif (target2 == 2):
                source = nx2[j]
            else:
                source = nx3[j]
            #this loop is for 100 instruction of 1 program
            for i in range(0,100):

                mode = modeM[indexn][i]
                op = opM[indexn][i]
                target1 = target1M[indexn][i]
                target2 = target2M[indexn][i]        
                        
                #base on the mode decide the calculation            
                if (mode == 1):
                    if (op == 0):
                        gpr[target1]=gpr[target1]+source
                    elif (op == 1):
                        gpr[target1]=gpr[target1]-source
                    elif (op == 2):
                        gpr[target1]=gpr[target1]%source
                    else:
                        gpr[target1]=gpr[target1]*source
                else:
                    if (op == 0):
                        gpr[target1]=gpr[target1]+gpr[target2]
                    elif (op == 1):
                        gpr[target1]=gpr[target1]-gpr[target2]
                    elif (op == 2):
                        try:
                            gpr[target1]=gpr[target1]%gpr[target2]
                        except ZeroDivisionError :
                            gpr[target1]=1
                    else:
                        gpr[target1]=gpr[target1]*gpr[target2]
                      
            signValid0(gpr[0],gpr[1],gpr[2])
                
            #compare valid with iris classification
            if(valid0[j]==ny[j]):
                count+=1
                if(ny[j]==0):
                    count0+=1
                    total0+=1
                if(ny[j]==1):
                    count1+=1
                    total1+=1
                if(ny[j]==2):
                    count2+=1
                    total2+=1
        
        countA0.append(count0)
        countA1.append(count1)
        countA2.append(count2)
        
        #countB.append([indexn,count])
        countB.append(indexn)
                
    #count for parents fitness sharing
    countfs=[]
    fittness=0
    indexf=0
    #get the fitness sharing
    for n in range(0,80):
        number0 = (countA0[n])/total0
        number1 = (countA1[n])/total1
        number2 = (countA2[n])/total2           
        countA0[n] = number0
        countA1[n] = number1
        countA2[n] = number2
        indexf=countB[n]
        fittness = number0+number1+number2
        total += fittness
        countfs.append([indexf,fittness])
        
        #find the best program
        if(fittness>bestc):
            bestc=fittness
            bestprogram=[]
            for i in range(0,100):
                mode = modeM[indexf][i]
                op = opM[indexf][i]
                target1 = target1M[indexf][i]
                target2 = target2M[indexf][i]
                bestprogram.append([mode,op,target1,target2])
                
    #from random import sample
    parents=sample(newlist,20)
    #print(parents)
    #this loop is for 20 programs
    mutate=[]  
   
    for h in range(0,20):
        
        #print(parents[h][0])
        indexp=parents[h][0]
        numberOfMutation=randint(0,99)

        count=0;
        valid0=[]

        count0=0
        count1=0
        count2=0
         
        #this loop is for 105 lines of data
        for j in range(0,105):
            #reset gpr array with 8 element
            gpr = [1,1,1,1,1,1,1,1]        
            
            #decided which column of iris I sould use
            if (target2 == 0):
                source = nx0[j]
            elif (target2 == 1):
                source = nx1[j]
            elif (target2 == 2):
                source = nx2[j]
            else:
                source = nx3[j]
            #this loop is for 100 instruction of 1 program
            for i in range(0,100):
                
                if (i == numberOfMutation) :
                    mode = randint(0,1)
                    op = randint(0,3)
                    target1 = randint(0,7)
                    target2 = randint(0,7)
                    if (mode == 1):
                        target2=target2%4
                else:
                    mode = modeM[indexp][i]
                    op = opM[indexp][i]
                    target1 = target1M[indexp][i]
                    target2 = target2M[indexp][i]       
                mutate.append([mode,op,target1,target2])    
                #base on the mode decide the calculation            
                if (mode == 1):
                    if (op == 0):
                        gpr[target1]=gpr[target1]+source
                    elif (op == 1):
                        gpr[target1]=gpr[target1]-source
                    elif (op == 2):
                        gpr[target1]=gpr[target1]%source
                    else:
                        gpr[target1]=gpr[target1]*source
                else:
                    if (op == 0):
                        gpr[target1]=gpr[target1]+gpr[target2]
                    elif (op == 1):
                        gpr[target1]=gpr[target1]-gpr[target2]
                    elif (op == 2):
                        try:
                            gpr[target1]=gpr[target1]%gpr[target2]
                        except ZeroDivisionError :
                            gpr[target1]=1
                    else:
                        gpr[target1]=gpr[target1]*gpr[target2]

            signValid0(gpr[0],gpr[1],gpr[2])
                
            #compare valid with iris classification
            if(valid0[j]==ny[j]):
                count+=1
                if(ny[j]==0):
                    count0+=1
                    total0+=1
                if(ny[j]==1):
                    count1+=1
                    total1+=1
                if(ny[j]==2):
                    count2+=1
                    total2+=1
        
        countA0.append(count0)
        countA1.append(count1)
        countA2.append(count2)

        #countB.append([indexp,count])       
        countB.append(indexp)
        
        #print("mute",mutate)
        
        #print("20",len(bestprogram))
        #print("20",bestc)
        #print("20",bestprogram)
       #print("found!",foundBest)
    #get the fitness sharing
    for n in range(0,20):
        number0 = (countA0[n])/total0
        number1 = (countA1[n])/total1
        number2 = (countA2[n])/total2           
        countA0[n] = number0
        countA1[n] = number1
        countA2[n] = number2
        indexf=countB[n]
        fittness = number0+number1+number2
        total += fittness
        countfs.append([indexf,fittness])
        if(fittness>bestc):
            #foundBest=[k,h]
            bestc=fittness
            #bestprogram=[]   
            bestprogram=mutate[n]
    #print("countf k",k,countfs )
    #print("/ntotal",total)
    average=total/100
    averageA.append(average)    
    #print("average",total/100)
#print(countB)
print("best fitness: ",bestc)  
#print("bestprogram: ",bestc/105)    
plt.plot(averageA)
plt.plot(bestA) 
plt.show()    


###################################################################
#use the best program so testing set could run
###################################################################
#this loop is for rest 45 lines of data
counttest=0

for j in range(105,150):
    #reset gpr array with 8 element
    gpr = [1,1,1,1,1,1,1,1]        
    
    #decided which column of iris I sould use
    if (target2 == 0):
        source = nx0[j]
    elif (target2 == 1):
        source = nx1[j]
    elif (target2 == 2):
        source = nx2[j]
    else:
        source = nx3[j]
    #this loop is for 100 instruction of 1 program
    for i in range(0,100):

        mode = bestprogram[i][0]
        op = bestprogram[i][1]
        target1 = bestprogram[i][2]
        target2 = bestprogram[i][3]        
        
        #base on the mode decide the calculation            
        if (mode == 1):
            if (op == 0):
                gpr[target1]=gpr[target1]+source
            elif (op == 1):
                gpr[target1]=gpr[target1]-source
            elif (op == 2):
                gpr[target1]=gpr[target1]%source
            else:
                gpr[target1]=gpr[target1]*source
        else:
            if (op == 0):
                gpr[target1]=gpr[target1]+gpr[target2]
            elif (op == 1):
                gpr[target1]=gpr[target1]-gpr[target2]
            elif (op == 2):
                try:
                    gpr[target1]=gpr[target1]%gpr[target2]
                except ZeroDivisionError :
                    gpr[target1]=1
            else:
                gpr[target1]=gpr[target1]*gpr[target2]
              
    signValid0(gpr[0],gpr[1],gpr[2])

    #compare valid with iris classification
    if(valid0[j]==ny[j]):
        counttest+=1
print("count correct out of 45: ",counttest)
correct=counttest/45   
print("test: ",correct)

