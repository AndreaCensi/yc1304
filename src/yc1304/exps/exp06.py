from quickapp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from . import CampaignCmd
from yc1304.exps.exp_utils import iterate_context_episodes

class Exp06(CampaignCmd, QuickApp):
    """ Let's try BGDS """
    cmd = 'exp06'
    
    comment = """ Still need to implement servo """

    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        id_agent = 'exp06_bgds1'
        
        id_robot = 'exp05_uA_xy'
        id_convert_job = 'exp05_uA_xy'
          
        jobs_convert = self.call_recursive(context, 'convert',
                       RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                              '--dummy',
                              
                              'convert',
                              '--boot_root', self.get_boot_root(),
                              '--jobs', id_convert_job,
                              ])
 
        jobs_learn = context.subtask(LearnLog, agent=id_agent, robot=id_robot, interval_publish=5000,
                                     extra_dep=jobs_convert.all_jobs())

        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
        
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default',
                                  id_episode=id_episode,
                        extra_dep=jobs_learn.all_jobs())
 
