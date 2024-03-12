"""
sign_info.py

Creating the sign info class and associated functions.

SignInfo will be used to store all static Sign Information, such as:

name
text_desc
video_loc
image_loc
module_name

This will be used for the process of learning signs
"""
from price_testing.save_load2 import*

class SignInfo:
    def __init__(self, name, text_desc, video_loc, image_loc, module_name):
        self.name = name
        self.text_desc = text_desc
        self.video_loc = video_loc
        self.image_loc = image_loc
        self.module_name = module_name

    def display_sign_info(self):
        print(self.name)
        print(self.text_desc)
        print(self.video_loc)
        print(self.image_loc)
        print(self.module_name)


# Displaying the sign names to terminal. Only used in console version
def display_signs(chosen_mod, sign_info_list):
    chosen_mod_name = chosen_mod.module_name
    for si in sign_info_list:
        if si.module_name == chosen_mod_name:
            print(si.name)

def search_si_list(sign_name, sign_info_list):
    for si in sign_info_list:
        if si.name == sign_name:
            return si
    return None

# creating a sign info list to use in assessments and learning
def create_si_name_list(sign_info_list, mod_name):
    si_name_list = []
    for si in sign_info_list:
        if si.module_name == mod_name:
            si_name_list.append(si.name)
    return si_name_list



