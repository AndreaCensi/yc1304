from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (jobs_publish_learning_agents_robots,
    recipe_agentlearn_by_parallel)
from quickapp_boot.recipes.recipes_learning_parallel import (
    recipe_agentlearn_by_parallel_concurrent_reps)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos, good_logs_cf
 
__all__ = ['Exp25']

class Exp25(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ using the good hokuyo logs  """
     
    cmd = 'exp25'
    
    robots = [
        'exp23_unicornA_hlhr_sane_3'
    ]
              
    explogs_learn = list(set(good_logs_hokuyos + good_logs_cf))
    explogs_convert = explogs_learn
       
    agents = [
      'exp23_diffeof',
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent_reps(context, data_central,
            Exp25.explogs_learn, n=8, max_reps=20,
            only_agents=['exp23_diffeof', 'exp23_diffeo_fast'])
        
        recipe_agentlearn_by_parallel(context, data_central,
                                                Exp25.explogs_learn,
                                                only_agents=['stats2'])
        
        
        for id_robot in Exp25.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp25.agents, Exp25.robots)
        
            
    
