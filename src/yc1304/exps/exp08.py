from quickapp import QuickApp
from quickapp_boot import recipe_agentlearn_by_parallel
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.exps import iterate_context_episodes, CampaignCmd
from yc1304.s10_servo_field import jobs_servo_field

__all__ = ['Exp08']

class Exp08(CampaignCmd, QuickApp):
    """ Let's try BDSE robustified with range finder """

    cmd = 'exp08'
    
    comment = """ 
        The tensor M looks strange. Also should I normalize with the mean or not?    
        Hey, it actually works --- there was a problem plotting the results.
    """
    
    id_robot = 'exp05_uA_xy'
    id_agent = 'exp08_bdser1'
    
    explogs_learn = [
        'unicornA_base1_2013-04-11-20-14-27',
        'unicornA_tran1_2013-04-11-23-21-36',
        'unicornA_tran1_2013-04-12-22-29-16',
        'unicornA_tran1_2013-04-12-22-40-02',
        'unicornA_tran1_2013-04-12-23-34-08'
    ]
    
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08'
    ]
        
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()   
        data_central = self.get_data_central()
        
        # conversion 
        recipe_episodeready_by_convert2(context, boot_root, Exp08.id_robot)
        
        # learning
        recipe_agentlearn_by_parallel(context, data_central, Exp08.explogs_learn)
        
        # Everything before needs to be done before we do the rest
        context.checkpoint('learning')
        
        id_robot = Exp08.id_robot
        id_agent = Exp08.id_agent
        
        for c, id_episode in iterate_context_episodes(context, Exp08.explogs_test):
            jobs_servo_field(context=c, id_agent=id_agent, id_robot=id_robot,
                             id_episode=id_episode)
            

        

