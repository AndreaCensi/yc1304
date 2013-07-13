from conf_tools import GlobalConfig
from quickapp import QuickApp
from rosstream2boot.configuration import get_conftools_explogs
from yc1304.campaign import CampaignCmd
from yc1304.exps.exp_utils import iterate_context_explogs, jobs_learn_parallel
 
__all__ = ['UZHTurtleStats']


class UZHTurtleStats(CampaignCmd, QuickApp):
    """ 
        Simple statistics about the UZH Turtlebot data. 
    
        Uses environment variable DATASET_UZHTURTLE for linking to the 
        directory.
        
    """
    
    cmd = 'uzh-turtle-stats'
    
    def define_options(self, options):
        pass 

    def define_jobs_context(self, context):
        from pkg_resources import resource_filename  # @UnresolvedImport
        config_dir = resource_filename("yc1304.uzhturtle", "config")
        
        GlobalConfig.global_load_dir(config_dir)
        GlobalConfig.global_load_dir('${DATASET_UZHTURTLE}')
        
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('uzh-turtle-stats')

        data_central = self.get_data_central()
        
        logs = list(self.get_explogs_by_tag('uzhturtle'))
        agents = ['stats2', 'bdse_e1_ss']
        robots = ['uzhturtle_un1_cf1', 'uzhturtle_un1_cf1_third']


        for c, id_explog in iterate_context_explogs(context, logs):
            explog = get_conftools_explogs().instance(id_explog)

            print id_explog, explog

        jobs_learn_parallel(context,
                            data_central=data_central,
                            explogs_learn=logs,
                            agents=agents, robots=robots,
                            episodes_per_tranche=2)





