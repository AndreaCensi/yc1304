from bootstrapping_olympics.configuration.master import get_conftools_robots
from bootstrapping_olympics.misc.interaction import iterate_robot_observations
from compmake.utils.describe import describe_type
from procgraph.block_utils.iterator_generator import IteratorGenerator
from procgraph.core.block import Block
from procgraph.core.registrar_other import register_model_spec
from procgraph.scripts.pgmain import pg
from rosstream2boot.configuration import get_conftools_explogs
from rosstream2boot.library.ros_robot import ROSRobot
from yc1304.s00_videos.pg_fcpx_servo_markers import STATE_WAIT, STATE_SERVOING
import numpy as np


def reconstruct_servo_state(id_explog, id_robot, nmap, out_base,
                            navigation_params):
    """ reconstruct the servo state for navigation logs """
    explog = get_conftools_explogs().instance(id_explog)
    robot = get_conftools_robots().instance(id_robot)
    orig_robot = robot.get_inner_components()[-1]    
    if not isinstance(orig_robot, ROSRobot):
        msg = 'Expected ROSRobot, got %s' % describe_type(robot)
        raise ValueError(msg)
    orig_robot.read_from_log(explog)
    
    controller = NavigationController(nmap, **navigation_params)
    
    def read_data():
        servo_state = None
        for obs in iterate_robot_observations(robot, sleep=0):
            timestamp = obs.timestamp
            observations = obs.observations
            commands = obs.commands
          
          
            if servo_state != STATE_SERVOING and np.linalg.norm(commands) == 0:
                servo_state = STATE_WAIT
            else:
                servo_state = STATE_SERVOING
                
            controller.process_observations(observations)
            
            goal = controller.get_current_goal()
            yield 'y', timestamp, observations
            yield 'servo_state', timestamp, servo_state
            yield 'commands', timestamp, commands
            yield 'y_goal', timestamp, goal

    iterator = read_data()
    pg('read_reconstructed_data',
       config=dict(iterator=iterator, out_base=out_base))

def reconstruct_servo_state_nomap(id_explog, id_robot, out_base, goal_at):
    """ reconstruct the servo state for navigation logs """
    explog = get_conftools_explogs().instance(id_explog)
    bag = explog.get_bagfile()
    times = reconstruct(bag, topic='/youbot_safety/in_cmd_vel')
    print times
    
    robot = get_conftools_robots().instance(id_robot)
    orig_robot = robot.get_inner_components()[-1]    
    if not isinstance(orig_robot, ROSRobot):
        msg = 'Expected ROSRobot, got %s' % describe_type(robot)
        raise ValueError(msg)
    orig_robot.read_from_log(explog)
    
    def read_data():
        goal = None
        t0 = None
        for obs in iterate_robot_observations(robot, sleep=0):
            timestamp = obs.timestamp
            if t0 is None:
                t0 = timestamp

            observations = obs.observations

            if goal is None and timestamp - t0 > goal_at:
                goal = observations
                
            commands = obs.commands
            
            if np.linalg.norm(commands) == 0:
                servo_state = STATE_WAIT
            else:
                servo_state = STATE_SERVOING
            
            n = np.sum(commands != 0)
            # print "%20s" % servo_state + "n: %5s " % n + ",".join('%+10.6f' % s for s in commands)
                            
            # goal = controller.get_current_goal()
            yield 'y', timestamp, observations
            yield 'servo_state', timestamp, servo_state
            yield 'commands', timestamp, commands
            if goal is None:
                yield 'y_goal', timestamp, observations
            else:
                yield 'y_goal', timestamp, goal
                

    iterator = read_data()
    pg('read_reconstructed_data',
       config=dict(iterator=iterator, out_base=out_base))



register_model_spec("""
--- model read_reconstructed_data
config out_base
config iterator 

|x:reconstructed_data iterator=$iterator| 

x.y, x.y_goal, x.servo_state -> |sync| -> |video_servo_multi_vis out_base=$out_base|

#x.commands, x.servo_state --> |info|
    
""")



class ReadData(IteratorGenerator):
    Block.alias('reconstructed_data')
    Block.output('y_goal')
    Block.output('y')
    Block.output('commands')
    Block.output('servo_state')
    Block.config('iterator')
    
    def init_iterator(self):
        return self.config.iterator
     
class NavigationController():
    
    def __init__(self, nmap, d_next_threshold, d_next_threshold_alone, ratio_threshold):
        self.nmap = nmap
        self.d_next_threshold = d_next_threshold
        self.d_next_threshold_alone = d_next_threshold_alone
        self.ratio_threshold = ratio_threshold
        
        self.index_cur = None
        self.index_target = None
        
    def process_observations(self, y):
        plus = 1
        
        if self.index_cur is None:
            # self.index_cur = inst
            self.index_cur = self.get_initial_closest_point(y)
            self.index_target = self.index_cur + plus
            
        if self.index_cur >= self.nmap.npoints() - 1 - plus:
            self.index_cur = 0
            
        index_next = self.index_cur + 1 
        # if we are closer to target
        d_cur = self.get_distance(y, self.nmap.get_observations_at(self.index_cur))
        d_next = self.get_distance(y, self.nmap.get_observations_at(index_next))
        ratio = d_next / d_cur
        if False:
            print('ratio: %1.4f <= %1.4f  d_next: %1.4f < %1.4f' % (ratio, self.ratio_threshold,
                                                                d_next, self.d_next_threshold))
        if (d_next < self.ratio_threshold * d_cur and d_next < self.d_next_threshold) or \
            d_next < self.d_next_threshold_alone:
            self.index_cur += 1
            self.index_target = self.index_cur + plus

    def get_current_goal(self):
        return self.nmap.get_observations_at(self.index_target)

    def get_distance(self, y1, y2):
        disc = np.abs(y1 - y2)
        L1_robust = np.percentile(disc, 80)
        return L1_robust
    
    def get_initial_closest_point(self, y):
        i = 0 
        r = 50
        return self.nmap.get_closest_point_around(y, i, r, self.get_distance)

     
def reconstruct(bag, topic='/youbot_safety/in_cmd_vel'):
    import rosbag     
    t0 = None
    for topic, msg, t in rosbag.Bag(bag).read_messages(topics=[topic]):
        if t0 is None:
            t0 = t
            continue
        delta = (t - t0).to_sec()
        linear = msg.linear
        angular = msg.angular
        if delta > 1.2:
            print '-' * 50 
        print('delta %s %s %s %s %s %s %s' % (delta, linear.x, linear.y, linear.z, angular.x, angular.y, angular.z))
        # print topic, msg, t
        t0 = t 
        
    
