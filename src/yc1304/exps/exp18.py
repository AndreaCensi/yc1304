from . import CampaignCmd, campaign_sub
from bootstrapping_olympics import get_boot_config
from quickapp import QuickApp, ResourceManager
from rosstream2boot.programs import RS2BConvert2
from yc1304.exps.exp15 import (recipe_agent_learn, jobs_servo_field,
    jobs_publish_learning)


def recipe_convert3(context, boot_root, id_robot):
    """
    
        Provides episode-ready.
    """
    my_id_robot = id_robot
    
    def rp_convert(c, id_robot, id_episode):
        if my_id_robot != id_robot:
            msg = ('I only know how to create %r, not %r.' % 
                   (my_id_robot, id_robot))
            raise ResourceManager.CannotProvide(msg)
        id_explog = id_episode
        boot_config = get_boot_config()
        boot_config.robots.instance(id_robot)
        return c.subtask(RS2BConvert2,
                           boot_root=boot_root,
                           id_explog=id_explog,
                           id_robot=id_robot,
                           id_robot_res=id_robot,
                           add_job_prefix='')
    
    rm = context.get_resource_manager()        
    rm.set_resource_provider('episode-ready', rp_convert)
    
    
@campaign_sub
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
        rs2b_config = self.get_rs2b_config()
        
        all_logs = rs2b_config.explogs.keys()
        explogs_landroid = [x for x in all_logs if 'logger' in x]
        
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        recipe_convert3(context, boot_root, id_robot=Exp18.id_robot)
        recipe_agent_learn(context, data_central, explogs_landroid)
        jobs_servo_field(context, id_robot=Exp18.id_robot,
                         agents=Exp18.agents, episodes=Exp18.explogs_test)
        jobs_publish_learning(context, Exp18.agents, id_robot=Exp18.id_robot)
        
            
      
