from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel_concurrent_reps,
    jobs_publish_learning_agents_robots)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos, good_logs_cf, good_logs_cam_eye
 
__all__ = ['Exp32']

class Exp32(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Trying camera  """
     
    cmd = 'exp32'
    
    robots = [
        # 'exp23_unicornA_hlhr_sane_3'
        'exp21_unicornA_ceil'
    ]
              
    explogs_learn = list(set(good_logs_cam_eye))
    explogs_convert = explogs_learn
       
    agents = [
      'exp32_diffeo',
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent_reps(context, data_central,
            Exp32.explogs_learn, n=8, max_reps=10) 
        for id_robot in Exp32.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp32.agents, Exp32.robots)
        
            
    
