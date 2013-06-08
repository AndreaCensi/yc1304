from contracts import contract
import numpy as np
from boot_navigation import NavigationMap
from geometry import R2
from bootstrapping_olympics import get_conftools_robots


@contract(nmap=NavigationMap)
def process(nmap, id_robot):
    res = {}
    index = nmap.get_R2_centroid_index()
    
    origin = nmap.get_pose_at_index(index)
    res['nmap'] = nmap.move_origin(origin)
    res['centroid'] = nmap.get_R2_points()[index]
    res['y_goal'] = nmap.get_observations_at(index)

    # we need to convert commands to velocities for visualization
    res['robot'] = get_conftools_robots().instance(id_robot)
    
    return res

def process_compute_distances(processed):
    nmap = processed['nmap']
    centroid = processed['centroid']
    y_goal = processed['y_goal']
    
    processed['p_distance'] = [R2.distance(p, centroid) for p in nmap.get_R2_points()]  
    
    # ... for observations
    y_dist = lambda y0, y1: np.linalg.norm(y0 - y1) 
    processed['y_distance'] = [y_dist(y, y_goal) for y in nmap.get_all_observations()]
    
    return processed

def compute_servo_action(processed, servo_agent):
    nmap = processed['nmap'] 
    y_goal = processed['y_goal']
    servo = []
    for bd, _ in nmap.get_all_points():
        res = compute_servo_commands(servo_agent, y_goal, bd)
        servo.append(res)
    processed['servo'] = servo
    return processed

def compute_servo_commands(servo_agent, y_goal, bd):
    servo_agent.set_goal_observations(y_goal)
    servo_agent.process_observations(bd) 
    res = servo_agent.choose_commands_ext()
    return res


