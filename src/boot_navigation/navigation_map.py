from bootstrapping_olympics import BootSpec
from contracts import contract
from geometry import (translation_angle_from_SE2, se2_from_linear_angular,
    linear_angular_from_se2, DifferentiableManifold, PointSet, R2)
import numpy as np


__all__ = ['NavigationMap']


class NavigationMap(object):
    
    @contract(boot_spec=BootSpec, manifold=DifferentiableManifold)
    def __init__(self, boot_spec, manifold):
        self.boot_spec = boot_spec
        self.manifold = manifold
        
        self.data = []
        
    def get_all_points(self):
        """ yields bd, pose """
        return list(self.data)
    
    @contract(robot_pose='None|array', bd='array')
    def add_point(self, bd, robot_pose=None):
        if robot_pose is not None:
            self.manifold.belongs(robot_pose)
    
        d = (bd, robot_pose)
        self.data.append(d)
        
    def npoints(self):
        return len(self.data)
    
    def display(self, report):
        f = report.figure()
        with f.plot('map') as pylab:
            for bd, pose in self.data:
                commands = bd['commands']
                if len(commands) == 3:
                    x, y, omega = commands
                else:
                    x, y = commands
                    omega = 0
                vel = se2_from_linear_angular([x, y], omega)
                plot_arrow_SE2(pylab, pose)
                plot_arrow_se2(pylab, pose, vel, color='g')
            pylab.axis('equal')
    
    def plot_points(self, pylab):
        xy = np.array(self.get_R2_points())
        pylab.plot(xy[:, 0], xy[:, 1], 'k.')

#     @contract(commands='list(array)')
#     def plot_commands(self, pylab, commands, normalize=True):
#         for i in range(len(self.data)):
#             self.plot_commands_at_index(pylab, i, commands[i], normalize=normalize)

    @contract(ss='seq(number)')
    def plot_scalar_field_sign(self, pylab, ss):        
        style = {}
        for p, s in zip(self.get_R2_points(), ss):
            if s > 0:
                style['markerfacecolor'] = 'red'
            else:
                style['markerfacecolor'] = 'blue'
            
            pylab.plot(p[0], p[1], 'o', markersize=5, **style)

    @contract(vels='list(se2)')
    def plot_vels(self, pylab, vels, normalize=True):
        for pose, vel in zip(self.get_poses(), vels):
            cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')
            plot_arrow_se2(pylab, pose, vel, normalize=normalize, **cmd_style)
    
    @contract(vel='se2', i='Int')
    def plot_vel_at_index(self, pylab, i, vel):
        pose = self.get_pose_at_index(i)
        cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')
        plot_arrow_se2(pylab, pose, vel, normalize=True, **cmd_style)
#     def plot_commands_at_index(self, pylab, j, commands, normalize=True):
#         pose = self.get_pose_at_index(j)
#         cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')
#         plot_arrow_se2(pylab, pose, vel, normalize=normalize, **cmd_style)

    def get_poses(self):
        return list(map(self.get_pose_at_index, range(len(self.data))))
    
    def get_pose_at_index(self, j):
        return self.data[j][1]
                
    def get_closest_point(self, y, distance):
        return self._get_closest_point(y, self.data, distance)
    
    def move_origin(self, origin):
        """ Creates a new map where the origin is pose. """
        nmap = NavigationMap(self.boot_spec, self.manifold)
        for bd, pose in self.data:
            pose2 = self.manifold.multiply(self.manifold.inverse(origin), pose)
            nmap.add_point(bd, pose2)
        return nmap
            
    def get_closest_point_around(self, y, i, r, distance):
        a = max(i - r, 0)
        b = min(i + r, len(self.data) - 1)    
        data = self.data[a:b]
        return self._get_closest_point(y, data, distance)
    
    def _get_closest_point(self, y, data, distance):
        def distance_to_y(point):
            bd, _ = point
            y0 = bd['observations']
            # return np.linalg.norm(y - y0)
            return distance(y0, y)
        distances = map(distance_to_y, data)
        closest = np.argmin(distances)
        # print('closest: %d' % closest)
        return closest
        
    def get_observations_at(self, index):
        if index >= len(self.data):
            raise ValueError('index out of bounds: %s' % index)
        bd, _ = self.data[index]
        return self._censor(bd['observations'])
    
    def get_all_observations(self):
        return map(self.get_observations_at, range(len(self.data)))
    
    def _censor(self, y0):
        y = y0.copy() 
        for i in range(1, y.size):
            delta = y[i] - y[i - 1]
            if np.abs(delta) > 0.04:
                y[i] = y0[i - 1]
        return y
    
    def _project_pose(self, manifold):
        for _, pose in self.data:
            yield self.manifold.project_to(manifold, pose)
        
    def get_R2_points(self):
        return list(self._project_pose(R2))
                
    def get_R2_centroid_index(self):
        points = list(self.get_R2_points()) 
        pointset = PointSet(R2, points=points)
        return pointset.centroid_index()


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
def plot_arrow_se2(pylab, pose, vel, normalize=True, length=0.05, **style):
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
    
    
