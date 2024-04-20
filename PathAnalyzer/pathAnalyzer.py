import Graph

exampleList = [
    [1, [[1, 'Open Path', [274, 308]]]],
    [2, [[2, 'Open Path', [120, 329]], [3, 'Open Path', [368, 338]]]],
    [3, []],
    [4, [[4, 'Open Path', [274, 308]]]],
    [5, [[5, 'Open Path', [120, 329]], [6, 'Open Path', [368, 338]]]],
    [6, []],
    [7, []]
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
        counter = 1
        previous = 0
        weight = 1
        self.graph.add_node(0)
        print("Room 0 Added")
        for room in rooms:
            
            print("Pending Nodes:",pendingList)
            print("Current room in list:", room)
            if (room == []):
                if (len(pendingList)>0):
                    pendingFlag = True

            for i in range(len(room)):
                if (pendingFlag == True):
                    weight += 1
                    print("Working pending nodes logic")
                    previous = pendingList.pop(0)
                    self.addToGraph(previous,counter, weight)
                    pendingFlag = False
                    counter+=1
                    previous= counter - len(room) -1
                else:
                    print("Current path in list:", room[i])
                    if(i!=0):
                        pendingList.append(counter)
                        self.addToGraph(previous,counter,weight + 1)
                    else:
                        self.addToGraph(previous,counter,weight)
                    counter+=1

                    print("------PATH END--------")
            if(pendingFlag == False):
                previous+=1


            print("----------------- \n")

                
    def addToGraph(self,previous,current,weight):
        self.graph.add_node(current)
        self.graph.add_edge(previous,current,weight)
        print("Room added:",current)
        print("Conected to:",previous)

    def getConnectedRoomsByWeight(self,rooms):
        """
        Analyzes a dictionary representing room connections and returns a dictionary 
        where keys are weights and values are lists of connected rooms at that weight.

        Args:
            rooms: A dictionary where keys are rooms and values are lists of 
                tuples (neighboring_room, weight).

        Returns:
            A dictionary with weights as keys and lists of connected rooms as values.
        """
        connectedWeight = {}
        uniqueWeights = set()
        for room in rooms.values():
            for connection in room:
                uniqueWeights.add(connection[1])  # Extract and add individual weights
        for weight in uniqueWeights:
            connectedRooms = []
            for room, connections in rooms.items():
                for neighbor, edge_weight in connections:
                    if edge_weight == weight:
                        connectedRooms.append(room)
            connectedWeight[weight] = connectedRooms
        return {key: [item for item in set(value)] for key, value in connectedWeight.items()}  # Set comprehension for unique values
        return  {key: [item for item in set(value)] for key, value in connectedWeight.items()}

        
        


        

                    


a = PathAnalyzer()
list = a.removeClosedPaths(exampleList)
print(a.openPathList)
print("\n")
a.createRoomsGraph()
a.graph.print_graph()
print("--------------\n")
rooms = a.graph.adj_list
print("--------------\n")
print(rooms)
print("--------------\n")
print(a.getConnectedRoomsByWeight(rooms))



