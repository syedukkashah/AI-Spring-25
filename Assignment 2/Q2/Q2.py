import random

# Data
task_times = [5, 8, 4, 7, 6, 3, 9]
facility_capacities = [24, 30, 28]
cost_matrix = [
    [10, 12, 9],
    [15, 14, 16],
    [8, 9, 7],
    [12, 10, 13],
    [14, 13, 12],
    [9, 8, 10],
    [11, 12, 13]
]

num_tasks = len(task_times)
num_facilities = len(facility_capacities)

# GA parameters
population_size = 6
crossover_rate = 0.8
mutation_rate = 0.2
generations = 2  # 2 iterations performed
penalty_factor = 1000


def calc_fitness(assignment):
    total_cost = 0
    facility_loads = [0] * num_facilities
    penalty = 0
    for task, facility in enumerate(assignment):
        facility_idx = facility - 1
        total_cost += task_times[task] * cost_matrix[task][facility_idx]
        facility_loads[facility_idx] += task_times[task]
    for load, capacity in zip(facility_loads, facility_capacities):
        if load > capacity:
            penalty += penalty_factor * (load - capacity)
    return total_cost + penalty, facility_loads


def verify_assignment(assignment):
    fitness, loads = calc_fitness(assignment)
    is_valid = all(load <= cap for load, cap in zip(loads, facility_capacities))
    print(f"\nAssignment: {assignment}")
    print(f"Total Cost: {fitness if penalty_factor == 0 else fitness % penalty_factor}")
    print(f"Facility Loads: {loads}")
    print(f"Capacities: {facility_capacities}")
    print(f"Constraints Satisfied: {is_valid}")
    return fitness, is_valid


def create_population():
    return [
        [2, 3, 1, 2, 3, 1, 2],
        [1, 2, 3, 1, 2, 3, 2],
        [3, 1, 2, 3, 1, 2, 1],
        [2, 1, 3, 2, 1, 3, 2],
        [1, 3, 2, 1, 3, 2, 1],
        [3, 2, 1, 3, 2, 1, 3]
    ]


def select_parents(population, fitnesses):
    total_fitness = sum(1 / f for f in fitnesses)
    probabilities = [(1 / f) / total_fitness for f in fitnesses]
    return random.choices(population, weights=probabilities, k=2)


def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        point = random.randint(1, num_tasks - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]


def mutate(assignment):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(num_tasks), 2)
        assignment[idx1], assignment[idx2] = assignment[idx2], assignment[idx1]
    return assignment


def genetic_algorithm():
    population = create_population()
    best_solution = None
    best_fitness = float('inf')

    print("Initial Population:")
    for i, chrom in enumerate(population):
        fit, loads = calc_fitness(chrom)
        print(f"Chromosome {i + 1}: {chrom}, Cost: {fit}, Loads: {loads}")

    for gen in range(generations):
        fitnesses = []
        for individual in population:
            fit, _ = calc_fitness(individual)
            fitnesses.append(fit)
            if fit < best_fitness:
                best_fitness = fit
                best_solution = individual[:]

        print(f"\nGeneration {gen + 1}:")
        print(f"Population: {population}")
        print(f"Fitness Values: {fitnesses}")
        print(f"Best Cost So Far: {best_fitness}")

        new_population = [best_solution[:]]  # Elitism
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population[:population_size]

    return best_solution, best_fitness


best_assignment, best_cost = genetic_algorithm()
print("\nGenetic Algorithm Results After 2 Generations:")
verify_assignment(best_assignment)
