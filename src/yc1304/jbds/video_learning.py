from bootstrapping_olympics.programs.manager.meat.log_learn import learn_log
from procgraph_boot.procgraph_bridge import ProcgraphBridge
from quickapp_boot import RM_EPISODE_READY


__all__ = ['jobs_learn_real_videos', 'jobs_learn_real_video']


def jobs_learn_real_videos(context, data_central, combinations, episodes):
    
    for id_robot, id_agent in combinations:
        jobs_learn_real_video(context, data_central, id_agent, id_robot, episodes, 'video_bdse_learn')
        jobs_learn_real_video(context, data_central, id_agent, id_robot, episodes, 'video_bdse_learn2')
        

def jobs_learn_real_video(context, data_central, id_agent, id_robot, episodes, model):    
    procgraph_code = [model, {}]
    plugin = ProcgraphBridge(procgraph_code,
                             procgraph_extra_modules=['procgraph_bdse'],
                             suffix=model)
    
    deps = [context.get_resource(RM_EPISODE_READY, id_robot=id_robot, id_episode=e) 
            for e in episodes]
    
    context.comp_config(learn_log,
                        data_central=data_central,
                        id_agent=id_agent,
                        id_robot=id_robot,
                        live_plugins=[plugin],
                        save_state=False,
                        extra_dep=deps,
                        reset=True,
                        job_id='%s-%s-%s' % (id_agent, id_robot, model))
