from collections import deque
from map_creation_stephen_gabe_shanthosh import create_board, prompt_user_node
from math import cos
from math import sin
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    #step 1: Define Actions in a Mathematical Format
    
    def move_factory(step_length:float,angle_change:int):
        """creates a move function with input changes

        Args:
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
            
            new_ori = ori + angle_change * 30
            
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
    #green
    starting_x = [start_point[0]]
    starting_y = [start_point[1]]
    #blue
    goal_x = [goal_point[0]]
    goal_y = [goal_point[1]]
    #black
    obstacle_x =[]
    obstacle_y = []
    #white
    empty_x = []
    empty_y = []
    #red
    interference_x = []
    interference_y = []
    #cyan
    visited_x = []
    visited_y = []
    #yellow
    path_x = []
    path_y = []
    
    #fill x and y data structures with nodes of colors to be plotted
    for (x,y),value in game_board.items():
        if value["color"] == 'b':
            obstacle_x.append(x)
            obstacle_y.append(y)
        elif value["color"] == 'w':
            empty_x.append(x)
            empty_y.append(y)
        elif value["color"] == 'r':
            interference_x.append(x)
            interference_y.append(y)
        elif value["color"] == 'c':
            visited_x.append(x)
            visited_y.append(y)
    
    #plot each set of x/y lists
    plt.scatter(empty_x, empty_y, c="white", label = "Empty Space")
    plt.scatter(interference_x,interference_y, c="red", label = "Robot Radius of Interference")
    plt.scatter(obstacle_x,obstacle_y, c ="black", edgecolors="black", label = "Obstacles")
    plt.scatter(visited_x,visited_y, c="cyan", label = "Explored Nodes")
    plt.scatter(path_x,path_y, c="yellow",label ="Optimal Path")
    plt.scatter(starting_x,starting_y, c="blue", label ="Starting Point")
    plt.scatter(goal_x,goal_y, c="green", label ="Goal Point")
    
    #plot labels
    plt.title("A* Search and Optimal Path Plot - Stephen Gabe Shanthosh")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc='upper left')
    
    #show plot
    print("Program will continue upon closure of the plot window.")
    plt.show()    