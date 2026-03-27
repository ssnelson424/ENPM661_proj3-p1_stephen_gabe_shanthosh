# Stephen Snelson
# ENPM661-RO01 Planning for Autonomous Robots
# Project 2
# Map Creation

def mark_obstacle(x:int,y:int) -> dict:
    """marks a node as part of an obstacle by changing the color to black

    Args:
        node ((x,y) coordinates, color])

    Returns:
        dictionary object key is the coordaintes, node color is black, no additional keys
    """
    return {(x,y):{"color":'b',"cost":None}}

def mark_clear_space(x:int,y:int) -> dict:
    """marks a node as traversable space for the robot

    Args:
        x (int): node's x-coordinates
        y (int): node's y-coordinates
    
    Returns:
        dictionary object key is the coordaintes, node color is black, parent node and cost-to-go are empty
    """
    return {(x,y):{"color":'w',"parent":None,"cost":None}}

def mark_interference(x:int,y:int) -> dict:
    """marks a node as within the robots interference size (2 cms)

    Args:
        x (int): node's x-coordinates
        y (int): node's y-coordinates
        
    Returns:
        dictionary object key is the coordaintes, node color is red, no additional keys
    """
    return {(x,y):{"color":'r',"cost":None}}

def prompt_user(all_nodes:dict, node_name:str)->tuple:

    data_verification = False
    while not data_verification:
        print(f"Please define a {node_name} point (x,y)")
        user_input = input("please enter integers 0-180 for x, and 0-50 for y seperated by a comma: ")
        
        if "," not in user_input:
            print("I only see one value, please enter two coordinates")
            continue
        
        elif user_input.count(",") > 1:
            print("There are too many numbers there, please enter only 1 comma.")
            continue
        
        elif not all(c in "0123456789," for c in user_input):
            print("There are non-intiger, non-comma characters! Please enter only intigers and commas.")
            continue
        
        else:
            x,y = map(int,user_input.split(","))
        
        if x < 0 or x > 180 or y > 50 or y < 0:
            print("that location is out of bounds, please enter a locations betwen 0<= x <= 180 and 0<= y <=50")
            continue
        
        else:        
            if all_nodes[(x,y)]["color"]!='w':
                print(f"That node is within an obstacle and is not a valid {node_name} point! Please enter another node.")                        
                continue
            else:
                print(f"Thank you, {node_name} nodes is {x,y}")
                data_verification = True
                break

            

    origin = (x,y)

    return origin
    
def create_board(length, height)->dict:
    """creates a set of nodes and determines if they are within pre-determiend obstacles

    Args:
        length (int): length of desired board in cm
        height (_type_): height of desired board in cm
    """
    
    #board dimensions in cms
    board_length = range(length)
    board_height = range(height)
    
    #create data structure to hold node information
    node_dict = {}

    #determine nodes which are in obstacles
    for x in board_length:
        for y in board_height:
            
            #set boundry nodes
            if x == 0 or x == length-1 or y == 0 or y == height-1:
                node_dict.update(mark_obstacle(x,y))

            #set boundry interferences
            elif x <= 2 or x >= length-3 or y <= 2 or y >= height -3:
                node_dict.update(mark_interference(x,y))
            
            #top of 1st "S"
            elif 16 <= (x-22)**2 + (y-31)**2 <= 49 and y >= 31:
                node_dict.update(mark_obstacle(x,y))
            
            #top/mid of 1st "S"
            elif 16 <= (x-22)**2 + (y-31)**2 <= 49 and x <= 22 and y <= 31:
                node_dict.update(mark_obstacle(x,y))           
          
            #bottom/mid of 1st "S"
            elif 16 <= (x-22)**2 + (y-20)**2 <= 49 and x >= 22 and y >= 20:
                node_dict.update(mark_obstacle(x,y))    
            
            #bottom of 1st "S"
            elif 16 <= (x-22)**2 + (y-20)**2 < 49 and y <= 20:
                node_dict.update(mark_obstacle(x,y))
            
            #top of 1st "S" - interference
            elif (x-22)**2 + (y-31)**2 <= 81 and y >= 29:
                node_dict.update(mark_interference(x,y))
                
            #top/mid of 1st "S" - interference
            elif (x-22)**2 + (y-31)**2 <= 81  and x<= 22 and y <= 31:
                node_dict.update(mark_interference(x,y))
            
            #mid/bot of 1st "S" - interference               
            elif (x-22)**2 + (y-20)**2 <= 81 and x >= 22 and y >= 20:
                node_dict.update(mark_interference(x,y))
            
            #bottom of 1st "S" - interference     
            elif (x-22)**2 + (y-20)**2 < 81 and y <= 22:
                node_dict.update(mark_interference(x,y))        
                
            #left left of "W"
            elif -5*x + 218 <= y <= -5*x + 233 and 13 <= y <=38:
                node_dict.update(mark_obstacle(x,y))  
            
            #left-middle of "W"
            elif 5*x - 192 >= y >= 5*x - 208 and 13 <= y <=38:
                node_dict.update(mark_obstacle(x,y))     
            
            #right-middle of "W"
            elif -5*x + 273 <= y <= -5*x + 288 and y>=13 and y<=38:
                node_dict.update(mark_obstacle(x,y))                   
            
            #right-right of "W"
            elif y <= 5*x - 248 and y>= 5*x - 262 and y>=13 and y<=38:
                node_dict.update(mark_obstacle(x,y))
            
            #left left of "W" - interference            
            elif y >= -5*x + 208 and y <= -5*x + 243 and y>=11 and y<=40:
                node_dict.update(mark_interference(x,y))
                
            #left mid of "W" - interference
            elif y <= 5*x - 183 and y>= 5*x - 218 and y>=11 and y<=40:
                node_dict.update(mark_interference(x,y))   
            
            #right mid of "W" - interference
            elif y >= -5*x+263 and y <= -5*x + 298 and y>=11 and y<=40:
                node_dict.update(mark_interference(x,y))  
            
            #right right of "W" - interference
            elif y <= 5*x - 238 and y>= 5*x - 273 and y>=11 and y<=40:
                node_dict.update(mark_interference(x,y))       
                
            #top of 2nd "S"
            elif 16 <= (x-74)**2 + (y-31)**2 <= 49 and y >= 31:
                node_dict.update(mark_obstacle(x,y))
         
            
            #top/mid of 2nd "S"
            elif 16 <= (x-74)**2 + (y-31)**2 <= 49 and x <= 74 and y <= 31:
                node_dict.update(mark_obstacle(x,y))
                
            
            #bottom/mid of 2nd "S"
            elif 16 <= (x-74)**2 + (y-20)**2 <= 49 and x >= 74 and y >= 20:
                node_dict.update(mark_obstacle(x,y))        
            
            #bottom of 2nd "S"
            elif 16 <= (x-74)**2 + (y-20)**2 < 49 and y <= 20:
                node_dict.update(mark_obstacle(x,y))
        
            #top of 2nd "S" - interference
            elif (x-74)**2 + (y-31)**2 <= 81 and y >= 29:
                node_dict.update(mark_interference(x,y))
                
            #top/mid of 2nd "S" - interference
            elif (x-74)**2 + (y-31)**2 <= 81 and x <= 74 and y <= 31:
                node_dict.update(mark_interference(x,y))
            
            #mid/bot of 2nd "S" - interference               
            elif (x-74)**2 + (y-20)**2 <= 81 and x >= 74 and y >= 20:
                node_dict.update(mark_interference(x,y))
            
            #bottom of 2nd "S" - interference     
            elif (x-74)**2 + (y-20)**2 < 81 and y <= 22:
                node_dict.update(mark_interference(x,y))                
            
            #cross of 1st "4"
            elif 88 <= x  <= 101 and 17 < y <= 20:
                node_dict.update(mark_obstacle(x,y))              
            
            #height of 1st "4"
            elif 96 < x <= 99 and 13 <= y <= 38:
                node_dict.update(mark_obstacle(x,y))        

            #slant of 1st "4"
            elif 3*x -253 <= y <= 3*x-244 and 20 <= y <= 38:
                node_dict.update(mark_obstacle(x,y))  
        
            #cross of 1st "4"  - interference
            elif 86 <= x  <= 103 and 15< y <= 22:
                node_dict.update(mark_interference(x,y))              
            
            #height of 1st "4" - interference
            elif 94 <= x <= 101 and 11 <= y <= 40:
                node_dict.update(mark_interference(x,y))        

            #slant of 1st "4" - interference
            elif 3*x -259 <= y <= 3*x-238 and 18 <= y <= 40:
                node_dict.update(mark_interference(x,y))                           
                
            #top of "0"
            elif 16 <= (x-116)**2 + (y-31)**2 <= 49 and y >= 31:
                node_dict.update(mark_obstacle(x,y))        
            
            #left side of "0"
            elif 109 <= x <= 112 and 20 <= y <= 31:
                node_dict.update(mark_obstacle(x,y))        
            
            #right side of "0"
            elif 120 <= x <= 123 and 20 <= y <= 31:
                node_dict.update(mark_obstacle(x,y))        
            
            #bottom of "0"
            elif 16 <= (x-116)**2 + (y-20)**2 <= 49 and y<=20:
                node_dict.update(mark_obstacle(x,y))
                
            #top of "0" - interferences
            elif (x-116)**2 + (y-31)**2 <= 81 and y >= 31:
                node_dict.update(mark_interference(x,y))        
            
            #left side of "0" - interferences
            elif 107 <= x <= 116 and 20 <= y <= 31:
                node_dict.update(mark_interference(x,y))        
            
            #right side of "0" - interferences
            elif 116 <= x <= 125 and 20 <= y <= 31:
                node_dict.update(mark_interference(x,y))        
            
            #bottom of "0" - interferences
            elif (x-116)**2 + (y-20)**2 <= 81 and y<=20:
                node_dict.update(mark_interference(x,y))        
            
            # Hat of "7"
            elif 130 <= x <= 144 and 35 < y <= 38:
                node_dict.update(mark_obstacle(x,y))        
            
            # Slant of "7"
            elif 2*x-253 <= y <= 2*x -245 and 13 <= y <= 35:
                node_dict.update(mark_obstacle(x,y))        

            # Hat of "7" - Interference
            elif 128 <= x <= 146 and 33 < y <= 40:
                node_dict.update(mark_interference(x,y))        
            
            # Slant of "7" - Interference
            elif 2*x-257 <= y <= 2*x -241 and 11 <= y <= 37:
                node_dict.update(mark_interference(x,y))    
            
            #cross of 2st "4"
            elif 151 <= x  <= 165 and 17 < y <= 20:
                node_dict.update(mark_obstacle(x,y))              
            
            #height of 2st "4"
            elif 160 <= x <= 163 and 13 <= y <= 38:
                node_dict.update(mark_obstacle(x,y))        
            
            #slant of 2st "4"
            elif 3*x-433 >= y >= 3*x - 442 and 20 <= y <= 38:
                node_dict.update(mark_obstacle(x,y))   
            
            #cross of 2st "4" - Interference
            elif 149 <= x  <= 167 and 15 < y <= 22:
                node_dict.update(mark_interference(x,y))              
            
            #height of 2st "4" - Interference
            elif 158 <= x <= 165 and 11 <= y <= 40:
                node_dict.update(mark_interference(x,y))        
            
            #slant of 2st "4" - Interference
            elif 3*x-427 >= y >= 3*x - 448 and 18 <= y <= 40:
                node_dict.update(mark_interference(x,y))                        
            
            else:
                node_dict.update(mark_clear_space(x,y))
        
         
    return node_dict