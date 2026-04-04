from math import cos
from math import sin
from math import floor
from math import sqrt
from math import radians

def move_factory(step_length:float,angle_change:int):
    """creates a move function with input changes

    Args:
        step_length(float): step length defined by the user
        angle_change (int): angle change * 30degs (0 is straight, 1 is 30 deg, -1 is -30, etc)
    """

    def move_function(current_position:tuple[float,float,int])->tuple[float,float,int]:
        """function returned by move_factory: moves in the specified direction

        Args:
            current_position (tuple): position provided by the program of the location being evaluated
            
        """
        
        #set current position and implement changes to x,y,phi for new position
        x,y,ori = current_position
        
        new_ori = (ori + angle_change * 30)%360
        
        new_x = x + step_length*cos(radians(new_ori))
        new_y = y + step_length*sin(radians(new_ori))
        
        return (new_x, new_y, new_ori)

    #return the function
    return move_function

def bucketize(position:tuple[float,float,int])->tuple[int,int,int]:
    """turns any position into the respective bucket position

    Args:
        position (tuple[float,float,int]): current position

    Returns:
        tuple[int,int,int]: bucket position
    """
    
    euclidean_dist = .5
    x,y,ori = position
    x_bucket = int(floor(x/euclidean_dist+ .5))
    y_bucket = int(floor(y/euclidean_dist+ .5))
    ori_bucket = int(ori // 30)
    
    return (x_bucket,y_bucket,ori_bucket)

def is_finished(position:tuple[float,float,int],goal_node:tuple[int,int,int],threshold:int)->bool:
    """checks if the current position is with the threshold distance to the goal node

    Args:
        position (tuple[float,float,int]): current position being evaluated
        goal_node (tuple[int,int,int]): goal node
        threshold (int): provided "close enough" distance to final point

    Returns:
        bool: True -> finished search False-> search continues
    """
    
    x,y,ori = position
    
    x_goal, y_goal, ori_goal = goal_node
    
    x_dist = (x-x_goal)**2
    y_dist = (y-y_goal)**2
    ori_dist = abs(ori - ori_goal)%360
    ori_dist = min(ori_dist, 360-ori_dist)
    
    if threshold**2 >= x_dist + y_dist and -30 <= ori_dist <= 30:
        return True
    
    return False

def find_dist_to_goal(position:tuple[float,float,int], goal_node:tuple[int,int,int])->float:
    """estimates distance to goal

    Args:
        position (tuple[float,float,int]): current position
        goal_node (tuple[int,int,int]): end position

    Returns:
        float: linear distance from current location to goal
    """
    
    x,y,ori = position
    
    x_goal, y_goal, ori_goal = goal_node
    
    x_dist = (x-x_goal)**2
    y_dist = (y-y_goal)**2
    
    return sqrt(x_dist+y_dist)

