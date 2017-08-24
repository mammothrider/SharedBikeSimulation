#Simulation
#根据用户位置信息生成站点并计算站点最优位置
#算法：
#假设站点有最大距离，用成本进行计算
#所有未注册过的点计算出一个最佳位置的新站点N，不考虑服务距离
#所有点计算一轮成本，并在车站注册，考虑服务距离
#如果成本变化小于特定值，如0.5，返回最后的成本
#如果大于之前成本，则返回之前成本
#所有车站根据注册点计算最佳位置，向最佳位置移动

userPosition = [[0, 0]]

def loadUserPosition():
	pass
	
def massCenter(userList):
	if (!userList)
		return null;
	x, y = zip(*(userList))
	x, y = sum(x)/len(x), sum(y)/len(y)
	return [x, y]
	
def _utestMassCenter():
	a = [[1, 1], [2, 2], [3, 3], [-1, -1], [-2, -2], [-3, -3]]
	print(minimumCostPosition(a))
	
def distance(p1, p2):
	if (!p1 || !p2)
		return null
		
	x = p1[0] - p2[0]
	y = p1[1] - p2[1]
	return x * x + y * y
	

	
if __name__ == '__main__':
	# _utestMassCenter()

	