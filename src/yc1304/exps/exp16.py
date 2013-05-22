from . import CampaignCmd
from quickapp import QuickApp

__all__ = ['Exp16']

class Exp16(CampaignCmd, QuickApp):
    
    cmd = 'exp16'
    short = """ Trying with landroid, only sane """
    comment = """ 
        
    """
    
    id_robot = 'exp16_ldr_tt_h_sane'
    id_adapter = 'ldr_tt_h_sane'

    agents = ['exp16_bdser_s1']
             
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

        recipe_convert(context, boot_root, Exp16.id_adapter)
        recipe_agent_learn(context, data_central, explogs_landroid)
        jobs_servo_field(context, id_robot=Exp16.id_robot,
                         agents=Exp16.agents, episodes=Exp16.explogs_test)
        jobs_publish_learning(context, Exp16.agents, id_robot=Exp16.id_robot)
        
            
      
