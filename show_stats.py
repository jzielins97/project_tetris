import matplotlib
import neat
import numpy as np
# ustawienie pliku konfiguracyjnego
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     '.\\checkpoints\\nauka_2\\config-feedforward')

population = neat.checkpoint.Checkpointer.restore_checkpoint(".\\checkpoints\\nauka_2\\neat-checkpoint-198")

stats = neat.StatisticsReporter()
stats.post_evaluate(config,population,population.species,population.best_genome)

neat.visualize.plot_stats(stats, ylog=False, view=True)
neat.visualize.plot_species(stats, view=True)

print(population.best_genome)

