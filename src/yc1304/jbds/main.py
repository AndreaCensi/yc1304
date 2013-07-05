from quickapp import QuickApp
from yc1304.campaign import CampaignCmd
from .servo import JBDSServoVisualization
from .navigation import JBDSNavigationVisualization
from .estimation import JBDSEstimation
from .estimation_fraction import JBDSEstimationFraction

__all__ = ['JBDS']


class JBDS(CampaignCmd, QuickApp):  # @UndefinedVariable
    cmd = 'jbds'
    
    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        # these were the ones with defined launch files
        separate = dict(separate_resource_manager=True, separate_report_manager=True)
        context.subtask(JBDSEstimation, **separate)
        context.subtask(JBDSEstimationFraction, **separate)
        context.subtask(JBDSNavigationVisualization, **separate)
        context.subtask(JBDSServoVisualization, **separate)
        
