from . import CampaignCmd, campaign_sub
from quickapp import QuickApp
from rosstream2boot.programs import RS2BConvertOne
from .exp14 import jobs_parallel_learning
from .exp_utils import (iterate_context_agents_and_episodes,
    iterate_context_agents)
from yc1304.s03_learning.log_learn import PublishLearningResult
from yc1304.s10_servo_field.apps import ServoField
import warnings

        
@campaign_sub
class Exp16(CampaignCmd, QuickApp):
    
    cmd = 'exp16'
    short = """ Trying with landroid """
    comment = """ 
        
    """
    
    robot2adapter = {'Exp16_ldr_tt_h': 'Exp16_ldr_tt_h',
                     'Exp16_ldr_tt_h_sane': 'Exp16_ldr_tt_h_sane'}

    agents = ['Exp16_bdser_s1']
             
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
        
            
      
