import streamlit as st
import random

# Streamlit page configuration
st.set_page_config(
    page_title="Genetic Algorithm: Scheduling Problem",
    page_icon="🧬"
)

st.header("Genetic Algorithm: Scheduling Problem", divider="gray")

# Constants and Gene Pool (10 time slots)
POP_SIZE = 500
GENES = range(10)

# Function to initialize the population with random schedules
def initialize_pop(num_tasks):
    population = []
    for _ in range(POP_SIZE):
        schedule = [random.choice(GENES) for _ in range(num_tasks)]
        population.append(schedule)
    return population

# Function to calculate fitness (conflicts minimization)
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

# Crossover: Generate offspring with crossover rate
def crossover(selected, num_tasks, co_rate):
    offspring = []
    for _ in range(POP_SIZE):
        if random.random() < co_rate:  # Perform crossover with probability `co_rate`
            parent1, parent2 = random.sample(selected, 2)
            crossover_point = random.randint(1, num_tasks - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
        else:
            child = random.choice(selected)  # Retain a parent directly
        offspring.append(child)
    return offspring

# Mutation: Randomly alter tasks based on mutation rate
def mutate(offspring, mut_rate):
    for schedule in offspring:
        for i in range(len(schedule)):
            if random.random() < mut_rate:  # Mutate with probability `mut_rate`
                schedule[i] = random.choice(GENES)
    return offspring

# Main Genetic Algorithm function
def main(num_tasks, co_rate, mut_rate):
    # Initialize the population
    population = initialize_pop(num_tasks)
    population = [[schedule, fitness_cal(schedule)] for schedule in population]
    generation = 1

    while True:
        # Selection of best schedules
        selected = selection(population)

        # Extract schedules for crossover
        selected_schedules = [chromosome for chromosome, _ in selected]

        # Crossover to produce offspring
        offspring = crossover(selected_schedules, num_tasks, co_rate)

        # Mutate the offspring
        mutated_offspring = mutate(offspring, mut_rate)

        # Evaluate fitness of the new generation
        new_generation = [[schedule, fitness_cal(schedule)] for schedule in mutated_offspring]

        # Replace the worst schedules with new generation
        population = selection(population + new_generation)

        # Check for optimal solution (no conflicts)
        if population[0][1] == 0:
            st.write(f"🎉 **Optimal schedule found in generation {generation}**")
            st.write("📅 Schedule:", population[0][0])
            break

        # Display progress
        st.write(f"Generation: {generation}, Best Fitness: {population[0][1]}")
        generation += 1

# Streamlit form for input
with st.form("scheduler_form"):
    num_tasks = st.number_input("🔢 Number of tasks", min_value=1, value=5)
    co_rate = st.number_input("⚙️ Crossover rate (CO_R)", min_value=0.0, max_value=0.95, value=0.8)
    mut_rate = st.number_input("🧬 Mutation rate (MUT_R)", min_value=0.01, max_value=0.05, value=0.2)
    calculate = st.form_submit_button("🚀 Run Genetic Algorithm")

    if calculate:
        main(num_tasks, co_rate, mut_rate)
