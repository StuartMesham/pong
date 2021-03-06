# Pong
A quick and dirty evolved pong player.

![Screenshot](https://user-images.githubusercontent.com/28049022/57804781-c1489700-775b-11e9-8caa-88a0d2456c08.png)

I wanted to play around with generating a simple pong opponent through evolution.
First I wrote a little pong game in python simulating the movement of the ball and accepting player movement input.
I added an optional GUI that would allow human player(s) to play against another human player or one of my generated computer players.

At each timestep, a player (human or computer) may move left, stay still or move right.
The computer players simply used a weighted linear combination of their position, their opponent's position, the ball's position and the ball's velocity.
The result of this combination decided (based on 2 threshold values) whether the player would go left, stay still or go right.

The weights for the player were generated by spawning a generation of 200 players with randomly initialised weights and having them play 30000 games against each other. After each game the loser was eliminated and a duplicate of the winner was created with slightly mutated (tweaked) weights.

The ```train.py``` script runs this training process and then allows the user to play against the generated player.