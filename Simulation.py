import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

#运输成本
b = 0.01
#用户距离
c = 10
#分裂
S = 10
#合并
R = 100
#固定成本
F = 2000


userPosition = [[0, 0]]

def loadUserPosition():
    file = open("user.txt", "r").readlines()
    user = []
    for line in file:
        tmp = line.strip().split(',')
        x = tmp[0].strip('[]')
        y = tmp[1].strip('[]')
        # print(x, y)
        user.append([float(x), float(y)])
    return user
    
    
def massCenter(userList):
    if not userList:
        return None;
    x, y = zip(*(userList))
    sumx = sum(x) * c
    sumy = sum(y) * c
    x = sumx / (len(x) * c + b)
    y = sumy / (len(y) * c + b)
    return [x, y]
    
def _utestMassCenter():
    a = [[1, 1], [2, 2], [3, 3], [-1, -1], [-2, -2], [-3, -3]]
    print(massCenter(a))
    
def distance(p1, p2):
    if not p1 or not p2:
        return None
        
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return np.sqrt(x * x + y * y)
    
def _utestDistance():
    print(distance([-1, -1], [2, 2]))
    
def forceBaseStation(muList):
    if [0, 0] in muList:
        return

    minDis = 10000
    minNum = 0
    for i in range(len(muList)):
        tmpDis = distance(muList[i], (0, 0))
        if tmpDis < minDis:
            minDis = tmpDis
            minNum = i
    
    muList[minNum] = [0, 0]
    
def _utestForceBaseStation():
    g = [[-1, -2], [1, 1], [2, 2], [3, 3], [4, 4]]
    forceBaseStation(g)
    print(g)

    
def stationCostCalculation(group, massCenter):
    if not group:
        return None
        
    d = sum(c * distance(i, massCenter) for i in group)
    t = b * distance(massCenter, (0, 0))
    return d + t + F
    
def _utestStationCostCalculation():
    g = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
    m = massCenter(g)
    a = stationCostCalculation(g, m)
    print(a)
    
def splitGroup(group, mc):
    if not group:
        return None
    
    stdDeviation = [np.sqrt(1/len(group) * sum((i[j] - mc[j])**2 for i in group)) for j in range(len(group[0]))]
    # print(stdDeviation)
    if not [i for i in stdDeviation if i > S]:
        return None
        
    if mc == [0, 0]:
        mcplus = massCenter(group)
        mcminus = [0, 0]
    else:
        mcplus = [mc[i] + stdDeviation[i] for i in range(len(mc))]
        mcminus = [mc[i] - stdDeviation[i] for i in range(len(mc))]
    
    mpgroup, mmgroup = buildGroup(group, [mcplus, mcminus])
    mpcost = stationCostCalculation(mpgroup, mcplus)
    mmcost = stationCostCalculation(mmgroup, mcminus)
    precost = stationCostCalculation(group, mc)
    
    # print(mcplus, mcminus)
    
    if mpcost and mmcost and precost > mpcost + mmcost:
        return [mcplus, mcminus]
    else:
        return None
    
def _utestSplitGroup():
    g = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
    m = massCenter(g)
    a = splitGroup(g, m)
    print(a)
    
def mergeGroup(group1, massCenter1, group2, massCenter2):
    if not group1 or not group2:
        return None
        
    dis = distance(massCenter1, massCenter2)
    if dis > R:
        return None
    
    weight1 = len(group1)
    weight2 = len(group2)
    #std deviation
    if massCenter1 == [0, 0] or massCenter2 == [0, 0]:
        mu = [0, 0]
    else:
        mu = [(massCenter1[i] * weight1 + massCenter2[i] * weight2)/(weight1 + weight2) for i in range(len(massCenter1))]
    
    m1cost = stationCostCalculation(group1, massCenter1)
    m2cost = stationCostCalculation(group2, massCenter2)
    precost = stationCostCalculation(group1 + group2, mu)
    
    if precost > m1cost + m2cost:
        return None
    else:
        return [mu]
    
def _utestMergeGroup():
    g1 = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
    m1 = massCenter(g1)
    print(m1)
    
    g2 = [[0, 4], [1, 3], [2, 2], [3, 1], [4, 0]]
    m2 = massCenter(g2)
    print(m2)
    
    a = mergeGroup(g1, m1, g2, m2)
    print(a)
    
def buildGroup(userList, muList):
    group = [[] for i in range(len(muList))]
    for user in userList:
        minGroup = 0
        minDis = 10000000
        for i in range(len(muList)):
            tmpDis = distance(user, muList[i])
            if tmpDis < minDis:
                minDis = tmpDis
                minGroup = i
        
        group[minGroup].append(user)
    
    # print(group)
    return group
    
def removeEmptyGroup(group, muList):
    i = 0
    while i < len(group): 
        #empty group
        if not group[i]:
            muList.pop(i)
            group.pop(i)
            i -= 1
            
        i += 1

def _utestBuildGroup(): 
    g = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
    m = [[1, 1], [3, 3]]
    a = buildGroup(g, m)
    print(a)
    
def StationCalculation(userList):
    #step 1
    group = [userList]
    lastMuList = []
    
    maxStep = 1000
    maxError = 1
    error = 100
    step = 0
    
    while step < maxStep and error > maxError:
        print("Step ", step)
        step += 1
        
        #step 2
        massCenterList = [massCenter(g) for g in group]
    
        #step 3
        forceBaseStation(massCenterList)
    
        #step 4
        muList = []
        i = 0
        while i < len(group):
            sg = splitGroup(group[i], massCenterList[i])
            #if split, then do not check for merge
            if sg:
                group.pop(i)
                massCenterList.pop(i)
                i -= 1
                muList += sg
            i += 1
                
        #step 5
        i = 0
        while i < len(group):
            j = 0
            while j < len(group):
                if i is not j:
                    mg = mergeGroup(group[i], massCenterList[i], group[j], massCenterList[j])
                    if mg:
                        group.pop(i)
                        massCenterList.pop(i)
                        if i > j:
                            group.pop(j)
                            massCenterList.pop(j)
                        else:
                            group.pop(j - 1)
                            massCenterList.pop(j - 1)
                        i -= 1
                        j -= 1
                        
                        muList += mg
                        
                        break
                j += 1
            i += 1
        
        muList += massCenterList
        
        #step 6
        group = buildGroup(userList, muList)
        removeEmptyGroup(group, muList)
        
        #step 7
        if lastMuList and muList and len(lastMuList) == len(muList):
            error = [np.sqrt(1/len(lastMuList) * sum((lastMuList[i][j] - muList[i][j])**2 for i in range(len(muList)))) for j in range(len(muList[0]))]
            error = sum(i**2 for i in error)
            print("Error: ", error)
        
        lastMuList = muList
        
    return group, muList
    
def _utestStationCalculation():
    group, muList = StationCalculation([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
    print(group, muList)
    print(stationCostCalculation([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]], [0, 0]))
    finalProcess(group, muList)
    
def finalProcess(group, muList):
    totalCost = sum(stationCostCalculation(group[i], muList[i]) for i in range(len(group)))
    print(totalCost)
    
    colormap = cm.jet(range(256))
    # colormap = colormap[10:245]
    step = int(len(colormap)/len(group))
    step = 1 if step == 0 else step
    tmp = 0
    for g in group:
        for p in g:
            plt.plot(p[0], p[1], color = colormap[tmp], linestyle = 'None', marker = '.')
        tmp += step
            
    tmp = 0
    count = 0
    for m in muList:
        plt.plot(m[0], m[1], color = colormap[tmp], linestyle = 'None', marker = 'o')
        plt.annotate(str(count), m)
        count += 1
        tmp += step
        
    s = " b = {}\n c = {}\n S = {}\n R = {}\n F = {}\n".format(b, c, S, R, F)
    plt.text(-1000, -1000, s, bbox=dict(facecolor='white', alpha=0.5))
    plt.title("finalcost = {:.2f}".format(totalCost))
    
    plt.savefig("final_{}_{}_{}_{}_{}.png".format(b, c, S, R, F))
    plt.show()
    
    return totalCost
    
                
if __name__ == '__main__':
    # _utestMassCenter()
    # _utestDistance()
    # _utestSplitGroup()
    # _utestMergeGroup()
    # _utestForceBaseStation()
    # _utestBuildGroup()
    # _utestStationCostCalculation()
    # _utestStationCalculation()
    
    user = loadUserPosition()
    g, s = StationCalculation(user)
    finalProcess(g, s)