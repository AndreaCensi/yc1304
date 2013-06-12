from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import recipe_agentlearn_by_parallel, jobs_publish_learning
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.exps.exp_utils import jobs_learnp_and_servo
  

class Exp10(CampaignCmd, QuickApp):
    """ Let's try again with theta """
    
    cmd = 'exp10'
    
    comment = """ 

    """

    agents = ['exp10_bdser1']
    robots = ['exp10_uA_b1_tw_hlhr_s4']
    
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
        data_central = self.get_data_central()

        robots = Exp10.robots
        agents = Exp10.agents
        explogs_learn = Exp10.explogs_learn
        explogs_test = Exp10.explogs_test

        jobs_learnp_and_servo(context, data_central, explogs_learn,
                                        explogs_test, agents, robots)
        

