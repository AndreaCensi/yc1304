from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from . import CampaignCmd, campaign_sub
from yc1304.s03_learning.log_learn import LearnLog
from yc1304.s10_servo_field.apps import ServoField
from yc1304.exps.exp_utils import iterate_context_episodes

@campaign_sub
class Exp08(CampaignCmd, QuickApp):
    
    cmd = 'exp08'
    short = """ Let's try BDSE robustified """
    comment = """ 
        The tensor M looks strange. Also should I normalize with the mean or not?
        
        
        Hey, it actually works --- there was a problem plotting the results.
    """

    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        id_agent = 'exp08_bdser1'
        
        id_robot = 'exp05_uA_xy'
        id_convert_job = 'exp05_uA_xy'
          
        self.call_recursive(context, 'convert',
                       RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                              '--dummy',
                              
                              'convert',
                              '--boot_root', self.get_boot_root(),
                              '--jobs', id_convert_job,
                              ])
        
        # Everything before needs to be done before we do the rest
        context.checkpoint('conversion')
        
        context.subtask(LearnLog, agent=id_agent, robot=id_robot, interval_publish=5000)


        # Everything before needs to be done before we do the rest
        context.checkpoint('learning')
        
        
        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
        
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default', id_episode=id_episode)
 
