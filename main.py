from src import functions
from src.schemes import angle_scheme, lax_scheme
from src.plot import plot_over_time


foo_list = [functions.sine, functions.parabola, functions.bell, functions.pulse]

for foo in foo_list:
    # camera = plot_over_time(foo, angle_scheme, h1=0.1, h2=0.01)
    # animation = camera.animate()
    # animation.save(f'inprecise/angle/angle_{foo.__name__}.mp4', fps=72/8, dpi=100)

    camera = plot_over_time(foo, lax_scheme, h1=0.1, h2=0.01)
    animation = camera.animate()
    animation.save(f'inprecise/lax/lax_{foo.__name__}.mp4', fps=72/8, dpi=100)

# for foo in foo_list:
#     camera = plot_over_time(foo, numeric_angle_scheme, h1=0.01, h2=0.001)
#     animation = camera.animate()
#     animation.save(f'precise/angle/angle_{foo.__name__}.mp4', fps=720/8, dpi=100)

# for foo in foo_list:
# camera = plot_over_time(foo, numeric_lax_scheme, h1=0.01, h2=0.001)
# animation = camera.animate()
# animation.save(f'precise/lax/lax_{foo.__name__}.mp4', fps=720/8, dpi=100)
