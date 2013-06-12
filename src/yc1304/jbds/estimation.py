from quickapp import iterate_context_names, iterate_context_names_pair, QuickApp
from quickapp_boot import recipe_agentlearn_by_parallel, recipe_agent_servo
from rosstream2boot import recipe_episodeready_by_convert2
from yc1304.campaign import CampaignCmd
from yc1304.s10_servo_field.jobs import jobs_servo_field
from reprep.report_utils.storing.store_results import StoreResults
from contracts import contract
from reprep import Report
from quickapp.report_manager import basename_from_key

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

    combs = [
        # from exp30
         ('unicornA_tw1_hlhr_sane_s4', 'bdser_er4_i2_sr', explogs_learn),
         ('unicornA_tw1_hl_sane_s4', 'bdser_er4_i2_sr', explogs_learn),
        # from exp30c
         ('unicornA_tr1_cf_strip', 'bdser_e1_i2_slt', explogs_learn),
         ('unicornA_tr1_cf_strip', 'bdser_e1_i2_ss', explogs_learn),
         ('unicornA_tw1_cf_strip', 'bdser_e1_i2_slt', explogs_learn),
         ('unicornA_tw1_cf_strip', 'bdser_e1_i2_ss', explogs_learn),
        # from exp33
         ('unicornA_tw1_fs1', 'bdse_e1_ss', explogs_learn),
         ('unicornA_tw1_fs1', 'bdser_er1_i1_ss', explogs_learn),
    ]
    
    grids_xy = [
        'unicornA_corner3_grid_all0_2013-06-08-19-26-30',
        'unicornA_corner3_grid_fine_2013-06-08-19-18-55',
        'unicornA_lab_grid_2013-06-01-21-00-47',
        'unicornA_lab_grid_2013-06-01-21-04-51',
        'unicornA_tran1_2013-04-12-23-34-08'       
    ]

    grids_th = [
        'unicornA_lab_gridth_2013-06-01-21-11-15',
    ]
    
    grids = grids_xy + grids_th


    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        rm = context.get_report_manager()
        rm.set_html_resources_prefix('jbds-est')
        
        explogs_learn = JBDSEstimation.explogs_learn
        explogs_test = JBDSEstimation.grids
        robots = set()
        agents = set()
        robots_agents = set()  # (robot, agent) tuple
        for robot, agent, _ in JBDSEstimation.combs:
            robots.add(robot)
            agents.add(agent)
            robots_agents.add((robot, agent))
        robots = sorted(list(robots))
        agents = sorted(list(agents))
         
        data_central = self.get_data_central()
        
        boot_root = data_central.get_boot_root()
        recipe_agentlearn_by_parallel(context, data_central, explogs_learn)
        recipe_agent_servo(context, create_report=True)
    
        for id_robot in robots:
            recipe_episodeready_by_convert2(context, boot_root, id_robot)
            
        for c, id_robot, id_agent in iterate_context_names_pair(context, robots, agents):
            if not (id_robot, id_agent) in robots_agents:
                continue
            for cc, id_episode in iterate_context_names(c, explogs_test):
                jobs_servo_field(cc, data_central=data_central,
                                    id_robot=id_robot,
                                    id_agent=id_agent,
                                    id_episode=id_episode)
            
        parts = StoreResults()
        for id_robot, id_agent, _ in JBDSEstimation.combs:
            for id_episode_test in explogs_test:
                key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode_test)
                parts[key] = context.comp(get_node, 'xy_arrows_colors',
                                          c.get_report('servo1', **key)) 
        
        r = context.comp(report_servo1_global, JBDSEstimation.combs,
                         JBDSEstimation.grids_xy, parts)
        context.add_report(r,
                           'servo1_global')
        
        
@contract(explogs_test='seq[str]', parts=StoreResults, returns=Report)
def report_servo1_global(combs, explogs_test, parts):
    r = Report()
    f = r.figure(cols=len(explogs_test))
    for id_robot, id_agent, _ in combs:
        for id_episode in explogs_test:
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            part = parts[key]
            part.nid = basename_from_key(key)
            part.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(part)
            f.sub(part)
    return r

@contract(url=str, r=Report, returns=Report)
def get_node(url, r):
    return r.resolve_url(url)





