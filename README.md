# SmartPong
Using genetic algorithm and neural networks to develop a smart pong artificial player

*Scripts*:
 - singleplayer_pong.py - 
     You play against a simple AI that just follows the ball wherever it goes.
 - playing-god-of-pong.py - 
     Receives 3 numerical arguments: population size, how many of the best players 'survive' and number of generations to run. It starts with a random population, probably lots of dumb guys, and pass the best 'genes' to next generations neural networks.
 - you-against-champ.py - 
     Receive a parameter of PATH to champion .dat file, so you can play against this evolution generated player.

*Players description*:
  - Abraham - 
      First 'succesful' try. He plays very well against the simple heuristic AI but sucks against humans. This is because he pays to much attention to where is his opponent instead of where is the ball. He's basically a football player that is in love with the goalkeeper.
  - Bella - 
      Soooo i fixed the Abraham problem and Bella follows the ball like it's the only thing that matters. That is precisely the problem, doesn't feel that smart.
  - Coruja - 
      This is the first that satisfied me when i played against him. He seems to follow the ball in a very smart way to walk no much more than necessary and is very precise.
  - Dio - 
      Now we're talking! After having the most obvious idea of not showing the game in screen during the learning rounds, we were able to run populations of hundreds, for some big time number of generations. Dio is the result of that. One more diference, he is trained to play in a game where the ball first goes to his opponent, unlike the other players. Did this to avoid the (lots of) cases where the best players were the ones that learned to play when the ball starts going only in a specific direction.
      
*Some explanations*:
  The main plan here was to simulate evolutionary learning in a interactive and visual way. Each player defines each frame move from a 1 layer neural network. The inputs to this network are 7: ball x location, ball y location, ball x velocity, ball y velocity, his y location, opponent y location and bias.
  
Made with pygame: https://www.pygame.org/news by Giovanni Amorim
