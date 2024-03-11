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

LIVES = 3

# Some Default information. Will change later
#s1 = Sign("A", 0, 0, "alphabet1")
s2 = Sign("B", 0, 0, "The Alphabet I")
s3 = Sign("C", 0, 0, "The Alphabet I")

#s4 = Sign("D", 0, 0, "alphabet1")
#s5 = Sign("E", 0, 0, "alphabet1")
#s6 = Sign("F", 0, 0, "alphabet1")

s_list1 = [s2, s3]
#s_list2 = [s4, s5, s6]
s_list2 = []
s_list3 = []
s_list4 = []
s_list5 = []
s_list6 = []

MOD1 = Module("The Alphabet I", "valid_alphabet_a_to_f", s_list1, 0)
MOD2 = Module("The Alphabet II", "valid_alphabet_g_to_m", s_list2, 0)
MOD3 = Module("The Alphabet III", "valid_alphabet_n_to_s", s_list3, 0)
MOD4 = Module("The Alphabet IV", "valid_alphabet_t_to_y", s_list4, 0)
MOD5 = Module("Numbers I: Even Numbers", "valid_num_even", s_list5, 0)
MOD6 = Module("Numbers II: Odd Numbers", "valid_num_odd2", s_list6, 0)

ALL_MODS = [MOD1, MOD2, MOD3, MOD4, MOD5, MOD6] # Currently use mod_list in states instead

# Extract descriptions from descriptions.txt
descriptions = {}

# Extract urls from video_urls.txt
urls = {}

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
            item, url = line.split(': ', 1)  # Split on the first colon found
            urls[item.strip()] = url.strip()
            
# Sign Info (always stays the same)
siA = SignInfo("A", descriptions.get('A'), urls.get('A'), "../asl_images/letter_a.svg", "The Alphabet I")
siB = SignInfo("B", descriptions.get('B'), urls.get('B'), "../asl_images/letter_b.svg", "The Alphabet I")
siC = SignInfo("C", descriptions.get('C'), urls.get('C'), "../asl_images/letter_c.svg", "The Alphabet I")
siD = SignInfo("D", descriptions.get('D'), urls.get('D'), "../asl_images/letter_d.svg", "The Alphabet I")
siE = SignInfo("E", descriptions.get('E'), urls.get('E'), "../asl_images/letter_e.svg", "The Alphabet I")
siF = SignInfo("F", descriptions.get('F'), urls.get('F'), "../asl_images/letter_f.svg", "The Alphabet I")

siG = SignInfo("G", descriptions.get('G'), urls.get('G'), "../asl_images/letter_g.svg", "The Alphabet II")
siH = SignInfo("H", descriptions.get('H'), urls.get('H'), "../asl_images/letter_h.svg", "The Alphabet II")
siI = SignInfo("I", descriptions.get('I'), urls.get('I'), "../asl_images/letter_i.svg", "The Alphabet II")
siK = SignInfo("K", descriptions.get('K'), urls.get('K'), "../asl_images/letter_k.svg", "The Alphabet II")
siL = SignInfo("L", descriptions.get('L'), urls.get('L'), "../asl_images/letter_l.svg", "The Alphabet II")
siM = SignInfo("M", descriptions.get('M'), urls.get('M'), "../asl_images/letter_m.svg", "The Alphabet II")

siN = SignInfo("N", descriptions.get('N'), urls.get('N'), "../asl_images/letter_n.svg", "The Alphabet III")
siO = SignInfo("O", descriptions.get('O'), urls.get('O'), "../asl_images/letter_o.svg", "The Alphabet III")
siP = SignInfo("P", descriptions.get('P'), urls.get('P'), "../asl_images/letter_p.svg", "The Alphabet III")
siQ = SignInfo("Q", descriptions.get('Q'), urls.get('Q'), "../asl_images/letter_q.svg", "The Alphabet III")
siR = SignInfo("R", descriptions.get('R'), urls.get('R'), "../asl_images/letter_r.svg", "The Alphabet III")
siS = SignInfo("S", descriptions.get('S'), urls.get('S'), "../asl_images/letter_s.svg", "The Alphabet III")

siT = SignInfo("T", descriptions.get('T'), urls.get('T'), "../asl_images/letter_t.svg", "The Alphabet IV")
siU = SignInfo("U", descriptions.get('U'), urls.get('U'), "../asl_images/letter_u.svg", "The Alphabet IV")
siV = SignInfo("V", descriptions.get('V'), urls.get('V'), "../asl_images/letter_v.svg", "The Alphabet IV")
siW = SignInfo("W", descriptions.get('W'), urls.get('W'), "../asl_images/letter_w.svg", "The Alphabet IV")
siX = SignInfo("X", descriptions.get('X'), urls.get('X'), "../asl_images/letter_x.svg", "The Alphabet IV")
siY = SignInfo("Y", descriptions.get('Y'), urls.get('Y'), "../asl_images/letter_y.svg", "The Alphabet IV")

si0 = SignInfo("0", descriptions.get('0'), urls.get('0'), "../asl_images/number_0.svg", "Numbers I: Even Numbers")
si1 = SignInfo("1", descriptions.get('1'), urls.get('1'), "../asl_images/number_1.svg", "Numbers II: Odd Numbers")
si2 = SignInfo("2", descriptions.get('2'), urls.get('2'), "../asl_images/number_2.svg", "Numbers I: Even Numbers")
si3 = SignInfo("3", descriptions.get('3'), urls.get('3'), "../asl_images/number_3.svg", "Numbers II: Odd Numbers")
si4 = SignInfo("4", descriptions.get('4'), urls.get('4'), "../asl_images/number_4.svg", "Numbers I: Even Numbers")

si5 = SignInfo("5", descriptions.get('5'), urls.get('5'), "../asl_images/number_5.svg", "Numbers II: Odd Numbers")
si6 = SignInfo("6", descriptions.get('6'), urls.get('6'), "../asl_images/number_6.svg", "Numbers I: Even Numbers")
si7 = SignInfo("7", descriptions.get('7'), urls.get('7'), "../asl_images/number_7.svg", "Numbers II: Odd Numbers")
si8 = SignInfo("8", descriptions.get('8'), urls.get('8'), "../asl_images/number_8.svg", "Numbers I: Even Numbers")
si9 = SignInfo("9", descriptions.get('9'), urls.get('9'), "../asl_images/number_9.svg", "Numbers II: Odd Numbers")




SI_LIST = [siA, siB, siC, siD, siE, siF, siG, siH, siI, siK, siL, siM, siN, siO, siP, siQ, siR, siS, siT, siU, siV, siW, siX, siY, si0, si1, si2, si3, si4, si5, si6, si7, si8, si9]

