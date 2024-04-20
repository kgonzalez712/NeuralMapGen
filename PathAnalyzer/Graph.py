import sys
sys.setrecursionlimit(10000)  # Increase to a larger value if needed
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


# Example usage
# graph = Graph()
# graph.add_edge(0, 1,1)
# graph.add_edge(0, 2, 1)
# graph.print_graph()


graph = Graph(directed=False)
graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "D")
graph.add_edge("D", "E")

source = "A"
graph.print_graph()
print(graph.adj_list)
all_paths = graph.get_all_paths(source)

print(f"All paths starting from '{source}':")
for path in all_paths:
  print(" -> ".join(path))