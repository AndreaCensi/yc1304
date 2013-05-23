from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel, jobs_publish_learning_agents_robots)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_cf
 
__all__ = ['Exp21']


class Exp21(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ All different ways to make images  """
     
    cmd = 'exp21'
    
    robots = ['exp21_unicornA_ceil',
              'exp21_unicornA_front',
              'exp21_unicornA_hlhr_sane_1']
              
    explogs_learn = good_logs_cf
    explogs_convert = explogs_learn
        
    agents = ['exp21_diffeof', 'stats2']
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_agentlearn_by_parallel(context, data_central, Exp21.explogs_learn)
        
        for id_robot in Exp21.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp21.agents, Exp21.robots)
        
            
    
