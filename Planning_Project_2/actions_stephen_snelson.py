# Stephen Snelson
# ENPM661-RO01 Planning for Autonomous Robots
# Project 2
# Robot Actions

from queue import PriorityQueue

def move_factory(x_change:int,y_change:int,cost_change:float):
    """creates a move function with input changes

    Args:
        x_change (int): movement in the x-direction
        y_change (int): movement in the y-direction
        cost_change (float): cost assosociated with move
    """
    
    def move_function(current_position:tuple,all_nodes:dict,node_queue:PriorityQueue):
        """function returned by move_factory

        Args:
            current_position (tuple): position provided by the program of the location being evaluated
            all_nodes (dict): dictionary of all node information explored by the program
            node_queue (PriorityQueue): list of nodes to be explored in order of lowest cost
        """

        #set current position and implement changes to x,y for new position
        x,y = current_position
        new_position = (x+x_change,y+y_change)
        
        #is the new position to be explored in obstacle('b') or interference ('r') space
        if all_nodes[new_position]["color"] in "br": 
            return
        
        #has this node been found before?
        elif all_nodes[new_position]["cost"] is None: 
            all_nodes[new_position] = {"color":'c',"parent":current_position,"cost":all_nodes[current_position]["cost"]+cost_change}
            node_queue.put((all_nodes[current_position]["cost"]+cost_change,new_position))
            return
        
        #is this a lower cost-to-go to this node 
        elif all_nodes[new_position]["cost"] > all_nodes[current_position]["cost"]+cost_change:   
            
            #if so, remove the "larger" cost-to-go cost from the priority queue
            storage_set = set()
            while not node_queue.empty():
                top_node = node_queue.get()
                
                #is the node removed from the node_queue the coordinate we are looking for?
                if top_node[1] == new_position:
                    while len(storage_set) != 0:
                        node_queue.put(storage_set.pop())
                    break
                #if not, add it to the storage set and keep get next node
                else:
                    storage_set.add(top_node)                    
            
            #update node information and node_queue with new node information (cost, parent, etc)
            all_nodes[new_position] = {"color":'c',"parent":current_position,"cost":all_nodes[current_position]["cost"]+cost_change}      
            node_queue.put((all_nodes[current_position]["cost"]+cost_change,new_position))
            return
        
        else:   # this route is higher cost, no changes to node_dictionary or priority queue
            return    
    
    #return the function
    return move_function  


