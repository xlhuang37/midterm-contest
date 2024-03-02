## Read Me
This is a submission for midterm contest at UC Berkeley's Introduction to Artificial Intelligence course. In short, we program intelligent Pacmans to collect all food on the map. To get a higher score, Pacmans must use the least amount of computation to come up with the shortest path to foods.

Here is the specific policy:
1. We start with 1000 points for each map.
2. Eating a food gives 5 points. Passing the map gives 500 points.
3. Each step of a pacman costs 5 points. Each 100ms of computation costs 10 points. (Roughly like that)
4. The average of points across all maps is your score.

Here is what I did:
1. The backbone is searching with AStar Algorithm and Manhattan heuristics.
2. I noticed that pacmans like to aim for the same food, leading to performance degradation, so I simply made them turn away when a food is already targetted.

Potential Improvements:
1. When pacman searches, I should remove all the food that is on Pacman's way from the map, and thereby totally preventing pacmans from going to the same food.
2. Diversify the heuristics of Pacman?
