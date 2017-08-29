import numpy.random as random
import matplotlib.pyplot as plt

weightMap = [                              \
    3,5,4,4,4,4,4,4,4,5,4,4,4,4,4,4,5,4,4,4,\
    3,5,5,4,4,4,4,4,4,5,2,2,2,3,2,2,5,3,0,3,\
    3,3,5,4,3,3,3,3,4,5,2,0,2,3,2,2,5,3,0,3,\
    2,3,5,4,3,3,2,3,4,5,2,0,2,3,2,2,5,3,2,2,\
    2,3,5,5,4,3,2,3,4,5,2,0,2,3,3,2,5,2,2,2,\
    2,3,3,5,4,3,3,3,4,5,3,3,2,2,3,2,5,2,2,2,\
    2,2,3,5,4,3,3,4,4,5,3,3,5,5,5,5,5,5,5,5,\
    3,3,3,5,5,4,5,5,5,5,5,5,4,4,4,3,5,2,2,2,\
    4,4,4,4,5,5,5,4,4,5,4,4,3,3,4,3,5,2,2,2,\
    3,3,2,3,5,3,3,3,2,5,4,2,2,3,4,3,5,2,2,2,\
    2,2,1,3,5,3,3,0,0,5,4,2,2,3,4,3,5,3,2,2,\
    1,1,0,2,5,3,3,0,0,5,3,2,2,3,4,3,5,3,2,2,\
    0,0,0,1,5,3,3,3,3,5,3,3,3,3,4,3,5,3,2,2,\
    0,0,0,1,3,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,\
    0,0,0,0,2,3,3,4,4,5,3,3,3,3,4,3,4,5,3,3,\
    0,0,0,0,0,1,3,4,4,5,3,2,2,3,4,3,4,5,2,2,\
    0,0,0,0,0,0,1,3,4,5,4,3,2,3,4,3,4,5,2,2,\
    0,0,0,0,0,0,1,2,3,5,4,3,3,4,4,3,4,5,2,2,\
    0,0,0,0,0,0,0,1,2,4,5,3,3,4,3,3,4,5,2,2,\
    0,0,0,0,0,0,0,0,2,4,5,3,3,4,3,3,4,5,2,2 \
]

row = 20
# sumWeight = sum(weightMap)
# probabilityMap = [i/sumWeight for i in weightMap]
sumWeight = sum(i**2 for i in weightMap)
probabilityMap = [i**2 /sumWeight for i in weightMap]

userNumber = 1000
userList = []

for i in range(userNumber):
    # if i > 0 and i * 100 % userNumber == 0:
        # print("Processing..{}%".format(i/100))
    r = random.ranf()
    x = random.ranf()
    y = random.ranf()

    for i in range(len(probabilityMap)):
        if r >= probabilityMap[i]:
            r -= probabilityMap[i]
        else:
            #-1000~1000 total, 100 per grid
            x = (i % row) * 100 + 100 * x - 1000
            y = (20 - 1 - int(i / row)) * 100 + 100 * y - 1000
            userList.append([x, y])
            plt.plot(x, y, 'r.')
            
            break

plt.savefig("userpoint-square.png")
plt.show()


file = open("user.txt", "w")
for u in userList:
    file.write(str(u))
    file.write('\n')
file.close()
            
# if __name__ == '__main__':
    # r1 = random.ranf()
    # print(r1)