import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap, BoundaryNorm
from collections import deque

def animate(all_nodes:dict,path_to_goal:deque)->None:
    """animates the search and the backtracking of the path.
    Summary:
        Uses obstacle and interference points to make a "base map"
        Finds all the cost thresholds and sorts all nodes into a dict with key:cost, value:[list of all nodes w/ said cost]
        Creates(plots) an image based changed by the increaseing cost threshhold -> saves each image in search_image_library
        Follows the provided backtracking cost and creates a new image with the next path node highlighted
        Merges those lists together
        Passes image_library to matlab animator
        Saves GIF as "dijkstra_stephen_snelson.GIF"

    Args:
        all_nodes (dict): dictionary containing all the node information found during search
        path_to_goal (deque): double-queue of the optimal path from the start to goal
        
    Returns:
        technically nothing, saves a GIF "dijkstra_stephen_snelson.GIF" with the animated search/backtracking
    """
    
    #list to maintaing the location of obstacles and interference space
    obstacles_points = []
    interference_points = []
    
    #creates a dictionary to track all of the costs and sort all nodes by cost
    cost_dictionary = {}  
    
    #Iterate through all node information dictionary
    for key, value in all_nodes.items():
        
        cost = value["cost"]
        color = value["color"]
        
        #If this is an obstacle/interference node, add to cords to obstacle/interference lists
        if cost is None:
            if color == 'b':
                obstacles_points.append(key)
            elif color == 'r':
                interference_points.append(key)
            continue
        
        #If this is a new cost, create a new cost threshold
        if cost not in cost_dictionary:
            cost_dictionary[cost] = []
        
        #add cords to associated cost list in cost dictionary
        cost_dictionary[cost].append(key)
    
    #create search image datastructures
    search_image_library = []
    current_image = []
    
    #iterate through cost dictionary, add the coordinates of changed (explored) nodes to each image, then save it in the search_image_library
    for threshold in sorted(cost_dictionary.keys()):
        current_image.extend(cost_dictionary[threshold])
        search_image_library.append(current_image.copy())
    
    
    #create optimal path image data structures
    path_image_library = []
    path = []
    
    #add the coordinates from the path to goal to the path_image_library
    for cords in path_to_goal:
        path.append(cords)
        path_image_library.append(path.copy())    
    
    
    #plot the images
 
    #plot details
    figure, axes = plt.subplots(figsize=(12,6))       
    axes.set_xlim(0,180)
    axes.set_ylim(0,50)
    axes.set_aspect("equal")
    
    #plot the base image of the obstacle/interference for every image
    axes.scatter([x for x,y in obstacles_points],[y for x,y in obstacles_points], c="black",s=60,marker="s")
    axes.scatter([x for x,y in interference_points],[y for x,y in interference_points], c="red",s=60,marker="s")
    
    #search will be done in cyan, path in gold
    search_scatter = axes.scatter([],[],c="cyan")    
    path_scatter = axes.scatter([],[],c="yellow",s=35)
    
    #animation parameters    
    fps = 60
    interval = 200
    
    #add frames at end of image to show optimal path before restarting GIF
    end_of_gif_pause = 3 #seconds
    pause_frames = int (end_of_gif_pause * 100*fps/200)    
    for iterator in range(pause_frames):
        path_image_library.append(path_image_library[-1])
        
    total_frames = len(search_image_library)+len(path_image_library)+pause_frames
    
    def update(frame):
        #if searching
        if frame < len(search_image_library):
            search_points = search_image_library[frame]
            search_scatter.set_offsets(np.array(search_points) if search_points else np.empty((0,2)))
            axes.set_title("Backwards Dijkstra Search")
        
        #if pathfinding
        elif frame < len(search_image_library)+len(path_image_library):
            #keep the searched nodes on the plot
            search_scatter.set_offsets(np.array(search_image_library[-1]))
            
            #update plot with
            path_frame = frame - len(search_image_library)
            current_path_point = path_image_library[path_frame]
            path_scatter.set_offsets(np.array(current_path_point) if current_path_point else np.empty((0,2)))                      
            axes.set_title("Drawing Optimal Path")
        
        else:
            path_scatter.set_offsets(np.array(path_image_library[-1]))
            axes.set_title("Search/Pathfinding Complete")    

    
    animation = FuncAnimation(figure, update, frames=total_frames, interval=interval)
    
    animation.save("dijkstra_stephen_snelson.gif",writer=PillowWriter(fps=fps))    
    
    print("Animation saved in folder as 'djikstra_stephen_snelson.gif'")