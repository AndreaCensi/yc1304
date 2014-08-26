from . import CampaignCmd
from boot_reports.latex.jbds.jobs import job_tex_report
from conf_tools import GlobalConfig
from contracts import contract
from quickapp import QuickApp, iterate_context_names_pair
from quickapp_boot.jobs.jobs_publish import jobs_publish_learning_agents_robots
from quickapp_boot.jobs.jobs_simulation import recipe_episodeready_by_simulation
from quickapp_boot.recipes.recipes_learning_parallel import (
    recipe_agentlearn_by_parallel)
import os


__all__ = ['Exp40']


class Exp40(CampaignCmd, QuickApp):
    """ Trying to run simulations """
    
    cmd = 'exp40'
    
    comment = """ 
        
    """
    
    sets = ['bv1bds1']
    config_dir = '${B11_SRC}/bvapps/bdse1'
    explorer = 'expsw1'
 
    robots = [
        # Base cases
        # Se0Vt1cc, 
#         'Se0Vci1cc',
#         'Se0Vci1rc',
        'Se0Vrb1ro',
#         'Se0Vrb1co',
#         'Yfl1Se0Vrb1fsq1',
        # Different environment
        # Se1Vt1cc,
#         'Se1Vci1cc',
#         'Se1Vci1rc',
#         # With smoothing
#         'Se0Vci1s1cc',
#         'Se0Vci1s1cic',  # irregular sampling
#         'Se0Vci1s2cc',
#         'Se0Vci1s4cc',
#         'Se0Vci1s8cc'
    ]   
    
    agents = [
        'bdse_e1_ss'
    ]
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        GlobalConfig.global_load_dir(Exp40.config_dir)
    
        robots = Exp40.robots
        agents = Exp40.agents
        explorer = Exp40.explorer
        num_episodes = 2
        max_episode_len = 5
        data_central = self.get_data_central()
        boot_root = data_central.get_boot_root()

        episodes = [episode_id_exploration(explorer, i) for i in range(num_episodes)]
        
        for id_robot in robots:
            recipe_episodeready_by_simulation(context, data_central, id_robot,
                                              explorer, max_episode_len)

        recipe_agentlearn_by_parallel(context, data_central, episodes)
   
        jobs_publish_learning_agents_robots(context, boot_root, agents, robots)

 
        output_dir = os.path.join(context.get_output_dir(), 'tex')
        
        for c, id_agent, id_robot in iterate_context_names_pair(context, agents, robots):
            job_tex_report(c, output_dir, id_agent=id_agent, id_robot=id_robot)
            


@contract(id_agent='str', K='int')
def episode_id_exploration(id_agent, K):
    return 'ep_expl_%s_%05d' % (id_agent, K)






