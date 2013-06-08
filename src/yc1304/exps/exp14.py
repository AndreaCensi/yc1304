from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import (iterate_context_agents_and_episodes,
    jobs_publish_learning_agents, recipe_agentlearn_by_parallel)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.exps import good_logs_cf
from yc1304.s10_servo_field import jobs_servo_field
import warnings


class Exp14(CampaignCmd, QuickApp):
    """ Cleaning up servo interface """
    cmd = 'exp14'
    
    comment = """ 
        
    """
    
    id_robot = 'exp14_uA_b1_xy_cf_strip'
    id_adapter = 'uA_b1_xy_cf_strip'
    agents = ['exp14_bdser_s1', 'exp14_bdser_s2', 'exp14_bdser_s3']
    
    warnings.warn('only one log')
         
    explogs_learn = good_logs_cf
    explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']
    
    def define_options(self, params):
        pass
     
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()   
        data_central = self.get_data_central()
        
        id_robot = Exp14.id_robot
        agents = Exp14.agents

        # conversion 
        recipe_episodeready_by_convert2(context, boot_root, id_robot)
        
        # learning
        recipe_agentlearn_by_parallel(context, data_central, Exp14.explogs_learn)
                                     
        jobs_publish_learning_agents(context, boot_root=boot_root,
                                    agents=agents, id_robot=id_robot)
        
        cases = iterate_context_agents_and_episodes(context, agents,
                                                    Exp14.explogs_test)
        for c, id_agent, id_episode in cases:
            jobs_servo_field(context=c, id_agent=id_agent, id_robot=id_robot,
                             id_episode=id_episode)
            
                    
        
