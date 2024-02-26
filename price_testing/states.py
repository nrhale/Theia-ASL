"""
states.py

Used for navigating terminal version of program
"""

from common import *
from assessment import*
from save_load2 import*
import os.path

# Main loop replicates app in the console
def main():
    print("---THEIA ASL---")
    state = STATE_NUM_START
    chosen_mod = None
    user_id = "who?"
    user_mod_data = None
    while state == STATE_NUM_START:
        user_id = input("Please enter username: ")
        if os.path.isfile(f"./{user_id}_data.json") == False:
            print("new user!")
            mod_list = [mod1, mod2] # from common. Load new user with starter modules
            save_module_data(mod_list, f"{user_id}_data")
        user_mod_data = load_module_objects(f"{user_id}_data")
        state = STATE_HOME
    while state == STATE_HOME:
        print("\n\nHOMEPAGE\n")
        user_ip = int(input("1. Modules\n2. Statistics\n"))
        if user_ip == 1:
            state = STATE_MOD_LIST
        elif user_ip == 2:
            print("\n\nSTATISTICS\n")
            print_module_stats(user_mod_data)
    while state == STATE_MOD_LIST:
        mod_index = list_modules(user_mod_data)
        chosen_mod = user_mod_data[mod_index]
        state = STATE_MOD
    while state == STATE_MOD:
        print(f"\n{chosen_mod.module_name}")
        mod_input = int(input("1. Learn Signs\n2. Assessments\n"))
        if mod_input == 1:
            print("not yet implemented!")
        elif mod_input == 2:
            state = STATE_ASSESSMENTS
    while state == STATE_ASSESSMENTS:
        print("\n\nASSESSMENTS\n")
        print(f"1. Basic Assessment (high score: {chosen_mod.high_score})")
        assess_num = int(input("Choose an assessment:"))
        if assess_num == 1:
            full_process(chosen_mod)
            save_module_data(user_mod_data, f"{user_id}_data")


    if(user_mod_data == None):
        print("yeah")
    else:
        print(user_mod_data)

if __name__ == "__main__":
    main()

