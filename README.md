# project_tetris
 Creating AI for Tetris using neat-python

## Tetris
Tetris game was written based on the: https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/ 

to play Tetris yourself just run play_tetris.py

## Neural evolution
Entire process of teaching is based on neural evolution using neat algorithm. The neat-python module is used for the implementation of the algorithm. 5 different methods of teaching were used, each tested with at least 200 generations. The difference between teaching methods 1-4 are in the number of sample games per player, length of the games (number of pieces to place) or number of players in the generation. Teaching method 5 has differently calculated fitness function and the neural network has different number of inputs.

### Neural network:
#### inputs:
teaching method 1-4: NN uses entire grid (20x10), the current piece (4x4) and the next piece (4x4). It gives 232 inputs

teaching method 5: NN uses grif (20x10); however, it doesn't represent every cell, rather hightes (so it is 1 if there is a block on the position or above it), current piece (7 inputs, so piece with shape #3: 0010000), next piece (the same as current piece). It gives 214 inputs 

#### outputs:
each combination of the position of the piece (10) and its rotation (4). So 40 outputs

### Teaching
Summary of each teaching method is in the buffer file (information about fitness function used, number of generations, number of players in each generation, etc). Each config file is in the configs directory. \
To teach AI just run teach_ai.py with config of your choice and correct fitness function. 

NOTE: make sure that output and input methods in the teach_ai.py are correct with the config you are submitting (number of output and input nodes has to be the same in the config and the teach_ai.py)

## Results
The teaching method no. 5 was the most promising. Because of that, it has been teaching through 1000 generations. However, in the end, the best player is not a very good one. It can sometimes clean a line, but there is no good strategy developed. It either has to keep on learning for much longer or some other improvements to fitness function should be made. Best player from each generation is saved in the results directory and it can be tested with using play_ai.py (for methods 1-4) or play_ai_nauka_5.py (for method 5).
