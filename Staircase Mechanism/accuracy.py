import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from staircase import Staircase
from laplace import Laplace
# from diffprivlib.mechanisms import Laplace
# from diffprivlib.mechanisms import Staircase

# Load the data
data = pd.read_csv('dataset/adult.csv')

# Extract column
query_data = data['age']

# Define sensitivity
sensitivity = 1

# Define gamma value for the Staircase mechanism
gamma = 1

# Define epsilon values
epsilon_values = np.linspace(1, 100, 10)

# Calculate actual mean value
actual_mean = query_data.mean()

# Initialize lists to store absolute differences for Laplace and Staircase mechanisms
laplace_accuracy = []
staircase_accuracy = []

# Create instances of Laplace and Staircase mechanisms
laplace = Laplace(epsilon=epsilon_values[0], sensitivity=sensitivity)
staircase = Staircase(epsilon=epsilon_values[0], sensitivity=sensitivity, gamma=gamma)

# Calculate accuracy for Laplace mechanism
for epsilon in epsilon_values:
    laplace.epsilon = epsilon
    noisy_mean = laplace.randomise(query_data.mean())
    laplace_accuracy.append(abs(noisy_mean - actual_mean))

# Calculate accuracy for Staircase mechanism
for epsilon in epsilon_values:
    staircase.epsilon = epsilon
    noisy_mean = staircase.randomise(query_data.mean())
    staircase_accuracy.append(abs(noisy_mean - actual_mean))

# Plot the results
plt.plot(epsilon_values, laplace_accuracy, label='Laplace Mechanism', marker='o', linestyle='-', color='blue')
plt.plot(epsilon_values, staircase_accuracy, label='Staircase Mechanism', marker='o', linestyle='-', color='green')

plt.xlabel('Epsilon')
plt.ylabel('Absolute Difference')
plt.title('Accuracy Comparison between Laplace and Staircase Mechanisms')
plt.legend()
plt.grid(True)
plt.show()
