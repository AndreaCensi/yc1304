from contracts import contract, describe_type

from bootstrapping_olympics import get_conftools_robots
from bootstrapping_olympics.misc.interaction import iterate_robot_observations
import numpy as np
from procgraph import Block, pg, register_model_spec
from procgraph.block_utils import IteratorGenerator
from rosstream2boot import get_conftools_explogs
from rosstream2boot.library import ROSRobot
from yc1304.s00_videos.pg_fcpx_servo_markers import STATE_WAIT, STATE_SERVOING


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
    # get a list of state transitions
    transitions = reconstruct(bag, topic='/youbot_safety/in_cmd_vel')
    print(transitions)
    
    robot = get_conftools_robots().instance(id_robot)
    orig_robot = robot.get_inner_components()[-1]    
    if not isinstance(orig_robot, ROSRobot):
        msg = 'Expected ROSRobot, got %s' % describe_type(robot)
        raise ValueError(msg)
    orig_robot.read_from_log(explog)
    
    def read_data():
        goal = None
        t0 = None
        servo_state = STATE_WAIT
        for obs in iterate_robot_observations(robot, sleep=0):
            timestamp = obs.timestamp
            if t0 is None:
                t0 = timestamp

            observations = obs.observations

            if goal is None and timestamp - t0 > goal_at:
                goal = observations
                
            commands = obs.commands
            
            # if still have transitions
            if transitions:
                next_transition = transitions[0][0]
                if timestamp > next_transition:
                    servo_state = transitions[0][1]
                    transitions.pop(0)
            
#             if np.linalg.norm(commands) == 0:
#                 servo_state = STATE_WAIT
#             else:
#                 servo_state = STATE_SERVOING
#             
#             n = np.sum(commands != 0)
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
            print('ratio: %1.4f <= %1.4f  d_next: %1.4f < %1.4f' % 
                  (ratio, self.ratio_threshold,
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



@contract(returns='list(tuple(float, str))')
def reconstruct(bag, topic='/youbot_safety/in_cmd_vel'):
    """ 
        Returns a list of state transitions (time, state) for 
        when servoing started or stopped.
        
        It looks for intervals in the command sequence.
        
        (For some runs I had forgotten to log this information originally.)
    """
    import rosbag     
    t0 = None
    cur_state = STATE_WAIT
    transitions = []
    for topic, msg, t in rosbag.Bag(bag).read_messages(topics=[topic]):
        if t0 is None:
            t0 = t
            continue
        delta = (t - t0).to_sec()
        linear = msg.linear
        angular = msg.angular
        
        nonzero = np.linalg.norm([linear.x, linear.y, angular.z]) > 0
        
        if delta > 1.2:
            transition = True
        else:
            transition = False
            
        if transition:
            print('-' * 50)
        
            if cur_state == STATE_WAIT and nonzero:
                cur_state = STATE_SERVOING
                transitions.append((t.to_sec(), cur_state))
                print('new state: %s' % cur_state)
            else:
                cur_state = STATE_WAIT
                transitions.append((t.to_sec(), cur_state))
            
                print('new state: %s' % cur_state)
        print('%s delta %s %s %s %s %s %s %s' % 
              (cur_state, delta, linear.x, linear.y, linear.z,
                angular.x, angular.y, angular.z))
        t0 = t 
        
    return transitions
    
