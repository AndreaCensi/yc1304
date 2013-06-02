from bootstrapping_olympics.interfaces.boot_spec import BootSpec
from contracts import contract
from geometry import (translation_angle_from_SE2, se2_from_linear_angular,
    linear_angular_from_se2, DifferentiableManifold)
import numpy as np


__all__ = ['NavigationMap']


class NavigationMap(object):
    
    @contract(boot_spec=BootSpec, manifold=DifferentiableManifold)
    def __init__(self, boot_spec, manifold):
        self.boot_spec = boot_spec
        self.manifold = manifold
        
        self.data = []
        
    @contract(robot_pose='None|SE3', bd='array')
    def add_point(self, bd, robot_pose=None):
        if robot_pose is not None:
            self.manifold.belongs(robot_pose)
    
        d = (bd, robot_pose)
        self.data.append(d)
        
    def display(self, report):
        f = report.figure()
        with f.plot('map') as pylab:
            for bd, pose in self.data:
                commands = bd['commands']
                x, y, omega = commands
                vel = se2_from_linear_angular([x, y], omega)
                plot_arrow_SE2(pylab, pose)
                plot_arrow_se2(pylab, pose, vel, color='g')
            pylab.axis('equal')
                
    def get_closest_point(self, y):
        return self._get_closest_point(y, self.data)
    
    def get_closest_point_around(self, y, i, r):
        a = max(i - r, 0)
        b = min(i + r, len(self.data) - 1)    
        data = self.data[a:b]
        return self._get_closest_point(y, data)
    
    def _get_closest_point(self, y, data):
        def distance_to_y(point):
            bd, _ = point
            y0 = bd['observations']
#             return np.abs(y - y0).sum()
            return np.linalg.norm(y - y0)
        distances = map(distance_to_y, data)
        closest = np.argmin(distances)
        # print('closest: %d' % closest)
        return closest
        
    def get_observations_at(self, index):
        bd, _ = self.data[index]
        return bd['observations']
        

@contract(pose='SE2')
def plot_arrow_SE2(pylab, pose, length=0.1, **style):
    (x, y), theta = translation_angle_from_SE2(pose)
    pylab.plot(x, y, 'rx')
    a = np.cos(theta) * length        
    b = np.sin(theta) * length
    pylab.arrow(x, y, a, b, **style)

@contract(pose='SE2', vel='se2')
def plot_arrow_se2(pylab, pose, vel, normalize=True, length=0.05, **style):
    (x, y), _ = translation_angle_from_SE2(pose)
    vel2 = np.dot(pose, vel)
    (vx, vy), _ = linear_angular_from_se2(vel2)
    if normalize:
        vn = np.hypot(vx, vy)
        if vn > 0:
            vx = vx / vn * length
            vy = vy / vn * length 
    pylab.arrow(x, y, vx, vy, **style)

    
    
