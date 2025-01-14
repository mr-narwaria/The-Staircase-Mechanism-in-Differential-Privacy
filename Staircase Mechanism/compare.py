import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from staircase import Staircase
from laplace import Laplace

# Load the data
data = pd.read_csv('dataset/adult.csv')

# Extract column
query_data = data['hours-per-week']
# query_data = data['age']

# Define sensitivity (for age, it could be 1 as an approximation) global parameter
sensitivity = 1

# Define gamma value for the Staircase mechanism
gamma = 1

# Define epsilon values
epsilon_values = np.linspace(1, 100, 10)

# Calculate actual values
actual_values = query_data.mean()
print("Actual mean value: ", actual_values)

# Initialize lists to store randomized values for Staircase and Laplace mechanisms
staircase_randomized_values = []
laplace_randomized_values = []

# Create instances of Staircase and Laplace mechanisms
staircase = Staircase(epsilon=epsilon_values[0], sensitivity=sensitivity, gamma=gamma)
laplace = Laplace(epsilon=epsilon_values[0], sensitivity=sensitivity)

# Randomize the values for each epsilon value for Staircase mechanism
print("\nStaircase values: ")
for epsilon in epsilon_values:
    staircase.epsilon = epsilon
    staircase.gamma = gamma
    randomized_value = np.mean([staircase.randomise(val) for val in query_data])
    staircase_randomized_values.append(randomized_value)
    print(randomized_value)

# Randomize the values for each epsilon value for Laplace mechanism
print("\nLaplace values: ")
for epsilon in epsilon_values:
    laplace.epsilon = epsilon
    randomized_value = np.mean([laplace.randomise(val) for val in query_data])
    laplace_randomized_values.append(randomized_value)
    print(randomized_value)

# Plot the graph for Actual, Staircase, and Laplace Randomized Values
plt.plot(epsilon_values, [actual_values]*len(epsilon_values), label='Actual Values', linestyle='--', color='blue')
plt.plot(epsilon_values, staircase_randomized_values, label='Staircase Randomized Values', marker='o', linestyle='-', color='green')
plt.plot(epsilon_values, laplace_randomized_values, label='Laplace Randomized Values', marker='o', linestyle='-', color='red')

plt.xlabel('Epsilon')
plt.ylabel('Value')
plt.title('Actual vs Randomized Values Laplace vs Randomized Values Staircase')
plt.legend()
plt.grid(True)
plt.show()
