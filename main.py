import copy
import random

def fitness(parent):
    mutual_attacks = {
        0: 0,
        1: 0,
        2: 1,
        3: 3,
        4: 6,
        5: 10,
        6: 15,
        7: 21,
        8: 28
    }
    num_of_mutual_attacks = 0
    for x in range(1, 9):
        num_of_mutual_attacks += mutual_attacks[parent.count(x)]
        # print("Row attackers for " + str(x) + " = " + str(mutual_attacks[parent.count(x)]))
        if x != 8:
            for y in range((x + 1), 9):
                if abs(x - y) == abs(parent[x - 1] - parent[y - 1]):
                    num_of_mutual_attacks += 1
    return 28 - num_of_mutual_attacks


def population_generator(population_size):
    temp_list = []
    population = []
    for x in range(0, population_size):
        for y in range(0, 8):
            temp_list.append(random.randint(1, 8))
        population.append((copy.deepcopy(temp_list), fitness(temp_list)))
        temp_list = []
    return population


def mutation(mutation_pct, parent):
    rand_num = random.randint(0, 100)
    if rand_num <= mutation_pct:
        mutation_point = random.randint(0, 7)
        mutation_value = random.randint(1, 8)
        parent[mutation_point] = mutation_value


def cross_over(parent_one, parent_two, temp_population, mutation_pct):
    cross_over_point = random.randint(0, 6)
    new_parent_one = []
    new_parent_two = []
    pivot_point = True
    for x in range(0, 8):
        if pivot_point:
            new_parent_one.append(parent_one[x])
            new_parent_two.append(parent_two[x])
        else:
            new_parent_one.append(parent_two[x])
            new_parent_two.append(parent_one[x])
        if x == cross_over_point:
            pivot_point = False
    mutation(mutation_pct, new_parent_one)
    mutation(mutation_pct, new_parent_two)
    temp_population.append((copy.deepcopy(new_parent_one), fitness(new_parent_one)))
    temp_population.append((copy.deepcopy(new_parent_two), fitness(new_parent_two)))
    # return [(copy.deepcopy(new_parent_one), fitness(new_parent_one)), (copy.deepcopy(new_parent_two), fitness(new_parent_two))]


def print_board(parent):
    for x in range(8, 0, -1):
        row = ""
        for y in parent:
            if y == x:
                row += "Q   "
            else:
                row += "X   "
        print(row)


def parent_selection(population):
    import random
    parent_list = []
    fitness_list = []
    for x in population:
        parent_list.append(copy.deepcopy(x[0]))
        fitness_list.append(copy.deepcopy(x[1]))
    return random.choices(parent_list, fitness_list, k=len(population))


def solve_eight_queens(num_of_iterations, population_size, mutation_pct):
    population = population_generator(population_size)
    temp_population = []
    for x in range(0, num_of_iterations):
        parents_to_pick = parent_selection(population)
        for y in range(0, int(population_size/2)):
            cross_over(parents_to_pick[y], parents_to_pick[y+1], temp_population, mutation_pct)
        population = copy.deepcopy(temp_population)
        temp_population = []

        avg_fitness = 0
        highest_fitness = 0
        best_parent = []

        for z in population:
            avg_fitness = avg_fitness + copy.deepcopy(z[1])
            if z[1] > highest_fitness:
                best_parent = copy.deepcopy(z[0])
                highest_fitness = copy.deepcopy(z[1])

        print("Highest Fitness: " + str(highest_fitness))
        avg_fitness = avg_fitness/population_size
        print("Average Fitness: " + str(avg_fitness))
        if highest_fitness == 28:
            print("Highest Fitness Board:")
            print_board(best_parent)


print("Welcome to the eight queens problem")
population_size = input("Please enter a population size:\n")
mutation_pct = input("Please enter a desired mutation percent (Please enter a number without the percent sign (%)):\n")
num_of_iterations = input("Please enter the number of iterations:\n")
solve_eight_queens(int(num_of_iterations), int(population_size), int(mutation_pct))
