from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import recipe_agentlearn_by_parallel, jobs_publish_learning
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.exps.exp_utils import iterate_context_episodes
from yc1304.s10_servo_field.apps import jobs_servo_field


class Exp10(CampaignCmd, QuickApp):
    """ Let's try again with theta """
    
    cmd = 'exp10'
    
    comment = """ 

    """

    id_agent = 'exp10_bdser1'
    id_robot = 'exp10_uA_b1_tw_hlhr_s4'
    
    explogs_learn = [
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
    
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08'
    ]
    
    def define_options(self, params):
        pass
 
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()   
        data_central = self.get_data_central()
        
        id_robot = Exp10.id_robot
        id_agent = Exp10.id_agent

        # conversion 
        recipe_episodeready_by_convert2(context, boot_root, Exp10.id_robot)
        
        # learning
        recipe_agentlearn_by_parallel(context, data_central, Exp10.explogs_learn)
        
        # Everything before needs to be done before we do the rest
        context.checkpoint('learning')
        
        jobs_publish_learning(context, boot_root=boot_root,
                              id_agent=id_agent, id_robot=id_robot)

        for c, id_episode in iterate_context_episodes(context, Exp10.explogs_test):
            jobs_servo_field(context=c, id_agent=id_agent, id_robot=id_robot,
                             id_episode=id_episode)
            

