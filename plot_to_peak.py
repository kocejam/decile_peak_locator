import matplotlib.pyplot as plt
import scipy
import numpy as np
import pandas as pd
import random

def input_true_or_false(string):
    yes = {'yes','y', 'Yes', 'Y', 'Yes.', 'yes.'}
    no = {'no', 'n', 'No', 'N', 'No.', 'no.'}

    if choice in yes:
        DEFAULT = True
    elif choice in no:
        DEFAULT = False
    else:
        DEFAULT = True

    return DEFAULT


choice = input("Use default values? Answer with yes (y) or no (n). \n "
               "(Percentage threshold = 90%, lift threshold = 5%, grids = on)\n")

DEFAULT = input_true_or_false(choice)

if DEFAULT:
    MAX_THRESHOLD = 0.9
    LIFT_THRESHOLD = 0.05
    GRID_OR_NO = True
else:
    while (True):
        try:
            MAX_THRESHOLD = float(input("Percentage threshold? Answer with percentage from 0 to 100.\n")) / 100
        except:
            print("Please respond with a number between 0 and 100.\n")
            continue

        try:
            LIFT_THRESHOLD = float(input("Lift threshold? Answer with percentage from 0 to 100.\n")) / 100
        except:
            print("Please respond with a number between 0 and 100.\n")
            continue

        GRID_OR_NO = input_true_or_false(input("Grids?\n"))

        break


example = {}
counter = 0
for i in range(11):
    example[i] = counter
    counter += 100 * (2 ** - i)

print(example)

def function_to_values(function):
    pass

def dict_to_tuples(d):
    tups = []
    for k, v in d.items():
        tups.append(tuple([k, v]))

    return tups

def tuples_to_plot_ready(tups):
    x = []
    y = []
    for tup in tups:
        x.append(tup[0])
        y.append(tup[1])

    return x, y

def dict_to_decile_list(d):
    _ , y = tuples_to_plot_ready(dict_to_tuples(d))
    return y


def peak_for_lift(decile, lift):
    """
    :param decile: (list/dict) ex: [0, 5, 89, 104, 188, 249, 277, 300, 341, 432, 479]
    :param lift: (float) percentage of total where you'd want to stop for a peak
    :return the decile in which you should stop for this peak
    """
    total = decile[10]

    threshold_step = lift * total

    for i in range(2, len(decile)):
        current = decile[i]
        previous = decile[i - 1]

        # If the current decile's step was too high, then return the previous decile to make the threshold cut
        if current - previous < threshold_step:
            return i - 1


    # No peak was found
    return 10


def peak_for_max_threshold(decile, thresh_per):
    """
    :param decile: (list/dict) ex: [0, 5, 89, 104, 188, 249, 277, 300, 341, 432, 479]
    :param thresh_per:
    :return: the decile in which you should stop for this peak
    """
    total = decile[10]

    threshold = thresh_per * total

    for i in range(1, len(decile)):
        current = decile[i]

        # If the current decile's step was too low, then return the previous decile to make the threshold cut
        if current > threshold:
            return i - 1

def peak_for_last_lift(decile, lift):
    """
    :param decile: (list/dict) ex: [0, 5, 89, 104, 188, 249, 277, 300, 341, 432, 479]
    :param lift: (float) percentage of total where you'd want to stop for a peak
    :return the decile in which you should stop for this peak
    """
    total = decile[10]

    threshold_step = lift * total

    for i in range(len(decile) - 1, 0, -1):
        current = decile[i]
        previous = decile[i - 1]

        # If the current decile's step was too high, then return the previous decile to make the threshold cut
        if current - previous > threshold_step:
            return i


    # No peak was found
    return 10

def draw_horizontal_line(decile, thresh_per):
    total = decile[10]

    threshold = thresh_per * total

    x = []
    y = []

    for i in range(11):
        x.append(i)
        y.append(threshold)

    plt.plot(x, y, 'r')

    return


def df_to_list(dataf):
    new = []

    for elem in dataf[0]:
        new.append(elem)

    return new

def create_curve():
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

    df.plot(kind="line")

    return df


x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
example_list = [0, 300, 500, 700, 850, 900, 920, 940, 970, 990, 1000]   # Dummy example

example_list = df_to_list(create_curve())



# Regular plot
ax = plt.subplot(221)
ax.set_yticks(scipy.arange(0, 1.1, 0.1))
ax.set_xticks(scipy.arange(0, 11, 1))
plt.plot(x, example_list)
plt.grid(GRID_OR_NO)

# Plot showing percentage threshold
ax = plt.subplot(222)
ax.set_yticks(scipy.arange(0, 1.1, 0.1))
ax.set_xticks(scipy.arange(0, 11, 1))
plt.plot(x, example_list)
plt.grid(GRID_OR_NO)
draw_horizontal_line(example_list, MAX_THRESHOLD)
percentage_max = peak_for_max_threshold(example_list, MAX_THRESHOLD)
plt.annotate('percentage peak',
             xy=(percentage_max, (example_list[percentage_max])),
             xytext=(3, 0),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

# Plot showing lift thresholds
ax = plt.subplot(223)
ax.set_yticks(scipy.arange(0, 1.1, 0.1))
ax.set_xticks(scipy.arange(0, 11, 1))
plt.plot(x, example_list)
plt.grid(GRID_OR_NO)
lift_max = peak_for_lift(example_list, LIFT_THRESHOLD)
lift_last_max = peak_for_last_lift(example_list, LIFT_THRESHOLD)
plt.annotate('first lift',
             xy=(lift_max - 0.5, (example_list[lift_max] + example_list[lift_max - 1]) / 2),
             xytext=(3, 0),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
plt.annotate('last lift',
             xy=(lift_last_max - 0.5, (example_list[lift_last_max] + example_list[lift_last_max - 1]) / 2),
             xytext=(6, .15),
             arrowprops=dict(facecolor='black', shrink=0.015),
             )

# Plot with annotations stating best deciles to use
ax = plt.subplot(224)
ax.set_yticks(scipy.arange(0, 1.1, 0.1))
ax.set_xticks(scipy.arange(0, 11, 1))
plt.plot(x, example_list)
plt.grid(GRID_OR_NO)
plt.annotate('best per decile = ' + str(percentage_max),
             xy=(lift_max - 0.5, (example_list[lift_max] + example_list[lift_max - 1]) / 2),
             xytext=(5, 0),
             )
plt.annotate('best first lift decile = ' + str(lift_max),
             xy=(lift_max - 0.5, (example_list[lift_max] + example_list[lift_max - 1]) / 2),
             xytext=(5, .15),
             )
plt.annotate('best last lift decile = ' + str(lift_last_max),
             xy=(lift_max - 0.5, (example_list[lift_max] + example_list[lift_max - 1]) / 2),
             xytext=(5, .3),
             )




plt.show()
