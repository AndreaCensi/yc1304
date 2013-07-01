from quickapp import QuickApp
from yc1304.campaign import CampaignCmd
from .servo import JBDSServoVisualization
from .navigation import JBDSNavigationVisualization
from .estimation import JBDSEstimation

__all__ = ['JBDS']


class JBDS(CampaignCmd, QuickApp):  # @UndefinedVariable
    cmd = 'jbds'
    
    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        # these were the ones with defined launch files
        context.subtask(JBDSEstimation, separate_resource_manager=True)
        context.subtask(JBDSNavigationVisualization, separate_resource_manager=True)
        context.subtask(JBDSServoVisualization, separate_resource_manager=True)
        
