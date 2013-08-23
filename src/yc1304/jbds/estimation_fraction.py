from .estimation import JBDSEstimation, jobs_learn_real, jobs_servo
from .estimation_summaries import job_report_learn, jobs_report_summary_servo_xy
from quickapp import QuickApp
from yc1304.campaign import CampaignCmd


__all__ = ['JBDSEstimationFraction']


class JBDSEstimationFraction(CampaignCmd, QuickApp):
    """ Estimation/servo figures with fraction of learned samples """
    
    cmd = 'jbds-estimation-fraction'
    
    patterns = [
#         "%s_f00001",
#         "%s_f00002",
        "%s_f00003",
        "%s_f00004",
        "%s_f00005",
        "%s_f00007",
        "%s_f0001",
        "%s_f0002",
        "%s_f0003",
        "%s_f001",
        "%s_f002",
        "%s_f003",
        "%s_f0031",
        "%s_f0032",
        "%s_f0033",
        "%s_f0034",
        "%s_f0035",
        "%s_f0036",
        "%s_f0037",
        "%s_f0038",
        "%s_f0039",
        "%s_f004",
        "%s_f005",
        "%s_f010",
        "%s_f100",
        "%s_f500",
        "%s_f990"          
    ] 
    
    robots = ['unicornA_tr1_hlhr_sane_s4']  # , 'unicornA_tr1_fs1']
    combs_servo_xy = []
    
    for robot, agent in JBDSEstimation.combs_servo_xy:
        if not robot in robots:
            # print('skipping %s' % robot)
            continue
        
        for p in patterns:
            agent2 = p % agent
            combs_servo_xy.append((robot, agent2)) 
    
#     combs_servo_xy.extend([(robot, agent) 
#                           for robot, agent in itertools.product(robots, agents)])
#      
        
    grids_xy = JBDSEstimation.grids_xy
    unicorn_explogs_learn = JBDSEstimation.unicorn_explogs_learn
    

    def define_options(self, options):
        pass 

    def define_jobs_context(self, context):
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('jbds-estfr')
        data_central = self.get_data_central()
        
        jobs_learn_real(context, data_central,
                        real_robots=JBDSEstimationFraction.robots,
                        explogs_learn=JBDSEstimationFraction.unicorn_explogs_learn)
         
        r = job_report_learn(context, JBDSEstimationFraction.combs_servo_xy)
        context.add_report(r, 'learn_global')
 
        # jobs_tex(context, JBDSEstimationFraction.combs_servo_xy)
 
        jobs_servo(context, data_central,
                   combinations=JBDSEstimationFraction.combs_servo_xy,
                   explogs_test=JBDSEstimationFraction.grids_xy)
         
        jobs_report_summary_servo_xy(context,
                           combinations=JBDSEstimationFraction.combs_servo_xy,
                           explogs_test=JBDSEstimationFraction.grids_xy)


