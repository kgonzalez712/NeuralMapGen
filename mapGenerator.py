import pygame
import pygame.font
import PathAnalyzer.pathAnalyzer as PathAnalyzer
import PathFinder.pathFinder as PathFinder
import logger
import sys


# #TEST DATA
# exampleRoomsList1 = [
#   [1, []]
#   ]

# exampleRoomsList2 = [
#   [1, [[1, 'Open Path', [274, 308], '88.0%']]],
#   [2, []]
# ]

# exampleRoomsList3 = [
#   [1, [[1, 'Open Path', [274, 308], '87.0%']]],
#   [2, [[2, 'Open Path', [120, 329], '68.0%'], [3, 'Open Path', [368, 338], '89.0%']]],
#   [3, []],
#   [4, [[4, 'Open Path', [274, 308], '58.0%']]],
#   [5, [[5, 'Open Path', [120, 329], '78.0%'], [6, 'Open Path', [368, 338], '88.0%']]],
#   [6, []],
#   [7, []]
# ]


#Folder Paths
weightsPath = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/bestTS3.pt"
imagesFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/testImages"
outputFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/outputTest"

log = logger.NMGLogger("NMGLogger")


print("Starting Path Detection ...\n")
log("Starting path detecttion...")
pathFinder =  PathFinder.PathFinder(weightsPath,imagesFolder,outputFolder,log)
roomsList = pathFinder.detectPathsInFolder()
print("Rooms detected in images:\n")
print(roomsList)
print("\n")
print("Analyzing detected paths ...\n")
log("Analyzing detected paths ...")
pathAnalyzer = PathAnalyzer.PathAnalyzer(log)
print("\n")
print("Filtering dead ends and closed paths...")
log("Filtering dead ends and closed paths...")
pathAnalyzer.removeClosedPaths(roomsList)
print("Filtered path list: \n")
print(str(pathAnalyzer.openPathList))
print("\n")
print("Generating graph of the territory...")
log("Generating graph of the territory......")
pathAnalyzer.createRoomsGraph()
print("Graph of the territory: \n")
pathAnalyzer.graph.printGraph()
print("\n")
print("Creating an exploration strategy for the territory: \n")
log("Creating an exploration strategy for the territory: \n")
print("Exploration strategy: \n")
roomsDict = pathAnalyzer.graph.adjList
data = pathAnalyzer.getConnectedRoomsByWeight(roomsDict)
print(str(data))






# pathAnalyzer.removeClosedPaths(roomsList)
# print(pathAnalyzer.openPathList)
# pathAnalyzer.createRoomsGraph()
# pathAnalyzer.graph.printGraph()
# roomsDict = pathAnalyzer.graph.adjList
# data = pathAnalyzer.getConnectedRoomsByWeight(roomsDict)

# data = {
#     1: [0,1,2,3],
#     2: [1,4,5],
#     3: [5,6]
# }

def createRooms(window, data):
    """
    Creates rooms as rectangles based on the provided dictionary and connects them with lines.
    rooms with the same connected room number are red if they appear more than once
    within the entire data, and green otherwise. Other rooms within a row use light gray.
    Rectangles with the same connected room number are aligned horizontally across rows.

    Args:
        window (pygame.Surface): The Pygame window surface to draw on.
        data (dict): A dictionary with keys representing room numbers
                    and values as lists of connected room indices.
    """

    used_positions = set()
    margin = 30
    room_positions = {} 
    window_width, window_height = window.get_size()
    if (len(data)) != 0: 
        num_rows = len(data) 
    else: num_rows =1
    usable_width = 300 - 1.5 * margin
    usable_height = 300 - 1.5 * margin

    font = pygame.font.SysFont(None, 20)
    
    # Calculate usable area within the window after considering margins
    rect_width = usable_width // num_rows
    rect_height = usable_height // num_rows

    current_y = margin
    global total_drawable_height
    # Total height of all rectangles
    total_drawable_height = rect_height * num_rows 
    
    # Calculate usable area within the window after considering margins

    

    current_y = margin
    if (len(data)) == 0:
        color = (185,184,211)
        pygame.draw.rect(window, color, (100,100,100,50))
        text_surface = font.render("Only Room.  Press q to quit the program", True, (255,255,255))
        text_rect = text_surface.get_rect(center=(225, 75))
        window.blit(text_surface, text_rect)
    else:
        for row_num, (room_num, connected_rooms) in enumerate(data.items()):
            current_x = margin
            for i, connected_room in enumerate(connected_rooms):
                # Determine color based on overall appearance count
                appearance_count = sum(room.count(connected_room) for room in data.values())
                if appearance_count > 1:
                     # Light blue for rooms appearing more than once
                    color = (144,195,200)
                else:
                    # Light purple for rooms appearing once (including first time)
                    color = (185,184,211)  

                # Check for overlapping positions before drawing
                if connected_room not in room_positions or row_num == 0:
                    # New room or first row, calculate position based on current_x
                    rect = pygame.Rect(current_x, current_y, rect_width, rect_height)
                    room_positions[connected_room] = rect.x  # Store x-coordinate for alignment
                else:
                    # Use previously stored x-coordinate for alignment
                    current_x = room_positions[connected_room]
                    rect = pygame.Rect(current_x, current_y, rect_width, rect_height)

                pygame.draw.rect(window, color, rect) 
                used_positions.add((current_x, current_y))
                    
                room_text = f"Room: {connected_room}"
                room_surface = font.render(room_text, True, (0, 0, 0))
                drone_text = f"Drone #{room_num}"
                drone_surface = font.render(drone_text, True, (0, 0, 0))

                # Center the label on the rectangle
                room_x = rect.centerx - room_surface.get_width() // 2
                room_y = rect.centery - room_surface.get_height() // 2
                window.blit(room_surface, (room_x, room_y))
                window.blit(drone_surface, (room_x, room_y - 20))

                # Connect rectangles with lines (if not the last one in the row)
                if i < len(connected_rooms) - 1:
                    start_pos = (current_x + rect_width, current_y + rect_height // 2)
                    end_pos = (start_pos[0] + 10, start_pos[1])  
                    pygame.draw.line(window,(94,90,92), start_pos, end_pos, 50) 

                current_x += rect_width + 10  

            current_y += rect_height + 10  
            last_row_y = window_height - margin  
            label_text = "Press 'q' to quit or close the window."
            label_surface = font.render(label_text, True, (255,255,255)) 
            label_x = window_width // 2 - label_surface.get_width() // 2 
            label_y = last_row_y + margin // 2 

            # Draw the label on the window
            window.blit(label_surface, (label_x, label_y))

# Save image function
def saveMapImage(window, filename="Map.png"):
    """
    Saves the contents of the Pygame window as an image.

    Args:
        window (pygame.Surface): The Pygame window surface to save.
        filename (str, optional): The filename for the saved image. Defaults to "rectangles.png".
    """
    pygame.image.save(window, filename)  # Save the window surface as an image

log("Initializing Pygame")
print("Initializing Pygame")
pygame.init()

#window size
window_width = 1000
window_height = 1000
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#Window title
pygame.display.set_caption("Neural Map Generator")


log("Creating rooms and its connections...")
print("Creating rooms and its connections...")
createRooms(window, data)

log("Saving an image of the map...")
print("Saving an image of the map...")
saveMapImage(window)  # Use default filename (rectangles.png) or provide a custom filename

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Additional check for 'q' key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False  # Quit the program if 'q' is pressed
        
    # Update the display
    pygame.display.flip()
    
# Quit Pygame
pygame.quit()


