from . import CampaignCmd, campaign_sub
from quickapp import QuickApp
from .exp14 import jobs_parallel_learning
from .exp_utils import (iterate_context_agents_and_episodes,
    iterate_context_agents)
from yc1304.s03_learning.log_learn import PublishLearningResult
from yc1304.s10_servo_field.apps import ServoField
import warnings
from rosstream2boot.config.rbconfig import get_rs2b_config


def recipe_convert(context, boot_root, id_adapter):
    """
    
        provides episode-ready
    """
    def rp_convert(c, id_robot, id_episode):
        id_explog = id_episode
        rs2b_config = get_rs2b_config()
        rs2b_config.adapters[id_adapter]
        return c.subtask(RS2BConvertOne,
                           boot_root=boot_root,
                           id_explog=id_explog,
                           id_adapter=id_adapter,
                           id_robot=id_robot,
                           add_job_prefix='')
    
    rm = context.get_resource_manager()        
    rm.set_resource_provider('episode-ready', rp_convert)


def recipe_agent_learn(context, data_central, episodes):
    """
        agent-learn (id_agent, id_robot)
        
        learns all episodes for the robot in the db
    """

    rm = context.get_resource_manager()
    
    def rp_learn(context, id_agent, id_robot):
        return jobs_parallel_learning(context, data_central,
                                      id_agent, id_robot, episodes)
    rm.set_resource_provider('agent-learn', rp_learn)
    
def jobs_publish_learning(context, agents, id_robot):
    for c, id_agent in iterate_context_agents(context, agents):
        c.needs('agent-learn', id_agent=id_agent, id_robot=id_robot)        
        c.subtask(PublishLearningResult, agent=id_agent, robot=id_robot)

def jobs_servo_field(context, id_robot, agents, episodes):
    cases = iterate_context_agents_and_episodes(context, agents, episodes)
    for c, id_agent, id_episode in cases:
        c.needs('agent-learn', id_agent=id_agent, id_robot=id_robot)
        c.needs('episode-ready', id_robot=id_robot, id_episode=id_episode)
        c.subtask(ServoField, id_robot=id_robot,
                  id_agent=id_agent, id_episode=id_episode)
     
        
@campaign_sub
class Exp15(CampaignCmd, QuickApp):
    
    cmd = 'exp15'
    short = """ Trying with landroid """
    comment = """ 
        
    """
    id_robot = 'exp15_ldr_tt_h'
    id_adapter = 'ldr_tt_h'
    
    agents = ['exp15_bdser_s1']
    
    warnings.warn('only one log')
         
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
        jobs_servo_field(context, id_robot=Exp15.id_robot,
                         agents=Exp15.agents, episodes=Exp15.explogs_test)
        jobs_publish_learning(context, Exp15.agents, id_robot=Exp15.id_robot)
        
