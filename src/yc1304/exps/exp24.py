from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (jobs_publish_learning_agents_robots,
    recipe_agentlearn_by_parallel_concurrent, recipe_agentlearn_by_parallel)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos
 
__all__ = ['Exp24']

class Exp24(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ using the good hokuyo logs  """
     
    cmd = 'exp24'
    
    robots = [
        'exp23_unicornA_hlhr_sane_3'
    ]
              
    explogs_learn = good_logs_hokuyos
    explogs_convert = explogs_learn
       
    agents = [
      'exp23_diffeof',
      'exp23_diffeo_fast',
      'stats2'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent(context, data_central, \
            Exp24.explogs_learn, n=8, only_agents=['exp23_diffeof', 'exp23_diffeo_fast'])
        
        recipe_agentlearn_by_parallel(context, data_central,
                                                Exp24.explogs_learn,
                                                only_agents=['stats2'])
        
        
        for id_robot in Exp24.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp24.agents, Exp24.robots)
        
            
    
