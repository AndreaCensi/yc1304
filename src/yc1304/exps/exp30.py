from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import  recipe_agentlearn_by_parallel
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.s10_servo_field import jobs_servo_field_agents
from quickapp_boot import jobs_publish_learning_agents
from yc1304.exps import good_logs_hokuyos
from quickapp_boot.jobs.jobs_publish import jobs_publish_learning_agents_robots

__all__ = ['Exp30']

class Exp30(CampaignCmd, QuickApp):
    """ Checking whether servo really works """
    
    cmd = 'exp30'
    
    comment = """ 
        
    """
    
    robots = ['unicornA_tw1_hlhr_sane_s4']

    agents = ['exp30_bdser_so', 'exp30_bdser_ss',
              'exp30_bdser_sn',  # robust, L2
              'exp30_bdser_sn1'  # robust, L1
              ]
             
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08',  # convex environment
        'unicornA_lab_grid_2013-06-01-21-00-47',  # non-convex environment 1
        'unicornA_lab_grid_2013-06-01-21-04-51',  # non-convex environment 2
        'unicornA_lab_gridth_2013-06-01-21-11-15'  # pure rotation on theta
        ]
    explogs_learn = list(set(good_logs_hokuyos))
    
    explogs_convert = []
    explogs_convert.extend(explogs_test) 
    explogs_convert.extend(explogs_learn)

    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        agents = Exp30.agents
        robots = Exp30.robots
        explogs_learn = Exp30.explogs_learn
        explogs_test = Exp30.explogs_test
        
        recipe_agentlearn_by_parallel(context, data_central, explogs_learn)

        for id_robot in robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)
            
            jobs_servo_field_agents(context, id_robot=id_robot,
                                    agents=agents, episodes=explogs_test)
        
        jobs_publish_learning_agents_robots(context, boot_root, agents, robots)
