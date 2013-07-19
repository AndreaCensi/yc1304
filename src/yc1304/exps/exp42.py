from .exp40sim import episode_id_exploration
from conf_tools import GlobalConfig
from quickapp import QuickApp
from quickapp_boot import (recipe_episodeready_by_simulation_tranches,
    jobs_publish_learning_agents_robots, recipe_agentlearn_by_parallel)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_hokuyos
 
 
__all__ = ['Exp42']


class Exp42(CampaignCmd, QuickApp): 
     
    cmd = 'exp42'

    explorer = 'expsw1'
    num_episodes = 500
    simulated_episodes = [episode_id_exploration(explorer, i) for i in range(num_episodes)]

    combinations = [
        dict(id_robot='unicornA_tw1_hl_sane_s4', episodes=good_logs_hokuyos),
        dict(id_robot='unicornA_tw1_hlhr_sane_s4', episodes=good_logs_hokuyos),
        dict(id_robot='Se0Vrb1ro', episodes=simulated_episodes),
        dict(id_robot='Se1Vrb1ro', episodes=simulated_episodes),
        dict(id_robot='Se0Vrb1rc', episodes=simulated_episodes),
        dict(id_robot='Se0Vrb1rh', episodes=simulated_episodes),
    ]
    
    robots = list(c['id_robot'] for c in combinations)
    agents = [
      'bdse_e1_ss',
      'exp42_stats',
      'exp42_cond30',
      'stats1'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        boot_root = self.get_boot_root()
        data_central = self.get_data_central()

        # for vehicles
        GlobalConfig.global_load_dir('${B11_SRC}/bvapps/bdse1')
                
        recipe_episodeready_by_convert2(context, boot_root)

        recipe_episodeready_by_simulation_tranches(context, data_central,
                                                   explorer=Exp42.explorer,
                                                   episodes=Exp42.simulated_episodes,
                                                   max_episode_len=30,
                                                   episodes_per_tranche=50)
        
        for c in Exp42.combinations:
            recipe_agentlearn_by_parallel(context, data_central, c['episodes'],
                                          only_robots=[c['id_robot']],
                                          intermediate_reports=False,
                                          episodes_per_tranche=50)

        jobs_publish_learning_agents_robots(context, boot_root,
                                            Exp42.agents, Exp42.robots)
        
            
    
