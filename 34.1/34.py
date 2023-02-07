import sys
import random
import time
import copy
import math

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
points=copy.deepcopy(inputText[slice(n)])
costmatrix=copy.deepcopy(inputText[slice(n,2*n)])

iters=100000
noOfAnts=n//5
alpha=1
beta=10
rho=0.5
qfactor=n//10
startvalp=0.000000001

maxTabuLength=1000000

pmatrix=[]
for i in range(0,n):
    a = list()
    for j in range(0,n):
        a.append(startvalp)
    pmatrix.append(a)

def antColonyOptimisation(noOfAnts,alpha,beta,rho,qfactor):
    ant=[]
    for i in range(0,noOfAnts):
        ant.append([])
    tabuList=[]
    def antTour(ant):
        tourCost=copy.deepcopy(0)
        startCity=(math.floor(random.random()*n))
        while startCity in startCities:
            startCity = (math.floor(random.random() * n))
        startCities.append(startCity)
        ant.append(startCity)
        while(len(ant)<n):
            edges={}
            cities=[]
            totalprob=0
            for i in range(0,n):
                if i not in ant:
                    # print(i,ant[-1],costmatrix[ant[-1]][i],pmatrix[ant[-1]][i],alpha,beta,[ant[-1],i])
                    cities.append(i)
                    edges[(ant[-1],i)]=math.pow(float(pmatrix[ant[-1]][i]),alpha)*math.pow(float(costmatrix[ant[-1]][i]),-beta)
                    totalprob+=(math.pow(float(pmatrix[ant[-1]][i]),alpha))*(math.pow(float(costmatrix[ant[-1]][i]),-beta))
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
            ant.append(cityToAppend)
            tourCost=tourCost+float(costmatrix[ant[-2]][ant[-1]])
        ant.append(tourCost)
        if ant not in tabuList:
            if(len(tabuList)>maxTabuLength):
                tabuList.sort(key=lambda x:x[n])
                tabuList.pop(0)
            tabuList.append(ant)
        else:
            startCities.pop()
            ant=[]
            antTour(ant)
    def updatePheromones(arr):
        for i in range(0,n-1):
            pmatrix[arr[i]][arr[i+1]]+=math.pow((arr[n]/qfactor),-1)


    startCities=[]
    firstTour=[]
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
            if(i[n]<bestTour[n]):
                bestTour=copy.deepcopy(i)
        ant=copy.deepcopy([])
        for i in range(0, noOfAnts):
            ant.append([])
        et=time.time()
        if(et-st<300):
            print("TimeStamp:",et-st,"seconds"," , Iteration no:",iterno+1)
            # print(pmatrix)
            print(bestTour)
        iterno+=1
    # print(pmatrix)
    # print(bestTour)

# antColonyOptimisation(noOfAnts,alpha,beta,rho,qfactor)
fi.close()
fi=open(sys.argv[1],"r")
ip2=fi.read().split("\n")
p1=copy.deepcopy(ip2[slice(n+2,2*n+2)])
p1=" ".join(p1)
p1=p1.split(" ")
p1=[float(x) for x in p1]
p1.sort(reverse=True)
popped=0
for i in range(0,n):
    p1.pop()
    popped+=1
p2=[]
for i in range(0,len(p1)):
    if(i%2==0):
        p2.append(p1[i])
sum=0
p3=[]
for i in range(len(p2)-n-1,len(p2)-1):
    p3.append(p2[i])
    sum+=float(p2[i])
print(p3)
print(len(p3))
print(sum)
print(popped)
