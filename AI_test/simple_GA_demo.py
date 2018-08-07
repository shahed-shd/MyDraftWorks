# Given below is a simple example implementation of a genetic algorithm in Python.
# Given a set of 5 genes, each gene can hold one of the binary values 0 and 1.
# The fitness value is calculated as the number of 1s present in the genome. If there are five 1s, then it is having maximum fitness. If there are no 1s, then it has the minimum fitness.
# This genetic algorithm tries to maximize the fitness function to provide a population consisting of the fittest individual, i.e. individuals with five 1s.
# Note: In this example, after crossover and mutation, the least fit individual is replaced from the new fittest offspring.


import random
import copy


class Individual(object):
    def __init__(self):
        self.__genes = [random.randint(0, 1) for _ in range(5)]   # Set genes randomly
        self.__fitness = sum(self.__genes)  # Total number of 1s


    def get_fitness(self):
        '''Get the fitness of this individual.'''
        return self.__fitness


    def get_gene(self, gene_idx):
        '''Get the gene value of the gene at index gene_idx.'''
        return self.__genes[gene_idx]


    def set_gene(self, gene_idx, gene_val):
        '''Set the value gene_val to the gene at index gene_idx.'''
        if self.__genes[gene_idx] != gene_val:
            self.__genes[gene_idx] = gene_val
            self.__fitness += 1 if gene_val == 1 else -1


    def print_genes(self):
        print(self.__genes)


class Population(object):
    def __init__(self, ini_pop_size):
        self.__individuals = [Individual() for _ in range(ini_pop_size)]


    def get_fittests(self):
        '''Get the 1st and 2nd fittest individual.'''

        mx_fitness1 = -1
        mx_fitness2 = -1
        fittest1 = None
        fittest2 = None

        for x in self.__individuals:
            f = x.get_fitness()

            if f >= mx_fitness1:
                mx_fitness2 = mx_fitness1
                fittest2 = fittest1
                mx_fitness1 = f
                fittest1 = x
            elif f > mx_fitness2:
                mx_fitness2 = f
                fittest2 = x

        return (fittest1, fittest2)


    def get_least_fittest_index(self):
        '''Get the index of the least fittest individual.'''
        mn_fitness = 6
        least_fittest_idx = int()

        for (i, x) in enumerate(self.__individuals):
            f = x.get_fitness()

            if f < mn_fitness:
                mn_fitness = f
                least_fittest_idx = i

        return least_fittest_idx


    def get_individual(self, idx):
        '''Get the individual at index idx.'''
        return self.__individuals[idx]


    def set_individual(self, idx, val):
        '''Individual at index idx will be removed and new individual 'val' will be inserted at that index.'''
        self.__individuals[idx] = val


def selection(population):
    '''Select the 1st and 2nd fittest individual from population.'''
    fittest1, fittest2 = population.get_fittests()
    return (fittest1, fittest2)


def crossover(fittest1, fittest2):
    '''Perform crossover between 2 individuals (as parents) fittest1 and fittest2.'''
    crossover_point = random.randint(0, 4)

    for i in range(crossover_point+1):
        g1 = fittest1.get_gene(i)
        g2 = fittest2.get_gene(i)

        fittest1.set_gene(i, g2)
        fittest2.set_gene(i, g1)


def mutation(fittest1, fittest2):
    '''Perform mutation  to maintain diversity within the population.'''
    mutation_point = random.randint(0, 4)

    g = fittest1.get_gene(mutation_point)
    fittest1.set_gene(mutation_point, 1 if g == 0 else 0)

    g = fittest2.get_gene(mutation_point)
    fittest2.set_gene(mutation_point, 1 if g == 0 else 0)


def get_fittest_offspring(fittest1, fittest2):
    '''Returns the fittest offsprint formed form parents fittest1 and fittest2.'''

    f1 = fittest1.get_fitness()
    f2 = fittest2.get_fitness()
    return (fittest1 if f1 >= f2 else fittest2)


def main():
    # Initial population
    population = Population(10)
    generation_cnt = 0

    # Find out the fittest
    fittest1 = population.get_fittests()[0]
    print("Generation: %d Fitness of the Fittest: %d" % (generation_cnt, fittest1.get_fitness()))

    # While population gets an individual with maximum fitness
    while fittest1.get_fitness() < 5:
        generation_cnt += 1

        # Do selection
        fittest1, fittest2 = selection(population)

        # Do crossover
        fittest1 = copy.deepcopy(fittest1)
        fittest2 = copy.deepcopy(fittest2)
        crossover(fittest1, fittest2)

        # Do mutation under a random probability
        if random.randint(0, 100) % 10 < 5:
            mutation(fittest1, fittest2)

        # Add fittest offspring to the population
        fittest_offspring = get_fittest_offspring(fittest1, fittest2)
        least_fittest_idx = population.get_least_fittest_index()
        population.set_individual(least_fittest_idx, fittest_offspring)

        # Find out the fittest
        fittest1 = population.get_fittests()[0]
        print("Generation: %d Fitness of the Fittest: %d" % (generation_cnt, fittest1.get_fitness()))

    print("\nSolution found in generation %d" % generation_cnt)
    print("Fitness: %d" % fittest1.get_fitness())
    print("Genes: ", end='')
    fittest1.print_genes()


if __name__ == '__main__':
    main()