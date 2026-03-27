
# **Stephen Snelson - ENPM661 - Project 2**
ENPM661-RO01 Planning for Autonomous Robots
Project 2 - Backwards Dijkstra search and optimal pathfinding through spacial map

GitHub Repository Link: https://github.com/ssnelson424/ENPM661_proj2_stephen_snelson

## Description:
This program uses backwards djikstra search method to determine the fastest path of a point robot through a maze. The program creates a board
through set equations of which spell out "SWS4074". Then prompts the user for the start and goal locations. It checks the provided nodes
to ensure they are not within the obstacles or the space the robot cannot reach due to its own dimensions. The planning algorithm then
branches out from the goal node, where North, South, East, West have a cost of 1 and Northeast, Southeast, Northwest, Southwest have a cost of 
1.4 (approximately sqrt(2)), until it reaches the start node. It then iterates through the data structure of lowest-cost-to-go parent nodes until it
returns to the start node again. It then provides a plot displaying the game board (black,red,white), the nodes explored(cyan), and the path from start
to finish (blue, yellow, green)

## Dependencies:
    Python 3.10+
    -Libraries used: 
        - Collections
        - Matplotlib.pyplot
        - Queue
        - Numpy
        - matplotlib.animation
        - matplotlib.colors

## Run Instructions:
    1. Add the following to the chosen repository:
        - BW-dijkstra_stephen_snelson.py
        - animate_stephen_snelson.py
        - map_creation_stephen_snelson.py
        - actions_stephen_snelson.py
    
    2. From terminal, change to focus on the previously chosen directory (cd...)

    3. Run the script: python3 BW-Dijkstra_stephen_snelson.py
        1. The script will prompt user for a starting point. Enter two intigers seperated by a comma such as:5,5
            -If the user enters an invalid point or a point that is within an obstacle/interference space, the user will be prompted for another input
        
        2. The script will prompt the user for a goal point. Enter two intigers seperated by a comma such as:145,75
            -If the user enters an invalid point or a point that is within an obstacle/interference space, the user will be prompted for another input
        
        3. The script will run and display a plot of the searched nodes and optimal path in yellow.

        4. After user exits the plot, the user will be prompted if they want a animated version of the plot. The animated version
           is a GIF showing the expanding explored nodes and then the creation of the optimal path from start to goal. User
           should enter Y or N based on their preference.
        
        5. After a few moments, an animated plot will be saved in the chosen directory under "dijkstra_stephen_snelson.gif". (No pop-up, outside of
           terminal link)

        6. Script is complete and close
        

## Outputs:
    -Terminal Output: User will be prompted for inputs and additional information will be provided for operational clarity
    -Still-plot of all explored nodes and path from start to goal
    -Animated GIF saved as "dijkstra_stephen_snelson.gif"
