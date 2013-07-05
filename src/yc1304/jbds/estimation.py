from boot_reports.latex.jbds.jobs import job_tex_report
from conf_tools import GlobalConfig
from quickapp import iterate_context_names, QuickApp
from quickapp_boot import (recipe_episodeready_by_simulation_tranches,
    recipe_agentlearn_by_parallel, recipe_agent_servo)
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.exps.exp40sim import episode_id_exploration
from yc1304.jbds.estimation_summaries import (job_report_learn,
    iterate_context_combinations, jobs_report_summary_servo_xy,
    report_summary_servo_theta)
from yc1304.s10_servo_field.jobs import jobs_servo_field
import numpy as np
import os

__all__ = ['JBDSEstimation']


class JBDSEstimation(CampaignCmd, QuickApp):
    """ Estimation figures """
    cmd = 'jbds-estimation-figures'
    
    explogs_learn = [
        'unicornA_base1_2013-04-03-13-30-28',  # :  38m, nominal, ok
        'unicornA_car1_2013-04-08-21-37-47',  # :  ??m, nominal
        'unicornA_tran1_2013-04-09-14-35-11',  # :  ??min, nominal
        'unicornA_base1_2013-04-02-20-37-43',  # :  37m, nominal, boxes
        'unicornA_base1_2013-04-08-19-10-12',  # :  15m, has occlusions for camera
        'unicornA_base1_2013-04-03-12-58-11',  # :  17m, nominal, boxes
        'unicornA_base1_2013-04-08-16-43-10',  # :  25m, gripper not properly placed
        'unicornA_base1_2013-04-06-15-30-06',  # :  6m, nominal
        'unicornA_base1_2013-04-03-16-36-03',  # :  17m, nominal, ends for under-voltage
        
        # logs hokuyo
        'unicornA_base1_2013-04-11-20-14-27',
        'unicornA_tran1_2013-04-12-22-29-16',
        'unicornA_tran1_2013-04-12-22-40-02',
    ]

    simulated_robots = [
        'Se0Vrb1ro',
        'Se0Vrb1co',
        'Yfl1Se0Vrb1fsq1',
    ]

    real_robots = [
        'unicornA_tr1_hl_sane_s4',
        'unicornA_tw1_hl_sane_s4',
        'unicornA_tr1_hlhr_sane_s4',
        'unicornA_tw1_hlhr_sane_s4',
        'unicornA_tr1_cf_strip',
        'unicornA_tw1_cf_strip',
        'unicornA_tr1_fs1',
        'unicornA_tw1_fs1',
    ]

    combs_estimation = [
         ('Se0Vrb1ro', 'bdser_er4_i2_sr'),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_sr'),
         ('unicornA_tw1_hlhr_sane_s4', 'bdser_er4_i2_sr'),
         ('Se0Vrb1co', 'bdse_e1_ss'),
         ('unicornA_tw1_cf_strip', 'bdse_e1_ss'),
         ('Yfl1Se0Vrb1fsq1', 'bdse_e1_ss'),
         ('unicornA_tw1_fs1', 'bdse_e1_ss'),
    ]
    
    
    combs_servo_xy = [
         ('unicornA_tr1_hl_sane_s4', 'bdser_er4_i2_sr'),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_sr'),
         ('unicornA_tr1_hl_sane_s4', 'bdser_er4_i2_srl'),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_srl'),
         ('unicornA_tr1_hlhr_sane_s4', 'bdser_er4_i2_sr'),
         ('unicornA_tr1_hlhr_sane_s4', 'bdser_er4_i2_srl'),
         ('unicornA_tr1_cf_strip', 'bdser_e1_i2_ss'),
         ('unicornA_tr1_cf_strip', 'bdser_e1_i2_slt'),
         ('unicornA_tr1_fs1', 'bdse_e1_ss'),
         ('unicornA_tr1_fs1', 'bdser_er1_i1_ss'),
         ('unicornA_tr1_fs1', 'bdser_er1_i1_srl'),
    ]

    combs_servo_th = [
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_sr'),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_srl'),
         ('unicornA_tw1_hlhr_sane_s4', 'bdser_er4_i2_sr'),
         ('unicornA_tw1_hlhr_sane_s4', 'bdser_er4_i2_srl'),
         ('unicornA_tw1_cf_strip', 'bdser_e1_i2_ss'),
         ('unicornA_tw1_cf_strip', 'bdser_e1_i2_slt'),
         ('unicornA_tw1_fs1', 'bdse_e1_ss'),
         ('unicornA_tw1_fs1', 'bdser_er1_i1_ss'),
         ('unicornA_tw1_fs1', 'bdser_er1_i1_srl'),
    ]
    
    combs_servo = list(set(combs_servo_xy + combs_servo_th))
    
    class ExplogsTest():
        def __init__(self, id_episode, params={}):
            self.id_episode = id_episode
            self.params = params
        
        def __str__(self):
            return self.id_episode
        
    grids_xy = [
        ExplogsTest('unicornA_corner3_grid_fine_2013-06-08-19-18-55',
                    dict(min_dist=0.02, min_th_dist=np.deg2rad(4),
                         area_graphs=0.5)),
                
        ExplogsTest('unicornA_tran1_2013-04-12-23-34-08',
                    dict(area_graphs=1.3)),

        ExplogsTest('unicornA_corner3_grid_all0_2013-06-08-19-26-30'),

        ExplogsTest('unicornA_lab_grid_2013-06-01-21-00-47',
                    dict(area_graphs=0.9, min_dist=0.05)),
                
        ExplogsTest('unicornA_lab_grid_2013-06-01-21-04-51',
                    dict(area_graphs=1.5)),
    ]

    grids_th = [
        ExplogsTest('unicornA_lab_gridth_2013-06-01-21-11-15'),
    ]
    
    grids = grids_xy + grids_th


    def define_options(self, options):
        pass 

    def define_jobs_context(self, context):
        GlobalConfig.global_load_dir('${B11_SRC}/bvapps/bdse1')
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('jbds-est')
        data_central = self.get_data_central()
        
        jobs_learn_real(context, data_central,
                        real_robots=JBDSEstimation.real_robots,
                        explogs_learn=JBDSEstimation.explogs_learn)
        
        jobs_learn_simulations(context, data_central,
                               simulated_robots=JBDSEstimation.simulated_robots,
                               num_sim_episodes=1000,
                               max_episode_len=30,
                               episodes_per_tranche=50,
                               explorer='expsw1')
        
        r = job_report_learn(context, JBDSEstimation.combs_estimation)
        context.add_report(r, 'learn_global')
 
        jobs_tex(context, JBDSEstimation.combs_estimation)
 
        jobs_servo(context, data_central,
                   combinations=JBDSEstimation.combs_servo,
                   explogs_test=JBDSEstimation.grids)
        
        jobs_report_summary_servo_xy(context,
                           combinations=JBDSEstimation.combs_servo,
                           explogs_test=JBDSEstimation.grids_xy)

        r = report_summary_servo_theta(context,
                                   combinations=JBDSEstimation.combs_servo_th,
                                   explogs_test=JBDSEstimation.grids_th)
                                    
        context.add_report(r, 'servo_theta_global')

        

def jobs_learn_real(context, data_central, real_robots, explogs_learn):
    for id_robot in real_robots:
        recipe_agentlearn_by_parallel(context, data_central,
                                      only_robots=[id_robot],
                                      episodes=explogs_learn)
    boot_root = data_central.get_boot_root()
    
    for id_robot in real_robots:
        recipe_episodeready_by_convert2(context, boot_root, id_robot)    

def jobs_tex(context, combinations):
    output_dir = os.path.join(context.get_output_dir(), 'tex')
    for c, id_robot, id_agent in iterate_context_combinations(context, combinations):
        job_tex_report(c, output_dir, id_agent=id_agent, id_robot=id_robot)



def jobs_learn_simulations(context, data_central, simulated_robots, num_sim_episodes,
                           max_episode_len, explorer, episodes_per_tranche=50):        
    sim_episodes = [episode_id_exploration(explorer, i) for i in range(num_sim_episodes)]

    for id_robot in simulated_robots:
        # recipe_episodeready_by_simulation(context, data_central, id_robot,
        #                                   explorer, max_episode_len)

        recipe_episodeready_by_simulation_tranches(context, data_central, id_robot,
                                                   explorer, max_episode_len,
                                                   sim_episodes, episodes_per_tranche=50)

        recipe_agentlearn_by_parallel(context, data_central,
                                      only_robots=[id_robot],
                                      episodes=sim_episodes,
                                      episodes_per_tranche=episodes_per_tranche)


def jobs_servo(context, data_central, combinations, explogs_test):
    
    recipe_agent_servo(context, create_report=True)

    for c, id_robot, id_agent in iterate_context_combinations(context, combinations):        
        for cc, e in iterate_context_names(c, explogs_test):
            jobs_servo_field(cc, data_central=data_central,
                                id_robot=id_robot,
                                id_agent=id_agent,
                                id_episode=e.id_episode,
                                **e.params)




