from . import CampaignCmd
from quickapp import QuickApp

from yc1304.exps import good_logs_cf
from yc1304.exps.exp_utils import (iterate_context_episodes,
    iterate_context_explogs)
from yc1304.s10_servo_field.apps import ServoField



class Exp12(CampaignCmd, QuickApp):
    """ Parallel learning """
    
    cmd = 'exp12'
    
    comment = """ 

    """
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        id_agent = 'exp10_bdser1'
        
        id_robot = 'exp12_uA_b1_tw_cf'
        id_adapter = 'uA_b1_tw_cf'
        
        explogs_learn = good_logs_cf
        explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']        
        explogs_convert = explogs_learn + explogs_test

        agent = None
        for c, id_explog in iterate_context_explogs(context, explogs_convert):
            episodes = c.subtask(RS2BConvertOne,
                                   boot_root=self.get_boot_root(),
                                   id_explog=id_explog,
                                   id_adapter=id_adapter,
                                   id_robot=id_robot)
        
            if id_explog in explogs_learn:
                agent_i = c.subtask(LearnLogNoSave, agent=id_agent, robot=id_robot,
                                    episodes=episodes)
                if agent is None:
                    agent = agent_i
                else:
                    agent = context.comp(merge_agents, agent, agent_i) 
            
        id_episodes = explogs_learn
        data_central = self.get_data_central()
        context.comp(save_state, data_central, id_agent, id_robot, agent, id_episodes)
            

        context.checkpoint('learning')
        
        context.subtask(PublishLearningResult, agent=id_agent, robot=id_robot)

         
        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
         
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default', id_episode=id_episode)
 
