import bisect
import copy
import itertools
import math
import operator
import random
import matplotlib.pyplot as plt


class City(object):
    def __init__(self, x, y):
        '''Initialize a city having coordinate (x, y).'''
        self.x = x
        self.y = y


    def distance(self, another_city):
        '''Calculate the distance between this city and another_city.'''
        return math.hypot(self.x - another_city.x, self.y - another_city.y)


    def __repr__(self):
        '''Defining how to represent an instance of City class.'''
        return "City({}, {})".format(self.x, self.y)


class Individual(object):
    def __init__(self, route):
        '''Initialize an individual of GA. Each individual has a route for TSP.
        Here route means the sequence indices of cities in which the sales man will travel.'''
        self.__route = copy.deepcopy(route)
        self.__route_distance = None
        self.__fitness = None


    def get_route(self):
        '''Returns a copy of route of this individual.'''
        return copy.deepcopy(self.__route)


    def get_route_distance(self):
        '''Returns the total distance of the route.'''
        if self.__route_distance == None:
            tot_dist = 0
            sz = len(self.__route)

            for from_idx in range(sz):
                to_idx = from_idx+1 if from_idx+1 < sz else 0
                tot_dist += cities[self.__route[from_idx]].distance(cities[self.__route[to_idx]])

            self.__route_distance = tot_dist

        return self.__route_distance


    def get_fitness(self):
        '''Returns the fitness of the individual.'''
        if self.__fitness == None:
            self.__fitness = 1 / self.get_route_distance()

        return self.__fitness


class GA(object):
    def ranking(self, population):
        '''Performs ranking of population considering fitness.
        Returns a list of tuple, each tuple contains index and fitness.'''

        rank = [(index, individual.get_fitness()) for index, individual in enumerate(population)]
        rank.sort(key=operator.itemgetter(1), reverse=True)
        return rank


    def selection(self, population, elite_size):
        '''Returns a list of indices of individuals from population who are selected and ranked, considering elite_size (an integer value).'''
        rank = self.ranking(population)

        # Fitness proportionate selection, (aka roulette wheel selection).
        fitness_cum_sum = list(itertools.accumulate([x[1] for x in rank]))
        fitness_sum = fitness_cum_sum[-1]

        fitness_cum_percentage = [100 * x / fitness_sum for x in fitness_cum_sum]

        selected = []
        for i in range(elite_size):
            selected.append(rank[i][0])

        for _ in range(len(population) - elite_size):
            pick = random.random() * 100
            i = bisect.bisect_left(fitness_cum_percentage, pick)
            selected.append(rank[i][0])

        return selected


    def get_mating_pool(self, population, selected):
        '''Returns mating pool from population (list of individuals) and selected (a list of indices of individuals in population, individuals are ranked by fitness).'''
        pool = [population[i] for i in selected]
        return pool


    def get_breed(self, parent1, parent2):
        '''Returns breed from parent1 and parent2. parent1, parent2, breed are instances of Individual class.'''
        parent_route1 = parent1.get_route()
        parent_route2 = parent2.get_route()

        a = random.randrange(0, len(parent_route1))
        b = random.randrange(0, len(parent_route1))
        a, b = min(a, b), max(a, b)

        child_route1 = [parent_route1[i] for i in range(a, b+1)]
        child_route2 = list(set(parent_route2) - set(child_route1))
        child_route = child_route1 + child_route2

        return Individual(child_route)


    def get_breed_population(self, mating_pool, elite_size):
        '''Returns breed population from mating_pool (a list of individuals ranked by fitness) considering elite_size (an integer value).'''
        # pool = random.sample(mating_pool, len(mating_pool))
        pool = copy.deepcopy(mating_pool)
        children = []

        for i in range(elite_size):
            children.append(mating_pool[i])

        pool = random.sample(mating_pool, len(mating_pool))
        remain = len(mating_pool) - elite_size

        for i in range(remain):
            child = self.get_breed(pool[i], pool[-i-1])
            children.append(child)

        return children


    def mutate(self, individual, mutation_rate):
        '''Apply mutation on individual which is an instance of Individual class, mutation_rate is a float value.'''
        route = individual.get_route()
        sz = len(route)

        for i in range(sz):
            if random.random() < mutation_rate:
                j = random.randrange(sz)
                # Swap
                tmp = route[i]
                route[i] = route[j]
                route[j] = tmp

        return Individual(route)


    def get_mutated_population(self, population, mutation_rate):
        '''Apply mutation on population considering mutation_rate.
        population is a list of individuals, mutation_rate is a float value.'''

        mutated_population = []

        for i in range(len(population)):
            mutated_individual = self.mutate(population[i], mutation_rate)
            mutated_population.append(mutated_individual)

        return mutated_population


    def get_next_generation(self, curr_gen, elite_size, mutation_rate):
        '''Generates next generation from curr_gen considering elite_size and mutation_rate.
        curr_gen is a list of individuals, elite_size is an integer value, mutation_rate is a float value.'''

        selected = self.selection(curr_gen, elite_size)
        mating_pool = self.get_mating_pool(curr_gen, selected)
        children = self.get_breed_population(mating_pool, elite_size)
        next_gen = self.get_mutated_population(children, mutation_rate)
        return next_gen


    def run(self, initial_population, elite_size, mutation_rate, generation_count):
        '''Runs the genetic algorithm. initial_population is a list of individuals, elite_size is an integer value, mutation rate is a float value, generation_count is an integer value.'''
        pop = copy.deepcopy(initial_population)
        progress = []

        a = pop[self.ranking(pop)[0][0]]
        d = a.get_route_distance()
        f = a.get_fitness()
        print("Initially, distance: {}, fitness: {}".format(d, f))

        progress.append(d)

        for _ in range(generation_count):
            pop = self.get_next_generation(pop, elite_size, mutation_rate)

            a = pop[self.ranking(pop)[0][0]]
            d = a.get_route_distance()
            progress.append(d)

        f = a.get_fitness()
        print("Finally, distance: {}, fitness: {}".format(d, f))

        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show(block=False)

        return a.get_route()    # Best route


def get_cities(total_city, xmin, xmax, ymin, ymax):
    '''Ranodmly generates total_city cities having integer coordinates such that
    x coordinates are between xmin and xmax inclusive, y coordinates are between ymin and ymax inclusive.
    Returns a list of cities and the indicies of cities.'''

    city_list = [City(random.randint(xmin, xmax), random.randint(ymin, ymax)) for _ in range(total_city)]
    city_index_list = list(range(total_city))

    return city_list, city_index_list


def get_initial_population(pop_size, city_index_list):
    '''Initialize a population of size pop_size. Different individuls in population will have different sequences of city indices from city_index_list.'''
    initial_population = []

    for _ in range(pop_size):
        random.shuffle(city_index_list)
        initial_population.append(Individual(city_index_list))

    return initial_population


def print_city_sequence(best_route):
    '''Prints the sequence of cities maintaining the sequence in best_route (a list of ordered indices of cities).'''
    print("\nCity sequence:\n")

    for i in range(len(best_route)):
        from_idx = best_route[i]
        to_idx = best_route[i+1 if i+1 < len(best_route) else 0]

        from_city = cities[from_idx]
        to_city = cities[to_idx]

        d = from_city.distance(to_city)

        print("%s  --%.2f-->  %s" % (from_city, d, to_city))


cities = []


def main():
    global cities
    cities, city_index_list = get_cities(total_city=25, xmin=-100, xmax=100, ymin=-100, ymax=100)
    initial_population = get_initial_population(pop_size=100, city_index_list=city_index_list)

    ga = GA()
    best_route = ga.run(initial_population, elite_size=20, mutation_rate=0.001, generation_count=500)

    print_city_sequence(best_route)

    plt.show()


if __name__ == '__main__':
    main()