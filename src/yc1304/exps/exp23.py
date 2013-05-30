from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (jobs_publish_learning_agents_robots,
    recipe_agentlearn_by_parallel_concurrent, recipe_agentlearn_by_parallel)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_cf
from diffeo2dds_learn.programs.devel.save_video import video_visualize_diffeo_stream1_robot
from quickapp.app_utils.subcontexts import iterate_context_names
import os
 
__all__ = ['Exp23']

class Exp23(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Experimenting with different deltas  """
     
    cmd = 'exp23'
    
    robots = [
        # 'exp23_unicornA_hlhr_sane_3'
        'exp21_unicornA_front'
    ]
              
    explogs_learn = good_logs_cf
    explogs_convert = explogs_learn
       
    agents = [
      'exp23_diffeof',
      'cmdstats',
      'stats2'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')

        recipe_agentlearn_by_parallel_concurrent(context, data_central,
            Exp23.explogs_learn, n=8, only_agents=['exp23_diffeof', 'exp23_diffeo_fast'])
        
        recipe_agentlearn_by_parallel(context, data_central,
                                                Exp23.explogs_learn,
                                                only_agents=['stats2'])
        

        for c, id_robot in iterate_context_names(context, Exp23.robots):
            out = os.path.join(context.get_output_dir(),
                               'videos', '%s-diffeo_stream1.mp4' % id_robot)
            c.comp_config(video_visualize_diffeo_stream1_robot,
                          id_robot=id_robot, boot_root=boot_root,
                          out=out)
        
        for id_robot in Exp23.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp23.agents, Exp23.robots)
        
            
    
