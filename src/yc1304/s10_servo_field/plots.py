'''
    Functions like plot_* take pylab as first instance
'''
from boot_navigation.navigation_map import plot_arrow_se2
from contracts import contract
from geometry.poses import se2_from_linear_angular, SE2_from_SE3
from reprep.plot_utils import x_axis_extra_space, y_axis_set
import numpy as np
import warnings

def plot_style_sensels(pylab):
    y_axis_set(pylab, -0.1, 1.1)
    x_axis_extra_space(pylab)

def plot_style_sensels_deriv(pylab):
    y_axis_set(pylab, -0.1, 0.1)
    x_axis_extra_space(pylab)

@contract(ps='array[Nx2]', ss='array[N]')
def plot_scalar_field_sign(pylab, ps, ss):
    """
        ps : list of 2D points
       s: associated scalar field
    """
    
    style = {}
    for p, s in zip(ps, ss):
        if s > 0:
            style['markerfacecolor'] = 'red'
        else:
            style['markerfacecolor'] = 'blue'
        
        pylab.plot(p[0], p[1], 'o', markersize=5, **style)

def plot_reference_points(pylab, processed):
    centroid = processed['centroid']
    sparse_xy = processed['sparse_xy']
    pylab.plot(sparse_xy[:, 0], sparse_xy[:, 1], 'o', zorder=(-1200),  # markeredgecolor='none',
               markerfacecolor=[0.3, 0.3, 0.3], markersize=0.5)
    pylab.plot(centroid[0], centroid[1], 'o', zorder=(-1000))


def plot_reference_points_poses(pylab, processed):
    arrow_length = 0.05
    style = dict(head_width=0.01, head_length=0.01,
                 edgecolor='green')
    
    for bd in processed['sparse']:
        extra = bd['extra'].item()
        p = extra['odom_xy']
        th = extra['odom_th']
        a = np.cos(th) * arrow_length        
        b = np.sin(th) * arrow_length
        pylab.arrow(p[0], p[1], a, b, **style)


def plot_odom_commands(pylab, bds):
    poses = [bd['extra'].item()['odom'] for bd in bds]    
    commands = [bd['commands'] for bd in  bds]
    plot_poses_commands(pylab, poses, commands)


def plot_poses_commands(pylab, poses, commands, normalize,
                        cmd_arrow_length=0.05):

    # scale to given arrow_length
    us = np.array(commands)[:, :2]
    u_max = np.max(np.hypot(us[:, 0], us[:, 1]))
    us = us / u_max * cmd_arrow_length
    
    cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')
    
    for pose, u in zip(poses, us):        
        warnings.warn('should use robot to make conversion')
        x, y = u
        omega = 0
        vel = se2_from_linear_angular([x, y], omega)
        plot_arrow_se2(pylab, SE2_from_SE3(pose), vel, normalize=normalize, **cmd_style)
