from bootstrapping_olympics import get_boot_config
from bootstrapping_olympics.programs.manager import DataCentral
from conf_tools import GlobalConfig
from quickapp import QuickMultiCmdApp
from rosstream2boot import ExpLogFromYaml, get_rs2b_config
import os


class Campaign(QuickMultiCmdApp):
    cmd = 'yc'
    short = 'Main campaign program'

    boot_root = 'out/boot-root'
    
    def define_multicmd_options(self, params):
        # params.add_flag('dummy', help='workaround for a bug')
        # params.add_string_list('config', help='Configuration directory')
        pass
    
    def get_config_dirs(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        config_dir = resource_filename("yc1304", "config")
        return [config_dir]

    def get_data_central(self):
        return self.data_central
    
    def get_boot_root(self):
        return Campaign.boot_root

    def initial_setup(self):
        config_dirs = self.get_config_dirs()
        GlobalConfig.global_load_dirs(config_dirs)
        
        self.rs2b_config = get_rs2b_config()
        self.boot_config = get_boot_config()

        boot_root = self.get_boot_root()
        if not os.path.exists(boot_root):
            os.makedirs(boot_root)
        self.data_central = DataCentral(boot_root)
                    
                             
class CampaignCmd(Campaign.sub):
    
    def use_private_dirs(self):
        return False
    
    def get_config_dirs(self):
        return self.get_parent().get_config_dirs()

    def get_boot_root(self):
        if self.use_private_dirs():
            outdir = self.context.get_output_dir()
            return outdir
        else:
            return self.get_parent().get_boot_root()
    
    def get_data_central(self):
        if self.use_private_dirs():
            return DataCentral(self.get_boot_root())
        else:
            return self.get_parent().get_data_central()

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

    

