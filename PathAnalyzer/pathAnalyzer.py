import os
from logger import NMGLogger


class PathAnalyzer:
    def __init__(self,logger:NMGLogger):
        self.openPathList = []
        self.graph = Graph()
        self.logger = logger

    def removeClosedPaths(self,pathList):
        rooms = pathList

        # print("Entering remove close paths")
        for room in rooms:
          if (len(rooms)==1):
            self.openPathList.append([])
            break
          pathList = []
          for path in room[1]:
              # print("Analizando path:")
              # print(path)
              if(path[1] == 'Open Path'):
                  # print("append")
                  pathList.append((path[0],path[2]))
                  # print(pathList)
              elif(path[1] == 'Closed Path' or path == []):
                  # print("elif")
                  pass
              else:
                  # print("else")
                  pathList.append(([]))
          self.openPathList.append(pathList)
      #self.openPathList.pop(0)


    def createRoomsGraph(self):
        rooms = self.openPathList
        pendingList = []
        pendingFlag = False
        counter = 2
        previous = 1
        weight = 1
        self.graph.addNode(1)
        print("Room added: 0")
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
        self.graph.addNode(current)
        self.graph.addEdge(previous,current,weight)
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
    
class Graph:
  #Graph representation using an adjacency list.


  def __init__(self, directed=False):
    """
    Initialize an empty graph.
    Args:
      directed: Boolean flag indicating if the graph is directed.
    """
    self.adjList = {}
    self.directed = directed
    

  def addNode(self, node):
    """
    Adds a new node to the graph.
    Args:
      node: The value of the new node.
    """
    if node not in self.adjList:
      self.adjList[node] = []

  def addEdge(self, source, destination, weight=1):
    """
    Adds an edge between two nodes.
    Args:
      source: The starting node of the edge.
      destination: The ending node of the edge.
      weight: Optional weight associated with the edge (default: 1).
    """
    # Check if nodes exist before adding edge
    if source not in self.adjList:
      self.addNode(source)
    if destination not in self.adjList:
      self.addNode(destination)

    self.adjList[source].append((destination, weight))

    # Add edge in the opposite direction for undirected graphs
    if not self.directed:
      self.adjList[destination].append((source, weight))

  def removeNode(self, node):
    """
    Removes a node from the graph.
    Args:
      node: The node to be removed.
    """
    if node in self.adjList:
      for neighbor, _ in self.adjList[node]:
        self.removeEdge(node, neighbor)
      del self.adjList[node]

  def removeEdge(self, source, destination):
    """
    Removes an edge between two nodes.
    Args:
      source: The starting node of the edge.
      destination: The ending node of the edge.
    """
    if source in self.adjList:
      for i, (neighbor, _) in enumerate(self.adjList[source]):
        if neighbor == destination:
          del self.adjList[source][i]
          break

  def neighbors(self, node):
    """
    Returns a list of neighbors for a given node.
    Args:
      node: The node for which to get neighbors.
    Returns:
      A list of neighboring nodes and their weights (if weighted).
    """
    if node in self.adjList:
      return self.adjList[node]
    return []

  def printGraph(self, filename="graph.txt"):
    """
    Prints the graph in a human-readable format and saves it to a txt file.

    Args:
        filename (str, optional): The filename to save the graph. Defaults to "graph.txt".
    """
    # Create Outputs/Graph directory if it doesn't exist
    output_dir = "Outputs/Graph"
    os.makedirs(output_dir, exist_ok=True)  # exist_ok prevents errors if folder exists

    # Build the string representation of the graph
    graph_string = ""
    for node, neighbors in self.adjList.items():
        graph_string += f"{node}: {', '.join(str(n) + (' (' + str(w) + ')' if w != 1 else '') for n, w in neighbors)}\n"

    # Save the string to a txt file
    with open(os.path.join(output_dir, filename), "w") as f:
        f.write(graph_string)

    # Print the graph to console for optional viewing
    print(graph_string)

 
#Test Code


# print(a.openPathList)
# print("\n")
# a.createRoomsGraph()
# a.graph.printGraph()
# print("--------------\n")
# rooms = a.graph.adjList
# print("--------------\n")
# print(rooms)
# print("--------------\n")
# print(a.getConnectedRoomsByWeight(rooms))
