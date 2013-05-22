from quickapp_boot.utils import (_good_context_name, iterate_context_episodes,
    iterate_context_agents, iterate_context_agents_and_episodes)




def iterate_context_explogs(context, explogs):
    """ Yields context, id_agent,  """
    for id_explog in explogs:
        name = _good_context_name(id_explog)
        e_c = context.child(name)
        yield e_c, id_explog


def iterate_context_robots(context, robots):
    """ Yields context, id_robot  """
    for id_robot in robots:
        name = _good_context_name(id_robot)
        e_c = context.child(name)
        yield e_c, id_robot




def iterate_context_explogs_and_robots(context, explogs, robots):
    """ Yields context, id_explog, id_robot  """
    for cc, id_explog in iterate_context_explogs(context, explogs):
        for c, id_robot in iterate_context_robots(cc, robots):
            yield c, id_explog, id_robot

