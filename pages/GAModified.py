import streamlit as st
import csv
import random
import requests

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

# Function to read CSV from GitHub raw URL
def read_csv_from_github(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we get a valid response
    lines = response.text.splitlines()
    program_ratings = {}

    reader = csv.reader(lines)
    header = next(reader)  # Skip the header
    for row in reader:
        program = row[0]
        ratings = [float(x) for x in row[1:]]  # Convert ratings to floats
        program_ratings[program] = ratings
    return program_ratings

# Sidebar for Input
st.sidebar.header("Upload Data or Enter GitHub URL")
uploaded_file = st.sidebar.file_uploader("Upload the program ratings CSV file", type=["csv"])
github_url = st.sidebar.text_input(
    "Alternatively, enter GitHub raw CSV URL",
    "https://raw.githubusercontent.com/your_username/your_repo/main/program_ratings.csv"
)

ratings = {}
if uploaded_file:
    def read_csv_to_dict(file_obj):
        program_ratings = {}
        reader = csv.reader(file_obj)
        header = next(reader)  # Skip the header
        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]
            program_ratings[program] = ratings
        return program_ratings

    ratings = read_csv_to_dict(uploaded_file)
    st.sidebar.success("Data uploaded successfully!")
elif github_url:
    try:
        ratings = read_csv_from_github(github_url)
        st.sidebar.success("Data loaded from GitHub successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading data from GitHub: {e}")

# Continue with optimization code...
all_programs = list(ratings.keys()) if ratings else []
if not ratings:
    st.warning("Please provide a CSV file or a valid GitHub URL to proceed.")
else:
    # Rest of your existing optimization code goes here...
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
