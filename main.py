import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera

a = 0.1  # propagation speed
l = 10   # right border (x-axis)
lt = 50  # right border (t-axis)


def get_grid(x_list, t_list):
    grid = []  # grid[i][j] - usage, where grid[i] is a row

    for t in t_list:
        grid += [[(x, t) for x in x_list]]
    return grid


def pulse_function(x, t):
    if a*t <= x <= a*t + 1:
        return 1
    return 0


def bell_function(x, t):
    if a*t < x < a*t + 1:
        x0 = 0.5 + a*t
        return np.exp(-(x-x0)**2/(0.25-(x-x0)**2))
    return 0


def parabola_function(x, t):
    x0 = 1 + a*t
    if x0-1 <= x <= x0+1:
        return 1-(x-x0)**2
    return 0


def sine_function(x, t):
    x0 = 1 + a*t
    if x0-1 <= x <= x0+1:
        return (np.cos(np.pi/2*np.abs(x-x0)))**3
    return 0


def numeric_angle_scheme(foo, h, courant, desired_time_index, renowned_row, renowned_time_index):
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


def numeric_lax_scheme(foo, h, courant):
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


def plot_over_time(foo, scheme, h1=0.1, h2=0.01, courant=0.7):
    tau_h1 = courant*h1/a

    x_list_h1 = np.arange(0, l, h1)
    x_list_h2 = np.arange(0, l, h2)

    t_list_h1 = np.arange(0, lt, tau_h1)

    t0_h1 = [foo(x, 0) for x in x_list_h1]
    t0_h2 = [foo(x, 0) for x in x_list_h2]

    numeric_solution_h1 = []
    numeric_solution_h2 = []

    error_list_h1 = []
    error_list_h2 = []

    fig, ax = plt.subplots(2, figsize=(16, 9))
    camera = Camera(fig)

    ax[0].set_title(f'{scheme.__name__}, {foo.__name__}, a = {a}, Courant = {courant}')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')

    ax[1].set_title('Error from time')
    ax[1].set_xlabel('t')
    ax[1].set_ylabel('max_error')

    plt.subplots_adjust(hspace=0.4)

    for i in range(1, len(t_list_h1)):
        t = t_list_h1[i]

        if i == 1:
            numeric_solution_h1 = scheme(foo, h1, courant, i, t0_h1, i-1)
            numeric_solution_h2 = scheme(foo, h2, courant, i*10, t0_h2, (i-1)*10)
        else:
            numeric_solution_h1 = scheme(foo, h1, courant, i, list(numeric_solution_h1), i-1)
            numeric_solution_h2 = scheme(foo, h2, courant, i*10, list(numeric_solution_h2), (i-1)*10)

        y_list_for_foo = [foo(x, t) for x in x_list_h1]

        error_list_h1 += [max([np.abs(x-y) for x, y in zip(y_list_for_foo, numeric_solution_h1)])]
        error_list_h2 += [max([np.abs(x-y) for x, y in zip(y_list_for_foo, numeric_solution_h2[::10])])]

        error_h1 = error_list_h1[i-1]
        error_h2 = error_list_h2[i-1]

        ax[0].plot(x_list_h1, y_list_for_foo, color='black')
        ax[0].plot(x_list_h1, numeric_solution_h1, color='red')
        ax[0].plot(x_list_h1, numeric_solution_h2[::10], color='blue')

        # ax[0].annotate(f't = {t}', ha='center', xy=(5, 1.4))
        ax[0].set_ylim(0, 1.2)
        ax[0].legend([f'Precise, t = {round(t, 2)}', f'h1 = {h1}', f'h2 = {h2}'])

        ax[1].plot(t_list_h1[1:i], error_list_h1[1:i], color='red')
        ax[1].plot(t_list_h1[1:i], error_list_h2[1:i], color='blue')

        # ax[1].set_ylim(0, max(error_h1, error_h2))
        ax[1].annotate(f'eps1/eps2 = {error_h1/error_h2}', ha='center', xy=(0.5, 10))
        ax[1].legend([f'h1 = {h1}, eps1/eps2 = {round(error_h1/error_h2, 2)}', f'h2 = {h2}'])

        camera.snap()

    return camera


foo_list = [sine_function, parabola_function, bell_function, pulse_function]
# foo_list = [sine_function]

# for foo in foo_list:
#     camera = plot_over_time(foo, numeric_angle_scheme, h1=0.1, h2=0.01)
#     animation = camera.animate()
#     animation.save(f'inprecise/angle_scheme_{foo.__name__}.mp4', fps=72/8, dpi=100)

for foo in foo_list:
    camera = plot_over_time(foo, numeric_angle_scheme, h1=0.01, h2=0.001)
    animation = camera.animate()
    animation.save(f'precise/angle_scheme_{foo.__name__}.mp4', fps=720/8, dpi=100)

# for foo in foo_list:
#     camera = plot_over_time(foo, numeric_lax_scheme)
#     animation = camera.animate(interval=50, blit=True)
#     animation.save('animation_lax_scheme ' + foo.__name__ + '.gif', writer='pillow')
