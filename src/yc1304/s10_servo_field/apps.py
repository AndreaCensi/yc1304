from . import process, read_pose_observations, report_raw_display
from yc1304.campaign import CampaignCmd
from yc1304.s10_servo_field.report_long_term import report_long_term
from yc1304.s10_servo_field.reports import (report_distances, report_servo1, report_servo_details)
from yc1304.s10_servo_field.show_field import (compute_servo_action,
    remove_discontinuities, process_compute_distances)
from conf_tools.master import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import iterate_context_agents_and_episodes


__all__ = ['CreateField', 'ServoField', 'jobs_servo_field', 'jobs_servo_field_agents']


class CreateField(CampaignCmd, QuickApp):
    cmd = 'create_field'
 
    def define_options(self, params):
        params.add_string('id_robot', help='', compulsory=True)
        params.add_string('id_episode', help='', compulsory=True)
        params.add_float('min_dist', help='Minimum distance for fake grid',
                         default=0.07)

    def define_jobs_context(self, context):
        options = self.get_options()

        id_robot = options.id_robot
        id_episode = options.id_episode
        min_dist = options.min_dist
        
        data_central = self.get_data_central()
        
        all_data = context.comp(read_pose_observations, data_central, id_robot, id_episode)
        _processed = context.comp(process, all_data, min_dist)
        processed = context.comp(process_compute_distances, _processed)
        context.add_report(context.comp(report_raw_display, processed),
                           'raw_display', id_robot=id_robot, id_episode=id_episode)
        context.add_report(context.comp(report_distances, processed),
                           'distances', id_robot=id_robot, id_episode=id_episode)
    
        keys = dict(id_robot=id_robot, id_episode=id_episode)
        
        reports = {'distances': report_distances,
                   'raw_display': report_raw_display}
        
        for k, v in reports.items(): 
            context.add_report(context.comp(v, processed), k, **keys)
    

class ServoField(CampaignCmd, QuickApp):
    cmd = 'servo_field'
 
    def define_options(self, params):
        params.add_string('id_robot', help='', compulsory=True)
        params.add_string('id_episode', help='', compulsory=True)
        params.add_string('id_agent', help='', compulsory=True)
        params.add_string('variation', help='')
        params.add_float('min_dist', help='Minimum distance for fake grid',
                         default=0.07)

    def define_jobs_context(self, context):
        options = self.get_options()

        id_agent = options.id_agent
        variation = options.variation
        id_robot = options.id_robot
        
        id_episode = options.id_episode
        min_dist = options.min_dist
        
        data_central = self.get_data_central()
        
        all_data = context.comp(read_pose_observations, data_central, id_robot, id_episode)
        _processed = context.comp(process, all_data, min_dist)
        _processed = context.comp(remove_discontinuities, _processed, threshold=0.2)
        _processed = context.comp(compute_servo_action, GlobalConfig.get_state(), _processed, data_central,
                                  id_agent, id_robot, variation)
        processed = context.comp(process_compute_distances, _processed)
        
        
        keys = dict(id_robot=id_robot, id_episode=id_episode, id_agent=id_agent, variation=variation)
        
        reports = {'distances': report_distances,
                   'servo1': report_servo1,
                   'servo_details': report_servo_details,
                   'long_term': report_long_term,
                   'raw_display': report_raw_display}
        
        for k, v in reports.items(): 
            context.add_report(context.comp(v, processed), k, **keys)
    


def jobs_servo_field(context, id_agent, id_robot, id_episode):
    context.needs('agent-learn', id_agent=id_agent, id_robot=id_robot)
    context.needs('episode-ready', id_robot=id_robot, id_episode=id_episode)
    # TODO: episode ready?
    context.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                          variation='default', id_episode=id_episode)
       
def jobs_servo_field_agents(context, id_robot, agents, episodes):
    cases = iterate_context_agents_and_episodes(context, agents, episodes)
    for c, id_agent, id_episode in cases:
        jobs_servo_field(c, id_agent, id_robot, id_episode)
        
