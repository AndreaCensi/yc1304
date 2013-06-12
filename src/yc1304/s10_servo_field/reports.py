from boot_navigation import plot_arrow_se2_yt, plot_arrow_se2_xt
from contracts import contract
from geometry import (linear_angular_from_se2, angle_from_SE2,
    se2_project_from_se3, translation_angle_from_SE2, angular_from_se2, SE2)
from reprep import Report
from reprep.plot_utils import x_axis_balanced, y_axis_balanced
import numpy as np
from geometry.poses import translation_from_SE2
from reprep.plot_utils.axes import turn_all_axes_off

 
 
def report_raw_display(processed):
    r = Report('raw_display')
    f = r.figure()

    centroid = processed['centroid']
    nmap = processed['nmap']
    xy = processed['nmap'].get_R2_points() 

    caption = "Raw trajectory and selected points"
    with f.plot('sparse_xy', caption=caption) as pylab:
        xy = np.array(xy)
        pylab.plot(xy[:, 0], xy[:, 1], 'k+')
        pylab.plot(centroid[0], centroid[1], 'go')
        nmap.plot_points(pylab)
        pylab.axis('equal')

    with r.subsection('nmap') as n:
        processed['nmap'].display(n) 

    return r


def report_distances(processed):
    r = Report('distances')
    p_dist = processed['p_distance']
    y_dist = processed['y_distance']
    
    f = r.figure('distance_stats') 

    with f.plot('y_vs_p') as pylab:
        pylab.plot(y_dist, p_dist, 's')
        pylab.xlabel('d(y_0, y_1)')
        pylab.ylabel('d(p_0, p_1)')

    with f.plot('p_vs_y') as pylab:
        pylab.plot(p_dist, y_dist, 's')
        pylab.ylabel('d(y_0, y_1)')
        pylab.xlabel('d(p_0, p_1)')

    return r 


def plot_style_servo_field_xy(pylab):
    centroid = [0, 0]
    pylab.plot(centroid[0], centroid[1], 'go')
    
    M = 2.0
    b = 0.1
    pylab.plot([-M + b, -M + b], [-M + b, -M + 1 + b], 'k-')
    
    pylab.axis('equal')
    pylab.axis((-M, +M, -M, +M))
    
    turn_all_axes_off(pylab)


@contract(vels='list(se2)')
def repsec_servo1_generic_vel_field(r, fname, centroid, nmap, vels, normalize=True):
    f = r.figure(cols=2)
    
    omegas = map(angular_from_se2, vels)

    has_theta = np.any(omegas != 0)

    figsize = (6, 6)

    caption = 'First two components of "%s".' % fname
    
    with f.plot('xy_arrows', caption=caption, figsize=figsize) as pylab:
        nmap.plot_points(pylab)
        nmap.plot_vels(pylab, vels, normalize)
        plot_style_servo_field_xy(pylab)

    @contract(pose='SE2', returns='>=0')
    def distance_to_centroid(pose):
        t = translation_from_SE2(pose)
        d = np.linalg.norm(t - centroid)
        return d
        
    poses = nmap.get_poses()
    derivs = vector_field_derivs(SE2, poses, vels, distance_to_centroid)
    
    def deriv2color(s):
        if s == 0:
            return 'k'
        if s > 0:
            return 'r'
        if s < 0:
            return 'g'
        
    colors = map(deriv2color, derivs)


    with f.plot('xy_arrows_colors', caption=caption, figsize=figsize) as pylab:
        nmap.plot_vels(pylab, vels, normalize, colors=colors)        
        plot_style_servo_field_xy(pylab)

    if has_theta:
        caption = 'Third component of "%s".' % fname
        with f.plot('xy_u_th_sign', caption=caption) as pylab:
            nmap.plot_scalar_field_sign(pylab, omegas)
            plot_style_servo_field_xy(pylab)

    f = r.figure()

    if has_theta:
        poses = nmap.get_poses()
        with f.plot('tw', caption=caption) as pylab:
            plot_poses_vels_yt(pylab, poses, vels, normalize=True)
            pylab.xlabel('y (m)')
            pylab.ylabel('theta (deg)')
            y_axis_balanced(pylab)
            x_axis_balanced(pylab)

        with f.plot('xt', caption=caption) as pylab:
            plot_poses_vels_xt(pylab, poses, vels, normalize=True)
            pylab.xlabel('x (m)')
            pylab.ylabel('theta (deg)')
            y_axis_balanced(pylab)
            x_axis_balanced(pylab)

        with f.plot('yt', caption=caption) as pylab:
            plot_poses_vels_theta_omega(pylab, poses, vels)
            pylab.xlabel('theta (deg)')
            pylab.ylabel('omega')
            y_axis_balanced(pylab)
            x_axis_balanced(pylab)

def vector_field_deriv(manifold, tpoint, f, epsilon=0.0001):
    """ Computes the derivative of a function f at the tangent
        space tpoint. """
    manifold.belongs_ts(tpoint)
    p1, v0 = tpoint
    # todo: normalize
    v = epsilon * v0
    p2 = manifold.expmap((p1, v))
    f1 = f(p1)
    f2 = f(p2)
    delta = f2 - f1
    return delta / epsilon
    
    
def vector_field_derivs(manifold, poses, vels, f):
    return [vector_field_deriv(manifold, (pose, manifold.multiply(pose, vel)), f)
             for pose, vel in zip(poses, vels)]
    


@contract(poses='list(SE2)', vels='list(se2)')
def plot_poses_vels_theta_omega(pylab, poses, vels):
    thetas = np.array([angle_from_SE2(p) for p in poses])
    omegas = np.array([linear_angular_from_se2(vel)[1] for vel in vels])
    positive = omegas > 0
    negative = np.logical_not(positive)
    pylab.plot(np.rad2deg(thetas)[positive], omegas[positive], 'r.')
    pylab.plot(np.rad2deg(thetas)[negative], omegas[negative], 'b.')
    
    
@contract(poses='list(SE2)', vels='list(se2)', normalize='bool')
def plot_poses_vels_xt(pylab, poses, vels, normalize=True):
    cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')    
    for pose, vel in zip(poses, vels):  
        (x, _), theta = translation_angle_from_SE2(pose)
        omega = angular_from_se2(vel)
        style = 'r.' if omega > 0 else 'b.'
        pylab.plot(x, np.rad2deg(theta), style)
        plot_arrow_se2_xt(pylab, pose, vel, normalize=normalize, **cmd_style)


@contract(poses='list(SE2)', vels='list(se2)', normalize='bool')
def plot_poses_vels_yt(pylab, poses, vels, normalize=True):
    cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')    
        
    for pose, vel in zip(poses, vels): 
        (_, y), theta = translation_angle_from_SE2(pose)
        omega = angular_from_se2(vel)
        style = 'r.' if omega > 0 else 'b.'
        pylab.plot(y, np.rad2deg(theta), style)
        plot_arrow_se2_yt(pylab, pose, vel, normalize=normalize, **cmd_style)


def report_servo1(processed):
    r = Report('servo1')
    
    nmap = processed['nmap']
    servo = processed['servo']
    centroid = processed['centroid']
    robot = processed['robot']
    
    with r.subsection('u', robust=False) as s:
        commands = [x['u'] for x in servo]
        vels = map(robot.debug_get_vel_from_commands, commands)
        vels = map(se2_project_from_se3, vels)
        repsec_servo1_generic_vel_field(s, 'u', centroid, nmap, vels,
                                        normalize=True)
        
    if 'u_raw' in servo[0]:
        with r.subsection('u_raw', robust=True) as s:
            commands = [x['u_raw'] for x in servo]
            vels = map(robot.debug_get_vel_from_commands, commands)
            vels = map(se2_project_from_se3, vels)
            repsec_servo1_generic_vel_field(s, 'u_raw', centroid, nmap, vels,
                                            normalize=True)

    if 'descent' in servo[0]:
        with r.subsection('descent', robust=True) as s:
            commands = [x['descent'] for x in servo]
            vels = map(robot.debug_get_vel_from_commands, commands)
            vels = map(se2_project_from_se3, vels)
            repsec_servo1_generic_vel_field(s, 'descent', centroid, nmap, vels,
                                            normalize=False)
         
    return r


def report_servo_details(servo_agent, processed, nsamples=6):
    r = Report('servo_details')

    nmap = processed['nmap']
    y_goal = processed['y_goal']
    robot = processed['robot']

    for i in range(nsamples):
        j = np.random.randint(len(nmap.data))
        y0 = nmap.get_observations_at(j)
        servo = processed['servo'][j]
        with r.subsection('sample%s' % i) as r_i:
            f = r.figure(cols=4)
              
            with f.plot('map') as pylab:
                nmap.plot_points(pylab)
                vel = robot.debug_get_vel_from_commands(servo['u'])
                nmap.plot_vel_at_index(pylab, j, se2_project_from_se3(vel))

            with r_i.subsection('query') as rq:
                servo_agent.display_query(rq, observations=y0, goal=y_goal)
    
    return r
