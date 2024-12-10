import streamlit as st
import csv
import random

# Page Configuration
st.set_page_config(
    page_title="TV Program Scheduling Optimization",
    page_icon="📺"
)

st.header("📺 TV Program Scheduling Optimization", divider="gray")

# Constants
GEN = 100  # Number of generations
POP = 50  # Population size
DEFAULT_CO_R = 0.8  # Default Crossover rate
DEFAULT_MUT_R = 0.2  # Default Mutation rate
EL_S = 2  # Elitism size
ALL_TIME_SLOTS = list(range(6, 24))  # Time slots

# CSV Reading Function
def read_csv_to_dict(file_path):
    program_ratings = {}
    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]  # Convert ratings to floats
            program_ratings[program] = ratings
    return program_ratings

# Load Data
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload the program ratings CSV file", type=["csv"])
ratings = {}

if uploaded_file:
    ratings = read_csv_to_dict(uploaded_file)
    st.sidebar.success("Data uploaded successfully!")
    all_programs = list(ratings.keys())
else:
    st.sidebar.warning("Please upload a CSV file to proceed.")
    all_programs = []

# Fitness Function
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]
    return total_rating

# Initialize Population
def initialize_pop(programs, time_slots):
    if not programs:
        return [[]]

    all_schedules = []
    for i in range(len(programs)):
        for schedule in initialize_pop(programs[:i] + programs[i + 1:], time_slots):
            all_schedules.append([programs[i]] + schedule)

    return all_schedules

# Finding Best Schedule (Brute Force)
def finding_best_schedule(all_schedules):
    best_schedule = []
    max_ratings = 0

    for schedule in all_schedules:
        total_ratings = fitness_function(schedule)
        if total_ratings > max_ratings:
            max_ratings = total_ratings
            best_schedule = schedule

    return best_schedule

# Genetic Algorithm
def genetic_algorithm(initial_schedule, generations=GEN, population_size=POP, crossover_rate=DEFAULT_CO_R, mutation_rate=DEFAULT_MUT_R, elitism_size=EL_S):
    population = [initial_schedule]
    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for generation in range(generations):
        new_population = []

        # Elitism
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    return population[0]

# Crossover Function
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

# Mutation Function
def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

# Main Logic
if ratings:
    st.sidebar.header("Parameters")
    GEN = st.sidebar.number_input("Number of Generations", min_value=1, value=100)
    POP = st.sidebar.number_input("Population Size", min_value=2, value=50)
    CO_R = st.sidebar.slider("Crossover Rate", min_value=0.0, max_value=1.0, value=DEFAULT_CO_R, step=0.05)
    MUT_R = st.sidebar.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=DEFAULT_MUT_R, step=0.05)
    EL_S = st.sidebar.number_input("Elitism Size", min_value=1, value=2)

    initial_schedule = all_programs[:len(ALL_TIME_SLOTS)]
    all_possible_schedules = initialize_pop(all_programs, ALL_TIME_SLOTS)

    st.write("### Running Brute Force Optimization...")
    initial_best_schedule = finding_best_schedule(all_possible_schedules)
    rem_t_slots = len(ALL_TIME_SLOTS) - len(initial_best_schedule)

    st.write("### Running Genetic Algorithm...")
    genetic_schedule = genetic_algorithm(
        initial_best_schedule,
        generations=GEN,
        population_size=POP,
        crossover_rate=CO_R,
        mutation_rate=MUT_R,
        elitism_size=EL_S
    )
    final_schedule = initial_best_schedule + genetic_schedule[:rem_t_slots]

    st.subheader("📅 Final Optimal Schedule")
    for time_slot, program in enumerate(final_schedule):
        st.write(f"Time Slot {ALL_TIME_SLOTS[time_slot]:02d}:00 - Program {program}")

    st.write("💯 **Total Ratings:**", fitness_function(final_schedule))
else:
    st.warning("Please upload a CSV file to see results.")
