from quickapp_boot.utils import (_good_context_name,
    iterate_context_robots, iterate_context_episodes)
from quickapp_boot.recipes.recipes_agent_servo import recipe_agent_servo
from rosstream2boot.programs.recipes import recipe_episodeready_by_convert2
from quickapp_boot.recipes.recipes_learning_parallel import recipe_agentlearn_by_parallel
from quickapp.app_utils.subcontexts import iterate_context_names
from yc1304.s10_servo_field.jobs import jobs_servo_field_agents
from quickapp_boot.jobs.jobs_publish import jobs_publish_learning_agents_robots



def iterate_context_explogs(context, explogs):
    """ Yields context, id_agent,  """
    for id_explog in explogs:
        name = _good_context_name(id_explog)
        e_c = context.child(name)
        yield e_c, id_explog


def iterate_context_explogs_and_robots(context, explogs, robots):
    """ Yields context, id_explog, id_robot  """
    for cc, id_explog in iterate_context_explogs(context, explogs):
        for c, id_robot in iterate_context_robots(cc, robots):
            yield c, id_explog, id_robot


def jobs_learnp_and_servo(context, data_central, explogs_learn,
                         explogs_test, agents, robots):
    """ Learn parallel, create servo field """
    boot_root = data_central.get_boot_root()
    recipe_agentlearn_by_parallel(context, data_central, explogs_learn)
    recipe_agent_servo(context, create_report=True)

    for id_robot in robots:
        recipe_episodeready_by_convert2(context, boot_root, id_robot)
        
    for c, id_robot in iterate_context_names(context, robots):
        jobs_servo_field_agents(c, data_central=data_central,
                                id_robot=id_robot,
                                agents=agents, episodes=explogs_test)
    
    jobs_publish_learning_agents_robots(context, boot_root, agents, robots)
