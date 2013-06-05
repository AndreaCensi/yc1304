from . import CampaignCmd
from quickapp import QuickApp

__all__ = ['Exp19']

 
class Exp19(CampaignCmd, QuickApp):
    """ Trying to convert new ldr logs """
    
    cmd = 'exp19'
    
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
        
            
      
