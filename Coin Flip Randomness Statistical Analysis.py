# 23/08/21 - 31/08/21
# Uses array from CSV file and analyzes it to determine if it has been randomly generated
from itertools import groupby
from math import comb
import numpy as np
import matplotlib.pyplot as plt
# PROGRAMMER'S NOTE - Analysis is valid for up to 1020 Coin Flips


print("Coin Flip Randomness Statistical Analysis - by Shyam Kumar Rajput", "\n")
print("0 Represents Heads, 1 Represents Tails")

# Name of CVS file
filename = "Coin_flip_1000_165749-310821"

# Opens CSV file with coin flips (as 0 - for Heads, 1 - for Tails) and converts it to a NumPy array
flips = np.genfromtxt(f'{filename}.csv', delimiter=',').astype(int)
# Probability of success (p = 0.5 for unbiased coins)
p = 0.5
# Displays outcomes of each flip as a NumPy array
print(flips, "\n")
# Converts 0 and 1 outcomes to Heads and Tails respectively
Heads = np.count_nonzero(flips == 0)
Tails = np.count_nonzero(flips == 1)
# N - Total number of coin flips
N = Heads + Tails


# STREAKS TEST
streak_heads = 1
streak_tails = 1
max_streak_heads = 1
max_streak_tails = 1
for i in range(len(flips)):
    # Heads streaks
    if flips[i] == flips[i-1] == 0:
        streak_heads += 1
        streak_tails = 1
        if streak_heads > max_streak_heads:
            max_streak_heads = streak_heads
    # Tails streaks
    elif flips[i] == flips[i-1] == 1:
        streak_tails += 1
        streak_heads = 1
        if streak_tails > max_streak_tails:
            max_streak_tails = streak_tails
    else:
        streak_heads = 1
        streak_tails = 1


# RUNS TEST
# E - Expected number of runs
E = ((2*Heads*Tails)/N) + 1
# S - Standard deviation
S = np.sqrt((2*Heads*Tails*(2*Heads*Tails - N))/((N**2)*(N - 1)))
# R - Number of observed runs
R = len([i[0] for i in groupby(flips)])
# Z - Z-Value
if R > E:
    Z = (R - E - 0.5)/S
elif R < E:
    Z = (R - E + 0.5)/S
else:
    Z = (R - E)/S


# HEADS TEST
# Array for Heads
N_array = np.arange(0, N+1)
# Creates an array of Binomial PD P-values
B_pd_array = []
for i in N_array:
    B_pd = comb(N, i)*(p**i)*(1 - p)**(N - i)
    B_pd_array.append(B_pd)
# Converts Binomial PD array into a Binomial CD array (using cumulative sum)
B_cd_array = np.cumsum(B_pd_array)

# P-value for Heads flipped for Binomial PD (equal to {Heads})
B_heads_pd = B_pd_array[Heads]
# P-value for Tails flipped for Binomial PD (equal to {Tails})
B_tails_pd = B_pd_array[Tails]
# P-Value for Heads flipped for Binomial CD (less than or equal to {Heads} & greater than or equal to {Heads})
B_heads_less_cd = B_cd_array[Heads]
B_heads_greater_cd = 1 - B_cd_array[Heads - 1]
print(f"Heads~B({N}, {p})")
print(f"P(Heads≤{Heads}):", B_heads_less_cd)
print(f"P(Heads≥{Heads})", B_heads_greater_cd)
# Lower Critical Region (LCR) & Binomial PD at LCR
B_lcr = np.where(B_cd_array <= 0.05)[-1][-1]
B_lcr_pd = B_pd_array[B_lcr]
print(f"Lower Critical Region: P(≤{B_lcr})")
# Upper Critical Region (UCR) & Binomial PD at UCR
B_ucr = np.where(B_cd_array >= 0.95)[0][0] + 1
B_ucr_pd = B_pd_array[B_ucr]
print(f"Upper Critical Region: P(≥{B_ucr})")


# DISPLAY CALCULATIONS
print("")
print("Heads (0):", Heads)
print("Tails (1):", Tails)
print("N:", N)
print("Max Heads Streak:", max_streak_heads)
print("Max Tails Streak:", max_streak_tails)
print("Expected Runs:", E)
print("Observed Runs:", R)
print("Standard Deviation:", S)
print(f"Z-Value for {R} Runs:", Z)
print("")

# Displays P-Value Test for Heads Outcome
if B_heads_less_cd <= 0.05 or B_heads_greater_cd >= 0.95:
    print(f"P-Value Test for {Heads} Heads (at 2-Tail 10% Sig Level): FAILED - These Coin Flips are UNLIKELY RANDOM")
else:
    print(f"P-Value Test for {Heads} Heads (at 2-Tail 10% Sig Level): PASSED - These Coin Flips are LIKELY RANDOM")
print("")

# Displays Z-Value for
if -2 < Z < 2:
    print(f"Z-Value Test for {R} Runs (at 2 SD): PASSED - as Observed Number of Runs lies within {Z} Standard Deviations of the Expected Number of Runs")
else:
    print(f"Z-Value Test for {R} Runs (at 2 SD): FAILED - as Observed Number of Runs lies outside 2 Standard Deviations of the Expected Number of Runs")
print("")


# MATPLOTLIB
# Set X-Axis & Y-Axis
fig1, ax1 = plt.subplots()
ax1.spines["left"].set_position("zero")
ax1.spines["bottom"].set_position("zero")
ax1.spines["top"].set_color("none")
ax1.spines["right"].set_color("none")

# Plot Distribution
plt.plot(N_array, B_pd_array, color="tab:blue")
# Plot Mean
plt.vlines(x=np.argmax(B_pd_array), ymin=0, ymax=np.amax(B_pd_array), color='k', linestyle='-', label="Mean")
# Plot Heads
plt.vlines(x=Heads, ymin=0, ymax=B_heads_pd, color='g', linestyle='-', label="Heads")
# Plot Tails
plt.vlines(x=Tails, ymin=0, ymax=B_tails_pd, color='tab:purple', linestyle='-', label="Tails")
# Plot Lower Critical Area
B_lcr_array = np.arange(0, B_lcr+1)
B_lcr_pd_array = []
for i in range(len(B_lcr_array)):
    B_lcr_pd_array.append(B_pd_array[i])
ax1.fill_between(B_lcr_array, B_lcr_pd_array, color="tab:red", label="Critical Region")
# Plot Upper Critical Area
B_ucr_array = np.arange(B_ucr, N+1)
B_ucr_pd_array = []
for i in B_ucr_array:
    B_ucr_pd_array.append(B_pd_array[i])
ax1.fill_between(B_ucr_array, B_ucr_pd_array, color="r")

# Show Plot
plt.title("Binomial Distribution of Coin Flips")
plt.xlabel("Number Flipped")
plt.ylabel("Probability Density")
plt.grid()
plt.legend()
plt.show()
