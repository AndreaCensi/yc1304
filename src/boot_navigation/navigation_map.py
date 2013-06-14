from bootstrapping_olympics import BootSpec
from contracts import contract
from geometry import DifferentiableManifold, PointSet, R2
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
        from .reports import display_nmap
        display_nmap(report, self)
    
    def plot_points(self, pylab):
        xy = np.array(self.get_R2_points())
        pylab.plot(xy[:, 0], xy[:, 1], 'k.')


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
    def plot_vels(self, pylab, vels, normalize=True, colors=None, length=0.05):
        from .plots import plot_arrow_se2
        for i, (pose, vel) in enumerate(zip(self.get_poses(), vels)):
            head_width = length / 3
            head_length = length / 5
#             cmd_style = dict(head_width=head_width, head_length=head_length)
            cmd_style = {}
            if colors is not None:
                cmd_style['facecolor'] = colors[i]
                cmd_style['edgecolor'] = colors[i]
                
            plot_arrow_se2(pylab, pose, vel, length=length, normalize=normalize, **cmd_style)
    
    @contract(vel='se2', i='Int')
    def plot_vel_at_index(self, pylab, i, vel, length):
        from .plots import plot_arrow_se2
        pose = self.get_pose_at_index(i)
        head_width = length / 3
        head_length = length / 5
        cmd_style = dict(head_width=head_width, head_length=head_length, fc='blue')
        plot_arrow_se2(pylab, pose, vel, length=length, normalize=True, **cmd_style)

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
    
    @contract(returns='list(array)')
    def get_all_observations(self):
        """ Returns a list of arrays """
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

    def get_R2_point_at_index(self, i):
        return self.manifold.project_to(R2, self.get_pose_at_index(i))

    def get_average_interpoint_R2_distance(self):
        """ """
        points = self.get_R2_points()
        dists = []
        for i in range(len(points) - 1):
            d = R2.distance(points[i], points[i + 1])
            dists.append(d)
        return np.median(dists)
