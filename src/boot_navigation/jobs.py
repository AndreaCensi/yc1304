from .create_navigation_map import create_navigation_map_from_episode
from boot_navigation import RP_NAVIGATION_MAP
from bootstrapping_olympics.programs.manager import DataCentral
from bootstrapping_olympics.utils import safe_pickle_dump
from contracts import contract
from quickapp import CompmakeContext
from reprep import Report
import numpy as np
import os

__all__ = ['jobs_navigation_map', 'recipe_navigation_map1']


@contract(context=CompmakeContext, outdir='str', data_central=DataCentral, id_robot='str',
          id_episode='str')
def jobs_navigation_map(context, outdir, data_central, id_robot, id_episode):
    context.needs('episode-ready', id_robot=id_robot, id_episode=id_episode)
    min_dist = 0.05
    nmap = context.comp(create_navigation_map_from_episode,
                        data_central, id_robot, id_episode,
                        max_time=10000.0, max_num=200, min_dist=min_dist,
                        min_th_dist=np.deg2rad(5),
                        min_spacing=min_dist)
    filename = os.path.join(outdir, '%s-%s.pickle' % (id_robot, id_episode))
    context.comp(save_map, nmap, filename)
    report = context.comp(report_nmap, nmap)
    context.add_report(report, 'navmap_report', id_robot=id_robot,
                       id_episode=id_episode)
    return nmap


def recipe_navigation_map1(context, data_central):
    """
        Provides RP_NAVIGATION_MAP (id_robot, id_episode)
        
    """
    
    def rp_navigation_map(c, id_robot, id_episode):
        outdir = context.get_output_dir()
        return jobs_navigation_map(c, outdir, data_central, id_robot, id_episode)
        
    rm = context.get_resource_manager()        
    rm.set_resource_provider(RP_NAVIGATION_MAP, rp_navigation_map)


def save_map(nmap, filename):
    print('Saving to %r' % filename)
    safe_pickle_dump(nmap, filename)
    
    
def report_nmap(nmap):
    r = Report()
    nmap.display(r)        
    return r
