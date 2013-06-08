'''
    Functions like plot_* take pylab as first instance
'''
from boot_navigation.navigation_map import plot_arrow_se2
from contracts import contract
from geometry.poses import SE2_from_SE3
from reprep.plot_utils import x_axis_extra_space, y_axis_set
from yc1304 import logger
import numpy as np


def plot_style_sensels(pylab):
    y_axis_set(pylab, -0.1, 1.1)
    x_axis_extra_space(pylab)

def plot_style_sensels_deriv(pylab):
    y_axis_set(pylab, -0.1, 0.1)
    x_axis_extra_space(pylab)

# 
# def plot_reference_points(pylab, processed):
#     centroid = processed['centroid']
#     xy = processed['nmap'].get_R2_points()
#     xy = np.array(xy)
#     pylab.plot(xy[:, 0], xy[:, 1], 'o', zorder=(-1200),  # markeredgecolor='none',
#                markerfacecolor=[0.3, 0.3, 0.3], markersize=0.5)
#     pylab.plot(centroid[0], centroid[1], 'o', zorder=(-1000))

# 
# def plot_odom_commands(pylab, bds):
#     poses = [bd['extra'].item()['odom'] for bd in bds]    
#     commands = [bd['commands'] for bd in  bds]
#     plot_poses_commands(pylab, poses, commands)

# 
# @contract(poses='list(SE3)')
# def plot_poses_commands(pylab, poses, commands, normalize=True,
#                         cmd_arrow_length=0.05):
# 
#     # scale to given arrow_length
#     us = np.array(commands)[:, :2]
#     u_max = np.max(np.hypot(us[:, 0], us[:, 1]))
#     if u_max > 0:
#         us = us / u_max * cmd_arrow_length
#     else:
#         logger.error('Commands are invalid: %s' % us)
#     
#     cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')
#     
#     for pose, u in zip(poses, us):        
#         vel = se2_from_commands(u)
#         plot_arrow_se2(pylab, SE2_from_SE3(pose), vel, normalize=normalize, **cmd_style)
