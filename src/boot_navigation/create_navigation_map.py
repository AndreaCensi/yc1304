from .navigation_map import NavigationMap
from contracts import contract
from geometry import SE2, SE3, SE2_from_SE3
import itertools
import numpy as np
 

__all__ = ['create_navigation_map_from_episode']


def create_navigation_map_from_episode(data_central, id_robot, id_episode,
                                       max_time, max_num, min_dist, min_th_dist):
    log_index = data_central.get_log_index()
    log_index.reindex()
    
    boot_spec = log_index.get_robot_spec(id_robot)
    nmap = NavigationMap(boot_spec, SE2)
    
    bds = log_index.read_robot_episode(id_robot, id_episode, read_extra=True)
    bds = limit_time(bds, max_time=max_time)
    obs_pose = read_pose_data(bds)
    obs_pose = pose_starts_at_I(SE3, obs_pose)
    obs_pose = sparse_sequence(obs_pose, min_th_dist=min_th_dist, min_dist=min_dist)
    obs_pose = itertools.islice(obs_pose, max_num) 
    for bd, robot_pose in obs_pose:
        # print SE2.friendly(robot_pose)
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
#         robot_pose = SE2_from_SE3(pose)
        yield bd, pose
        

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

