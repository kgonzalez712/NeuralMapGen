import pygame
import pygame.font
import PathAnalyzer.pathAnalyzer as PathAnalyzer
from PathAnalyzer.Graph import *
import PathFinder.pathFinder as PathFinder

def create_rectangles(window, data):
    """
    Creates rectangles based on the provided dictionary and connects them with lines.
    Rectangles with the same connected room number are red if they appear more than once
    within the entire data, and green otherwise. Other rectangles within a row use light gray.
    Rectangles with the same connected_room number are aligned horizontally across rows.

    Args:
        window (pygame.Surface): The Pygame window surface to draw on.
        data (dict): A dictionary with keys representing room numbers
                     and values as lists of connected room indices.
    """

    used_positions = set()
    margin = 30
    room_positions = {}  # Dictionary to store positions of previously drawn rectangles for each room
    window_width, window_height = window.get_size()
    num_rows = len(data)
    max_rooms_per_group = max(len(rooms) for rooms in data.values()) if data else 0
    rect_width = (window_width - (max_rooms_per_group - 1) * 10) // max_rooms_per_group
    rect_height = window_height // len(data)
    font = pygame.font.SysFont(None, 20)  # Create a font object
    
    # Calculate usable area within the window after considering margins
    usable_width = window_width - 2 * margin
    usable_height = window_height - 2 * margin

    current_y = margin
    global total_drawable_height
    total_drawable_height = rect_height * num_rows  # Total height of all rectangles
    
    # Calculate usable area within the window after considering margins
    usable_width = 500 - 1.5 * margin
    usable_height = 500 - 1.5 * margin
    
    rect_width = (usable_width - (max_rooms_per_group - 1) * 10) // max_rooms_per_group
    rect_height = usable_height // num_rows

    current_y = margin
    for row_num, (room_num, connected_rooms) in enumerate(data.items()):
        current_x = margin
        for i, connected_room in enumerate(connected_rooms):
            # Determine color based on overall appearance count
            appearance_count = sum(room.count(connected_room) for room in data.values())
            if appearance_count > 1:
                color = (144,195,200) # Light blue for rooms appearing more than once
            else:
                color = (185,184,211)  # Light purple for rooms appearing once (including first time)

            # Check for overlapping positions before drawing
            if connected_room not in room_positions or row_num == 0:
                # New room or first row, calculate position based on current_x
                rect = pygame.Rect(current_x, current_y, rect_width, rect_height)
                room_positions[connected_room] = rect.x  # Store x-coordinate for alignment
            else:
                # Use previously stored x-coordinate for alignment
                current_x = room_positions[connected_room]
                rect = pygame.Rect(current_x, current_y, rect_width, rect_height)

            pygame.draw.rect(window, color, rect)  # Use color based on logic
            used_positions.add((current_x, current_y))
                
            # Create text surface with room number (use connected_room for current room)
            room_text = f"Room: {connected_room}"
            room_surface = font.render(room_text, True, (0, 0, 0))  # Black text
            drone_text = f"Drone #{room_num}"
            drone_surface = font.render(drone_text, True, (0, 0, 0))  # Black text

            # Center the label on the rectangle
            room_x = rect.centerx - room_surface.get_width() // 2
            room_y = rect.centery - room_surface.get_height() // 2
            window.blit(room_surface, (room_x, room_y))
            window.blit(drone_surface, (room_x, room_y - 20))

            # Connect rectangles with lines (if not the last one in the row)
            if i < len(connected_rooms) - 1:
                start_pos = (current_x + rect_width, current_y + rect_height // 2)
                end_pos = (start_pos[0] + 10, start_pos[1])  # Add a small offset for spacing
                pygame.draw.line(window,(94,90,92), start_pos, end_pos, 50)  # Blue lines, thickness 5

            current_x += rect_width + 10  # Move to the next rectangle

        current_y += rect_height + 10  # Move to the next row
        # Add a label below the last row
        last_row_y = window_height - margin  # Assuming margin is used for bottom padding
        label_text = "Press 'q' to quit or close the window."
        label_surface = font.render(label_text, True, (255,255,255))  # Black text
        label_x = window_width // 2 - label_surface.get_width() // 2  # Center the label
        label_y = last_row_y + margin // 2  # Place below last row with some margin

        # Draw the label on the window
        window.blit(label_surface, (label_x, label_y))

# Save image function
def save_window_image(window, filename="Map.png"):
    """
    Saves the contents of the Pygame window as an image.

    Args:
        window (pygame.Surface): The Pygame window surface to save.
        filename (str, optional): The filename for the saved image. Defaults to "rectangles.png".
    """
    pygame.image.save(window, filename)  # Save the window surface as an image

# Initialize Pygame
pygame.init()

#Folder Paths
weightsPath = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/bestTS4.pt"
imagesFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/testImages"
outputFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/outputTest"

# Set window size
window_width = 1000
window_height = 1000
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Set window title
pygame.display.set_caption("Rectangles from Dictionary with Connections")

# Sample data
data = {
    1: [0, 1, 2],
    2: [1, 3, 4, 5],
    3: [4, 6]
}

pathFinder =  PathFinder.PathFinder(weightsPath,imagesFolder,outputFolder)
roomsList = pathFinder.detectPathsInFolder()
pathAnalyzer = PathAnalyzer.PathAnalyzer()
pathAnalyzer.removeClosedPaths(roomsList)
pathAnalyzer.createRoomsGraph()
roomsDict = pathAnalyzer.graph.adj_list
#data = pathAnalyzer.getConnectedRoomsByWeight(roomsDict)



# Create rectangles and connections
create_rectangles(window, data)

save_window_image(window)  # Use default filename (rectangles.png) or provide a custom filename

# Main loop for handling events and updating the display
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
