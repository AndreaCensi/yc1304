


def iterate_context_episodes(context, episodes):
    """ Yields context, id_episode,  """
    for id_episode in episodes:
        name = _good_context_name(id_episode)
        e_c = context.child(name)
        yield e_c, id_episode


def iterate_context_agents(context, agents):
    """ Yields context, id_agent,  """
    for id_agent in agents:
        name = _good_context_name(id_agent)
        e_c = context.child(name)
        yield e_c, id_agent



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



def iterate_context_agents_and_episodes(context, agents, episodes):
    """ Yields context, id_agent, id_episode  """
    for cc, id_agent in iterate_context_agents(context, agents):
        for c, id_episode in iterate_context_episodes(cc, episodes):
            yield c, id_agent, id_episode


def iterate_context_explogs_and_robots(context, explogs, robots):
    """ Yields context, id_explog, id_robot  """
    for cc, id_explog in iterate_context_explogs(context, explogs):
        for c, id_robot in iterate_context_robots(cc, robots):
            yield c, id_explog, id_robot

def _good_context_name(id_object):
    return id_object.replace('-', '')



