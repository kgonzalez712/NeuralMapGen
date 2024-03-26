exampleList = [[0, [['Open Path', [274, 308], '88.0%']]], [1, [['Open Path', [120, 329], '89.0%'], ['Closed Path', [368, 338], '89.0%']]]]

class PathAnalizer:
    def __init__(self):
        self.unitsNo = 1
        self.openPathList = []

    def removeClosedPaths(self,pathList):
        rooms = pathList
        for room in rooms:
            for i in range(len(room[1])):
                if (room[1][i][0] == 'Closed Path'):
                    room[1].pop(i)


    
    # def calculateUAVNumber(pathList):
    #     uavId = 0
    #     actualUAV = uavId
    #     for room in pathList:

a = PathAnalizer()
print(exampleList)
list = a.removeClosedPaths(exampleList)

print(exampleList)
