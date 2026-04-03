from collections import deque
from map_create import create_board, prompt_user_node
from math import cos
from math import sin
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    #step 1: Define Actions in a Mathematical Format
    
    def move_factory(step_length:float,angle_change:int):
        """creates a move function with input changes

        Args:10,10
            step_length(float): step length defined by the user
            angle_change (int): angle change * 30degs (0 is straight, 1 is 30 deg, -1 is -30, etc)
        """
    
        def move_function(current_position:tuple):
            """function returned by move_factory

            Args:
                current_position (tuple): position provided by the program of the location being evaluated
                
            """
            
            #set current position and implement changes to x,y,phi for new position
            x,y,ori = current_position
            
            new_ori = (ori + angle_change * 30)%360
            
            new_x = x + step_length*cos(new_ori)
            new_y = y + step_length*sin(new_ori)
            
            return (new_x, new_y, new_ori)
    
        #return the function
        return move_function  
    
    #step 2: Find the mathematical Format for free space
        #equations must account for the 5 mm clearance of the robot
        #height 250 width 600
    
    given_width = 600
    given_height = 250
    
    game_board = create_board(given_width,given_height)
    
    start_point = prompt_user_node(game_board,"starting",given_width,given_height)
    goal_point = prompt_user_node(game_board,"goal",given_width,given_height)
    
    #User Input Step Length
    length_validation = False
    while not length_validation:
        step_length_str = input("Please enter an step length (float) between 1 and 10 (inclusive): ")
        if not all(c in "0123456789." for c in step_length_str):
            print("Please only enter numeric values for step length and only intiger values!")
            continue
        
        if step_length_str.count(".") > 1:
            print("There are too many decimal points, please enter a valid float value!")
            continue
        
        step_length = float(step_length_str)
        
        if 1 <= step_length <= 10:
            length_validation = True        

    #Create move actions from the move factory function
    move_straight = move_factory(step_length, 0)
    move_right_30 = move_factory(step_length, 1)
    move_right_60 = move_factory(step_length, 2)
    move_left_30 = move_factory(step_length, -1)
    move_left_60 = move_factory(step_length, -2)
    
    #_____________BELOW THIS IS ALL VISUALIZATION STUFF TO BO DELETED___________________


import cv2
import numpy as np

obs_map = np.zeros((given_height, given_width, 3), dtype=np.uint8)

colors = {
    "w": (255, 255, 255), #white
    "bk": (0, 0, 0), #black
    "r": (0, 0, 255), #red
    "cy": (255, 255, 0), #cyan
    "y": (255, 255, 255), #yellow
    "bl": (255, 0, 0), #blue
    "g": (0, 255, 0), #green
    

}
for (x, y), value in game_board.items():
    if value["color"] == 'b':
        color = colors["bk"]
    elif value["color"] == 'w':
        color = colors["w"]
    elif value["color"] == 'r':
        color = colors["r"]
    elif value["color"] == 'c':
        color = colors["cy"]
    else:
        continue

    if 0<=x<given_width and 0<=y<=given_height:
        obs_map[int(y),int(x)] = color
cv2.circle(obs_map, (int(start_point[0]), int(start_point[1])), 3, colors["bl"], -1)
cv2.circle(obs_map, (int(goal_point[0]), int(goal_point[1])), 3, colors["g"], -1) 

#for x, y in zip(path_x, path_y):
#    cv2.circle(obs_map, (int(x), int(y)), 1, colors["y"], -1)

obs_map = cv2.flip(obs_map, 0)

scale = 3

resized = cv2.resize(obs_map, (given_width*scale, given_height*scale), interpolation=cv2.INTER_NEAREST)

cv2.imshow("A* Search Visualization", resized)
print("Press any key to continue...")
cv2.waitKey(0)
cv2.destroyAllWindows()