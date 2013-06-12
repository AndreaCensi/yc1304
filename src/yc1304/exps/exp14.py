from . import CampaignCmd
from quickapp import QuickApp
from yc1304.exps import good_logs_cf
from yc1304.exps.exp_utils import jobs_learnp_and_servo
import warnings


class Exp14(CampaignCmd, QuickApp):
    """ Cleaning up servo interface """
    cmd = 'exp14'
    
    comment = """ 
        
    """
    
    robots = ['exp14_uA_b1_xy_cf_strip']
    agents = ['exp14_bdser_s1', 'exp14_bdser_s2', 'exp14_bdser_s3']
    
    warnings.warn('only one log')
         
    explogs_learn = good_logs_cf
    explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']
    
    def define_options(self, params):
        pass
        
    def define_jobs_context(self, context):
        data_central = self.get_data_central()

        robots = Exp14.robots
        agents = Exp14.agents
        explogs_learn = Exp14.explogs_learn
        explogs_test = Exp14.explogs_test

        jobs_learnp_and_servo(context, data_central, explogs_learn,
                                        explogs_test, agents, robots)
        

              
        
