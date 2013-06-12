from quickapp import QuickApp
from yc1304.campaign import CampaignCmd
from yc1304.exps import Exp08, Exp10, Exp14, Exp18, Exp29, Exp30, Exp30c, Exp33

class Good(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ The good bits --- those demos that need to keep working. """
    cmd = 'good'
    
    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        # these were the ones with defined launch files
        context.subtask(Exp08, separate_resource_manager=True)
        context.subtask(Exp10, separate_resource_manager=True)
        context.subtask(Exp14, separate_resource_manager=True)
        context.subtask(Exp18, separate_resource_manager=True)
        context.subtask(Exp29, separate_resource_manager=True)
        context.subtask(Exp30, separate_resource_manager=True)
        context.subtask(Exp30c, separate_resource_manager=True)
        context.subtask(Exp33, separate_resource_manager=True)
        
