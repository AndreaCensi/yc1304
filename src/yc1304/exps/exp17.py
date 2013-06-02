from . import CampaignCmd
from quickapp import QuickApp
 

class Exp17(CampaignCmd, QuickApp):
    
    cmd = 'exp17'
    short = """ New interface landroid"""
    comment = """ 
        
    """
    
    id_robot = 'exp17_ldr_tt_h_sane'
    id_adapter = 'ldr_tt_h_sane'

    agents = ['exp16_bdser_s1']
             
    explogs_learn = ['logger_2011-07-27-11-03-04']
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        rs2b_config = self.get_rs2b_config()
        
        all_logs = rs2b_config.explogs.keys()
        explogs_landroid = [x for x in all_logs if 'unicornA' in x]
        
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_convert2(context, boot_root, id_adapter=Exp17.id_adapter, id_robot=Exp17.id_robot)
        recipe_agent_learn(context, data_central, explogs_landroid)
        jobs_servo_field(context, id_robot=Exp17.id_robot,
                         agents=Exp17.agents, episodes=Exp17.explogs_test)
        jobs_publish_learning(context, Exp17.agents, id_robot=Exp17.id_robot)
        
            
      
