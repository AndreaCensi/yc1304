from boot_navigation import create_navigation_map_from_episode
from conf_tools import GlobalConfig
from quickapp import QuickApp, iterate_context_names
from quickapp_boot import (jobs_publish_learning_agents_robots,
    recipe_agentlearn_by_parallel)
from reprep import Report
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos
import numpy as np
 
__all__ = ['Exp29']

class Exp29(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ First navigation code  """
     
    cmd = 'exp29'
    
#     robot = 'pc3-unicornA_tw1_cr_320_rgb'
    robot = 'unicornA_tw1_hlhr_sane_s4'
    robots = [robot]
    
#     explog_episode = 'unicornA_base1_2013-04-02-20-37-43'  # 37m, nominal, boxes
    nmaps = ['unicornA_teleop_nmap_2013-05-31-19-51-24',  # figure 8 translation only
             'unicornA_teleop_nmap_2013-05-31-19-54-07']
#     explog_episode = 'unicornA_tran1_2013-04-12-22-29-16'
#     explog_episode = 'unicornA_tran1_2013-04-11-23-21-36'  # on grid 
    explogs_convert = []
    explogs_convert.extend(nmaps) 
    
    explogs_learn = list(set(good_logs_hokuyos))
    explogs_convert.extend(explogs_learn)
    

    agents = [
      'exp08_bdser1'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')
 
        id_robot = Exp29.robot
        
        recipe_episodeready_by_convert2(context, boot_root, id_robot)
        recipe_agentlearn_by_parallel(context, data_central, Exp29.explogs_learn)
        
        for c, id_episode in iterate_context_names(context, Exp29.nmaps): 
            jobs_navigation_map(c, data_central=data_central,
                                id_robot=id_robot,
                                id_episode=id_episode)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp29.agents, Exp29.robots)
        

def jobs_navigation_map(context, data_central, id_robot, id_episode):
    context.needs('episode-ready', id_robot=id_robot, id_episode=id_episode)
    
    nmap = context.comp(create_navigation_map_from_episode,
                        data_central, id_robot, id_episode,
                        max_time=10000.0, max_num=1000, min_dist=0.1,
                        min_th_dist=np.deg2rad(10))
    report = context.comp(report_nmap, nmap)
    context.add_report(report, 'navmap_report', id_robot=id_robot,
                       id_episode=id_episode)
    return nmap
    
def report_nmap(nmap):
    r = Report()
    nmap.display(r)        
    return r


