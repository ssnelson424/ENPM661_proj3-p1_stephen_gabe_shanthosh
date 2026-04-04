
**Group: Stephen Snelson, Gabe Szybalski, Shanthosh Raaj- ENPM661 - Project 3 Phase 1**
ENPM661-RO01 Planning for Autonomous Robots
Project 3 - Backwards A* search and optimal pathfinding through spacial map

GitHub Repository Link: https://github.com/ssnelson424/ENPM661_proj3-p1_stephen_gabe_shanthosh

## Description:
This program uses backwards A* search method to determine the fastest path of a robot through a maze. The program creates a board
through set equations of which spell out "SGS2026". Then prompts the user for the start and goal locations (x,y,theta), and a step length. It checks the 
provided nodes to ensure they are not within the obstacles or the space the robot cannot reach due to its own dimensions. The planning algorithm 
then branches out from the goal node in 5 directions; straight ahead then right and left, 30 and 60 degrees from straight each. The alogithm uses A* 
which takes into account the approximated cost towards the goal node, rather than only the cost already traveled. Once the start node has been reached,
the program determines the optimal path by backtracking through the parents nodes of the lowest cost previous node. It then provides a plot displaying the game 
board (black,red,white), the locations explored (green), and the path from start to finish (blue, purple, green)

## Dependencies:
    Python 3.10+
    -Libraries used: 
        - Collections
        - Queue
        - Numpy
        - Math
        - OpenCV

## Run Instructions:
    1. Add the following to the chosen repository:
        - a_star_stephen_gabe_shanthosh.py
        - map_creation_stephen_gabe_shanthosh.py
        - actions_stephen_gabe_shanthosh.py
    
    2. From terminal, change to focus on the previously chosen directory (cd...)

    3. Run the script: python3 a_star_stephen_gabe_shanthosh.py
        1. The script will prompt user for a starting point. Enter three intigers seperated by commas (x,y,theta) such as:5,5,6
            -The first two intigers are the x,y coordinates, and the third is the orientation which will be multipled by 30 degrees
            -If the user enters an invalid point or a point that is within an obstacle/interference space, the user will be prompted for another input
        
        2. The script will prompt the user for a goal point. Enter three intigers seperated by commas (x,y,theta) such as:5,5,6
            -The first two intigers are the x,y coordinates, and the third is the orientation which will be multipled by 30 degrees
            -If the user enters an invalid point or a point that is within an obstacle/interference space, the user will be prompted for another input
        
        3. The script will run and display a plot of the searched areas (green) and optimal path in purple

        4. After user exits the plot, the user will be prompted if they want a animated version of the plot. The animated version
           is a mp4 showing the expanding explored nodes and then the creation of the optimal path from start to goal. User
           should enter Y or N based on their preference.
        
        5. After a few moments, an animated plot will be saved in the chosen directory under "dijkstra_stephen_snelson.gif". (No pop-up, outside of
           terminal link)

        6. Script is complete and close
        

## Outputs:
    -Terminal Output: User will be prompted for inputs and additional information will be provided for operational clarity
    -Still-plot of all explored nodes and path from start to goal
    -Animated mp4 saved as "dijkstra_stephen_snelson.gif"
