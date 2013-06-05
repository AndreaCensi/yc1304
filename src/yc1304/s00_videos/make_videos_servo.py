from procgraph import pg
from quickapp import QuickApp
from rosstream2boot import ExpLogFromYaml, get_rs2b_config
from yc1304.campaign import CampaignCmd
import os


class MakeVideosServo(CampaignCmd, QuickApp):
    """ Creates video for servo experiments """
    
    cmd = 'make-videos-servo'
    
    def define_options(self, params):
        params.add_string('id_explog', help='Which exp log to use')

    def define_jobs_context(self, context):     

        id_explog = self.get_options().id_explog
        rs2b_config = get_rs2b_config()
        log = rs2b_config.explogs.instance(id_explog)
        if not isinstance(log, ExpLogFromYaml):
            self.info('Skipping log %r because not raw log.' % id_explog)
            return
        
        bag = log.get_bagfile() 
        
        comp = context.comp 
        out_base = os.path.join(context.get_output_dir(), id_explog)
        comp(create_video_servo_multi, bag, out_base,
                                job_id='servo_multi')
         

def create_video_servo_multi(bag, out_base):
    if os.path.exists(out_base + '.fcpxml'):
        print('Already exists: %s' % out_base)
        return  
    pg('video_servo_multi', config=dict(bag=bag, out_base=out_base))
    


def create_video_servo_error(bag, out):
    if os.path.exists(out):
        return out
    out_base = os.path.splitext(out)[0]
    pg('video_servo_error', config=dict(bag=bag, out_base=out_base))
    return out
