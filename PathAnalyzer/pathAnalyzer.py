
exampleList = [
    [1, [[1, 'Open Path', [274, 308]]]],
    [2, [[2, 'Open Path', [120, 329]], [3, 'Open Path', [368, 338]]]],
    [3, []],
    [4, [[4, 'Open Path', [274, 308]]]],
    [5, [[5, 'Open Path', [120, 329]], [6, 'Open Path', [368, 338]]]],
    [6, []],
    [7, []]
    ]

exampleList2 = [
    [1, [[1, 'Open Path', [120, 329]], [2, 'Open Path', [368, 338]]]],
    [2, []],
    [3, []]
    ]
class PathAnalyzer:
    def __init__(self):
        self.openPathList = []
        self.graph = Graph()

    def removeClosedPaths(self,pathList):
        rooms = pathList
        for room in rooms:
            pathList = []
            for path in room[1]:
                if(path[1] == 'Open Path'):
                    pathList.append((path[0],path[2]))
                elif(path[1] == 'Closed Path' or path == []):
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
    
class Graph:
  """
  This class represents a graph using an adjacency list.
  """

  def __init__(self, directed=False):
    """
    Initialize an empty graph.

    Args:
      directed: Boolean flag indicating if the graph is directed.
    """
    self.adj_list = {}
    self.directed = directed
    

  def add_node(self, node):
    """
    Adds a new node to the graph.

    Args:
      node: The value of the new node.
    """
    if node not in self.adj_list:
      self.adj_list[node] = []

  def add_edge(self, source, destination, weight=1):
    """
    Adds an edge between two nodes.

    Args:
      source: The starting node of the edge.
      destination: The ending node of the edge.
      weight: Optional weight associated with the edge (default: 1).
    """
    # Check if nodes exist before adding edge
    if source not in self.adj_list:
      self.add_node(source)
    if destination not in self.adj_list:
      self.add_node(destination)

    self.adj_list[source].append((destination, weight))

    # Add edge in the opposite direction for undirected graphs
    if not self.directed:
      self.adj_list[destination].append((source, weight))

  def remove_node(self, node):
    """
    Removes a node from the graph.

    Args:
      node: The node to be removed.
    """
    if node in self.adj_list:
      for neighbor, _ in self.adj_list[node]:
        self.remove_edge(node, neighbor)
      del self.adj_list[node]

  def remove_edge(self, source, destination):
    """
    Removes an edge between two nodes.

    Args:
      source: The starting node of the edge.
      destination: The ending node of the edge.
    """
    if source in self.adj_list:
      for i, (neighbor, _) in enumerate(self.adj_list[source]):
        if neighbor == destination:
          del self.adj_list[source][i]
          break

  def neighbors(self, node):
    """
    Returns a list of neighbors for a given node.

    Args:
      node: The node for which to get neighbors.

    Returns:
      A list of neighboring nodes and their weights (if weighted).
    """
    if node in self.adj_list:
      return self.adj_list[node]
    return []

  def is_connected(self, source, destination):
    """
    Checks if there is a path between two nodes.

    This implementation uses a basic Depth-First Search (DFS) to 
    check connectivity. More advanced algorithms can be used for 
    different purposes.

    Args:
      source: The starting node.
      destination: The ending node.

    Returns:
      True if there is a path, False otherwise.
    """
    if source not in self.adj_list:
      return False
    visited = set()
    return self._dfs(source, destination, visited)

  def _dfs(self, node, destination, visited):
    """
    Helper function for the is_connected method (DFS).

    Args:
      node: The current node being explored.
      destination: The ending node to find.
      visited: Set to keep track of visited nodes.

    Returns:
      True if the destination is found, False otherwise.
    """
    visited.add(node)
    if node == destination:
      return True
    for neighbor, _ in self.adj_list[node]:
      if neighbor not in visited:
        if self._dfs(neighbor, destination, visited):
          return True
    return False

  def print_graph(self):
    """
    Prints the graph in a human-readable format.
    """
    for node, neighbors in self.adj_list.items():
      # Print the node with its neighbors and weights (if weighted)
      print(f"{node}: {', '.join(str(n) + (' (' + str(w) + ')' if w != 1 else '') for n, w in neighbors)}")

  def get_all_paths(self, source):
    """
    Returns a list containing all possible paths starting from the 
    given source node and reaching any reachable node.

    This function uses Depth-First Search (DFS) to explore the graph 
    forward, keeping track of the current path. Backtracking is 
    not allowed (i.e., visiting a node already in the current path).

    Args:
      source: The starting node for finding paths.

    Returns:
      A list containing all possible paths as lists of nodes.
    """
    if source not in self.adj_list:
      return []

    paths = []
    visited = set()

    def _dfs_paths(node, current_path):
      visited.add(node)
      current_path.append(node)
      

      # Check if a path has reached an end node (no neighbors)
      if not self.adj_list[node]:
        paths.append(current_path.copy())  # Append a copy to avoid modification

      for neighbor, _ in self.adj_list[node]:
        if neighbor not in visited:
          _dfs_paths(neighbor, current_path)

      # Backtracking is not allowed, so remove the current node before returning
      current_path.pop()
      visited.remove(node)

    _dfs_paths(source, [])
    return paths                 
#Test Code

a = PathAnalyzer()
list = a.removeClosedPaths(exampleList2)
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



[[1, 'Open Path', [120, 329]], [2, 'Open Path', [368, 338]]]
[(1, 'Open Path', [2817, 2186], '67.0%'), []]