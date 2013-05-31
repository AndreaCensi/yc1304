from .navigation_map import NavigationMap
from contracts import contract
from geometry import DifferentiableManifold, SE2, SE3, SE2_from_SE3
from yc1304.s10_servo_field.show_field import Sparsifier
import itertools
import numpy as np


__all__ = ['create_navigation_map_from_episode']


def create_navigation_map_from_episode(data_central, id_robot, id_episode,
                                       max_time=10000.0, max_num=20, min_dist=0.1):
    log_index = data_central.get_log_index()
    log_index.reindex()
    
    boot_spec = log_index.get_robot_spec(id_robot)
    nmap = NavigationMap(boot_spec, SE2)
    
    bds = log_index.read_robot_episode(id_robot, id_episode, read_extra=True)
    bds = limit_time(bds, max_time=max_time)
    obs_pose = read_pose_data(bds)
    obs_pose = pose_starts_at_I(obs_pose)
    obs_pose = sparse_sequence(obs_pose, SE2, min_dist=min_dist)
    obs_pose = itertools.islice(obs_pose, max_num) 
    for bd, robot_pose in obs_pose:
        # print SE2.friendly(robot_pose)
        nmap.add_point(bd, robot_pose)
        
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

def pose_starts_at_I(obs_pose):
    pose0 = None
    for obs, pose in obs_pose:
        if pose0 is None:
            pose0 = pose
        pose2 = SE2.multiply(SE2.inverse(pose0), pose)
        yield obs, pose2
            
def read_pose_data(bds):
    for bd in bds:
        extra = bd['extra'].item()
        if not 'robot_pose' in extra:
            msg = 'Could not find pose "odom" in extra.'
            raise Exception(msg)
        pose = np.array(extra['robot_pose'])
        SE3.belongs(pose)
        robot_pose = SE2_from_SE3(pose)
#         observations = bd['observations']
        yield bd, robot_pose
        

#         extra['odom'] = np.array(extra['odom'])
#         extra['odom_th'] = angle_from_SE2(SE2_from_SE3(extra['odom']))
#         extra['odom_xy'] = translation_from_SE3(extra['odom'])[:2]
        
#         data.append(bd)


@contract(manifold=DifferentiableManifold, min_dist='float,>0')
def sparse_sequence(data, manifold, min_dist):
    """ Yields a sequence """
    sp = Sparsifier(manifold=manifold, min_dist=min_dist)
    for data, pose in data:  
        manifold.belongs(pose)      
        if sp.accept(pose):
            yield data, pose

