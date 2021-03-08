# project_tetris
 Creating AI for Tetris using neat-python

## Tetris
Tetris game was written based on the: https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/ 

to play Tetris yourself just run play_tetris.py

## Neural evolution
Entire process of teaching is based on neural evolution using neat algorithm. The neat-python module is used for the implementation of the algorithm. 5 different methods of teaching were used, each tested with at least 200 generations. The difference between teaching methods 1-4 are in the number of sample games per player, length of the games (number of pieces to place) or number of players in the generation. Teaching method 5 has differently calculated fitness function and the neural network has different number of inputs.

### Neural network:
#### inputs:
NN uses grid (20x10); however, it doesn't represent every cell, rather heights (so there is 1 if there is a block on the position or above it), current piece (7 inputs, so piece with shape #3: 0010000), next piece (the same as current piece). It gives 214 inputs 

#### outputs:
each combination of the position of the piece (10) and its rotation (4). So 40 outputs

### Teaching
Teaching is divided into generations. Each generation has 60 genomes. To teach neural-network 20 sets of pieces are randomly created. The neural network then plays a game with these pieces. After finishing a game, either losing or using all pieces, the fitness of each final state is calculated. Genome's final fitness is an average of fitness of all sets it played (each genome plays the same pieces). \
The number of pieces in a set depends on how much NN already learned. In the beginning it was given a single piece to place, then added another piece and so on. The number of pieces and corresponding generations are saved in the piecesNumber.txt file.

Fitness function:
+ +score/(number of lines) 
+ -50 for each hole (hole is a place where there is a block directly above it)
+ -height of the final structure
+ -difference between heights in each column (ex. h1=3, h2=4, h3=2 -> dh =3)

To teach AI just run teach_ai.py with config of your choice and correct fitness function. 

NOTE: make sure that output and input methods in the teach_ai.py are correct with the config you are submitting (number of output and input nodes has to be the same in the config and the teach_ai.py)

