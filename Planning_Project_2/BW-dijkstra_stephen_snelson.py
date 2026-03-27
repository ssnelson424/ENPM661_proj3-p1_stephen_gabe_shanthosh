# Stephen Snelson
# ENPM661-RO01 Planning for Autonomous Robots
# Project 2
# Main File

from map_creation_stephen_snelson import create_board, prompt_user
import matplotlib.pyplot as plt
from queue import PriorityQueue
from actions_stephen_snelson import move_factory
from collections import deque
from animate_stephen_snelson import animate


if __name__ == "__main__":
    
    #board dimensions
    length = 180
    height = 50
    
    #create data structure to hold node information   
    all_nodes = {}     
    all_nodes = create_board(length,height)
    
    #create data structure to hold next node to explore
    node_queue = PriorityQueue() #(cost:int, cords:(x,y))
    
    #get start and goal nodes from user
    start_point = prompt_user(all_nodes,"starting")
    goal_point = prompt_user(all_nodes,"goal")
    
    #update node information data structure with start/goal information
    all_nodes[start_point]["color"] ='u'
    all_nodes[goal_point]={"color":'g',"parent":"Initial","cost":0}
    
    #add goal node (backward dijkstra) to explore next node
    current_node = (all_nodes[goal_point]["cost"],goal_point)
    node_queue.put(current_node)
    
    print(f"starting node is: {start_point}")
    print(f"goal node is: {goal_point}")       

    #create move functions (x_change,y_change,movement_cost)
    move_up = move_factory(0,1,1)
    move_down = move_factory(0,-1,1)
    move_right = move_factory(1,0,1)
    move_left = move_factory(-1,0,1)
    move_up_right = move_factory(1,1,1.4)
    move_down_right = move_factory(1,-1,1.4)
    move_up_left = move_factory(-1,1,1.4)
    move_down_left = move_factory(-1,-1,1.4)
    
    #create data strutures for plotting x and y cords
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
    
    #iterate while the start node is not popped from node_queue
    while current_node[1] != start_point:
        move_up(current_node[1],all_nodes,node_queue)
        move_down(current_node[1],all_nodes,node_queue)
        move_right(current_node[1],all_nodes,node_queue)
        move_left(current_node[1],all_nodes,node_queue)
        move_up_right(current_node[1],all_nodes,node_queue)
        move_down_right(current_node[1],all_nodes,node_queue)
        move_up_left(current_node[1],all_nodes,node_queue)
        move_down_left(current_node[1],all_nodes,node_queue)
        
        #current node becomes next node with lowest cost
        current_node = node_queue.get()
    
    #initiate backtracking
    backtrack_cord = start_point
    
    #create back_track data structure add "start point" to structure
    path_to_goal = deque()
    path_to_goal.append(backtrack_cord)
    all_nodes[backtrack_cord]["color"] = 'y'
    
    #while not at the "goal node"
    while (backtrack_cord != goal_point):
        backtrack_cord = all_nodes[backtrack_cord]["parent"]
        path_to_goal.append(backtrack_cord)
        all_nodes[backtrack_cord]["color"] = 'y'
        path_x.append(backtrack_cord[0])
        path_y.append(backtrack_cord[1])
        
    #fill x and y data structures with nodes of colors to be plotted
    for (x,y),value in all_nodes.items():
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
    plt.title("Dijkstra Search and Optimal Path Plot-Stephen Snelson")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc='upper left')
    
    #show plot
    print("Program will continue upon closure of the Plot window.")
    plt.show()    
    
    #Does user want to create GIF
    user_animation_input_validation = False
    while not user_animation_input_validation:
        print("Would you like me to animate the searching and pathfinding?")    
        user_animation_input = input("(Y/N): ")

        if len(user_animation_input) > 1:
            print("Please only one character response!")
            continue
        elif user_animation_input.upper() not in "YN":
            print("I dont know that command! Please try again.")
            continue
        else:
            user_animation_input_validation=True          
        
    #create GIF of search/path
    if user_animation_input.upper() == 'Y':
        print("Animating, this might take a few minutes!")
        animate(all_nodes,path_to_goal)
        print("Animation complete!")
    else:
        print("Roger, no animation. Program complete.")
    
        
    
    
        
    