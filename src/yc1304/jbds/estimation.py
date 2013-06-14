from contracts import contract
from quickapp import iterate_context_names, iterate_context_names_pair, QuickApp
from quickapp.report_manager import basename_from_key
from quickapp_boot import recipe_agentlearn_by_parallel, recipe_agent_servo, \
    RM_AGENT_LEARN
from reprep import Report
from reprep.report_utils import StoreResults
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.s10_servo_field.jobs import jobs_servo_field
import numpy as np
from reprep_quickapp import ReportProxy
from yc1304.exps.exp40sim import episode_id_exploration
from quickapp_boot.jobs.jobs_simulation import recipe_episodeready_by_simulation
from conf_tools.master import GlobalConfig

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
        'unicornA_tr1_hlhr_sane_s4',
        'unicornA_tr1_cf_strip',
        'unicornA_tr1_fs1'
    ]

    combs_estimation = [
        ('Se0Vrb1ro', 'bdser_er4_i2_sr', []),
         ('unicornA_tr1_hl_sane_s4', 'bdser_er4_i2_sr', []),
         ('unicornA_tr1_hlhr_sane_s4', 'bdser_er4_i2_sr', []),
         ('Se0Vrb1co', 'bdse_e1_ss', []),
         ('unicornA_tr1_cf_strip', 'bdse_e1_ss', []),
         ('Yfl1Se0Vrb1fsq1', 'bdse_e1_ss', []),
         ('unicornA_tr1_fs1', 'bdse_e1_ss', []),
    ]
    
    combs_servo = [
         ('unicornA_tr1_hl_sane_s4', 'bdser_er4_i2_sr', []),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_sr', []),
         ('unicornA_tr1_hl_sane_s4', 'bdser_er4_i2_srl', []),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_srl', []),
         ('unicornA_tr1_hlhr_sane_s4', 'bdser_er4_i2_sr', []),
         ('unicornA_tr1_hlhr_sane_s4', 'bdser_er4_i2_srl', []),
         ('unicornA_tr1_cf_strip', 'bdser_e1_i2_ss', []),
         ('unicornA_tr1_cf_strip', 'bdser_e1_i2_slt', []),
         ('unicornA_tr1_fs1', 'bdse_e1_ss', []),
         ('unicornA_tr1_fs1', 'bdser_er1_i1_ss', []),
         ('unicornA_tr1_fs1', 'bdser_er1_i1_srl', []),
    ]
    
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
                               num_sim_episodes=5,
                               max_episode_len=5,
                               explorer='expsw1')
        
        r = job_report_learn(context, JBDSEstimation.combs_estimation)
        context.add_report(r, 'learn_global')
 
        jobs_servo(context, data_central,
                   combinations=JBDSEstimation.combs_servo,
                   explogs_test=JBDSEstimation.grids_xy)
        jobs_servo_reports(context,
                           combinations=JBDSEstimation.combs_servo,
                           explogs_test=JBDSEstimation.grids_xy)


def jobs_learn_real(context, data_central, real_robots, explogs_learn):
    for id_robot in real_robots:
        recipe_agentlearn_by_parallel(context, data_central,
                                      only_robots=[id_robot],
                                      episodes=explogs_learn)
    boot_root = data_central.get_boot_root()
    
    for id_robot in real_robots:
        recipe_episodeready_by_convert2(context, boot_root, id_robot)    


def job_report_learn(context, combs):
    rp = ReportProxy(context)
    for id_robot, id_agent, _ in combs:
        context.needs(RM_AGENT_LEARN, id_robot=id_robot, id_agent=id_agent)
        
        f = rp.figure('%s-%s-model' % (id_robot, id_agent), cols=8,
                      caption='%s, %s' % (id_robot, id_agent))
        
        key = dict(report_type='agent_report', id_robot=id_robot, id_agent=id_agent)
        
        s = 'bds-%s-' % basename_from_key(dict(id_agent=id_agent, id_robot=id_robot))
        add = lambda n, nid: f.sub(rp.add_child_from_other(n, s + nid, **key), caption=nid)
        
        add('estimator/model/M/slices/0/normalized/png', 'M0')
        add('estimator/model/M/slices/1/normalized/png', 'M1')
        add('estimator/model/M/slices/2/normalized/png', 'M2')
        add('estimator/model/N/slices/0/figure1/plot_scaled', 'N0')
        add('estimator/model/N/slices/1/figure1/plot_scaled', 'N1')
        add('estimator/model/N/slices/2/figure1/plot_scaled', 'N2')
        
        f = rp.figure('%s-%s-learn' % (id_robot, id_agent), cols=8,
                      caption='%s, %s' % (id_robot, id_agent))
        
        add('estimator/tensors/T/slices/0/normalized/png', 'T0')
        add('estimator/tensors/T/slices/1/normalized/png', 'T1')
        add('estimator/tensors/T/slices/2/normalized/png', 'T2')
        add('estimator/tensors/U/slices/0/figure1/plot_scaled', 'U0')
        add('estimator/tensors/U/slices/1/figure1/plot_scaled', 'U1')
        add('estimator/tensors/U/slices/2/figure1/plot_scaled', 'U2')
                
        add('estimator/tensors/P/posneg', 'P')
        
    return rp.get_job()

@contract(explogs_test='seq(str)', arrows=StoreResults, interps=StoreResults,
           returns=Report)
def report_distances2_global(combs, explogs_test, arrows, interps):
    r = Report()
    figs = {}
    
    def get_fig(id_robot):
        if not id_robot in figs:
            figs[id_robot] = r.figure(cols=len(explogs_test), caption=id_robot)
        return figs[id_robot]
    
    for id_robot, id_agent, _ in combs:

        for id_episode in explogs_test:
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            interp = interps[key]
            interp.nid = basename_from_key(key) + '-interp'
            interp.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(interp)
            get_fig(id_robot).sub(interp)

        for id_episode in explogs_test:
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            arrow = arrows[key]
            arrow.nid = basename_from_key(key) + '-vf'
            arrow.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(arrow)
            get_fig(id_robot).sub(arrow)

    return r

def jobs_learn_simulations(context, data_central, simulated_robots, num_sim_episodes,
                           max_episode_len, explorer):        
    sim_episodes = [episode_id_exploration(explorer, i) for i in range(num_sim_episodes)]

    for id_robot in simulated_robots:
        recipe_episodeready_by_simulation(context, data_central, id_robot,
                                          explorer, max_episode_len)

        recipe_agentlearn_by_parallel(context, data_central,
                                      only_robots=[id_robot],
                                      episodes=sim_episodes)


def jobs_servo(context, data_central, combinations, explogs_test):
    robots = set()
    agents = set()
    robots_agents = set()  # (robot, agent) tuple
    for robot, agent, _ in combinations:
        robots.add(robot)
        agents.add(agent)
        robots_agents.add((robot, agent))
    robots = sorted(list(robots))
    agents = sorted(list(agents))         
    
    recipe_agent_servo(context, create_report=True)


    for c, id_robot, id_agent in iterate_context_names_pair(context, robots, agents):
        if not (id_robot, id_agent) in robots_agents:
            continue
        
        for cc, e in iterate_context_names(c, explogs_test):
            jobs_servo_field(cc, data_central=data_central,
                                id_robot=id_robot,
                                id_agent=id_agent,
                                id_episode=e.id_episode,
                                **e.params)



def jobs_servo_reports(context, combinations, explogs_test):
    
    parts = StoreResults()
    for id_robot, id_agent, _ in combinations:
        for e in explogs_test:
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=e.id_episode)
            job_id = 'part-' + basename_from_key(key)
            arrows = context.comp(get_node, 'xy_arrows_colors',
                                      context.get_report('servo1', **key),
                                      job_id=job_id)
            parts[key] = arrows 
    
    r = context.comp(report_servo1_global, combinations,
                     map(str, explogs_test), parts)
    context.add_report(r, 'servo1_global')
    
    interps = StoreResults()
    for id_robot, id_agent, _ in combinations:
        for e in explogs_test:
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=e.id_episode)
            job_id = 'interpolation-' + basename_from_key(key)
            field = context.comp(get_node, 'interpolation',
                                 context.get_report('distances2', **key),
                                 job_id=job_id)
            interps[key] = field 
            
    r = context.comp(report_distances2_global, combinations,
                     map(str, explogs_test), parts, interps)
    context.add_report(r, 'distances2_global')
 
 
 

@contract(explogs_test='seq(str)', parts=StoreResults, returns=Report)
def report_servo1_global(combs, explogs_test, parts):
    r = Report()
    figs = {}
    
    def get_fig(id_robot):
        if not id_robot in figs:
            figs[id_robot] = r.figure(cols=len(explogs_test), caption=id_robot)
        return figs[id_robot]
    
    for id_robot, id_agent, _ in combs:
        for id_episode in explogs_test:
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            part = parts[key]
            part.nid = basename_from_key(key)
            part.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(part)
            get_fig(id_robot).sub(part)

    return r

@contract(url=str, r=Report, returns=Report)
def get_node(url, r):
    return r.resolve_url(url)





