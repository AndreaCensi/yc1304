'''
    Functions like plot_* take pylab as first instance
'''
from reprep.plot_utils import x_axis_extra_space, y_axis_set


def plot_style_sensels(pylab):
    y_axis_set(pylab, -0.1, 1.1)
    x_axis_extra_space(pylab)

def plot_style_sensels_deriv(pylab):
    y_axis_set(pylab, -0.1, 0.1)
    x_axis_extra_space(pylab)
