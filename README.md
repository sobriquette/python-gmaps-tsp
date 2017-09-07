# python-gmaps-tsp
Computing optimal travel routes using the Google Distance Matrix API and various approximation algorithms for the traveling salesman problem. Hoping to turn this into a recommendation engine -- i.e. "we recommend you take this route for the 5 POI you have submitted".

Approaches so far:
1) Using the best known TSP solver, Concorde, to produce results.
2) Constructing a minimum spanning tree and using a depth-first traversal on the tree to find a Hamiltonian path.
3) Genetic algorithms (?)

Goals for this project:
1) Learn how to make requests to Google APIs
2) Learn how to compute an optimal route through points
3) Integrate into a small Flask app with a form for end user to submit points of interest

Sources:
- Integrating with Concorde TSP Solver by Jean-Francois Puget: https://www.ibm.com/developerworks/community/blogs/jfp/resource/tsp_nb.html?lang=en
- Prim's Minimum Spanning Tree: http://www.bogotobogo.com/python/python_Prims_Spanning_Tree_Data_Structure.php
- Prim's Minimum Spanning Tree (2): www.geeksforgeeks.org/greedy-algorithms-set-5-prims-minimum-spanning-tree-mst-2/
- Optimal Tour of the US by Randy Olson: https://github.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/blob/master/optimal-road-trip/
- Applying a Genetic Algorithm to the Traveling Salesman Problem: http://www.theprojectspot.com/tutorial-post/applying-a-genetic-algorithm-to-the-travelling-salesman-problem/5