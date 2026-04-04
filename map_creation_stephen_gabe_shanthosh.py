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
    return {(x,y):{"color":'b'}}

def mark_clear_space(x:int,y:int) -> dict:
    """marks a node as traversable space for the robot

    Args:
        x (int): node's x-coordinates
        y (int): node's y-coordinates
    
    Returns:
        dictionary object key is the coordaintes, node color is black, parent node and cost-to-go are empty
    """
    return {(x,y):{"color":'w'}}

def mark_interference(x:int,y:int) -> dict:
    """marks a node as within the robots interference size (2 cms)

    Args:
        x (int): node's x-coordinates
        y (int): node's y-coordinates
        
    Returns:
        dictionary object key is the coordaintes, node color is red, no additional keys
    """
    return {(x,y):{"color":'r'}}

def prompt_user_node(all_nodes:dict, node_name:str, board_length:int,board_height:int)->tuple:
    """prompts the user for a node

    Args:
        all_nodes (dict): dictionary of all nodes on the board
        node_name (str): name of the node "starting" or "goal"
        board_length (int): length of the board
        board_height (int): height of the board

    Returns:
        tuple: coordinates for the node w/ the given name
    """

    data_verification = False
    while not data_verification:
        print(f"Please define a {node_name} point (x,y,phi)")
        user_input = input("please enter integers 0-600 for x, and 0-250 for y, and an intiger for orientation (multiplied by 30deg, -1 = 330, 5 = 150) seperated by a comma: ")
        
        if "," not in user_input:
            print("I only see one value, please enter three coordinates")
            continue
        
        elif user_input.count(",") > 2:
            print("There are too many numbers there, please enter exactly 3 values.")
            continue
        
        elif user_input.count(",") < 2:
            print("There are too few numbers there, please enter exactly 3 values")
        
        elif not all(c in "0123456789,-" for c in user_input):
            print("There are non-intiger, non-comma characters! Please enter only intigers and commas.")
            continue
        
        else:
            x,y,phi = map(int,user_input.split(","))
        
        if x < 0 or x > board_length or y > board_height or y < 0:
            print(f"that location is out of bounds, please enter a locations betwen 0<= x <= {board_length}, 0<= y <= {board_height}")
            continue
        
        else:        
            if all_nodes[(x,y)]["color"]!='w':
                print(f"That coordinate node is within an obstacle and is not a valid {node_name} point! Please enter another node.")                        
                continue
            else:
                ori = 30*(phi%12)
                print(f"Thank you, {node_name} nodes is {x,y,ori}")
                data_verification = True
                break           

    origin = (x,y,ori)

    return origin

def prompt_user_step()->float:
    """prompts user for a step length

    Returns:
        float: step length
    """
    
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
        
        return step_length
    
def ellipse(x1:int, y1:int , x_center:int, y_center:int):
    """equation for the ellipse used repeatedly in defining the volumes

    Args:
        x1 (int): node coordinate - x
        y1 (int): node coordinate -y
        x_center (int): center of the ellipse along x axis
        y_center (int): center of the ellipse along y axis
    """
    return(x1 - x_center)**2+((y1-y_center)**2)/2

def create_board(length:int, height:int)->dict:
    """creates a set of nodes and determines if they are within pre-determiend obstacles

    Args:
        length (int): length of desired board in mm
        height (int): height of desired board in mm
    """
    
    #board dimensions in cms
    board_length = range(length)
    board_height = range(height)
    
    #create data structure to hold node information
    node_dict = {}

    #following used to make mathematical volume creation easier
    
    #obstacle elipse inner and outer radii
    obs_ellipse_rad_out = 26**2
    obs_ellipse_rad_in = 15**2
    
    #interference ellipse inner and outer radii
    itfr_ellipse_rad_out = 31**2
    itfr_ellipse_rad_in = 10**2
    
    #determine nodes which are in obstacles
    for x in board_length:
        for y in board_height:
            
            #set boundry nodes
            if x == 0 or x == length-1 or y == 0 or y == height-1:
                node_dict.update(mark_obstacle(x,y))

            #set boundry interferences
            elif x <= 5 or x >= length-6 or y <= 5 or y >= height -6:
                node_dict.update(mark_interference(x,y))
            
            #top of 1st "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,75,155) <= obs_ellipse_rad_out and y >= 155:
                node_dict.update(mark_obstacle(x,y))
            
            #top/mid of 1st "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,75,155) <= obs_ellipse_rad_out and x <= 75 and y <= 155:
                node_dict.update(mark_obstacle(x,y))           
          
            #bottom/mid of 1st "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,75,95) <= obs_ellipse_rad_out and x >= 75 and y >= 95:
                node_dict.update(mark_obstacle(x,y))    
            
            #bottom of 1st "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,75,95) <= obs_ellipse_rad_out and y <= 95:
                node_dict.update(mark_obstacle(x,y))
            
            #top of 1st "S" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,75,155) <= itfr_ellipse_rad_out and y >= 150:
                node_dict.update(mark_interference(x,y))
                
            #top/mid of 1st "S" - interference
            elif itfr_ellipse_rad_in<=ellipse(x,y,75,155) <= itfr_ellipse_rad_out  and x<= 75 and y <= 155:
                node_dict.update(mark_interference(x,y))
            
            #mid/bot of 1st "S" - interference               
            elif itfr_ellipse_rad_in <= ellipse(x,y,75,95) <= itfr_ellipse_rad_out and x >= 75 and y >= 95:
                node_dict.update(mark_interference(x,y))
            
            #bottom of 1st "S" - interference     
            elif itfr_ellipse_rad_in <= ellipse(x,y,75,95) <= itfr_ellipse_rad_out and y <= 100:
                node_dict.update(mark_interference(x,y))        
                
            #upper round of "G"
            elif obs_ellipse_rad_in <= ellipse(x,y,150,155) <= obs_ellipse_rad_out and y >= 155:
                node_dict.update(mark_obstacle(x,y))  
            
            #back of "G"
            elif 125 <= x <= 135 and 95 <= y <= 155:
                node_dict.update(mark_obstacle(x,y))     
            
            #bottom curve of "G"
            elif obs_ellipse_rad_in <= ellipse(x,y,150,95) <= obs_ellipse_rad_out and y <= 95:
                node_dict.update(mark_obstacle(x,y))                   
            
            #kick-out of "G"
            elif 155<=x<=177 and 95 <= y <= 105:
                node_dict.update(mark_obstacle(x,y))
            
            #kick-down of "G"           
            elif 167<=x<=177 and 65<=y<=95:
                node_dict.update(mark_obstacle(x,y))
                
            #top curve of "G" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,150,155) <= itfr_ellipse_rad_out and y >= 150:
                node_dict.update(mark_interference(x,y))   
            
            #back of "G" - interference
            elif 120 <= x <= 140 and 90 <= y <= 160:
                node_dict.update(mark_interference(x,y))  
            
            #bottom curve of "G" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,150,95)<=itfr_ellipse_rad_out and y <= 100:
                node_dict.update(mark_interference(x,y))       
                
            #kick-out of "G" - interference
            elif 150<=x<=182 and 90<=y<=110:
                node_dict.update(mark_interference(x,y))                                
            
            #kick-down of "G" - interference
            elif 162 <=x<=182 and 60<=y<=95:
                node_dict.update(mark_interference(x,y))
            
            #top of 2nd "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,225,155) <= obs_ellipse_rad_out and y >= 155:
                node_dict.update(mark_obstacle(x,y))         
            
            #top/mid of 2nd "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,225,155) <= obs_ellipse_rad_out and x <= 225 and y <= 155:
                node_dict.update(mark_obstacle(x,y))                
            
            #bottom/mid of 2nd "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,225,95) <= obs_ellipse_rad_out and x >= 225 and y >= 95:
                node_dict.update(mark_obstacle(x,y))        
            
            #bottom of 2nd "S"
            elif obs_ellipse_rad_in <= ellipse(x,y,225,95) <= obs_ellipse_rad_out and y <= 95:
                node_dict.update(mark_obstacle(x,y))
        
            #top of 2nd "S" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,225,155) <= itfr_ellipse_rad_out and y >= 150:
                node_dict.update(mark_interference(x,y))
                
            #top/mid of 2nd "S" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,225,155) <= itfr_ellipse_rad_out and y <= 155 and x <= 225:
                node_dict.update(mark_interference(x,y))
            
            #mid/bot of 2nd "S" - interference               
            elif itfr_ellipse_rad_in <= ellipse(x,y,225,95) <= itfr_ellipse_rad_out and y >= 95 and x >= 225:
                node_dict.update(mark_interference(x,y))
            
            #bottom of 2nd "S" - interference     
            elif itfr_ellipse_rad_in <= ellipse(x,y,225,95) <= itfr_ellipse_rad_out and y <= 100 :
                node_dict.update(mark_interference(x,y))                
            
            #bottom cross of 1st "2"
            elif 275<=x<=325 and 60<=y<=70:
                node_dict.update(mark_obstacle(x,y))
                
            #verticle bit of 1st "2"          
            elif 275 <=x <= 285 and 70 <= y <= 88:
                node_dict.update(mark_obstacle(x,y))
            
            #slant of 1st "2"
            elif 275<=x<=315 and 13/9*x-329 <= y <= 13/9*x-309:
                node_dict.update(mark_obstacle(x,y))        

            #slant/top of 1st "2"
            elif obs_ellipse_rad_in <= ellipse(x,y,300,155) <= obs_ellipse_rad_out and x>=315 and y <= 155:
                node_dict.update(mark_obstacle(x,y))
                
            #top of 1st "2"
            elif obs_ellipse_rad_in <= ellipse(x,y,300,155) <= obs_ellipse_rad_out and y >= 155:
                node_dict.update(mark_obstacle(x,y))

            #bottom cross of 1st "2" - interference
            elif 270<=x<=330 and 55<=y<=75:
                node_dict.update(mark_interference(x,y))
                
            #verticle bit of 1st "2" - interference    
            elif 270 <=x <= 290 and 65 <= y <= 90:
                node_dict.update(mark_interference(x,y))
            
            #slant of 1st "2" - interference
            elif 270<=x<=320 and 13/9*x-339 <= y <= 13/9*x-300 and y >= 55:
                node_dict.update(mark_interference(x,y))        

            #slant/top of 1st "2" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,300,155) <= itfr_ellipse_rad_out and x>=310 and y <= 155:
                node_dict.update(mark_interference(x,y))
                
            #top of 1st "2" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,300,155) <= itfr_ellipse_rad_out and y >= 150:
                node_dict.update(mark_interference(x,y))
                
            #top of "0"
            elif obs_ellipse_rad_in <= ellipse(x,y,375,155) <= obs_ellipse_rad_out and y>=155:
                node_dict.update(mark_obstacle(x,y))        
            
            #left side of "0"
            elif 350 <= x <= 360 and 95 <= y <= 155:
                node_dict.update(mark_obstacle(x,y))        
            
            #right side of "0"
            elif 390 <= x <= 400 and 95 <= y <= 155:
                node_dict.update(mark_obstacle(x,y))        
            
            #bottom of "0"
            elif obs_ellipse_rad_in <= ellipse(x,y,375,95) <= obs_ellipse_rad_out and y<=95:
                node_dict.update(mark_obstacle(x,y))
                
            #top of "0" - interferences
            elif ellipse(x,y,375,155) <= itfr_ellipse_rad_out and y >= 155:
                node_dict.update(mark_interference(x,y))        
            
            #left side of "0" - interferences
            elif 345 <= x <= 375 and 95 <= y <= 155:
                node_dict.update(mark_interference(x,y))        
            
            #right side of "0" - interferences
            elif 375 <= x <= 405 and 95 <= y <= 155:
                node_dict.update(mark_interference(x,y))        
            
            #bottom of "0" - interferences
            elif ellipse(x,y,375,95) <= itfr_ellipse_rad_out and y<=95:
                node_dict.update(mark_interference(x,y))        
            
            #bottom cross of 2nd "2"
            elif 425<=x<=475 and 60<=y<=70:
                node_dict.update(mark_obstacle(x,y))
                
            #verticle bit of 2nd "2"          
            elif 425 <=x <= 435 and 70 <= y <= 88:
                node_dict.update(mark_obstacle(x,y))
            
            #slant of 2nd "2"
            elif 425<=x<=465 and 13/9*x-545 <= y <= 13/9*x-525:
                node_dict.update(mark_obstacle(x,y))        

            #slant/top of 2nd "2"
            elif obs_ellipse_rad_in <= ellipse(x,y,450,155) <= obs_ellipse_rad_out and x>=465 and y <= 155:
                node_dict.update(mark_obstacle(x,y))
                
            #top of 2nd "2"
            elif obs_ellipse_rad_in <= ellipse(x,y,450,155) <= obs_ellipse_rad_out and y >= 155:
                node_dict.update(mark_obstacle(x,y))

            #bottom cross of 2nd "2" - interference
            elif 420<=x<=480 and 55<=y<=75:
                node_dict.update(mark_interference(x,y))
                
            #verticle bit of 2nd "2" - interference    
            elif 420 <=x <= 440 and 65 <= y <= 90:
                node_dict.update(mark_interference(x,y))
            
            #slant of 2nd "2" - interference
            elif 420<=x<=480 and 13/9*x-555 <= y <= 13/9*x-516 and 55 <= y <= 155:
                node_dict.update(mark_interference(x,y))        

            #slant/top of 2nd "2" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,450,155) <= itfr_ellipse_rad_out and x>=460 and y <= 155:
                node_dict.update(mark_interference(x,y))
                
            #top of 2nd "2" - interference
            elif itfr_ellipse_rad_in <= ellipse(x,y,450,155) <= itfr_ellipse_rad_out and y >= 150:
                node_dict.update(mark_interference(x,y))
            
            #top of 6
            elif obs_ellipse_rad_in <= ellipse(x,y,525,155) <= obs_ellipse_rad_out and y >= 155:
                node_dict.update(mark_obstacle(x,y))
            
            #back of 6
            elif 500 <= x <= 510 and 95 <= y <= 155:
                node_dict.update(mark_obstacle(x,y))
            
            #bottom of 6
            elif obs_ellipse_rad_in <= ellipse(x,y,525,95) <= obs_ellipse_rad_out:
                node_dict.update(mark_obstacle(x,y))
            
            # top of 6 - interferences
            elif itfr_ellipse_rad_in <= ellipse(x,y,525,155) <= itfr_ellipse_rad_out and y >= 150:
                node_dict.update(mark_interference(x,y))
            
            # back of 6 - interference
            elif 495 <= x <= 515 and 95 <= y <= 155:
                node_dict.update(mark_interference(x,y))
            
            # bottom of 6 - interference
            elif ellipse(x,y,525,95) <= itfr_ellipse_rad_out:
                node_dict.update(mark_interference(x,y))

            else:
                node_dict.update(mark_clear_space(x,y))
        
         
    return node_dict


def is_obstructed_space(position:tuple[float,float,int])->bool:
    """checks if position is in obstucted space

    Args:
        position (tuple[float,float,int]): current position

    Returns:
        bool: true -> space obstucted, false -> space empty
    """
    
    x,y,ori = position
    
        
    #interference ellipse inner and outer radii
    itfr_ellipse_rad_out = 31**2
    itfr_ellipse_rad_in = 10**2
    
    if x <= 5 or x >= 595 or y <= 5 or y >= 245:
        return True
   
    #top of 1st "S" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,75,155) <= itfr_ellipse_rad_out and y >= 150:
        return True
        
    #top/mid of 1st "S" - interference
    elif itfr_ellipse_rad_in<=ellipse(x,y,75,155) <= itfr_ellipse_rad_out  and x<= 75 and y <= 155:
        return True
    
    #mid/bot of 1st "S" - interference               
    elif itfr_ellipse_rad_in <= ellipse(x,y,75,95) <= itfr_ellipse_rad_out and x >= 75 and y >= 95:
        return True
    
    #bottom of 1st "S" - interference     
    elif itfr_ellipse_rad_in <= ellipse(x,y,75,95) <= itfr_ellipse_rad_out and y <= 100:
        return True       
        
    #top curve of "G" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,150,155) <= itfr_ellipse_rad_out and y >= 150:
        return True
    
    #back of "G" - interference
    elif 120 <= x <= 140 and 90 <= y <= 160:
        return True
    
    #bottom curve of "G" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,150,95)<=itfr_ellipse_rad_out and y <= 100:
        return True   
        
    #kick-out of "G" - interference
    elif 150<=x<=182 and 90<=y<=110:
        return True                             
    
    #kick-down of "G" - interference
    elif 162 <=x<=182 and 60<=y<=95:
        return True

    #top of 2nd "S" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,225,155) <= itfr_ellipse_rad_out and y >= 150:
        return True
        
    #top/mid of 2nd "S" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,225,155) <= itfr_ellipse_rad_out and y <= 155 and x <= 225:
        return True
    
    #mid/bot of 2nd "S" - interference               
    elif itfr_ellipse_rad_in <= ellipse(x,y,225,95) <= itfr_ellipse_rad_out and y >= 95 and x >= 225:
        return True
    
    #bottom of 2nd "S" - interference     
    elif itfr_ellipse_rad_in <= ellipse(x,y,225,95) <= itfr_ellipse_rad_out and y <= 100 :
        return True              

    #bottom cross of 1st "2" - interference
    elif 270<=x<=330 and 55<=y<=75:
        return True
        
    #verticle bit of 1st "2" - interference    
    elif 270 <=x <= 290 and 65 <= y <= 90:
        return True
    
    #slant of 1st "2" - interference
    elif 270<=x<=320 and 13/9*x-339 <= y <= 13/9*x-300 and y >= 55:
        return True      

    #slant/top of 1st "2" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,300,155) <= itfr_ellipse_rad_out and x>=310 and y <= 155:
        return True
        
    #top of 1st "2" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,300,155) <= itfr_ellipse_rad_out and y >= 150:
        return True
        
    #top of "0" - interferences
    elif ellipse(x,y,375,155) <= itfr_ellipse_rad_out and y >= 155:
        return True     
    
    #left side of "0" - interferences
    elif 345 <= x <= 375 and 95 <= y <= 155:
        return True   
    
    #right side of "0" - interferences
    elif 375 <= x <= 405 and 95 <= y <= 155:
        return True      
    
    #bottom of "0" - interferences
    elif ellipse(x,y,375,95) <= itfr_ellipse_rad_out and y<=95:
        return True    

    #bottom cross of 2nd "2" - interference
    elif 420<=x<=480 and 55<=y<=75:
        return True
        
    #verticle bit of 2nd "2" - interference    
    elif 420 <=x <= 440 and 65 <= y <= 90:
        return True
    
    #slant of 2nd "2" - interference
    elif 420<=x<=480 and 13/9*x-555 <= y <= 13/9*x-516 and 55 <= y <= 155:
        return True   

    #slant/top of 2nd "2" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,450,155) <= itfr_ellipse_rad_out and x>=460 and y <= 155:
        return True
        
    #top of 2nd "2" - interference
    elif itfr_ellipse_rad_in <= ellipse(x,y,450,155) <= itfr_ellipse_rad_out and y >= 150:
        return True
    
    # top of 6 - interferences
    elif itfr_ellipse_rad_in <= ellipse(x,y,525,155) <= itfr_ellipse_rad_out and y >= 150:
        return True
    
    # back of 6 - interference
    elif 495 <= x <= 515 and 95 <= y <= 155:
        return True
    
    # bottom of 6 - interference
    elif ellipse(x,y,525,95) <= itfr_ellipse_rad_out:
        return True        
         
    return False
    