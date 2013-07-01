from contracts import contract
from geometry import linear_angular_from_se2, translation_angle_from_SE2
import numpy as np


@contract(pose='SE2')
def plot_arrow_SE2(pylab, pose, length=0.1, **style):
    (x, y), theta = translation_angle_from_SE2(pose)
    pylab.plot(x, y, 'rx')
    a = np.cos(theta) * length        
    b = np.sin(theta) * length
    pylab.arrow(x, y, a, b, **style)


@contract(pose='SE2', vel='se2')  # returns='tuple(x,y,$theta,vx,vy,omega)')
def get_vxy_world(pose, vel):
    (x, y), theta = translation_angle_from_SE2(pose)
    _, omega = linear_angular_from_se2(vel)
    vel2 = np.dot(pose, vel)
    vx = vel2[0, 2]
    vy = vel2[1, 2]
    return x, y, theta, vx, vy, omega

    
@contract(pose='SE2', vel='se2')
def plot_arrow_se2(pylab, pose, vel, length, normalize=True, **style):
    """ plots x, y plane """
    x, y, theta, vx, vy, omega = get_vxy_world(pose, vel)  # @UnusedVariable
    
    A, B = x, y
    a, b, = vx, vy
    _plot_arrow(pylab, A, B, a, b, normalize, length, **style)


@contract(pose='SE2', vel='se2')
def plot_arrow_se2_xt(pylab, pose, vel, normalize=True, length=0.05, **style):
    """ plots x, theta """
    x, y, theta, vx, vy, omega = get_vxy_world(pose, vel)  # @UnusedVariable
    theta = np.rad2deg(theta)
    omega = np.rad2deg(omega)
    
    A, B = x, theta
    a, b = vx, omega
    _plot_arrow(pylab, A, B, a, b, normalize, length, **style)


@contract(pose='SE2', vel='se2')
def plot_arrow_se2_yt(pylab, pose, vel, normalize=True, length=0.05, **style):
    """ plots y, theta """

    x, y, theta, vx, vy, omega = get_vxy_world(pose, vel)  # @UnusedVariable
    theta = np.rad2deg(theta)
    omega = np.rad2deg(omega)
    A, B = y, theta
    a, b = vy, omega
    
    pylab.plot(A, B, 'x')
    
    _plot_arrow(pylab, A, B, a, b, normalize, length, **style)
    
    
def _plot_arrow(pylab, x, y, a, b, normalize, length, **style):
    assert np.isfinite(a)
    assert np.isfinite(b)
    assert np.isfinite(x)
    assert np.isfinite(y)
    if normalize:
        vn = np.hypot(a, b)
        if vn > 0:
            a = a / vn * length
            b = b / vn * length 
    pylab.arrow(x, y, a, b, **style)
    
    
