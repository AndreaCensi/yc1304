from .campaign import CampaignCmd
from .exps import Exp08, Exp10, Exp14, Exp18
from quickapp import QuickApp

class Good(CampaignCmd, QuickApp):  # @UndefinedVariable
    """ The good bits --- those demos that need to keep working. """
    cmd = 'good'
    
    def define_options(self, options):
        pass
    
    def define_jobs_context(self, context):
        # these were the ones with defined launch files
        context.subtask(Exp08)
        context.subtask(Exp10)
        context.subtask(Exp14)
        context.subtask(Exp18)
        
