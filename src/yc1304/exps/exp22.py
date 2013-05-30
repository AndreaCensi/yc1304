from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (jobs_publish_learning_agents_robots,
    recipe_agentlearn_by_parallel_concurrent)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_cf
 
__all__ = ['Exp22']

class Exp22(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Experimenting with different deltas  """
     
    cmd = 'exp22'
    
    robots = [
        'exp22_unicornA_ceil',
#             'exp22_unicornA_front',
#             'exp22_unicornA_hlhr_sane_1'
    ]
              
    explogs_learn = good_logs_cf
    explogs_convert = explogs_learn
        
    agents = [
      'exp22_diffeof',
#       'exp22_diffeo2',
#       'stats2'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent(context, data_central, Exp22.explogs_learn)
        
        for id_robot in Exp22.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp22.agents, Exp22.robots)
        
            
    
