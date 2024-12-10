import streamlit as st
import random

st.set_page_config(
    page_title="Genetic Algorithm: Scheduling Problem"
)

st.header("Genetic Algorithm: Scheduling Problem", divider="gray")

# Define constants
POP_SIZE = 500  # Population size
GENES = range(10)  # Assume 10 time slots for simplicity

# Initialization: Random schedules
def initialize_pop(num_tasks):
    population = []
    for _ in range(POP_SIZE):
        schedule = [random.choice(GENES) for _ in range(num_tasks)]
        population.append(schedule)
    return population

# Fitness calculation: Minimize conflicts (e.g., tasks in the same time slot)
def fitness_cal(schedule):
    conflicts = 0
    seen = {}
    for time_slot in schedule:
        if time_slot in seen:
            conflicts += 1
        else:
            seen[time_slot] = True
    return conflicts

# Selection: Return top 50% based on fitness
def selection(population):
    population.sort(key=lambda x: x[1])  # Sort by fitness
    return population[:POP_SIZE // 2]

# Crossover: Create offspring by combining two parents
def crossover(selected, num_tasks, co_rate):
    offspring = []
    for _ in range(POP_SIZE):
        if random.random() < co_rate:
            parent1, parent2 = random.sample(selected, 2)
            crossover_point = random.randint(1, num_tasks - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            offspring.append(child)
        else:
            offspring.append(random.choice(selected))
    return offspring

# Mutation: Randomly alter time slots
def mutate(offspring, mut_rate):
    for schedule in offspring:
        for i in range(len(schedule)):
            if random.random() < mut_rate:
                schedule[i] = random.choice(GENES)
    return offspring

# Main Genetic Algorithm
def main(num_tasks, co_rate, mut_rate):
    # 1) Initialize population
    population = initialize_pop(num_tasks)
    population = [[schedule, fitness_cal(schedule)] for schedule in population]
    generation = 1

    while True:
        # 2) Select the best schedules
        selected = selection(population)

        # 3) Perform crossover
        selected_schedules = [chromosome for chromosome, _ in selected]
        offspring = crossover(selected_schedules, num_tasks, co_rate)

        # 4) Mutate offspring
        mutated_offspring = mutate(offspring, mut_rate)

        # 5) Evaluate fitness of offspring
        new_generation = [[schedule, fitness_cal(schedule)] for schedule in mutated_offspring]

        # 6) Replace worst individuals in the population
        population = selection(population + new_generation)

        # Check if an optimal solution is found
        if population[0][1] == 0:
            st.write(f"Optimal schedule found in generation {generation}")
            st.write("Schedule:", population[0][0])
            break

        # Display progress
        st.write(f"Generation: {generation}, Best Fitness: {population[0][1]}")
        generation += 1

# Streamlit form for input
with st.form("scheduler_form"):
    num_tasks = st.number_input("Number of tasks", min_value=1, value=5)
    co_rate = st.number_input("Crossover rate (CO_R)", min_value=0.0, max_value=0.95, value=0.8)
    mut_rate = st.number_input("Mutation rate (MUT_R)", min_value=0.01, max_value=0.05, value=0.2)
    calculate = st.form_submit_button("Calculate")

    if calculate:
        main(num_tasks, co_rate, mut_rate)

st.form_submit_button() 
