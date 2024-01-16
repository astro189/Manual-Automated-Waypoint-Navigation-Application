# Manual-Automated-Waypoint-Navigation-Application
<h4>What is MAWNA ?</h4>
<p>It provides a generalized Automated or Manual waypoint indoor navigation system this involves  allowing any robotic system to navigate autonomously within an indoor environment by following the waypoints present in its generated path, Avoiding collision and coordinating with other systems in its environment for safe navigation.</p>

<h2>Phase-I: A basic implementaton of the idea</h2>
<h3>Components of Phase-I</h3>
<li>A Simple Robotic System</li>
<li>Basic implementation of the Path finding algorithm</li>
<li>Set up a Coordinate mapping and Transformation system</li>
<li>Establish a communication in between the Software and Hardware</li>

<H4>1. The robotic system</H4>
<p>We currently work with a relatively simple 4-wheel drive bot working with the following components</p>
<li>Metal Chassis</li>
<li>L298n Motor Driver</li>
<li>4 Hobby Gear motor</li>
<li>12V LIPO Battery Pack</li>
<br>
 <div align="center" style="display: flex; justify-content: space-between;">
        <table>
           <tr>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/IMG20231216015212.jpg" alt="Bot image 1" width="300">
             </td>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/IMG20231216015219.jpg" alt="Bot Image 2" width="300">
             </td>
           </tr>
      </table>
  </div>
  
<h4>2. Path finding algorithm</h4>

<p>I plan on using the A star path find algorithm for this project with a optimized heuristic cost for indoor navigation. In this phase our only goal is to implement the path finding algorithm and get it working on our custom maps. There are two sub components to get it working</p>
<h5>1) Defining the Custom Maps</h5>
<p>To define a map for the indoor navigation system we need to have two elements</p>
<li>The space in which the AI agent is allowed to move</li> 
<li>The obstacles that the agent needs to avoid.</li>
<br>
<p>To do so we use a grid based system in which the entire area map is divided into cells, we then utilize contour detection for identifyting each cell of the grid, the black grid lines along with the white background makes this process a lot easier. Once the contours have been found we go on to get the coordinates of each cell. This solves both of our above problems at once as the obstacles are completely black thus their contours are not identified and the open space is defined by the identified cells</p>

<div align="center" style="display: flex; justify-content: space-between;">
        <table>
           <tr>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Photos/Final_Map1.png" alt="Custom Map" width="400">
               <p><b>Custom Map</b></p>
             </td>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Detected%20Map.png" alt="Cells Detected" width="400">
               <p><b>Detected Cells</b></p>
             </td>
           </tr>
      </table>
  </div>


<h5>2) A star algorithm</h5>
<p>Once the map has been defined, the obstacles marked and the possible traversal coordinates received we start to execute our path finding algorithm. The A star path find algorithm is a very popular informed searching based algorithm where we define our problem as a solution searching problem along with the search space in which the AI agent traverses for finding the solution</p>
<p><b>1)</b> We start by creating a graph of all the possible nodes in the search space</p>
<p><b>2)</b> Next we maintain two lists called the Open and the Closed list. The open list consist of all the nodes that haven't been explored by the agent yet and the closed list consit of all nodes which have been explored. We initialize the open list with the starting node of the graph</p>
<p><b>3)</b> Each node is evaluated based on it evaluation cost criteria which in the case of A star is given as the sum of the heuristic cost and the payth cost. Since our current goal is just a basic implemntation of the algorithm we begin with a relatively simple heuristic as the <b>Manhattan distance</b></p>
<p><b>4)</b> With the nodes defined and the evaluation criteria established we can begin our traversal uptil we meet the termination criteria. For each node we only consider cardinal movement ignoring any kind of diagnol movement and decreasing the overall complexity of the system</p>

<p>The algorithm then finds the sub-optimal route inbetween the start and the goal node</p>
 <p align="center"><img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/output.png" alt="Path" width="400"></p>
 <p align="center"><b>Sub-Optimal Path</b></p>

<p>The initial node for the the algorithm is defined by identifying the location of the aruco marker in the map.</p>

<h4>3. Coordinate Mapping and Transformation sytem</h4>
<P>The optimal path returned by the algorithm refers to the coordinates in pixels according to the size of the image, our next aim is to convert it into a valid set of real-world coordinates to pass to our robotic system for traversal. To do so we currently use a simple homography transformation by implementing a transformation matrix taking into consideration a set of point from both the real world as well as the image plane.</P>
<p>Once the transformation matrix is calculated we can use the homography transformation for converting our path coordinates in the image to the real world. I do plan on implementing a much more sophisticated system in the later phases, but the discussed approach works currently for simpler scenarios.</P>
<p>By getting a sense of the average speed of the bot we can calculate the time interval for moving from one coordinate to another thus allowing us to traverse in real world</p>

<h4>4. Establish Communication</h4>

<p>This is where the Wifi-Module comes into the picture. We use a ESP 8266 NodeMCU wifi module for establishing a wireless connection with the robotic system over a local IP Address.</p>
<p>The real world transformed coordinates are converted to commands and passed to the NodeMCU along with the time for which each command should be executed. The NodeMCU then executes the Arduino script which controls the components of the robotic system based on the received coordinates. This approach is also subject to change in the future phases as a much more robust system is required for a better real time tracking of the system coordinates.</p>

https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/assets/97799598/c8de8386-fb8a-4612-b30e-4beb85b01515

<b><hr>
<h2>Phase-II: Improving A star</h2>
My aim is to force the algorithm to go for simpler parallel paths and prefer open spaces over narrow paths to further cut down the risk of collision. This is what we try and achieve in this phase.
<br>
<p>There are 3 things we would like to achieve</p>

<li>Introduce collision awareness</li>
<li>Prioriatize parallel motion</li>
<li>Improve the initial a star algorithm</li>

<h3>1) Collision Awareness</h3>
<p>The idea is to penalize the edge and corner nodes allowing for a added degree of safety from collisions, narrow pathways and sharp turns.</p>
<p align="center"><img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/Corner_and_Edges.png" alt="Custom Map" width="400"></p>
<p align="center"><b>Edges and Corners</b></p>

<div align="center" style="display: flex; justify-content: space-between;">
        <table>
           <tr>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/Without_colision_aware.png" alt="Custom Map" width="400">
               <p><b>Origianl A*</b></p>
             </td>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/With_collision_aware.png" alt="Cells Detected" width="400">
               <p><b>Collision Aware</b></p>
             </td>
           </tr>
      </table>
  </div>
  
<h3>2) Parallel Motion</h3>
<p>By prioriatizing parallel motion we want to encourage horizontal/vertical movements, reducing turns and smoothing out the uncessary zig-zag portions that occur in the original algorithm due to the heuristic.The turn regularization is achieved by penalizing it based on its degree of rotation and adding it to the path cost of the node.</p>

<div align="center" style="display: flex; justify-content: space-between;">
        <table>
           <tr>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/zig_zag.png" alt="Custom Map" width="400">
               <p><b>Zig-Zag Path</b></p>
             </td>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/Turn_penalized.png" alt="Cells Detected" width="400">
               <p><b>Smoothened Path</b></p>
             </td>
           </tr>
      </table>
  </div>

<h3>3) Improved A star</h3>
<p>The final improvement we want to gain is to reduce the number of nodes to be expanded inorder to find the sub-optimal path. To do so, we majorly experimented with two algorithms.</p>
<li>Weighted A star</li>
<li>Dynamic weighted A star</li>

<h4>Weighted A star</h4>
<p>The idea behind weighted A star is to decrease the number of node expansions through a greedy approach by increasing the heuristics effect over g(n), thus expanding nodes that are closer to the goal. It assumes a constant weight w (w>1). Weighted A star can be considered to lie in between A star and Greedy Best First Search, it also allows us to swicth from in between BFS, Weighted A star and Dijsktra’s algorithm. In some cases it can reduce the number of expansions by 40-45%</p>

<div align="center" style="display: flex; justify-content: space-between;">
        <table>
           <tr>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/Astar_Expansion.png" alt="Cells Detected" width="400">
               <p><b>Original A* (Expansions:258)</b></p>
             </td>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/Weigted_A_star_expansions.png" alt="Cells Detected" width="400">
               <p><b>Weighted A* (Expansions:152)</b></p>
             </td>
           </tr>
      </table>
  </div>

<h4>Dynamic weighted A star</h4>
<p>There were a few problems noticed with the orginal algortihm, majorly that since it does follow a greedy approach in some cases it might expand more number of nodes than A star if the relation between h(n) and g(n) is not strong enough. To overcome this a dynamic weigted approach was developed where using the original evaluation function seemed to be more suitable in the initial stages of the search and switch to a weighted function as we reached near the goal node. This acts as a balanced approach in between the two and though it might expand a few more nodes than the weighted a star in some cases, it never expands more than the original.</p>

<div align="center" style="display: flex; justify-content: space-between;">
        <table>
           <tr>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/A_Star_output.png" alt="Cells Detected" width="400">
               <p><b>Original A* (Expansions:149)</b></p>
             </td>
             <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/weigted_astar_output.png" alt="Cells Detected" width="400">
               <p><b>Weighted A* (Expansions:152)</b></p>
             </td>
            <td align="center">
               <img src="https://github.com/astro189/Manual-Automated-Waypoint-Navigation-Application/blob/main/Readme_files/Phase-2/Dynamic_Weigthed_Astar.png" alt="Cells Detected" width="400">
               <p><b>Dynamic Weighted A* (Expansions:133)</b></p>
             </td>
           </tr>
      </table>
  </div>

The above mentioned methods significantly improve the over all perfromance as well as the paths found by the algorithm
