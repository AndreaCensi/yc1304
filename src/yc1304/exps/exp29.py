from boot_navigation.jobs import jobs_navigation_map
from conf_tools import GlobalConfig
from quickapp import QuickApp, iterate_context_names_pair
from quickapp_boot import recipe_agentlearn_by_parallel
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos


__all__ = ['Exp29']

class Exp29(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ Creates the maps used by exp30, 33  """
     
    cmd = 'exp29'
    
    robots = [
              'unicornA_tw1_hl_sane_s4',
              'unicornA_tw1_hlhr_sane_s4',
              'unicornA_tw1_cf_strip',
              'unicornA_tr1_cf_strip',
              'unicornA_tw1_fs1'
              ]
    
#     explog_episode = 'unicornA_base1_2013-04-02-20-37-43'  # 37m, nominal, boxes
    nmaps = ['unicornA_teleop_nmap_2013-05-31-19-51-24',  # figure 8 translation only
             'unicornA_teleop_nmap_2013-05-31-19-54-07',
             'unicornA_teleop_nmap_2013-06-02-18-25-23',
             'unicornA_teleop_nmap_corner2_2013-06-04-20-29-33',
             'unicornA_teleop_nmap_corner_2013-06-02-20-32-17',
             'unicornA_teleop_nmap_corner2_2013-06-04-21-05-42',
             'unicornA_teleop_nmap_corner3_2013-06-05-21-19-26']
#     explog_episode = 'unicornA_tran1_2013-04-12-22-29-16'
#     explog_episode = 'unicornA_tran1_2013-04-11-23-21-36'  # on grid 
    explogs_convert = []
    explogs_convert.extend(nmaps) 
    
    explogs_learn = list(set(good_logs_hokuyos))
    explogs_convert.extend(explogs_learn)
    
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        GlobalConfig.global_load_dir('default')
        
        recipe_agentlearn_by_parallel(context, data_central, Exp29.explogs_learn)
        
        for id_robot in Exp29.robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)
            
        combinations = iterate_context_names_pair(context, Exp29.nmaps, Exp29.robots)
        for c, id_episode, id_robot in combinations:
            jobs_navigation_map(c,
                                outdir=context.get_output_dir(),
                                data_central=data_central,
                                id_robot=id_robot,
                                id_episode=id_episode)
 


