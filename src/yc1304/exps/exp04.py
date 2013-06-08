from . import CampaignCmd
from quickapp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from yc1304.exps.exp_utils import iterate_context_episodes


class Exp04(CampaignCmd, QuickApp):
    """ Let's see what happens with changing rcond """
    
    cmd = 'exp04'
    
    
    comment = """ The problem was that we were looking at the xy plane only. """
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        
        # id_adapter = 'unicornA_base1_tw_hlhr_sane_s4'
        
        id_agent = 'exp04_bdse1'
        id_robot = 'exp03_uA_tran'
        id_convert_job = 'exp03_uA_tran'
        # variation = 'default'
          
        jobs_convert = self.call_recursive(context, 'convert',
                       RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                              '--dummy',
                              
                              'convert',
                              '--boot_root', self.get_boot_root(),
                              '--jobs', id_convert_job,
                              ])
 
        jobs_learn = context.subtask(LearnLog,
                                     agent=id_agent, robot=id_robot,
                                     interval_publish=5000,
                                     extra_dep=jobs_convert.all_jobs())

        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
        
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default',
                                  id_episode=id_episode,
                        extra_dep=jobs_learn.all_jobs())
 
