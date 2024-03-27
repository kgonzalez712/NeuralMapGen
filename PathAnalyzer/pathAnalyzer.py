exampleList = [[0, [[0, 'Open Path', [274, 308], '88.0%']]], [1, [[1, 'Open Path', [368, 338], '89.0%'], [2, 'Open Path', [120, 329], '89.0%']]]]
class PathAnalyzer:
    def __init__(self):
        self.unitsNo = 1
        self.openPathList = []

    def removeClosedPaths(self,pathList):
        rooms = pathList
        for room in rooms:
            print ("Room:",room)
            pathList = []
            for path in room[1]:
                print ("Path:",path)
                if(path[1] == 'Open Path'):
                   print ("PathList:",pathList)
                   pathList.append((path[0],path[2]))
            self.openPathList.append(pathList)

    def defineExplorationInformation(self):
        currentUAV = 0
        uavNeeded = 1

        openPaths = self.openPathList
        # for path in openPaths:
        #     if (a):

                    


a = PathAnalyzer()
list = a.removeClosedPaths(exampleList)
print(a.openPathList)


