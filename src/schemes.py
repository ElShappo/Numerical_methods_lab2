import numpy as np
from constants import a


def angle_scheme(foo, h, courant, desired_time_index, renowned_row, renowned_time_index):
    # 'desired_time' is the time for which the values of a 'foo' we are eager to find (corresponds to a row)
    # 'renowned_row' - row which values we all know, 'renowned_time' is the time that corresponds to this row
    tau = courant*h/a
    desired_row = np.zeros(len(renowned_row))

    next_val_t = lambda curr_x, prev_x: curr_x - courant * (curr_x - prev_x)
    delta = desired_time_index - renowned_time_index

    for i in range(delta):
        desired_row[0] = foo(0, (renowned_time_index+i+1)*tau)
        for j in range(1, len(desired_row)):  # iterate over x-axis
            desired_row[j] = next_val_t(renowned_row[j], renowned_row[j-1])
        renowned_row = list(desired_row)

    return desired_row


def lax_scheme(foo, h, courant, desired_time_index, renowned_row, renowned_time_index):
    # 'desired_time' is the time for which the values of a 'foo' we are eager to find (corresponds to a row)
    # 'renowned_row' - row which values we all know, 'renowned_time' is the time that corresponds to this row

    tau = courant*h/a
    delta = desired_time_index - renowned_time_index

    desired_row = np.zeros(len(renowned_row))

    next_val_t = lambda curr_x, prev_x, next_x: courant**2/2*(next_x-2*curr_x+prev_x)-courant/2*(next_x-prev_x)+curr_x

    # print('renowned:', len(renowned_row))
    # print('desired:', len(renowned_row)-delta)

    for i in range(delta):
        # print('i =',i)
        desired_row[0] = foo(0, (renowned_time_index+i+1)*tau)

        for j in range(1, len(desired_row)-i-1):  # iterate over x-axis
            # print('j =',j)
            desired_row[j] = next_val_t(renowned_row[j], renowned_row[j-1], renowned_row[j+1])
        renowned_row = list(desired_row)
        # print('hi')

    # base_x_list_len = math.ceil(l/h)
    # extra_x_list_len = int(base_x_list_len+last_t_index-desired_time_index)

    return desired_row[:len(renowned_row)-delta]
