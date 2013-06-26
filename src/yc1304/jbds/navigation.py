from .servo_reconstruct import reconstruct_servo_state
from boot_navigation import RP_NAVIGATION_MAP, recipe_navigation_map1
from boot_navigation.reports import _nmapobslist_to_rgb
from contracts import contract
from geometry import SE2, SE2_from_SE3, translation_from_SE2
from quickapp import QuickApp
from quickapp_boot import RM_EPISODE_READY
from reprep import Report, scale, filter_colormap
from reprep.plot_utils import turn_off_all_axes
from rosstream2boot import (get_conftools_explogs,
    recipe_episodeready_by_convert2)
from yc1304.campaign import CampaignCmd
from yc1304.exps.exp_utils import iterate_context_explogs
import itertools
import numpy as np
import os

__all__ = ['JBDSNavigationVisualization']

 
            
class JBDSNavigationVisualization(CampaignCmd, QuickApp): 
    
    """ Visualization of the servo logs for JBDS """
    cmd = 'jbds-videos-navigation'
    
    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('jbds-nav')

        logs = set(self.get_explogs_by_tag('navigation'))
        logs = list(logs)
        assert len(logs) >= 4

        data_central = self.get_data_central()
        recipe_episodeready_by_convert2(context, data_central.get_boot_root())
        recipe_navigation_map1(context, data_central)
        
        for c, id_explog in iterate_context_explogs(context, logs):
            explog = get_conftools_explogs().instance(id_explog)
            # Get the map that we need
            annotation_navigation = explog.get_annotations()['navigation'] 
            id_explog_map = annotation_navigation['map']
            id_robot = annotation_navigation['robot']
#             if not 'params' in annotation_navigation:
#                 self.error('incomplete %r' % id_explog)
#                 continue
            navigation_params = annotation_navigation['params']
                    
            nmap = c.get_resource(RP_NAVIGATION_MAP,
                                  id_episode=id_explog_map,
                                  id_robot=id_robot)
            
            out_base = os.path.join(c.get_output_dir(), '%s' % id_explog)
            c.comp_config(reconstruct_servo_state, id_explog, id_robot, nmap,
                          out_base=out_base,
                          navigation_params=navigation_params,
                          job_id='reconstruct')        
            
            extra_dep = [c.get_resource(RM_EPISODE_READY, id_robot=id_robot,
                                        id_episode=id_explog)]
            nmap_dist = c.comp_config(nmap_distances, data_central,
                                                id_episode=id_explog,
                                                id_robot=id_robot, nmap=nmap,
                                                extra_dep=extra_dep)
            
            report_keys = dict(id_robot=id_robot, id_episode=id_explog,
                               id_episode_map=id_explog_map)
            r = c.comp(report_nmap_distances, nmap, nmap_dist)
            c.add_report(r, 'nmap_distances', **report_keys)
            
            poses = c.comp_config(poses_from_episode, data_central=data_central,
                                  id_robot=id_robot, id_episode=id_explog)
            
            poses0 = c.comp_config(poses_from_episode, data_central=data_central,
                                  id_robot=id_robot, id_episode=id_explog_map)
             
            r = c.comp(report_trajectory, poses, poses0)
            c.add_report(r, 'trajectory', **report_keys)

    
@contract(returns='list(SE2)')
def poses_from_episode(data_central, id_robot, id_episode):
    """ Returns a list of poses """
    log_index = data_central.get_log_index()
    log_index.reindex()
    
    bds = log_index.read_robot_episode(id_robot=id_robot, id_episode=id_episode,
                                       read_extra=True)
    poses = []
    for bd in bds:
        pose = np.array(bd['extra'].item()['robot_pose'])
        pose = SE2_from_SE3(pose)
        poses.append(pose)

    return poses


@contract(poses='list[N](SE2)', returns='list[N](SE2)')
def align(poses):
    start = poses[0]
    poses2 = [SE2.multiply(SE2.inverse(start), p) for p in poses]
    return poses2


@contract(returns=Report, poses='list(SE2)')
def report_trajectory(poses, poses_nmap):
    poses2 = align(poses)
    poses_nmap2 = align(poses_nmap)

    r = Report()
    f = r.figure(cols=2)
    
    def axis(pylab, axes=False):
        pylab.axis('equal')
        x0 = -1
        x1 = 2
        y0 = -2
        y1 = +2
        b = 0.1
        if axes:
            pylab.plot([x0 + b, x0 + b], [y0 + b, y0 + b + 1], 'k-')
            pylab.plot([x0 + b, x0 + b + 1], [y0 + b, y0 + b], 'k-')
        pylab.axis([x0, x1, y0, y1])
        
        turn_off_all_axes(pylab)
        
    with f.plot('poses') as pylab:
        plot_poses_xy(pylab, poses, 'g-')
        axis(pylab, False)

    with f.plot('poses_nmap2') as pylab:
        plot_poses_xy(pylab, poses_nmap2, 'k-')
        axis(pylab)

    with f.plot('poses2') as pylab:
        plot_poses_xy(pylab, poses2, 'g-')
        axis(pylab)

    with f.plot('both') as pylab:
        plot_poses_xy(pylab, poses_nmap, 'k-')
        plot_poses_xy(pylab, poses, 'g-')
        axis(pylab, False)

    with f.plot('both2') as pylab:
        plot_poses_xy(pylab, poses_nmap2, 'k-')
        plot_poses_xy(pylab, poses2, 'g-')
        axis(pylab)
        
    return r


def plot_poses_xy(pylab, poses, color='k-'):
    xy = np.array(map(translation_from_SE2, poses))
    assert xy.shape[1] == 2
    x = xy[:, 0]
    y = xy[:, 1]
    pylab.plot(x, y, color)
    

def report_nmap_distances(nmap, nmap_distances):
    r = Report()
    timestamps = []
    alldists = []
    allobs = []
    poses = []
    for i, (timestamp, (y, distances, pose)) in enumerate(nmap_distances):
        timestamps.append(timestamp)
        alldists.append(distances)
        allobs.append(y)
        poses.append(pose)

    timestamp = np.array(timestamps)    
    alldists = np.vstack(alldists).T
        
    print ('ntimestamps: %s' % len(timestamps))
    nwaypoints, nmoments = alldists.shape
    print('nmoments: %s' % nmoments)
    print('nwaypoints: %s' % nwaypoints)
    
    assert len(timestamps) == nmoments
    
    f = r.figure(cols=1)
    GREEN = [0, 1, 0]
    RED = [1, 0, 0]
    
    alldists_rgb1 = scale(alldists, min_color=GREEN, max_color=RED)
    f.data_rgb('alldists', alldists_rgb1)
    alldists_rgb2 = filter_colormap(alldists,
                   cmap='jet',
                   min_value=None, max_value=None,
                   nan_color=[1, 0.6, 0.6],
                   inf_color=[0.6, 1, 0.6],
                   flat_color=[0.5, 0.5, 0.5])
    
    f.data_rgb('alldists2', alldists_rgb2)
    
    f.data_rgb('observations', _nmapobslist_to_rgb(allobs))
    
    waypoints = range(0, nwaypoints, 5)
    with f.plot('distances') as pylab:
        for a, i in enumerate(waypoints): 
            d = alldists[i, :]        
            d = d - np.min(d)
            d = d / np.max(d)
            x = timestamps
            y = d + a * 1.1
            pylab.plot(x, y, 'k-')
            
    return r
    
    
@contract(returns='list( tuple(float, array[M]) )')                
def nmap_distances(data_central, id_episode, id_robot, nmap):
    """ 
        Computes the distance of each observation in the log
        to the waypoints of the map. 
    """
    log_index = data_central.get_log_index()
    log_index.reindex()
    
    distance = lambda a, b: np.mean(np.abs(a - b))
    
    alldists = []
    bds = log_index.read_robot_episode(id_robot=id_robot, id_episode=id_episode,
                                       read_extra=True)
    bds = itertools.islice(bds, 0, 100000, 2)
    for bd in bds:
        y = bd['observations']
        timestamp = bd['timestamp']
        pose = np.array(bd['extra'].item()['robot_pose'])
        # ignore null commands
        if np.allclose(0, bd['commands']):
            continue
        dists = []
        for ym in nmap.get_all_observations():
            d = distance(y, ym)
            dists.append(d)
        dists = np.array(dists)
        alldists.append((timestamp, (y, dists, pose)))
    return alldists

            
