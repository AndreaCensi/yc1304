from .servo_reconstruct import reconstruct_servo_state_nomap
from quickapp import QuickApp
from rosstream2boot import get_conftools_explogs
from yc1304.campaign import CampaignCmd
from yc1304.exps.exp_utils import iterate_context_explogs
import os

__all__ = ['JBDSServoVisualization']


class JBDSServoVisualization(CampaignCmd, QuickApp): 
    
    """ Visualization of the servo logs for JBDS """
    cmd = 'jbds-videos-servo'
    
    
    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        logs = (set(self.get_explogs_by_tag('servo')) & 
                set(self.get_explogs_by_tag('fieldsampler')))
        
        assert len(logs) >= 4
        
        for c, id_explog in iterate_context_explogs(context, logs):
            explog = get_conftools_explogs().instance(id_explog)

            # jobs_video_servo_multi(c, id_explog)

            annotation_servo = explog.get_annotations()['servo'] 
            id_robot = annotation_servo['robot']
            goal_at = annotation_servo['goal']
                    
            out_base = os.path.join(c.get_output_dir(), '%s' % id_explog)
            
            c.comp_config(reconstruct_servo_state_nomap,
                          id_explog, id_robot, out_base, goal_at=goal_at)
            
            # c.subtask(MakeVideos2, id_explog=id_explog,
            #          add_job_prefix='videos', add_outdir='')
            
            
            
