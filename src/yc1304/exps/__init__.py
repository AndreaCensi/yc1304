from yc1304.campaign import CampaignCmd
from quickapp import QuickApp

# Good logs for learning frontal camera
good_logs_cf = [
'unicornA_base1_2013-04-03-13-30-28',  # 38m, nominal, ok
'unicornA_car1_2013-04-08-21-37-47',  # ??m, nominal
    # - unicornA_base1_2013-04-06-19-44-59',  people standing around; don't use for learning
'unicornA_tran1_2013-04-09-14-35-11',  # ??min, nominal
    # - unicornA_base1_2013-04-03-13-16-53',  7m, Crashes into curtains after 7 minutes; don't use for learning.
'unicornA_base1_2013-04-02-20-37-43',  # 37m, nominal, boxes
'unicornA_base1_2013-04-08-19-10-12',  # 15m, has occlusions for camera
'unicornA_base1_2013-04-03-12-58-11',  # :  17m, nominal, boxes
'unicornA_base1_2013-04-08-16-43-10',  #  25m, gripper not properly placed
'unicornA_base1_2013-04-06-15-30-06',  # 6m, nominal
'unicornA_base1_2013-04-03-16-36-03'  # 17m, nominal, ends for under-voltage
]

good_logs_cam_eye = [
'unicornA_base1_2013-04-03-13-30-28',  # 38m, nominal, ok
'unicornA_car1_2013-04-08-21-37-47',  # ??m, nominal
    # - unicornA_base1_2013-04-06-19-44-59',  people standing around; don't use for learning
'unicornA_tran1_2013-04-09-14-35-11',  # ??min, nominal
    # - unicornA_base1_2013-04-03-13-16-53',  7m, Crashes into curtains after 7 minutes; don't use for learning.
'unicornA_base1_2013-04-02-20-37-43',  # 37m, nominal, boxes
'unicornA_base1_2013-04-08-19-10-12',  # 15m, has occlusions for camera
'unicornA_base1_2013-04-03-12-58-11',  # :  17m, nominal, boxes
# 'unicornA_base1_2013-04-08-16-43-10',  #  25m, gripper not properly placed
'unicornA_base1_2013-04-06-15-30-06',  # 6m, nominal
'unicornA_base1_2013-04-03-16-36-03'  # 17m, nominal, ends for under-voltage
]


# good logs for hokuyo
good_logs_hokuyos = [
    'unicornA_base1_2013-04-11-20-14-27',
    # 'unicornA_tran1_2013-04-11-23-21-36', this is with 0.1 commands
    'unicornA_tran1_2013-04-12-22-29-16',
    'unicornA_tran1_2013-04-12-22-40-02',
    # 'unicornA_tran1_2013-04-12-23-34-08'  this is for testing (grid1)
]

grid1 = ['unicornA_tran1_2013-04-12-23-34-08']



from .exp01 import *
from .exp02 import *
from .exp03 import *
from .exp04 import *
from .exp05 import *
from .exp06 import *
from .exp07 import *
from .exp08 import *
from .exp09 import *
from .exp10 import *
from .exp11 import *  
from .exp12 import *
from .exp13 import *    
from .exp14 import *
from .exp15 import *
from .exp16 import *
from .exp17 import *
from .exp18 import *
from .exp19 import *
from .exp20diffeo import *
from .exp21 import *
from .exp22 import *
from .exp23 import *
from .exp24 import *
from .exp25 import *
from .exp26 import *
from .exp27 import *
from .exp28alldiffeos import *
from .exp29 import *
from .exp30 import *
from .exp30c import *
from .exp31 import *
from .exp32 import *
from .exp33fs import *
from .exp34 import *

from .exp40sim import *
