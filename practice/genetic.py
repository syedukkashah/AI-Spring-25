import random
import math

# Function to optimize
def f(x):
    return 2 * (x ** 2) - 1

# Convert binary string to decimal
def binary_to_decimal(binary_str):
    return int(binary_str, 2)

# Generate a random binary string of length `n`
def random_binary(n=6):
    return ''.join(random.choice('01') for _ in range(n))

# Generate initial population
def generate_population(size):
    return [random_binary() for _ in range(size)]

# Evaluate fitness for each individual
def evaluate_population(population):
    return {ind: f(binary_to_decimal(ind)) for ind in population}

# Tournament Selection
def tournament_selection(population, fitness):
    a, b = random.sample(population, 2)
    return a if fitness[a] > fitness[b] else b

# Uniform Crossover
def uniform_crossover(parent1, parent2):
    child = ''.join(random.choice([p1, p2]) for p1, p2 in zip(parent1, parent2))
    return child

# Adaptive Mutation
def adaptive_mutation(binary_str, generation, max_generations):
    mutation_prob = 1 / (1 + math.exp(generation - max_generations / 2))  # Sigmoid-based adaptive rate
    mutated = ''.join(
        bit if random.random() > mutation_prob else str(1 - int(bit))
        for bit in binary_str
    )
    return mutated

# Genetic Algorithm
def genetic_algorithm(pop_size=20, generations=50):
    population = generate_population(pop_size)

    for gen in range(generations):
        fitness = evaluate_population(population)
        new_population = []
        
        for _ in range(pop_size // 2):  # Create new population
            p1, p2 = tournament_selection(population, fitness), tournament_selection(population, fitness)
            child1, child2 = uniform_crossover(p1, p2), uniform_crossover(p1, p2)
            child1, child2 = adaptive_mutation(child1, gen, generations), adaptive_mutation(child2, gen, generations)
            new_population.extend([child1, child2])

        population = new_population

    # Get the best individual
    final_fitness = evaluate_population(population)
    best_individual = max(final_fitness, key=final_fitness.get)
    
    return best_individual, binary_to_decimal(best_individual), final_fitness[best_individual]

# Run the algorithm
best_bin, best_x, best_f = genetic_algorithm()
print(f"Best Individual: {best_bin} (x = {best_x}) -> f(x) = {best_f}")
