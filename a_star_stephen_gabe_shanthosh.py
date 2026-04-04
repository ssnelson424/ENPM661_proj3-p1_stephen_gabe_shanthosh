from collections import deque
from map_creation_stephen_gabe_shanthosh import create_board, prompt_user_node, prompt_user_step, is_obstructed_space
from math import cos
from math import sin
from queue import PriorityQueue
import matplotlib.pyplot as plt
from actions_stephen_gabe_shanthosh import move_factory, is_finished, find_dist_to_goal, bucketize


if __name__ == "__main__":
    #define data_structures
    node_queue = PriorityQueue()
    cost_dict = {}
    parent_dict = {}
    visualization_support=[]
    visualizataion_iterator = 0
    visualization_orientations = (0,0,0,0,0)
    
    
    given_width = 600
    given_height = 250
    
    game_board = create_board(given_width,given_height)
    
    start_point = prompt_user_node(game_board,"starting",given_width,given_height)
    goal_point = prompt_user_node(game_board,"goal",given_width,given_height)
    step_length = prompt_user_step()
    
    parent_dict[goal_point] = "Initial"
    cost_dict[bucketize(goal_point)] = find_dist_to_goal(goal_point,start_point)
    current_cost = 0+find_dist_to_goal(goal_point,start_point)
    initial_node = (current_cost,goal_point)
    
    node_queue.put(initial_node)
    current_node = node_queue.get()

    
    #Create move actions from the move factory function
    move_straight = move_factory(step_length, 0)
    move_right_30 = move_factory(step_length, 1)
    move_right_60 = move_factory(step_length, 2)
    move_left_30 = move_factory(step_length, -1)
    move_left_60 = move_factory(step_length, -2)
    
    #perform search
    while True:
        current_cost = current_node[0]
        current_position = current_node[1]

        #cost traveled (excluding estimate)
        cost_traveled = current_cost - find_dist_to_goal(current_position,start_point) + step_length
        
        #is this node near the goal node
        if is_finished(current_position,start_point,1.5):
            solution_found = True
            final_node = current_position
            print(f"search complete")
            break
        
        #perform moves to find new positions
        new_pos_list = []
        
        new_pos_list.append(move_straight(current_position))
        new_pos_list.append(move_left_30(current_position))
        new_pos_list.append(move_left_60(current_position))
        new_pos_list.append(move_right_30(current_position))
        new_pos_list.append(move_right_60(current_position))

        #iterate for each new position
        for new_pos in new_pos_list:
            
            new_cost = cost_traveled+find_dist_to_goal(new_pos,start_point)
            
            visualization_orientation_list = []
                           
            #bucketize position for simple comparison
            bucket_pos = bucketize(new_pos)            
        
            #check if new position is in a obstacle/interference space
            if is_obstructed_space(new_pos):
                continue
            else:
                visualization_orientation_list.append(new_pos[2])
                 
            #has node been visited before
            if bucket_pos in cost_dict:                  
                
                #is new pos a higher/equal cost
                if cost_dict[bucket_pos] <= new_cost:
                    continue
                
                #new pos is a lower cost
                else:                   
                    
                    #update cost dictionary
                    cost_dict[bucket_pos] = new_cost
                    
                    #update parent dictionary
                    parent_dict[new_pos] = current_position
                    
                    node_queue.put((new_cost,new_pos))
            
            #node has not be visited before
            else:
                node_queue.put((new_cost,new_pos))
                cost_dict[bucket_pos] = new_cost
                parent_dict[new_pos] = current_position
                
        if node_queue.empty():
            solution_found = False
            print("no solution")
            break
        
        current_node = node_queue.get()
        visualization_orientations = tuple(visualization_orientation_list)
        visualization_support.append((visualizataion_iterator,current_position,visualization_orientations))
        visualizataion_iterator += 1
        
    if solution_found:
        #backtracking
        back_path = deque()
        current_node = final_node
        
        while current_node != goal_point:
            
            back_path.append(current_node)
            current_node = parent_dict[current_node]

        