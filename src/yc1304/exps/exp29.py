from conf_tools import GlobalConfig
from quickapp import QuickApp
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from boot_navigation import create_navigation_map_from_episode
from reprep import Report
 
__all__ = ['Exp29']

class Exp29(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ First navigation code  """
     
    cmd = 'exp29'
    
    robot = 'unicornA_tw1_cr_320_rgb'
    robots = [robot]
#         'pc3-unicornA_tw1_cf_320_rgb',
        
#         'pc3-unicornA_tw1_hlhr_sanes4_pc128'
    
    explog_episode = 'unicornA_base1_2013-04-02-20-37-43'  # 37m, nominal, boxes
    explog_episode = 'unicornA_tran1_2013-04-12-22-29-16'
    explog_episode = 'unicornA_tran1_2013-04-11-23-21-36'  # on grid 
    explogs_convert = [explog_episode]
#     explogs_learn = list(set(good_logs_hokuyos + good_logs_cf))
#     explogs_convert = explogs_learn
#        
#     agents = [
#       'exp28_diffeo',
#       'cmdstats',
#     ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')
# 
#         recipe_agentlearn_by_parallel_concurrent_reps(context, data_central,
#             Exp29.explogs_learn, n=8, max_reps=10,
#             only_agents=['exp28_diffeo']
#             )
#         
#         recipe_agentlearn_by_parallel(context, data_central,
#                                                 Exp29.explogs_learn,
#                                                 only_agents=['stats2', 'cmdstats'])
#         
        id_robot = Exp29.robot
        id_episode = Exp29.explog_episode
        
        recipe_episodeready_by_convert2(context, boot_root, id_robot)
        jobs_navigation_map(context, data_central=data_central,
                            id_robot=id_robot,
                            id_episode=id_episode)

# 
#         jobs_publish_learning_agents_robots(context, boot_root,
#                                             Exp29.agents, Exp29.robots)
        
            
def jobs_navigation_map(context, data_central, id_robot, id_episode):
    context.needs('episode-ready', id_robot=id_robot, id_episode=id_episode)
    
    nmap = context.comp(create_navigation_map_from_episode,
                        data_central, id_robot, id_episode)
    report = context.comp(report_nmap, nmap)
    context.add_report(report, 'navmap_report', id_robot=id_robot,
                       id_episode=id_episode)
    return nmap
    
def report_nmap(nmap):
    r = Report()
    nmap.display(r)        
    return r


