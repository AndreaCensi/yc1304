from quickapp import QuickApp
from yc1304.exps import CampaignCmd
from yc1304.exps.exp_utils import jobs_learnp_and_servo

__all__ = ['Exp08']

class Exp08(CampaignCmd, QuickApp):
    """ Let's try BDSE robustified with range finder """

    cmd = 'exp08'
    
    comment = """ 
        The tensor M looks strange. Also should I normalize with the mean or not?    
        Hey, it actually works --- there was a problem plotting the results.
    """
    
    robots = ['exp05_uA_xy']
    agents = ['exp08_bdser1']
    
    explogs_learn = [
        'unicornA_base1_2013-04-11-20-14-27',
        'unicornA_tran1_2013-04-11-23-21-36',
        'unicornA_tran1_2013-04-12-22-29-16',
        'unicornA_tran1_2013-04-12-22-40-02',
        'unicornA_tran1_2013-04-12-23-34-08'
    ]
    
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08'
    ]
        
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        data_central = self.get_data_central()

        robots = Exp08.robots
        agents = Exp08.agents
        explogs_learn = Exp08.explogs_learn
        explogs_test = Exp08.explogs_test

        jobs_learnp_and_servo(context, data_central, explogs_learn,
                                        explogs_test, agents, robots)
        

