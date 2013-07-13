from .compute_actions import (compute_servo_action, process_compute_distances,
    process)
from .reports import (report_distances, report_servo1, report_servo_details,
    report_raw_display)
from boot_navigation import create_navigation_map_from_episode
from bootstrapping_olympics.programs.manager import DataCentral
from contracts import contract
from quickapp import CompmakeContext
from quickapp_boot import (iterate_context_agents_and_episodes, RM_EPISODE_READY,
    RM_AGENT_SERVO)
from yc1304.s10_servo_field.reports import report_servo_distances2
import numpy as np


__all__ = [ 
     'jobs_servo_field',
     'jobs_servo_field_agents',
]
 

def jobs_servo_field(context, data_central, id_agent, id_robot, id_episode,
                              min_dist=0.08, min_th_dist=np.deg2rad(4),
                              area_graphs=2.0):
    servo_agent = context.get_resource(RM_AGENT_SERVO,
                                       id_agent=id_agent, id_robot=id_robot)
    
    
    
    mainly_theta = 'gridth' in id_episode
    if mainly_theta:
        min_spacing = 0
        min_th_dist = np.deg2rad(0.5)
    else:
        min_spacing = min_dist
    
    extra_dep = context.get_resource(RM_EPISODE_READY, id_robot=id_robot, id_episode=id_episode)
    nmap = context.comp_config(create_navigation_map_from_episode,
                        data_central, id_robot, id_episode,
                        max_time=1000, max_num=100000,
                        min_dist=min_dist, min_th_dist=min_th_dist,
                        min_spacing=min_spacing,
                        extra_dep=[extra_dep])

    _processed = context.comp_config(process, nmap, id_robot)
    _processed = context.comp_config(compute_servo_action, _processed, servo_agent)
    processed = context.comp_config(process_compute_distances, _processed)
    
    keys = dict(id_robot=id_robot, id_episode=id_episode, id_agent=id_agent)
 
    r = context.comp_config(report_distances, processed)
    context.add_report(r, 'distances', **keys)

    r = context.comp_config(report_servo1, processed, area_graphs=area_graphs)
    context.add_report(r, 'servo1', **keys)

    r = context.comp_config(report_raw_display, processed)
    context.add_report(r, 'raw_display', **keys)
 
    r = context.comp_config(report_servo_details, servo_agent, processed)
    context.add_report(r, 'servo_details', **keys)
 
    r = context.comp_config(report_servo_distances2, servo_agent, processed,
                     area_graphs=area_graphs)
    context.add_report(r, 'distances2', **keys)
 
 
@contract(context=CompmakeContext, data_central=DataCentral,
          id_robot='str', agents='seq(str)',
          episodes='seq(str)')
def jobs_servo_field_agents(context, data_central, id_robot, agents, episodes):
    cases = iterate_context_agents_and_episodes(context, agents, episodes)
    for c, id_agent, id_episode in cases:
        jobs_servo_field(context=c,
                         data_central=data_central,
                         id_agent=id_agent,
                         id_robot=id_robot,
                         id_episode=id_episode,
                         min_dist=0.07)
        
