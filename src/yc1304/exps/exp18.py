from . import CampaignCmd
from quickapp import QuickApp
from rosstream2boot.configuration import get_conftools_explogs
from yc1304.exps.exp_utils import jobs_learnp_and_servo

__all__ = ['Exp18']

class Exp18(CampaignCmd, QuickApp):
    """ Trying ROSRobot """
    
    cmd = 'exp18'
    
    comment = """ 
        
    """
    
    robots = ['ldr_xt_h_sane']

    agents = ['exp18_bdser_s1']
             
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        data_central = self.get_data_central()

        all_logs = get_conftools_explogs().keys()
        explogs_landroid = [x for x in all_logs if 'logger' in x]

        robots = Exp18.robots
        agents = Exp18.agents
        explogs_learn = explogs_landroid
        explogs_test = Exp18.explogs_test

        jobs_learnp_and_servo(context, data_central, explogs_learn,
                                        explogs_test, agents, robots)
        

