from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel,
    jobs_publish_learning_agents_robots)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.exps import good_logs_hokuyos
from yc1304.s10_servo_field import jobs_servo_field_agents


__all__ = ['Exp31']


class Exp31(CampaignCmd, QuickApp):
    """ Now checking without removing the bad ones """
    
    cmd = 'exp31'
    
    comment = """ 
        
    """
    
    robots = [
        'unicornA_tw1_hlhr_s4',
        'unicornA_tw1_hl_s4'
    ]

    agents = [
        'exp30_bdser_nograd',  # does not penalize gradients
    ]
             
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08',  # convex environment
        'unicornA_lab_grid_2013-06-01-21-00-47',  # non-convex environment 1
        'unicornA_lab_grid_2013-06-01-21-04-51',  # non-convex environment 2
        'unicornA_lab_gridth_2013-06-01-21-11-15'  # pure rotation on theta
    ]

    logs_exp10 = [
        'unicornA_base1_2013-04-03-13-30-28',  # :  38m, nominal, ok
        'unicornA_car1_2013-04-08-21-37-47',  # :  ??m, nominal
        'unicornA_tran1_2013-04-09-14-35-11',  # :  ??min, nominal
        'unicornA_base1_2013-04-02-20-37-43',  # :  37m, nominal, boxes
        'unicornA_base1_2013-04-08-19-10-12',  # :  15m, has occlusions for camera
        'unicornA_base1_2013-04-03-12-58-11',  # :  17m, nominal, boxes
        'unicornA_base1_2013-04-08-16-43-10',  # :  25m, gripper not properly placed
        'unicornA_base1_2013-04-06-15-30-06',  # :  6m, nominal
        'unicornA_base1_2013-04-03-16-36-03',  # :  17m, nominal, ends for under-voltage
    ]
    explogs_learn = list(set(good_logs_hokuyos + logs_exp10))
    
    explogs_convert = []
    explogs_convert.extend(explogs_test) 
    explogs_convert.extend(explogs_learn)

    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        agents = Exp31.agents
        robots = Exp31.robots
        explogs_learn = Exp31.explogs_learn
        explogs_test = Exp31.explogs_test
        
        recipe_agentlearn_by_parallel(context, data_central, explogs_learn)

        for id_robot in robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)
            
            jobs_servo_field_agents(context, id_robot=id_robot,
                                    agents=agents, episodes=explogs_test)
        
        jobs_publish_learning_agents_robots(context, boot_root, agents, robots)
