from . import CampaignCmd
from quickapp import QuickApp
from yc1304.exps import good_logs_cf
from yc1304.exps.exp_utils import (iterate_context_episodes,
    iterate_context_explogs)
 
class Exp11(CampaignCmd, QuickApp):
    """ Let's try with luminance  """
    
    cmd = 'exp11'
    
    comment = """ 
        kind of works for learning
    """
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        id_agent = 'exp10_bdser1'
        
        id_robot = 'uA_b1_tw_cf'
        id_adapter = 'uA_b1_tw_cf'
        explogs_learn = good_logs_cf
        explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']
        
        explogs_convert = explogs_learn + explogs_test
        for c, id_explog in iterate_context_explogs(context, explogs_convert):
            c.subtask(RS2BConvertOne,
                        boot_root=self.get_boot_root(),
                        id_explog=id_explog,
                        id_adapter=id_adapter,
                        id_robot=id_robot)
         
        context.checkpoint('conversion')

        context.subtask(LearnLog, agent=id_agent, robot=id_robot, interval_publish=5000)

        context.checkpoint('learning')
        
        context.subtask(PublishLearningResult, agent=id_agent, robot=id_robot)

         
        test_episodes = explogs_test
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default', id_episode=id_episode)
 
