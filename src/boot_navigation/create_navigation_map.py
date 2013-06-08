from .navigation_map import NavigationMap
from contracts import contract
from geometry import PointSet, R2, SE2, SE3, SE2_from_SE3
import itertools
import numpy as np
 

__all__ = ['create_navigation_map_from_episode']


def create_navigation_map_from_episode(data_central, id_robot, id_episode,
                                       max_time, max_num, min_dist, min_th_dist,
                                       min_spacing):
    log_index = data_central.get_log_index()
    log_index.reindex()
    
    boot_spec = log_index.get_robot_spec(id_robot)
    nmap = NavigationMap(boot_spec, SE2)
    
    bds = log_index.read_robot_episode(id_robot, id_episode, read_extra=True)
    bds = limit_time(bds, max_time=max_time)
    obs_pose = read_pose_data(bds)
    obs_pose = regularly_spaced(obs_pose, min_spacing)
    obs_pose = pose_starts_at_I(SE3, obs_pose)
    obs_pose = sparse_sequence(obs_pose, min_th_dist=min_th_dist, min_dist=min_dist)
    obs_pose = itertools.islice(obs_pose, max_num)
     
    for bd, robot_pose in obs_pose:
        nmap.add_point(bd, SE2_from_SE3(robot_pose))
        
    return nmap


def limit_time(bds, max_time):
    t0 = None
    for b in bds:
        t = b['timestamp']
        if t0 is None:
            t0 = t
            continue
        delta = t - t0
        if delta >= max_time:
            break
        yield b


def pose_starts_at_I(group, obs_pose):
    pose0 = None
    for obs, pose in obs_pose:
        if pose0 is None:
            pose0 = pose
        pose2 = group.multiply(group.inverse(pose0), pose)
        yield obs, pose2
            
            
def read_pose_data(bds):
    for bd in bds:
        extra = bd['extra'].item()
        if not 'robot_pose' in extra:
            msg = 'Could not find pose "odom" in extra.'
            raise Exception(msg)
        pose = np.array(extra['robot_pose'])
        SE3.belongs(pose)
        yield bd, pose
        

class Sparsifier():
    def __init__(self, manifold, min_dist):
        self.min_dist = min_dist
        self.point_set = PointSet(manifold)
        
    def accept(self, p):
        """ Returns True or False """
        if self.point_set.__len__() == 0:
            self.point_set.add(p)
            return True
        
        accept = not self.point_set.is_closer_than(p, self.min_dist)
        if accept:
            self.point_set.add(p)
            return True
        else:
            return False


def regularly_spaced(data, min_dist):
    sp = Sparsifier(manifold=R2, min_dist=min_dist)
    for data, pose in data:
        p = SE3.project_to(R2, pose)        
        if sp.accept(p):
            yield data, pose

        
@contract(min_th_dist='float,>0', min_dist='float,>0')
def sparse_sequence(data, min_th_dist, min_dist):
    """ Yields a sequence """
    # sp = Sparsifier(manifold=R2, min_dist=min_dist)
    last_pose = None
    for data, pose in data:  
        if last_pose is None:
            ok = True
        else:
            distances = SE3.distances(pose, last_pose)
            # print distances
            ok = (distances[0] > min_dist) or (distances[1] > min_th_dist)
        if ok:
            last_pose = pose
            yield data, pose

