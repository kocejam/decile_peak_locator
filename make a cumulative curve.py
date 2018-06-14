import matplotlib as plt
import numpy as np
import pandas as pd
import random

# number of bins
NUM_PERCENTILES = 10

# create a data frame of ones
df = pd.DataFrame(np.ones(NUM_PERCENTILES + 1))

cumulative_value = 0
bin_value = 0
current_bin = 1
num_bins = len(df.index) - 1

# set the first bin's value to 0
df[0][0] = 0

# replace the 1's in the dataframe with the cumulative values
while (cumulative_value < 1) & (current_bin <= num_bins):
    # each segment can be one of three types
    curve_type = random.randint(1, 3)

    if (curve_type == 1):  # draw a straight line from the current cumulative value to 100% in the last bin
        bin_value = (1 - cumulative_value) / (num_bins - current_bin + 1)
    elif (curve_type == 2):  # increase the cumulative value more than a straight line
        min_value = (1 - cumulative_value) / (num_bins - current_bin + 1)
        bin_value = random.uniform(min_value, 1)
    else:  # increase the cumulative value less than a straight line
        max_value = (1 - cumulative_value) / (num_bins - current_bin + 1)
        bin_value = random.uniform(0, max_value)

    cumulative_value += bin_value
    print(current_bin, bin_value, cumulative_value)
    if (cumulative_value > 1):
        cumulative_value = 1
    df[0][current_bin] = cumulative_value
    current_bin += 1

print(df[0][1])
df.plot(kind="line")
# plt.show()