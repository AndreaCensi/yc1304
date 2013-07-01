from . import CampaignCmd
from quickapp import QuickApp
from yc1304.exps import good_logs_hokuyos
from yc1304.exps.exp_utils import jobs_learnp_and_servo


__all__ = ['Exp30']


class Exp30(CampaignCmd, QuickApp):
    """ Checking whether servo really works """
    
    cmd = 'exp30'
    
    comment = """ 
        
    """
    
    robots = [
        'unicornA_tw1_hlhr_sane_s4',
        'unicornA_tw1_hl_sane_s4',
        'unicornA_tr1_hlhr_sane_s4',
#         'unicornA_tw1_cf_strip',
#         'unicornA_tr1_cf_strip',
    ]

    agents = [ 
        "bdser_er1_i1_ss",
        "bdser_er1_i1_sr",
        "bdser_er1_i1_srl",
        "bdser_er1_i2_ss",
        "bdser_er1_i2_sr",
        "bdser_er1_i2_srl",
        "bdser_er2_i1_sr",
        "bdser_er2_i1_srl",
#         "bdser_er3_i2_ss",
        "bdser_er2_i2_sr",
        "bdser_er2_i2_srl",
        "bdser_er3_i1_sr",
        "bdser_er3_i1_srl",
        "bdser_er3_i2_ss",
        "bdser_er3_i2_sr",
        "bdser_er3_i2_srl",
        'bdser_er4_i2_ss',
        'bdser_er4_i2_sr',
        'bdser_er4_i2_srl',
    ]
             
    explogs_test = [
        'unicornA_tran1_2013-04-12-23-34-08',  # convex environment
        'unicornA_lab_grid_2013-06-01-21-00-47',  # non-convex environment 1
        'unicornA_lab_grid_2013-06-01-21-04-51',  # non-convex environment 2
        'unicornA_lab_gridth_2013-06-01-21-11-15'  # pure rotation on theta
    ]

    logs_exp10 = [
        'unicornA_base1_2013-04-03-13-30-28',  # :  38m, nominal, ok
        'unicornA_car1_2013-04-08-21-37-47',  # :  ??m, nominal
        'unicornA_tran1_2013-04-09-14-35-11',  # :  ??min, nominal
        'unicornA_base1_2013-04-02-20-37-43',  # :  37m, nominal, boxes
        'unicornA_base1_2013-04-08-19-10-12',  # :  15m, has occlusions for camera
        'unicornA_base1_2013-04-03-12-58-11',  # :  17m, nominal, boxes
        'unicornA_base1_2013-04-08-16-43-10',  # :  25m, gripper not properly placed
        'unicornA_base1_2013-04-06-15-30-06',  # :  6m, nominal
        'unicornA_base1_2013-04-03-16-36-03',  # :  17m, nominal, ends for under-voltage
    ]
    explogs_learn = list(set(good_logs_hokuyos + logs_exp10))
    
    explogs_convert = []
    explogs_convert.extend(explogs_test) 
    explogs_convert.extend(explogs_learn)

    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):
        data_central = self.get_data_central()

        agents = Exp30.agents
        robots = Exp30.robots
        explogs_learn = Exp30.explogs_learn
        explogs_test = Exp30.explogs_test
        
        jobs_learnp_and_servo(context, data_central=data_central,
                              explogs_learn=explogs_learn,
                              explogs_test=explogs_test, agents=agents, robots=robots)
        

