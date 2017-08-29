#Simulation
#根据用户位置信息生成站点并计算站点最优位置
#算法：
#假设站点有最大距离，用成本进行计算
#所有未注册过的点计算出一个最佳位置的新站点N，不考虑服务距离
#所有点计算一轮成本，并在车站注册，考虑服务距离
#如果成本变化小于特定值，如0.5，返回最后的成本
#如果大于之前成本，则返回之前成本
#所有车站根据注册点计算最佳位置，向最佳位置移动
import numpy as np

b = 0.1
c = 1
S = 1
R = 1


userPosition = [[0, 0]]

def loadUserPosition():
	pass
	
def massCenter(userList):
	if not userList:
		return null;
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
		return null
		
	x = p1[0] - p2[0]
	y = p1[1] - p2[1]
	return np.sqrt(x * x + y * y)
	
def _utestDistance():
	print(distance([-1, -1], [2, 2]))

def splitGroup(group, massCenter):
	if not group:
		return null
	
	# x, y = zip(*(group))
	# stdDeviation = [sum([(i[j] - for i in group])for j in range(len(group[0])]
	stdDeviation = [np.sqrt(1/len(group) * sum((i[j] - massCenter[j])**2 for i in group)) for j in range(len(group[0]))]
	print(stdDeviation)
	if not [i for i in stdDeviation if i > S]:
		return null
	
	mcplus = [massCenter[i] + stdDeviation[i] for i in range(len(massCenter))]
	mcminus = [massCenter[i] - stdDeviation[i] for i in range(len(massCenter))]
	return [mcplus, mcminus]
	
def _utestSplitGroup():
	g = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
	m = massCenter(g)
	a = splitGroup(g, m)
	print(a)
	
def mergeGroup(group1, massCenter1, group2, massCenter2):
	if not group1 or not group2:
		return null
		
	dis = distance(massCenter1, massCenter2)
	if dis > R:
		return null
	
	weight1 = len(group1)
	weight2 = len(group2)
	#std deviation
	mu = [(massCenter1[i] * weight1 + massCenter2[i] * weight2)/(weight1 + weight2) for i in range(len(massCenter1))]
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
	return group

def _utestMergeGroup():	
	g = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
	m = [[1, 1], [3, 3]]
	a = BuildGroup(g, m)
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
		step += 1
		
		#step 2
		massCenterList = [massCenter(g) for g in group]
	
		#step 3
		muList = []
		for i in range(len(group)):
			sg = splitGroup(group[i], massCenterList[i])
			#if split, then do not check for merge
			if sg:
				group.pop(i)
				massCenterList.pop(i)
				i -= 1
				muList += sg
				
		# where is the base point!???
				
		#step 4
		for i in range(len(group)):
			for j in range(len(group)):
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
		
		muList += massCenterList
		
		#step 5
		group = buildGroup(userList, muList)
		
		#step 6
		if len(lastMuList) != len(muList):
			continue
		
		error = [np.sqrt(1/len(lastMuList) * sum((lastMuList[i][j] - muList[i][j])**2 for i in group)) for j in range(len(group[0]))]
		error = sum(i^2 for i in error)
		
		lastMuList = muList
		
	return group, muList
				
if __name__ == '__main__':
	# _utestMassCenter()
	# _utestDistance()
	# _utestSplitGroup()
	# _utestMergeGroup()
	# _utestMergeGroup()
	a = [1, 2, 3, 4]
	a.pop(1)
	a.remove(2)
	print(a)
	