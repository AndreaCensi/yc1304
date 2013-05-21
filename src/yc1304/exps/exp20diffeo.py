from quickapp import QuickApp
from yc1304.campaign import CampaignCmd
from yc1304.exps.exp15 import recipe_agent_learn, jobs_publish_learning
from yc1304.exps.exp18 import recipe_convert3
from yc1304.exps import good_logs_cf
 
class Exp20(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Trying with top camera """
     
    cmd = 'exp20'

    comment = """ 
        
    """
    
    id_robot = 'exp20_unicornA_ceil'

    explogs_learn = good_logs_cf
    explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']    
    explogs_convert = explogs_learn + explogs_test
        
    agents = ['exp20_bdser_s1']
             
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_convert3(context, boot_root, id_robot=Exp20.id_robot)
        recipe_agent_learn(context, data_central, Exp20.explogs_learn)
        
        jobs_publish_learning(context, Exp20.agents, id_robot=Exp20.id_robot)
        
            
    
