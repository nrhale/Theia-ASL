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
STATE_SANDBOX = 7

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
mod2 = Module("alphabet2", "model_def", s_list2, 2)

# Extract descriptions from descriptions.txt
descriptions = {}

# Re-open the file and process each line to extract descriptions
with open('descriptions.txt', 'r') as file:
    for line in file:
        if ': ' in line:  # Ensure the line contains a colon to separate the item and its description
            item, description = line.split(': ', 1)  # Split on the first colon found
            descriptions[item.strip()] = description.strip()

# Re-open the file and process each line to extract urls
with open('video_urls.txt', 'r') as file:
    for line in file:
        if ': ' in line:  # Ensure the line contains a colon to separate the item and its description
            item, urls = line.split(': ', 1)  # Split on the first colon found
            urls[item.strip()] = urls.strip()
            
# Sign Info (always stays the same)
siA = SignInfo("A", descriptions.get('A'), urls.get('A'), "../asl_images/letter_a.svg", "alphabet1")
siB = SignInfo("B", descriptions.get('B'), urls.get('B'), "../asl_images/letter_b.svg", "alphabet1")
siC = SignInfo("C", descriptions.get('C'), urls.get('C'), "../asl_images/letter_c.svg", "alphabet1")

siD = SignInfo("D", descriptions.get('D'), urls.get('D'), "../asl_images/letter_d.svg", "alphabet2")
siE = SignInfo("E", descriptions.get('E'), urls.get('E'), "../asl_images/letter_e.svg", "alphabet2")
siF = SignInfo("F", descriptions.get('F'), urls.get('F'), "../asl_images/letter_f.svg", "alphabet2")

SI_LIST = [siA, siB, siC, siD, siE, siF]

