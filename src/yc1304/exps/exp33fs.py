from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel_concurrent_reps,
    jobs_publish_learning_agents_robots)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos, good_logs_cf, good_logs_cam_eye
from quickapp_boot.recipes.recipes_learning_parallel import recipe_agentlearn_by_parallel_concurrent, \
    recipe_agentlearn_by_parallel
from yc1304.s10_servo_field.jobs import jobs_servo_field_agents
from quickapp.app_utils.subcontexts import iterate_context_names
from yc1304.exps.exp_utils import jobs_learnp_and_servo

 
__all__ = ['Exp33']

class Exp33(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Trying field sampler """
     
    cmd = 'exp33'
    
    robots = [
        # 'exp23_unicornA_hlhr_sane_3'
        'unicornA_tw1_fs1',
        'unicornA_tr1_fs1',
        'unicornA_un1_fs1'
    ]
                     
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08',  # convex environment
        'unicornA_lab_grid_2013-06-01-21-00-47',  # non-convex environment 1
        'unicornA_lab_grid_2013-06-01-21-04-51',  # non-convex environment 2
        'unicornA_lab_gridth_2013-06-01-21-11-15'  # pure rotation on theta
    ]
          
    explogs_learn = list(set(good_logs_cam_eye))
    explogs_convert = explogs_learn
       
    agents = [
        "bdse_e1_ss",
        "bdser_er1_i1_ss",
#         "bdser_er1_i1_sr",
#         "bdser_er1_i1_srl",
#         "bdser_er1_i2_ss",
# #         "bdser_er1_i2_sr",
# #         "bdser_er1_i2_srl",
# #         "bdser_er2_i1_sr",
# #         "bdser_er2_i1_srl",
# #         "bdser_er3_i2_ss",
#         "bdser_er2_i2_sr",
#         "bdser_er2_i2_srl",
#         "bdser_er3_i1_sr",
#         "bdser_er3_i1_srl",
#         "bdser_er3_i2_ss",
#         "bdser_er3_i2_sr",
#         "bdser_er3_i2_srl",
#         'bdser_er4_i2_ss',
#         'bdser_er4_i2_sr',
#         'bdser_er4_i2_srl',
#         
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')
        
        agents = Exp33.agents
        robots = Exp33.robots
        explogs_learn = Exp33.explogs_learn
        explogs_test = Exp33.explogs_test
    
        jobs_learnp_and_servo(context, data_central=data_central,
                              explogs_learn=explogs_learn,
                              explogs_test=explogs_test, agents=agents, robots=robots)
        
     