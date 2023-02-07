import sys
import random
import time
import copy
import math
import numpy as np

st=time.time()

fi=open(sys.argv[1],"r")
inputText=fi.read().split('\n')
points=[]
costmatrix=[]
for i in range(0,len(inputText)):
    inputText[i]=inputText[i].split(" ")
typeOfInput=inputText.pop(0)
n=inputText.pop(0)
n=int(n[0])
points=np.array(inputText[slice(n)],dtype='f')
costmatrix=np.array(inputText[slice(n,2*n)],dtype='f')

iters=100000
noOfAnts=100
alpha=1
beta=10
rho=0.5
qfactor=10
startvalp=0.000000001

# maxTabuLength=1000000

pmatrix=np.full((100,100),startvalp)

def antColonyOptimisation(noOfAnts,alpha,beta,rho,qfactor):
    ant=np.empty((noOfAnts,n+1))
    # tabuList=[]
    def antTour(ant):
        ind=0
        tourCost=copy.deepcopy(0)
        startCity=(math.floor(random.random()*n))
        while startCity in startCities:
            startCity = (math.floor(random.random() * n))
        startCities.append(startCity)
        ant[ind]=startCity
        ind+=1
        while(len(ant)<n):
            edges={}
            cities=[]
            totalprob=0
            for i in range(0,n):
                if i not in ant:
                    # print(i,ant[-1],costmatrix[ant[-1]][i],pmatrix[ant[-1]][i],alpha,beta,[ant[-1],i])
                    cities.append(i)
                    edges[(ant[-1],i)]=math.pow(pmatrix[ant[-1],i],alpha)*math.pow(costmatrix[ant[-1],i],-beta)
                    totalprob+=(math.pow(pmatrix[ant[-1],i],alpha))*(math.pow(costmatrix[ant[-1],i],-beta))
            for i in edges.keys():
                edges[i]=edges[i]/totalprob
            cities.sort()
            for i in range(1,len(cities)):
                edges[(ant[-1],cities[i])]=edges[(ant[-1],cities[i])]+edges[(ant[-1],cities[i-1])]
            prob=random.random()
            cityToAppend=cities[0]
            for i in range(0,len(cities)-1):
                if prob>edges[(ant[-1],cities[i])]:
                    cityToAppend=cities[i+1]
                else:
                    break
            # print(edges,prob,cityToAppend)
            print(cityToAppend,"Hi")
            ant[ind]=cityToAppend
            ind+=1
            tourCost=tourCost+costmatrix[ant[-2],ant[-1]]
        ant[ind]=tourCost
        ind+=1
        # if ant not in tabuList:
        #     if(len(tabuList)>maxTabuLength):
        #         tabuList.sort(key=lambda x:x[n])
        #         tabuList.pop(0)
        #     tabuList.append(ant)
        # else:
        #     startCities.pop()
        #     ant=[]
        #     antTour(ant)
    def updatePheromones(arr):
        for i in range(0,n-1):
            pmatrix[int(arr[i]),int(arr[i+1])]+=qfactor/arr[n]


    startCities=[]
    firstTour=np.empty((n+1))
    antTour(firstTour)
    bestTour=copy.deepcopy(firstTour)
    iterno=0
    et=time.time()
    while iterno<iters and et-st<298:
        startCities=[]
        for i in ant:
            t=time.time()
            if(t-st>298):
                break
            antTour(i)
        for i in pmatrix:
            for j in i:
                j=(1-rho)*j
        for i in ant:
            t=time.time()
            if(t-st>298):
                break
            updatePheromones(i)
            qfactor+=0.5
            if(i[n]<bestTour[n]):
                bestTour=copy.deepcopy(i)
        ant=np.empty((noOfAnts,n+1))
        et=time.time()
        if(et-st<300):
            print("TimeStamp:",et-st,"seconds"," , Iteration no:",iterno+1)
            # print(pmatrix)
            print(bestTour)
        iterno+=1
        if(et-st>150):
            alpha=alpha*2
            beta=beta//2
    # print(pmatrix)
    # print(bestTour)

antColonyOptimisation(noOfAnts,alpha,beta,rho,qfactor)