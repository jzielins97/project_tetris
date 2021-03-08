import neat
import pickle
import matplotlib.pyplot as plt
import numpy as np
# ustawienie pliku konfiguracyjnego
"""
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     '.\\configs\\config-5')

population = neat.checkpoint.Checkpointer.restore_checkpoint(".\\checkpoints\\nauka_5\\neat-checkpoint-1000")
"""

with open(".\\checkpoints\\stats.pkl", "rb") as f:
    stats = pickle.load(f)

#stats = neat.statistics.StatisticsReporter()
#stats.post_evaluate(config,population,population.species,population.best_genome)
generation = np.arange(1,1006)
avg_fitness = stats.get_fitness_mean()
#print(avg_fitness)

plt.plot(generation,avg_fitness,'r')
plt.show()




