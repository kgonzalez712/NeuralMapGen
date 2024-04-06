import Graph

exampleList = [
    [1, [[1, 'Open Path', [274, 308]]]],
    [2, [[2, 'Open Path', [120, 329]], [3, 'Open Path', [368, 338]]]],
    [3, []],
    [4, []],
    [5, []]
    ]
class PathAnalyzer:
    def __init__(self):
        self.openPathList = []
        self.graph = Graph.Graph()

    def removeClosedPaths(self,pathList):
        rooms = pathList
        for room in rooms:
            pathList = []
            for path in room[1]:
                if(path[1] == 'Open Path'):
                    pathList.append((path[0],path[2]))
                elif(path[1] == 'Closed Path'):
                    pass
                else:
                    pathList.append(([]))
            self.openPathList.append(pathList)


    def createRoomsGraph(self):
        rooms = self.openPathList
        pendingList = []
        pendingFlag = False
        counter = 2
        previous = 1
        self.graph.add_node("Room 1")
        print("Room 1 Added")
        for room in rooms:
            
            print("Pending Nodes:",pendingList)
            print("Current room in list:", room)
            if (room == []):
                if (len(pendingList)>0):
                    pendingFlag = True

            for i in range(len(room)):
                if (pendingFlag == True):
                    print("Working pending nodes logic")
                    previous = pendingList.pop(0)
                    self.addToGraph(previous,counter)
                    pendingFlag = False
                    counter+=1
                    previous= counter - len(room) -1
                else:
                    print("Current path in list:", room[i])
                    self.addToGraph(previous,counter)
                    if(i!=0):
                        pendingList.append(counter)
                    counter+=1

                    print("------PATH END--------")
            if(pendingFlag == False):
                previous+=1


            print("----------------- \n")

                
    def addToGraph(self,previous,current):
        self.graph.add_node("Room "+str(current))
        self.graph.add_edge("Room "+str(previous),"Room "+str(current))
        print("Room added:",current)
        print("Conected to:",previous)
    
        


        

                    


a = PathAnalyzer()
list = a.removeClosedPaths(exampleList)
print(a.openPathList)
print("\n")
a.createRoomsGraph()
a.graph.print_graph()


