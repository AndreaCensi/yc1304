from contracts import contract
from quickapp import iterate_context_names_pair
from quickapp.report_manager import basename_from_key
from quickapp_boot import RM_AGENT_LEARN
from reprep import Report
from reprep.report_utils import StoreResults
from reprep_quickapp import ReportProxy

        
def report_summary_servo_theta(context, combinations, explogs_test):
    context = context.child('servo_theta')
    rp = ReportProxy(context)
    for id_robot, id_agent in combinations:
        context.needs(RM_AGENT_LEARN, id_robot=id_robot, id_agent=id_agent)
        
        f = rp.figure('%s-%s-servo_theta' % (id_robot, id_agent), cols=8,
                      caption='%s, %s' % (id_robot, id_agent))

        for e in explogs_test:

            key = dict(report_type='servo1', id_robot=id_robot,
                       id_agent=id_agent,
                       id_episode=e.id_episode)
        
            s = 'servo-%s-' % basename_from_key(dict(id_agent=id_agent,
                                                     id_robot=id_robot,
                                                     id_episode=e.id_episode))
            
            def add(url, nid, strict):
                r = rp.add_child_from_other(url, s + nid, strict=strict, ** key)
                f.sub(r, caption=nid)
        
            add('u/figure2/tw', 'u-tw', True)
            add('descent/figure2/tw', 'descent-tw', False)
        
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
    
    for id_robot, id_agent in combs:

        for id_episode in map(str, explogs_test):
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            interp = interps[key]
            interp.nid = basename_from_key(key) + '-interp'
            interp.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(interp)
            get_fig(id_robot).sub(interp)

        for id_episode in map(str, explogs_test):
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            arrow = arrows[key]
            arrow.nid = basename_from_key(key) + '-vf'
            arrow.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(arrow)
            get_fig(id_robot).sub(arrow)

    return r


def job_report_learn(context, combs):
    context = context.child('report_learn')
    rp = ReportProxy(context)
    for id_robot, id_agent in combs:
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


@contract(explogs_test='seq(str)', parts=StoreResults, returns=Report)
def report_servo1_global(combs, explogs_test, parts):
    r = Report()
    figs = {}
    
    def get_fig(id_robot):
        if not id_robot in figs:
            figs[id_robot] = r.figure(cols=len(explogs_test), caption=id_robot)
        return figs[id_robot]
    
    for id_robot, id_agent in combs:
        for id_episode in map(str, explogs_test):
            key = dict(id_robot=id_robot, id_agent=id_agent, id_episode=id_episode)
            part = parts[key]
            part.nid = basename_from_key(key)
            part.caption = '%s, %s' % (id_robot, id_agent)
            r.add_child(part)
            get_fig(id_robot).sub(part)

    return r


def iterate_context_combinations(context, combinations):
    robots = set()
    agents = set()
    robots_agents = set()  # (robot, agent) tuple
    for robot, agent in combinations:
        robots.add(robot)
        agents.add(agent)
        robots_agents.add((robot, agent))
    robots = sorted(list(robots))
    agents = sorted(list(agents))         
    for c, id_robot, id_agent in iterate_context_names_pair(context, robots, agents):
        if not (id_robot, id_agent) in robots_agents:
            continue
        yield c, id_robot, id_agent


def jobs_report_summary_servo_xy(context, combinations, explogs_test):
    parts = StoreResults()
    for id_robot, id_agent in combinations:
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
    for id_robot, id_agent in combinations:
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
 

@contract(url=str, r=Report, returns=Report)
def get_node(url, r):
    return r.resolve_url(url)

