#Stephen Snelson, Gabe Szybalski, Shanthosh Raaj
#ENPM661 Planning
#Project 3 - Phase 1 - Backwards A*
#Main file/alogithm

from collections import deque
from map_creation_stephen_gabe_shanthosh import create_board, prompt_user_node, prompt_user_step, is_obstructed_space
from math import cos
from math import sin
from queue import PriorityQueue
from actions_stephen_gabe_shanthosh import move_factory, is_finished, find_dist_to_goal, bucketize

if __name__ == "__main__":
    #define data_structures
    node_queue = PriorityQueue()
    cost_dict = {}
    parent_dict = {}
    
    #used to support visualization following search/backtrack
    visualization_support=[]
    visualizataion_iterator = 0
    visualization_orientations = (0,0,0,0,0)
    
    #board dimensions from spec
    given_width = 600
    given_height = 250
    
    game_board = create_board(given_width,given_height)
    
    #start/goal/stel informatino from user
    start_point = prompt_user_node(game_board,"starting",given_width,given_height)
    goal_point = prompt_user_node(game_board,"goal",given_width,given_height)
    step_length = prompt_user_step()
    
    #fill in data structures with knew information
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
    
    #perform backwards A* search
    while True:
        current_cost = current_node[0]
        current_position = current_node[1] 

        #cost traveled (excluding estimate)
        cost_traveled = current_cost - find_dist_to_goal(current_position,start_point) + step_length
        
        #is this node near the goal node
        if is_finished(current_position,start_point,1.5):
            solution_found = True
            final_node = current_position
            print(f"Search Complete, Beginning Backtracking")
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
            
            #determine new_cost for this node
            new_cost = cost_traveled+find_dist_to_goal(new_pos,start_point)
            
            #data structure to store orientations of new nodes for use in visualizations later
            visualization_orientation_list = []
                           
            #bucketize position for simple comparison
            bucket_pos = bucketize(new_pos)            
        
            #check if new position is in a obstacle/interference space
            if is_obstructed_space(new_pos):
                continue
            
            else:
                #add the positions orientation to the visualized board map
                visualization_orientation_list.append(new_pos[2])
                 
            #has node been visited before?
            if bucket_pos in cost_dict:                  
                
                #is new pos a higher/equal cost? if so, skip
                if cost_dict[bucket_pos] <= new_cost:
                    continue
                
                #new pos is a lower cost? if so, add to priority queue
                else:                   
                    
                    #update cost dictionary to keep track of lowest cost
                    cost_dict[bucket_pos] = new_cost
                    
                    #update parent dictionary for backtracking purposes
                    parent_dict[new_pos] = current_position
                    
                    #add to priority queue to be explored
                    node_queue.put((new_cost,new_pos))
            
            #node has not be visited before
            else:
                #add node to queue to be explored
                node_queue.put((new_cost,new_pos))
                
                #update cost dictionary with "best" cost
                cost_dict[bucket_pos] = new_cost
                
                #update parent dictionary for backtracking purposes
                parent_dict[new_pos] = current_position
                      
        #visualization support
        #turn visualization orientation from list to tuple 
        #this will be a list of orienation angle starting from a common point that do not end in obstacles
        visualization_orientations = tuple(visualization_orientation_list)
        
        #add this iteration's information to visualization support list (iterator:int,position:tuple[x,y,ori],valid orientations:tuple[30,60,0,-30,-60])
        visualization_support.append((visualizataion_iterator,current_position,visualization_orientations))
        
        #increase iterator by 1
        visualizataion_iterator += 1
        
        #Pop next priority node from que
        while not node_queue.empty():        
            test_node = node_queue.get()
            test_cost, test_pos = test_node

            # accept only if this iteration is the best known path (remove duplicates)
            if cost_dict.get(bucketize(test_pos), float('inf')) == test_cost:
                current_node = test_node
                break
        else:
            #node que is empty - no solution found
            solution_found = False
            print("no solution")
            break
    
    #backtracking - only if there is a solution from start to goal
    if solution_found:
        #backtracking data structure
        back_path = deque()
        
        current_node = final_node
        
        #iterate through dictionary of parent nodes from start to finish
        while current_node != goal_point:
            
            back_path.append(current_node)
            current_node = parent_dict[current_node]
    print("Backtracking Complete, Begining Visualization")