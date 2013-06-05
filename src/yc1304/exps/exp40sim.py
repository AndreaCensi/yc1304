from . import CampaignCmd
from quickapp import QuickApp
from quickapp_boot import (recipe_agentlearn_by_parallel,
    jobs_publish_learning_agents_robots)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.exps import good_logs_hokuyos
from yc1304.s10_servo_field import jobs_servo_field_agents
from conf_tools.master import GlobalConfig


__all__ = ['Exp40']


class Exp40(CampaignCmd, QuickApp):
    """ Trying to run simulations """
    
    cmd = 'exp40'
    
    comment = """ 
        
    """
    
    sets = ['bv1bds1']
    config_dir = '${B11_SRC}/bvapps/bdse1'

    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        GlobalConfig.global_load_dir(Exp40.config_dir)
        
        
