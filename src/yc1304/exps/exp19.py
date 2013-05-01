from . import CampaignCmd, campaign_sub
from quickapp import QuickApp
from yc1304.exps.exp15 import (recipe_agent_learn,
                               jobs_servo_field, jobs_publish_learning)
from yc1304.exps.exp18 import recipe_convert3
 
@campaign_sub
class Exp19(CampaignCmd, QuickApp):
    
    cmd = 'exp19'
    short = """ Trying to convert new ldr logs """
    comment = """ 
        
    """
    
    id_robot = 'ldr21'

    agents = ['exp18_bdser_s1']
             
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        rs2b_config = self.get_rs2b_config()
        
        all_logs = rs2b_config.explogs.keys()
        explogs_landroid = [x for x in all_logs if ('ldr21' in x or 'logger' in x)]
        
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_convert3(context, boot_root, id_robot=Exp19.id_robot)
        recipe_agent_learn(context, data_central, explogs_landroid)
        jobs_servo_field(context, id_robot=Exp19.id_robot,
                         agents=Exp19.agents, episodes=Exp19.explogs_test)
        jobs_publish_learning(context, Exp19.agents, id_robot=Exp19.id_robot)
        
            
      
