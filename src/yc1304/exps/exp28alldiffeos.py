from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel_concurrent_reps,
    jobs_publish_learning_agents_robots, recipe_agentlearn_by_parallel)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos, good_logs_cf
 
__all__ = ['Exp28']

class Exp28(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Runs all of the diffeo learning at once  """
     
    cmd = 'exp28'
    
    robots = [
        # 'pc3-unicornA_tw1_cf_320_rgb',
        'pc2-unicornA_tw1_cf_320_rgb',
        'pc3-unicornA_tw1_cr_320_rgb',
        'pc3-unicornA_tw1_hlhr_sanes4_pc128'
    ]
              
    explogs_learn = list(set(good_logs_hokuyos + good_logs_cf))
    explogs_convert = explogs_learn
       
    agents = [
      'exp28_diffeo',
      'cmdstats',
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent_reps(context, data_central,
            Exp28.explogs_learn, n=8, max_reps=10,
            only_agents=['exp28_diffeo']
            )
        
        recipe_agentlearn_by_parallel(context, data_central,
                                                Exp28.explogs_learn,
                                                only_agents=['stats2', 'cmdstats'])
        
        for id_robot in Exp28.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp28.agents, Exp28.robots)
        
            
    
