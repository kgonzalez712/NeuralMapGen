def getConnectedRoomsByWeight(rooms):
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
  return {key: list(dict.fromkeys(value)) for key, value in connectedWeight.items()}


# Example usage
room_connections = {'Room 0': [('Room 1', 1)], 'Room 1': [('Room 0', 1), ('Room 2', 1), ('Room 3', 2)], 'Room 2': [('Room 1', 1)], 'Room 3': [('Room 1', 2), ('Room 4', 2)], 'Room 4': [('Room 3', 2), ('Room 5', 2), ('Room 6', 3)], 'Room 5': [('Room 4', 2)], 'Room 6': [('Room 4', 3)]}
room_connections2 = {'Room 0': [('Room 1', 1)], 'Room 1': [('Room 0', 1), ('Room 2', 1), ('Room 3', 2)], 'Room 2': [('Room 1', 1)], 'Room 3': [('Room 1', 2), ('Room 4', 2)], 'Room 4': [('Room 3', 2), ('Room 5', 2), ('Room 6', 3)], 'Room 5': [('Room 4', 2)], 'Room 6': [('Room 4', 3)]}

weights_and_rooms = getConnectedRoomsByWeight(room_connections2)
print(weights_and_rooms)
