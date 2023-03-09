import matplotlib.pyplot as plt
import numpy as np
import math

from celluloid import Camera
from constants import a, l, lt
from schemes import lax_scheme


def plot_over_time(foo, scheme, h1=0.01, h2=0.001, courant=0.7):
    tau_h1 = courant*h1/a
    tau_h2 = courant*h2/a

    t_list_h1 = np.arange(0, lt, tau_h1)

    last_t_index_h1 = math.ceil(lt/tau_h1)-1
    last_t_index_h2 = math.ceil(lt/tau_h2)-1

    last_x_index_base_h1 = math.ceil(l/h1)-1
    last_x_index_base_h2 = math.ceil(l/h2)-1

    print('last index, x_list, h1:', last_x_index_base_h1)
    print('last index, x_list, h2:', last_x_index_base_h2)

    x_list_h1 = []
    x_list_h2 = []

    if (scheme == lax_scheme):
      x_list_h1 = np.arange(0, l + h1*last_t_index_h1, h1)
      x_list_h2 = np.arange(0, l + h2*last_t_index_h2, h2)
    else:
      x_list_h1 = np.arange(0, l, h1)
      x_list_h2 = np.arange(0, l, h2)

    fig, ax = plt.subplots(2, figsize=(16, 9))
    camera = Camera(fig)

    ax[0].set_title(f'{scheme.__name__}, {foo.__name__}, a = {a}, Courant = {courant}')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')

    ax[1].set_title('Error from time')
    ax[1].set_xlabel('t')
    ax[1].set_ylabel('max_error')

    plt.subplots_adjust(hspace=0.4)

    t0_h1 = [foo(x, 0) for x in x_list_h1]
    t0_h2 = [foo(x, 0) for x in x_list_h2]

    numeric_solution_h1 = []
    numeric_solution_h2 = []

    error_list_h1 = []
    error_list_h2 = []

    for i in range(1, len(t_list_h1)):
        t = t_list_h1[i]

        if i == 1:
            numeric_solution_h1 = scheme(foo, h1, courant, i, t0_h1, i-1)
            numeric_solution_h2 = scheme(foo, h2, courant, i*10, t0_h2, (i-1)*10)
        else:
            numeric_solution_h1 = scheme(foo, h1, courant, i, list(numeric_solution_h1), i-1)
            numeric_solution_h2 = scheme(foo, h2, courant, i*10, list(numeric_solution_h2), (i-1)*10)

        y_list_for_foo = [foo(x, t) for x in x_list_h1]

        error_list_h1 += [max([np.abs(x-y) for x,y in zip(y_list_for_foo, numeric_solution_h1)])]
        error_list_h2 += [max([np.abs(x-y) for x,y in zip(y_list_for_foo, numeric_solution_h2[::10])])]

        error_h1 = error_list_h1[i-1]
        error_h2 = error_list_h2[i-1]

        # print('theory:', len(x_list_h1[:last_x_index_base_h1+1]))
        # print('h1:', len(numeric_solution_h1[:last_x_index_base_h1+1]))
        # print('h2:', len(numeric_solution_h2[:last_x_index_base_h2+1:10]))

        ax[0].plot(x_list_h1[:last_x_index_base_h1+1], y_list_for_foo[:last_x_index_base_h1+1], color='black')
        ax[0].plot(x_list_h1[:last_x_index_base_h1+1], numeric_solution_h1[:last_x_index_base_h1+1], color='red')
        ax[0].plot(x_list_h1[:last_x_index_base_h1+1], numeric_solution_h2[:last_x_index_base_h2+1:10], color='blue')

        # ax[0].annotate(f't = {t}', ha='center', xy=(5, 1.4))
        ax[0].set_ylim(0, 1.2)
        ax[0].legend([f'Precise, t = {round(t, 2)}', f'h1 = {h1}', f'h2 = {h2}'])

        ax[1].plot(t_list_h1[1:i], error_list_h1[1:i], color='red')
        ax[1].plot(t_list_h1[1:i], error_list_h2[1:i], color='blue')

        # ax[1].set_ylim(0, max(error_h1, error_h2))
        ax[1].annotate(f'eps1/eps2 = {error_h1/error_h2}', ha='center', xy=(0.5, 10))
        ax[1].legend([f'h1 = {h1}, eps1/eps2 = {round(error_h1/error_h2, 2)}', f'h2 = {h2}'])

        camera.snap()

    plt.close()
    return camera
