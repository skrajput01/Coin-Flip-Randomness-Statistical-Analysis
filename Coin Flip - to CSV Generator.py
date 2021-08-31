# 23/08/21 - 31/08/21
# Creates a randomly generated array and saves it as a CSV file
import numpy as np
import time

# Number of trials (ranging from 0 to 1; where 0 represents Heads, and 1 represents Tails)
n = 1
# Probability of success
p = 0.5
# Size
n_flips = int(input("Enter Number of Flips: "))
# Binomial distribution (repeated 100 times) to flip a coin and record outcomes
flips = np.random.binomial(n, p, size=n_flips)
# Creates a time stamp of when flips were performed
t = time.strftime("%H%M%S-%d%m%y")
# Saves coin toss outcomes as a csv file (with a unique filename - allowing the user to store multiple trials)
np.savetxt(f"Coin_flip_{n_flips}_{t}.csv", flips, fmt="%i", delimiter=",")

# Displays outcomes of each flip as an array
print(flips)
# Displays number of Heads and Tails flipped
Heads = np.count_nonzero(flips == 0)
Tails = np.count_nonzero(flips == 1)
print("Heads", Heads)
print("Tails", Tails)
