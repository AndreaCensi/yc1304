from aer.logs.load_aer_logs import aer_raw_events_from_file_all
from conf_tools import GlobalConfig
from contracts import contract
from quickapp import QuickApp
from quickapp_boot import RM_EPISODE_READY
from reprep import Report, scale
from rosstream2boot import recipe_episodeready_by_convert2
from rosstream2boot.configuration import get_conftools_explogs
from yc1304.campaign import CampaignCmd
from yc1304.exps.exp_utils import iterate_context_explogs
import numpy as np

__all__ = ['UZHTurtlePlots']


class UZHTurtlePlots(CampaignCmd, QuickApp):
    """ 
        Plots 2D barcode grams.
        
        Uses environment variable DATASET_UZHTURTLE for linking to the 
        directory.
        
    """
    
    cmd = 'uzh-turtle-plots'
    
    def define_options(self, options):
        pass 

    def define_jobs_context(self, context):
        from pkg_resources import resource_filename  # @UnresolvedImport
        config_dir = resource_filename("yc1304.uzhturtle", "config")
        GlobalConfig.global_load_dir(config_dir)
        GlobalConfig.global_load_dir('${DATASET_UZHTURTLE}')
        
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('uzh-turtle-plots')

        data_central = self.get_data_central()

        id_robot = 'uzhturtle_un1_cf1_third'
        recipe_episodeready_by_convert2(context, boot_root=self.get_boot_root())

        logs = list(self.get_explogs_by_tag('uzhturtle'))
        for c, id_explog in iterate_context_explogs(context, logs):
            jobs_turtleplot(c, data_central, id_robot, id_episode=id_explog)
            

def jobs_turtleplot(context, data_central, id_robot, id_episode):
    comp = context.comp_config
    
    ready = context.get_resource(RM_EPISODE_READY,
                                 id_robot=id_robot, id_episode=id_episode)
    alldata = comp(read_all_data, data_central, id_robot, id_episode,
                   extra_dep=[ready])
    r = comp(report_alldata, alldata)
    context.add_report(r, 'alldata', id_robot=id_robot, id_episode=id_episode)
   
    events = comp(read_all_events, id_episode)
    r = comp(report_events, events)
    context.add_report(r, 'events', id_robot=id_robot, id_episode=id_episode)
    
def read_all_events(id_explog): 
    explog = get_conftools_explogs().instance(id_explog)
    files = explog.get_files()
    if not 'aer' in files:
        msg = 'Could not find aer log (%s)' % files
        raise ValueError(msg)
    
    filename = files['aer']
    events = aer_raw_events_from_file_all(filename, limit=None)
    return events 

@contract(events='array', delta='float,>0', returns='list[>=1](array)')
def make_events_slices(events, delta):
    """ 
        Slices the array of events according to the given delta.
        Returns a list of arrays of events.
    """
    timestamps = events['timestamp']
    slices = get_slices_indexes(timestamps, delta)
    xs = []
    for indices in slices:
        x = events[indices]
        xs.append(x)
    return xs 

@contract(timestamps='array[>=1](float)', delta='float,>0',
          returns='list[>=1](array[>=1](int))')
def get_slices_indexes(timestamps, delta):
    """
        Slices a timestamp list according to the given interval delta.
        Returns a list of arrays of timestamps.
    """
    N = timestamps.size
    slices = []
    cur_start = 0
    for i in range(1, N):
        cur_delta = timestamps[i] - timestamps[cur_start]
        if cur_delta > delta:
            S = range(cur_start, i)  # timestamps[cur_start:i - 1]
            # print('slice: %d elements' % len(S))
            slices.append(S)
            cur_start = i
    
    S = range(cur_start, N)
    slices.append(S)
    
    # check that we partitioned the array correctly
    sequence = []
    for s in slices:
        sequence.extend(s)
    assert sequence == range(timestamps.size), sequence
    return slices    
    

def report_alldata(alldata):
    r = Report()
    y = alldata['observations']
    yr = scale(y)
    f = r.figure()
    f.data_rgb('y', yr)
    
    return r


def report_events(events, delta=1.0 / 8):
    r = Report()
    
    f = r.figure()
    with f.plot('events') as pylab:
        plot_events_x(pylab, events)
        
    f = r.figure('slices')
    
    y = events['y']
    center = np.logical_and(y > 50, y < 75)
    events = events[center]

    slices = make_events_slices(events, delta)
    for i, s in enumerate(slices):
        with f.plot('slice%d' % i) as pylab:
            plot_events_x(pylab, s)
        
    return r


def plot_events_x(pylab, events):
    pos = events['sign'] > 0
    neg = events['sign'] < 0
    epos = events[pos]
    eneg = events[neg]
    t = events['timestamp'] - events['timestamp'][0]
    
    pylab.plot(epos['x'], t[pos], 'rs')
    pylab.plot(eneg['x'], t[neg], 'bs')
    
    
def read_all_data(data_central, id_robot, id_episode):
    log_index = data_central.get_log_index()
    ys = []
    for obs in log_index.read_robot_episode(id_robot, id_episode):
        ys.append(obs)
    ys = np.hstack(ys)
    return ys


