from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import  recipe_agentlearn_by_parallel
from rosstream2boot import get_rs2b_config, recipe_episodeready_by_convert2
from yc1304.s10_servo_field import jobs_servo_field_agents
from quickapp_boot.jobs import jobs_publish_learning_agents

__all__ = ['Exp18']

class Exp18(CampaignCmd, QuickApp):
    
    cmd = 'exp18'
    short = """ Trying ROSRobot """
    comment = """ 
        
    """
    
    id_robot = 'ldr_xt_h_sane'

    agents = ['exp18_bdser_s1']
             
    explogs_test = []
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        rs2b_config = get_rs2b_config()
        
        all_logs = rs2b_config.explogs.keys()
        explogs_landroid = [x for x in all_logs if 'logger' in x]
        
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_episodeready_by_convert2(context, boot_root, id_robot=Exp18.id_robot)
        recipe_agentlearn_by_parallel(context, data_central, explogs_landroid)
        jobs_servo_field_agents(context, id_robot=Exp18.id_robot,
                         agents=Exp18.agents, episodes=Exp18.explogs_test)
        jobs_publish_learning_agents(context=context, boot_root=boot_root,
                                     agents=Exp18.agents, id_robot=Exp18.id_robot)
        
            
      
