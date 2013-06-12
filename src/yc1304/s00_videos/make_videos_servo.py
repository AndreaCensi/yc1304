from procgraph import pg
from quickapp import QuickApp
from rosstream2boot import ExpLogFromYaml, get_rs2b_config
from yc1304.campaign import CampaignCmd
import os
from rosstream2boot.configuration import get_conftools_explogs


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
        
        jobs_video_servo_multi(context, id_explog)
        
def jobs_video_servo_multi(context, id_explog):
    out_base = os.path.join(context.get_output_dir(), id_explog)
    context.comp_config(create_video_servo_multi, id_explog, out_base)

def create_video_servo_multi(id_explog, out_base):
    explog = get_conftools_explogs().instance(id_explog)
    bag = explog.get_bagfile()
    
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
