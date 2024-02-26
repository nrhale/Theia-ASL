# Constant Variables
from save_load2 import*

STATE_NUM_START = 0
STATE_HOME = 1
STATE_MOD_LIST = 2
STATE_MOD = 3
STATE_ASSESSMENTS = 4


# Some Default information. Will change later
s1 = Sign("A", 0, 0, "alphabet1")
s2 = Sign("B", 0, 0, "alphabet1")
s3 = Sign("C", 0, 0, "alphabet1")

s4 = Sign("D", 0, 0, "alphabet2")
s5 = Sign("E", 0, 0, "alphabet2")
s6 = Sign("F", 0, 0, "alphabet2")

s_list1 = [s1, s2, s3]
s_list2 = [s4, s5, s6]

mod1 = Module("alphabet1", "model3", s_list1, 0)
mod2 = Module("alphabet2", "model3", s_list2, 2)

