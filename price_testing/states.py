"""
states.py

Used for navigating terminal version of program
"""

from common import *
from assessment import*
from save_load2 import*
from sandbox import*
import os.path

# Main loop replicates app in the console
def main():
    print("---THEIA ASL---")
    # states used to navigate different 'windows'. Acts similar to state machine
    state = STATE_NUM_START
    chosen_mod = None # used for keeping track of the module that has been selected by the user
    user_id = "who?"
    user_mod_data = None # will contain a list of module objects (used to keep track of user data)
    si = None # Represents the current sign selected when in the learning menu
    while True:
        while state == STATE_NUM_START:
            user_id = input("Please enter username: ")
            if os.path.isfile(f"../user_files/{user_id}_data.json") == False:
                print("new user!")
                mod_list = [MOD1, MOD2, MOD3, MOD4, MOD5, MOD6] # from common. Load new user with starter modules
                save_module_data(mod_list, f"../user_files/{user_id}_data")
            user_mod_data = load_module_objects(f"{user_id}_data")
            state = STATE_HOME

        # home page
        while state == STATE_HOME:
            print("\n\nHOMEPAGE\n")
            user_ip = int(input("1. Modules\n2. Statistics\n"))
            if user_ip == 1:
                state = STATE_MOD_LIST
            elif user_ip == 2:
                print("\n\nSTATISTICS\n")
                print_module_stats(user_mod_data)

        # listing learning modules
        while state == STATE_MOD_LIST:
            mod_index = list_modules(user_mod_data) # listing modules to user
            chosen_mod = user_mod_data[mod_index] # storing the module selected by user
            state = STATE_MOD

        # module page
        while state == STATE_MOD:
            print(f"\n{chosen_mod.module_name}")
            mod_input = input("1. Learn Signs\n2. Assessments\n3. Sandbox")
            if mod_input == "1":
                state = STATE_SIGN_LIST
            elif mod_input == "2":
                state = STATE_ASSESSMENTS
            elif mod_input == "3":
                state = STATE_SANDBOX
            elif mod_input == "back":
                state = STATE_MOD_LIST


        while state == STATE_SANDBOX:
            run_sandbox(chosen_mod)
            state = STATE_MOD


        while state == STATE_SIGN_LIST:
            display_signs(chosen_mod, SI_LIST)
            chosen_sign = input("enter name of sign: ")
            if chosen_sign == "back":
                state = STATE_MOD
            else:
                si = search_si_list(chosen_sign, SI_LIST)
                state = STATE_SIGN_INFO

        while state == STATE_SIGN_INFO:
            si.display_sign_info()
            state_sign_input = input("Try Sign(y/n)?")
            if state_sign_input == "y":
                learn_sign(chosen_mod, chosen_sign)
                save_module_data(user_mod_data, f"{user_id}_data")
            elif state_sign_input == "n":
                state = STATE_SIGN_LIST


        # Assessments page
        while state == STATE_ASSESSMENTS:
            print("\n\nASSESSMENTS\n")
            # TODO: Make it a list of assessments, add new high score variables to JSON
            print(f"1. Basic Assessment (high score: {chosen_mod.high_score})\n2. Smart Assessment (high score: {chosen_mod.high_score2})\n3. Redemption Assessment (high score: {chosen_mod.high_score3})\n4. Survival Assessment (high score: {chosen_mod.high_score4})\n")
            assess_num = (input("Choose an assessment:"))
            if assess_num == "1":
                full_process(chosen_mod)
                save_module_data(user_mod_data, f"{user_id}_data")
            elif assess_num == "2":
                smart_assessment(chosen_mod)
                save_module_data(user_mod_data, f"{user_id}_data")
            elif assess_num == "3":
                rounds_assessment(chosen_mod)
                save_module_data(user_mod_data, f"{user_id}_data")
            elif assess_num == "4":
                survival_assessment(chosen_mod)
                save_module_data(user_mod_data, f"{user_id}_data")
            elif assess_num == "back":
                state = STATE_MOD

    if(user_mod_data == None):
        print("yeah")
    else:
        print(user_mod_data)

if __name__ == "__main__":
    main()

