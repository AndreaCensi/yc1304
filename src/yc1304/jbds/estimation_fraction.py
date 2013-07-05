from quickapp import QuickApp
from yc1304.campaign import CampaignCmd
from yc1304.jbds.estimation import JBDSEstimation, jobs_learn_real, jobs_servo 
from yc1304.jbds.estimation_summaries import (job_report_learn,
    jobs_report_summary_servo_xy)


__all__ = ['JBDSEstimationFraction']


class JBDSEstimationFraction(CampaignCmd, QuickApp):
    """ Estimation/servo figures with fraction of learned samples """
    
    cmd = 'jbds-estimation-fraction'
    
    patterns = [
        "%s_f001",
        "%s_f002",
        "%s_f003",
        "%s_f004",
        "%s_f005",
#         "%s_f006",
#         "%s_f007",
#         "%s_f008",
#         "%s_f009",
        "%s_f010",
#         "%s_f020",
#         "%s_f030",
#         "%s_f040",
        "%s_f050",
#         "%s_f060",
#         "%s_f070",
#         "%s_f080",
#         "%s_f090",
        "%s_f100",
#         "%s_f200",
#         "%s_f300",
#         "%s_f400",
        "%s_f500",
#         "%s_f600",
#         "%s_f700",
#         "%s_f800",
#         "%s_f900",
        "%s_f990"          
    ] 
    
    robots = ['unicornA_tr1_hlhr_sane_s4', 'unicornA_tr1_fs1']
    combs_servo_xy = []
    
    for robot, agent in JBDSEstimation.combs_servo_xy:
        if not robot in robots:
            print('skipping %s' % robot)
            continue
        
        for p in patterns:
            agent2 = p % agent
            combs_servo_xy.append((robot, agent2)) 
    
#     combs_servo_xy.extend([(robot, agent) 
#                           for robot, agent in itertools.product(robots, agents)])
#      
        
    grids_xy = JBDSEstimation.grids_xy
    explogs_learn = JBDSEstimation.explogs_learn
    

    def define_options(self, options):
        pass 

    def define_jobs_context(self, context):
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('jbds-estfr')
        data_central = self.get_data_central()
        
        jobs_learn_real(context, data_central,
                        real_robots=JBDSEstimationFraction.robots,
                        explogs_learn=JBDSEstimationFraction.explogs_learn)
         
        r = job_report_learn(context, JBDSEstimationFraction.combs_servo_xy)
        context.add_report(r, 'learn_global')
 
        # jobs_tex(context, JBDSEstimationFraction.combs_servo_xy)
 
        jobs_servo(context, data_central,
                   combinations=JBDSEstimationFraction.combs_servo_xy,
                   explogs_test=JBDSEstimationFraction.grids_xy)
         
        jobs_report_summary_servo_xy(context,
                           combinations=JBDSEstimationFraction.combs_servo_xy,
                           explogs_test=JBDSEstimationFraction.grids_xy)


