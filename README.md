# 2048

This repository contains an implementation of the so called expectimax algorithm to beat the game 2048.

<b>Expectimax</b> is an extension of <b>MiniMax</b> which itself is an algorithm for finding the optimal game strategy 
for finite two-person zero-sum games with perfect information. These games include, in particular, board 
games such as Chess, Go, Othello / Reversi, Checkers, Mill, and Four Wins, where both players always know 
the entire history of the game. Also, for games with random influence like backgammon, the minimax algorithm 
can be extended based on expected values. Usually, but not exclusively, the minimax algorithm is applied to 
game with alternating move rights. Expectimax resembles in large parts the conventional MiniMax algorithm, 
but is extended by a case distinction. All possible events (resulting e.g. from different numbers of dice) 
are calculated separately as if they were real. Subsequently, all resulting probability branches of a probability 
depth are then multiplied by the probability of their occurrence and added. The sum then forms the criterion 
for the well-known minimization/maximization process. The values in the tree thus formally resemble the 
mathematical definition of the expected value.

While the algorithm (searchai.py) is an implementation of myself, the program frame which runs the browser game 
was developed by employees of Zurich University of Applied Sciences.

If you want to run the program, download this repo and execute <b>chrome</b> with the 
following option: <b>--remote-debugging-port=9222</b>

Then run python <b>2048.py</b>, choose <b>2048</b> from the appearing list and have fun!
