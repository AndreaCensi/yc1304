from conf_tools import GlobalConfig
from procgraph import pg
from quickapp import QuickApp
from rosstream2boot import ExpLogFromYaml, get_rs2b_config
from yc1304.campaign import CampaignCmd
from yc1304.exps import good_logs_cf
from yc1304.exps.exp_utils import iterate_context_explogs_and_robots
import os

class MakeVideosBootDataYC(CampaignCmd, QuickApp):
    """ Creates all the bootdata videos that I need. """
    
    cmd = 'make-videos-bd-mine'
    usage = 'make-videos-bd-mine'
    
    def define_options(self, params):
        pass

    def define_jobs_context(self, context):
        unicorn_robots_cam = [
            'ros_unicornA_base1_tw_cf',
            'ros_uA_b1_tw_cf',
            'ros_uA_b1_tw_cf_strip',
            'ros_uA_b1_xy_cf_strip']
        unicorn_robots_lasers = [
            'ros_unicornA_base1_tw_hr',
            'ros_unicornA_base1_tw_hl',
            'ros_unicornA_base1_tw_hlhr',
            # 'ros_unicornA_base1_tw_hlhr_sane',
            'ros_unicornA_base1_tw_hlhr_sane_s4',
        ]
        
        mine = [
            ('you', 'unicorn*', unicorn_robots_lasers),
            ('you', good_logs_cf, unicorn_robots_cam),
            ('ldr', 'logger*', ['ldr21'])    
        ]
        for part, explogs, robots in mine:
            context.subtask(MakeVideosBootDataMany,
                            robots=robots, explogs=explogs,
                            add_job_prefix=part, add_outdir=part)


class MakeVideosBootDataMany(CampaignCmd, QuickApp):
    """ Creates video for servo experiments """
    
    cmd = 'make-videos-bd-many'
    usage = 'make-videos-bd-many --explogs <log1> ... --robots <robot> <robot2> ...'

    def define_options(self, params):
        params.add_string_list('explogs', help='Which explogs to use')
        params.add_string_list('robots', help='Which robots to use')

    def define_jobs_context(self, context):
        options = self.get_options()
        
        rs2b_config = get_rs2b_config()
        
        self.info('explogs: %s' % options.explogs)
        self.info('robots: %s' % options.robots)
        explogs = rs2b_config.explogs.expand_names(options.explogs)
        robots = rs2b_config.explogs.expand_names(options.robots)
    
        
        s = iterate_context_explogs_and_robots(context, explogs, robots)
        for c, id_explog, id_robot in s:
            c.subtask(MakeVideosBootData, id_robot=id_robot, id_explog=id_explog,
                      add_job_prefix='', add_outdir='')
    

class MakeVideosBootData(CampaignCmd, QuickApp):
    """ Creates low-level visualization """
    
    cmd = 'make-videos-bd'
    usage = 'make-videos-bd --id_explog <log> --id_robot <robot> '
    
    
    def define_options(self, params):
        params.add_string('id_explog', help='Which exp log to use')
        params.add_string('id_robot', help='Which robots to use')

    def define_jobs_context(self, context):     
        id_explog = self.get_options().id_explog
        id_robot = self.get_options().id_robot

        rs2b_config = self.get_rs2b_config()
        explog = rs2b_config.explogs.instance(id_explog)
        if not isinstance(explog, ExpLogFromYaml):
            self.error('Skipping log %r because not raw log.' % id_explog)
            return
        
        
        boot_config = self.get_boot_config()
        
        md = explog.get_metadata()
        md['id_explog'] = id_explog
        
        bag = explog.get_bagfile()
        if not os.path.exists(bag):
            self.error('Skipping log %r because bag not found.' % id_explog)
            return
         
        
        b = '%s.%s' % (id_explog, id_robot)
        out_base = os.path.join(context.get_output_dir(), b)
        
        boot_config.robots.instance(id_robot)
        
        context.comp_config(create_video_bootdata,
                     bag, id_robot, out_base, md,
                     job_id='video_bootdata')
         

def create_video_bootdata(bag, id_robot, out_base, md):
#     
#     if os.path.exists(out_base + '.fcpxml'):  # FIXME
#         print('Already exists: %s' % out_base)
#         return  
    
    md['pg_model'] = 'video_bootdata'
    md['id_robot'] = id_robot
    config = dict(bag=bag, out_base=out_base, id_robot=id_robot, md=md)
    pg('video_bootdata', config=config)
    
