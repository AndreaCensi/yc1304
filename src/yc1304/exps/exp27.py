from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel_concurrent_reps,
    jobs_publish_learning_agents_robots, recipe_agentlearn_by_parallel)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos, good_logs_cf
 
__all__ = ['Exp27']

class Exp27(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Trying camera  """
     
    cmd = 'exp27'
    
    robots = [
        # 'exp23_unicornA_hlhr_sane_3'
        'exp21_unicornA_front'
    ]
              
    explogs_learn = list(set(good_logs_hokuyos + good_logs_cf))
    explogs_convert = explogs_learn
       
    agents = [
      'exp23_diffeof', 'cmdstats', 'stats2'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent_reps(context, data_central,
            Exp27.explogs_learn, n=8, max_reps=20,
            only_agents=['exp23_diffeof']
            )
        
        recipe_agentlearn_by_parallel(context, data_central,
                                                Exp27.explogs_learn,
                                                only_agents=['stats2', 'cmdstats'])
        
        for id_robot in Exp27.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp27.agents, Exp27.robots)
        
            
    
