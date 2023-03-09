def get_grid(x_list, t_list):
    grid = [] # grid[i][j] - usage, where grid[i] is a row

    for t in t_list:
        grid += [[(x, t) for x in x_list]]
    return grid