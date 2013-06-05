from bootstrapping_olympics.programs.manager import DataCentral
from conf_tools import GlobalConfig
from quickapp import QuickMultiCmdApp
from rosstream2boot import ExpLogFromYaml 

class Campaign(QuickMultiCmdApp):
    """ Main campaign program """
    
    cmd = 'yc'
    
    def define_multicmd_options(self, params):
        pass
    
    def get_config_dirs(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        config_dir = resource_filename("yc1304", "config")
        return [config_dir] 
    
    def initial_setup(self):
        config_dirs = self.get_config_dirs()
        GlobalConfig.global_load_dirs(config_dirs)
                    
                             
class CampaignCmd(Campaign.get_sub()):
    
    def get_boot_root(self):
        # If there are subtasks (A>B>{C,D}), then the first to call 
        # get_boot_root will establish the boot_root for the subtasks.
        # e.g. if B calls it, then C, D use the same directory
        if 'boot_root' in self.__dict__:
            return self.boot_root
        # first check if the top has defined it
        parent = self.get_parent()
        assert parent is not None
        if 'boot_root' in parent.__dict__:
            self.boot_root = parent.boot_root
        else:
            self.boot_root = self.context.get_output_dir()
        # print('Now: %s' % self.boot_root) 
        return self.boot_root

    def get_data_central(self):
        return DataCentral(self.get_boot_root())

    def get_log_index(self):
        return self.get_data_central().get_log_index()

    def instance_explog(self, id_explog):
        """ Instances the given explog and checks it is a ExpLogFromYaml """
        rs2b_config = self.get_rs2b_config()
        
        log = rs2b_config.explogs.instance(id_explog)
        if not isinstance(log, ExpLogFromYaml):
            self.info('Skipping log %r because not raw log.' % id_explog)
            return
        return log 
    
    
    
main = Campaign.get_sys_main()

    

