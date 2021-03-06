from bootstrapping_olympics import get_boot_config
from quickapp import QuickApp
from quickapp_boot import recipe_agentlearn_by_parallel, jobs_publish_learning
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_cf
 
__all__ = ['Exp20']

class Exp20(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Trying with top camera """
     
    cmd = 'exp20'

    comment = """ 
        
    """
    
    id_robot = 'exp20_unicornA_ceil'

    explogs_learn = good_logs_cf
    explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']    
    explogs_convert = explogs_learn + explogs_test
        
    agents = ['exp20_diffeo', 'exp20_diffeof']
             
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_config = get_boot_config()
        boot_config.agents.instance(Exp20.agents[0])
            
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_episodeready_by_convert2(context, boot_root, id_robot=Exp20.id_robot)
        recipe_agentlearn_by_parallel(context, data_central, Exp20.explogs_learn)
        jobs_publish_learning(context, Exp20.agents, id_robot=Exp20.id_robot)
        
            
    
