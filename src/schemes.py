import numpy as np
from constants import a, l, lt
from auxiliary import get_grid


def angle_scheme(foo, h, courant, desired_time_index, renowned_row, renowned_time_index):
    # 'desired_time' is the time for which the values of a 'foo' we are eager to find (corresponds to a row)
    # 'renowned_row' - row which values we all know, 'renowned_time' is the time that corresponds to this row
    tau = courant*h/a
    desired_time = tau*desired_time_index

    desired_row = np.arange(0, l, h)
    desired_row[0] = foo(0, desired_time)

    next_val_t = lambda curr_x, prev_x: curr_x - courant * (curr_x - prev_x)
    delta = desired_time_index - renowned_time_index

    for i in range(delta):
        for j in range(1, len(desired_row)):  # iterate over x-axis
            desired_row[j] = next_val_t(renowned_row[j], renowned_row[j-1])
        renowned_row = list(desired_row)

    return desired_row


def lax_scheme(foo, h, courant):
    tau = courant*h/a
    x_list = np.arange(0, l, h)
    t_list = np.arange(0, lt, tau)
    result = [[0 for x in x_list] for t in t_list]

    t0 = [foo(x, 0) for x in x_list]
    x0 = [foo(0, t) for t in t_list]

    result[0] = t0

    for i in range(len(t_list)):
        result[i][0] = x0[i]

    next_val_t = lambda curr, next_x, prev_x: courant**2/2*(next_x-2*curr+prev_x)-courant/2*(next_x-prev_x)+curr
    grid = get_grid(x_list, t_list)

    for i in range(1, len(grid)):  # i iterates over t-axis
        row = grid[i]
        for j in range(1, len(row)-1):  # j iterates over x-axis
            result[i][j] = next_val_t(result[i-1][j], result[i-1][j+1], result[i-1][j-1])
    return result