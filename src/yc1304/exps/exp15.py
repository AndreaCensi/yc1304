from . import CampaignCmd
from quickapp import QuickApp
import warnings


        
class Exp15(CampaignCmd, QuickApp):
    """ Trying with landroid """
    
    cmd = 'exp15'
    
    comment = """ 
        
    """
    id_robot = 'exp15_ldr_tt_h'
    id_adapter = 'ldr_tt_h'
    
    agents = ['exp15_bdser_s1']
    
    # warnings.warn('only one log')
         
    explogs_learn = ['logger_2011-07-27-11-03-04']
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        rs2b_config = self.get_rs2b_config()
        
        all_logs = rs2b_config.explogs.keys()
        explogs_landroid = [x for x in all_logs if 'logger' in x]
        
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_convert(context, boot_root, Exp15.id_adapter)
        recipe_agent_learn(context, data_central, explogs_landroid)
        jobs_servo_field_agents(context, id_robot=Exp15.id_robot,
                         agents=Exp15.agents, episodes=Exp15.explogs_test)
        jobs_publish_learning(context, Exp15.agents, id_robot=Exp15.id_robot)
        
