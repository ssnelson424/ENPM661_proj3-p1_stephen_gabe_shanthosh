from collections import deque
from map_create import create_board, prompt_user_node, prompt_user_step, is_obstructed_space
from math import cos, sin, radians
from queue import PriorityQueue
from actions import move_factory, is_finished, find_dist_to_goal, bucketize
import cv2
import numpy as np

def draw_map(game_board, width, height):
    obs_map = np.zeros((height, width, 3), dtype=np.uint8)

    colors = {
        "w": (255, 255, 255),  # free space
        "bk": (0, 0, 0),       # obstacle
        "r": (0, 0, 255),      # clearance
    }

    for (x, y), value in game_board.items():
        if 0 <= int(x) < width and 0 <= int(y) < height:
            if value["color"] == 'b':
                obs_map[int(y), int(x)] = colors["bk"]
            elif value["color"] == 'w':
                obs_map[int(y), int(x)] = colors["w"]
            elif value["color"] == 'r':
                obs_map[int(y), int(x)] = colors["r"]

    return obs_map


if __name__ == "__main__":
    #define data_structures
    node_queue = PriorityQueue()
    cost_dict = {}
    parent_dict = {}

    #used to support visualization following search/backtrack
    visualization_support = []
    visualizataion_iterator = 0
    visualization_orientations = (0,0,0,0,0)
    
    #board dimensions from spec
    given_width = 600
    given_height = 250
    scale = 3

    game_board = create_board(given_width, given_height)

    #start/goal/stel informatino from user
    start_point = prompt_user_node(game_board, "starting", given_width, given_height)
    goal_point = prompt_user_node(game_board, "goal", given_width, given_height)
    step_length = prompt_user_step()

    #fill in data structures with knew information
    parent_dict[goal_point] = None
    cost_dict[bucketize(goal_point)] = find_dist_to_goal(goal_point, start_point)
    current_cost = find_dist_to_goal(goal_point, start_point)
    initial_node = (current_cost, goal_point)
    node_queue.put(initial_node)

    #Create move actions from the move factory function
    move_straight = move_factory(step_length, 0)
    move_right_30 = move_factory(step_length, 1)
    move_right_60 = move_factory(step_length, 2)
    move_left_30 = move_factory(step_length, -1)
    move_left_60 = move_factory(step_length, -2)

    solution_found = False
    final_node = None

    #perform backwards A* search
    while not node_queue.empty():
        current_node = node_queue.get()
        current_cost = current_node[0]
        current_position = current_node[1]

        #cost traveled (excluding estimate)
        cost_traveled = current_cost - find_dist_to_goal(current_position, start_point) + step_length

        #is this node near the goal node
        if is_finished(current_position, start_point, 1.5):
            solution_found = True
            final_node = current_position
            print("search complete")
            break

        #perform moves to find new positions
        new_pos_list = []
        
        new_pos_list.append(move_straight(current_position))
        new_pos_list.append(move_left_30(current_position))
        new_pos_list.append(move_left_60(current_position))
        new_pos_list.append(move_right_30(current_position))
        new_pos_list.append(move_right_60(current_position))

        #data structure to store orientations of new nodes for use in visualizations later
        visualization_orientation_list = []

        #iterate for each new position
        for new_pos in new_pos_list:

            #determine new_cost for this node
            new_cost = cost_traveled + find_dist_to_goal(new_pos, start_point)
            
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
                    node_queue.put((new_cost, new_pos))

            #node has not be visited before
            else:
                #add node to queue to be explored
                node_queue.put((new_cost, new_pos))
                
                #update cost dictionary with "best" cost
                cost_dict[bucket_pos] = new_cost
                
                #update parent dictionary for backtracking purposes
                parent_dict[new_pos] = current_position

        #visualization support
        #turn visualization orientation from list to tuple 
        #this will be a list of orienation angle starting from a common point that do not end in obstacles
        visualization_orientations = tuple(visualization_orientation_list)
        
        #add this iteration's information to visualization support list (iterator:int,position:tuple[x,y,ori],valid orientations:tuple[30,60,0,-30,-60])
        visualization_support.append((visualizataion_iterator, current_position, visualization_orientations))
        
        #increase iterator by 1
        visualizataion_iterator += 1

    if not solution_found:
        print("no solution")

    #exploration

    init_map = draw_map(game_board, given_width, given_height)#makes a blank map to start
    snapshot = init_map.copy()

    visited_edges = set() #prevents repeat arrows
    batch_size = 75 #draws multiple explored nodes before refreshing the screen

    for i in range(0, len(visualization_support), batch_size): #for each batch in visualization support

        batch = visualization_support[i:i + batch_size]

        for _, pos, orientations in batch: #for each position/orientation in visualization support

            x, y, _ = pos

            # draw all theta orientations
            for theta in orientations:
                dx = step_length * cos(radians(theta))
                dy = step_length * sin(radians(theta))
                next_x = int(x + dx)
                next_y = int(y + dy)

                edge_key = ((int(x), int(y)), (next_x, next_y))

                # skips repeat arrows
                if edge_key in visited_edges:
                    continue
                visited_edges.add(edge_key) #adds all non-repeat arrows

                cv2.arrowedLine(snapshot,(int(x), int(y)),(next_x, next_y),(0, 180, 0),1,tipLength=0.25) #small dark green arrow

        frame_to_show = snapshot.copy()
        cv2.circle(frame_to_show, (int(start_point[0]), int(start_point[1])), 4, (255, 0, 0), -1)
        cv2.circle(frame_to_show, (int(goal_point[0]), int(goal_point[1])), 4, (0, 255, 0), -1)

        display = cv2.flip(frame_to_show, 0) #flips display so its not upside down since openCV is kinda goofy
        display = cv2.resize(display,(given_width * scale, given_height * scale),interpolation=cv2.INTER_NEAREST)

        cv2.imshow("exploration", display) #shows each frame

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # final finished explored display after animation is complete
    frame_to_show = snapshot.copy()
    cv2.circle(frame_to_show, (int(start_point[0]), int(start_point[1])), 4, (255, 0, 0), -1)
    cv2.circle(frame_to_show, (int(goal_point[0]), int(goal_point[1])), 4, (0, 255, 0), -1)

    display = cv2.flip(frame_to_show, 0)
    display = cv2.resize(
        display,
        (given_width * scale, given_height * scale),
        interpolation=cv2.INTER_NEAREST
    )
    cv2.imshow("exploration", display)
    key = cv2.waitKey(400)

    # backtracking
    if solution_found:

        back_path = deque()
        current = final_node
        while current is not None:
            back_path.appendleft(current)
            current = parent_dict[current]

        #display 
        final_snapshot = snapshot.copy() #makes the final path

        path_batch_size = 3 #draws multiple final path arrows before refreshing the screen

        for i in range(0, len(back_path) - 1, path_batch_size):
            for j in range(i, min(i + path_batch_size, len(back_path) - 1)):
                x1, y1, _ = back_path[j] #calls points from backpath
                x2, y2, _ = back_path[j + 1]
                cv2.arrowedLine(final_snapshot,(int(x1), int(y1)),(int(x2), int(y2)),(255, 0, 255),2,tipLength=0.12) #makes a magenta arrow for each point in the final path

            frame_to_show = final_snapshot.copy()
            cv2.circle(frame_to_show, (int(start_point[0]), int(start_point[1])), 4, (255, 0, 0), -1) #makes start and end again
            cv2.circle(frame_to_show, (int(goal_point[0]), int(goal_point[1])), 4, (0, 255, 0), -1)

            display = cv2.flip(frame_to_show, 0)
            display = cv2.resize(display,(given_width * scale, given_height * scale),interpolation=cv2.INTER_NEAREST)

            cv2.imshow("final path", display) #shows final snapshot with arrows

            if cv2.waitKey(40) & 0xFF == 27:
                break

        # final path

        frame_to_show = final_snapshot.copy()
        cv2.circle(frame_to_show, (int(start_point[0]), int(start_point[1])), 4, (255, 0, 0), -1)
        cv2.circle(frame_to_show, (int(goal_point[0]), int(goal_point[1])), 4, (0, 255, 0), -1)

        display = cv2.flip(frame_to_show, 0)
        display = cv2.resize(display,(given_width * scale, given_height * scale),interpolation=cv2.INTER_NEAREST)

        cv2.imshow("final path", display)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
