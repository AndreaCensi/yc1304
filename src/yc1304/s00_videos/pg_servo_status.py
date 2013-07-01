import numpy as np
from procgraph import Block
from procgraph_mpl import PlotGeneric
from contracts import contract
from reprep.plot_utils.spines import turn_off_all_axes
from procgraph_mpl.plot_anim import PlotAnim
from procgraph.core.registrar_other import simple_block
from procgraph_images.solid import solid
from reprep.plot_utils import x_axis_set, y_axis_set


STATE_WAIT = 'wait'
STATE_SERVOING = 'servoing'

        

class ServoStatus(Block):
    Block.alias('servo_status')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=240)
    Block.config('style', 'Style (0=lines, 1=points)', default=0)
    Block.input('y')
    Block.input('y_goal')
    Block.input('state')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.first_timestamp = None
        self.plot_anim = PlotAnim()
        
    def update(self):
        if self.first_timestamp is None:
            self.first_timestamp = self.get_input_timestamp(0)
        self.time_since_start = self.get_input_timestamp(0) - self.first_timestamp
        
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
        
    def plot(self, pylab):
        y = data_from_msg(self.input.y)
        y_goal = data_from_msg(self.input.y_goal)
        sensels = np.array(range(y.size))
        
        self.plot_anim.set_pylab(pylab)
        
        M = 0.1
        y_min = 0
        y_max = 1

        if self.config.style == 0:
            y_style = 'k-'
            y_goal_style = 'g-' 
        elif self.config.style == 1:
            y_style = 'ko'
            y_goal_style = 'go' 
        else:
            raise ValueError(self.config.style)
        
        self.plot_anim.plot('y_goal', sensels, y_goal, y_goal_style)
        self.plot_anim.plot('y', sensels, y, y_style)
        
        n = y.size
        border = n / 100.0
        pylab.axis((-border, n - 1 + border, y_min - M, y_max + M))
        turn_off_all_axes(pylab)
    
        # state = self.input.state.data
        # self.plot_anim.text('state', 1, 0.7, state)
        self.plot_anim.text('clock', 0, 1, '%5.2f' % self.time_since_start)

 

class ServoError(Block):
    """ 
        Captures the error since the start of the data.
    """
    Block.alias('servo_error')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=240)
    Block.config('use_first_y_goal', default=True)
    
    Block.input('y')
    Block.input('y_goal')
    Block.input('state')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.plot_anim = PlotAnim()
        self.timestamps = []
        self.ys = []
        self.y_goals = []
        self.y_goal = None
        self.servo_state = STATE_WAIT
        
        self.first_timestamp = None
        
        
        self.plot_line = None
        
    def update_values(self):
        if self.first_timestamp is None:
            self.first_timestamp = self.get_input_timestamp(0)
        self.time_since_start = self.get_input_timestamp(0) - self.first_timestamp

        if isinstance(self.input.state, str):
            state = self.input.state
        else:
            state = self.input.state.data
        assert state in [STATE_WAIT, STATE_SERVOING]
        
        self.y_goal = data_from_msg(self.input.y_goal)
        y = data_from_msg(self.input.y)
        
        assert self.y_goal.shape == y.shape
        
        timestamp = self.get_input_timestamp(0)
        
        
        if self.servo_state == STATE_WAIT and state == STATE_SERVOING:
            # we started now
            self.timestamps = []
            self.ys = []
            self.y_goals = []
            self.info('%s: Started servoing' % self.time_since_start)
            
        if self.servo_state == STATE_SERVOING and state == STATE_WAIT:
            self.info('%s: Stopped servoing' % self.time_since_start)
            self.timestamps = []
            self.ys = []
            self.y_goals = []
        
        # only add values if we are servoing
        if state == STATE_SERVOING:
            self.timestamps.append(timestamp)
            self.ys.append(y)
            self.y_goals.append(self.y_goal)
    
        self.servo_state = state
        self.timestamp = timestamp
        
    def get_relative_times(self):
        T = np.array(self.timestamps)
        if T.size > 0:
            T -= T[0]
        return T

    @contract(y0='array[N]', y1='array[N]')
    def metric(self, y0, y1):
        return np.linalg.norm(y0 - y1)
    
    def get_errors(self):
        if self.config.use_first_y_goal:
            es = [self.metric(self.y_goal, y) for y in self.ys]
        else:
            es = [self.metric(y_goal, y) 
                  for y_goal, y in zip(self.y_goals, self.ys)]
        return np.array(es)
    
    def get_relative_errors(self):
        es = self.get_errors()
        if es.size > 0:
            es = es / es[0]
        return es
        
    def update(self):
        self.update_values()
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
    def get_T(self, duration, chunk, min_time):
        duration = max(duration, min_time)
        T = np.ceil(duration / chunk) * chunk
        return T  
        
    def plot(self, pylab):
        ts = self.get_relative_times()
        es = self.get_relative_errors()
        assert ts.size == es.size
        
        self.plot_anim.set_pylab(pylab)
        
        if ts.size > 0:
            T = self.get_T(duration=(ts[-1] - ts[0]), chunk=5, min_time=15)
            assert T >= ts[-1]
        else:
            T = 10
        
        if self.plot_line is None:            
            ax1 = pylab.gca()
            ax1.axes.get_xaxis().set_visible(False)
            ax1.axes.get_yaxis().set_visible(False)
            self.plot_line = True
        
        border = 2
        if self.config.use_first_y_goal:
            pylab.axis((-1, T + border, -0.1, 1.3))
        else:
            x_axis_set(pylab, -1, T + border)
            if es.size > 0:
                y_axis_set(pylab, -0.1, np.max(es) * 1.3)

        # s = '%s %s' % (self.servo_state, self.timestamp)
        # self.plot_anim.text('status', 0.7 * T, 1.2, s)
        # self.plot_anim.text('clock', 0.7 * T, 1.2, '%5.2f' % self.time_since_start)
        self.plot_anim.plot('error', ts, es, 'k-')
        
        if es.size > 0:
            self.plot_anim.plot('error1', ts[0], es[0], 'rs')
            self.plot_anim.plot('error2', ts[-1], es[-1], 'rs')
        else:
            self.plot_anim.plot('error1', [], [], 'ro')
            self.plot_anim.plot('error2', [], [], 'ro')
        
        self.plot_anim.plot('zero', [0, T], [0, 0], 'k--')
            
        if self.servo_state == STATE_SERVOING:
            # self.info('Servoing')
            pass
        else:
            pass
            # self.info('Not servoing')
        
        # self.info('%10s %10s' % (self.time_since_start, self.servo_state))
        

@simple_block
def servo_state_indicator(state_msg, width=64, height=64):
    if isinstance(state_msg, str):
        state = state_msg
    else:
        state = state_msg.data
    
    colors = {
          STATE_WAIT: [0, 0, 0],
          STATE_SERVOING: [255, 0, 0],
          None: [255, 255, 0]
    }
    
    color = colors.get(state, colors[None])
    return solid(width, height, color)
     


def data_from_msg(x):
    if isinstance(x, np.ndarray):
            return x
    else:        
        return  np.array(x.values)
