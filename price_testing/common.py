# Constant Variables
from save_load2 import*
from sign_info import*

STATE_NUM_START = 0
STATE_HOME = 1
STATE_MOD_LIST = 2
STATE_MOD = 3
STATE_ASSESSMENTS = 4
STATE_SIGN_LIST = 5
STATE_SIGN_INFO = 6


# Some Default information. Will change later
#s1 = Sign("A", 0, 0, "alphabet1")
s2 = Sign("B", 0, 0, "alphabet1")
s3 = Sign("C", 0, 0, "alphabet1")

s4 = Sign("D", 0, 0, "alphabet2")
s5 = Sign("E", 0, 0, "alphabet2")
s6 = Sign("F", 0, 0, "alphabet2")

s_list1 = [s2, s3]
s_list2 = [s4, s5, s6]

mod1 = Module("alphabet1", "model3", s_list1, 0)
mod2 = Module("alphabet2", "model3", s_list2, 2)

# Sign Info (always stays the same)

siA = SignInfo("A", "*text desc A*", "*video_loc for A*", "*image_loc for A*", "alphabet1")
siB = SignInfo("B", "*text desc B*", "*video_loc for B*", "*image_loc for B*", "alphabet1")
siC = SignInfo("C", "*text desc C*", "*video_loc for C*", "*image_loc for C*", "alphabet1")

siD = SignInfo("D", "*text desc D*", "*video_loc for D*", "*image_loc for D*", "alphabet2")
siE = SignInfo("E", "*text desc E*", "*video_loc for E*", "*image_loc for E*", "alphabet2")
siF = SignInfo("F", "*text desc F*", "*video_loc for F*", "*image_loc for F*", "alphabet2")

SI_LIST = [siA, siB, siC, siD, siE, siF]

