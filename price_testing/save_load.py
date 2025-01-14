"""
save_load.py

This file is for saving and loading information to text files

This may be replaced later using React methods
"""
import pickle
import json

# Creating classes for keeping track of user data
class Sign:
    def __init__(self, sign_name, assessed_count, correct_count, associated_module):
        self.sign_name = sign_name
        self.assessed_count = assessed_count
        self.correct_count = correct_count
        self.associated_module = associated_module

class Module:
    def __init__(self, module_name, model, sign_list=[], high_score=0):
        self.module_name = module_name
        self.model = model
        self.sign_list = sign_list
        self.sign_name_list = self.get_sign_names()
        self.high_score = high_score


    # Get a list of signs names so that the actual sign_list doesn't have to make one each assessment
    def get_sign_names(self):
        sign_names = []
        for sign in self.sign_list:
            sign_names.append(sign.sign_name)
        return sign_names



"""
def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
"""

# user must have a list of modules and a list of signs that they know

# Loads user data from a JSON file and returns module_list and sign_list.

"""
def load_user_data(file_name):
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
            sign_list = [Sign(**item) for item in data[0]]
            module_list = [Module(**item) for item in data[1]]
            return module_list, sign_list
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None, None
"""

# Loads user data from a JSON file and returns module_list and sign_list.
def load_user_data(file_name):
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
            # the below lines are creating lists of their respective objects. It first checks if it is a Sign or Module,
            # and then adds it to its associated list accordingly
            sign_list = [Sign(item["sign_name"], item["assessed_count"], item["correct_count"], item["associated_module"]) for item in data if "sign_name" in item]
            module_list = [Module(item["module_name"], item["sign_list"], item["high_score"]) for item in data if
                           "module_name" in item]
            return module_list, sign_list
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None, None


"""

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Sign, Module)):
            return obj.__dict__
        return super().default(obj)

def save_user_data(file_name, sign_list, module_list):
    data = {"sign_list": sign_list, "module_list": module_list}
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4, cls=CustomEncoder)
"""

# Saves user data to a JSON file.
def save_user_data(file_name, sign_list, module_list):

    # Convert Sign objects to dictionaries (must be done to store an object in JSON)
    sign_dicts = [{"sign_name": s.sign_name, "assessed_count": s.assessed_count, "correct_count": s.correct_count, "associated_module": s.associated_module} for s in sign_list]
    # Convert Module objects to dictionaries
    module_dicts = [{"module_name": m.module_name, "model": m.model, "sign_list": m.sign_list, "sign_name_list": m.sign_name_list, "high_score": m.high_score} for m in module_list]
    # Combine sign_dicts and module_dicts (must be done in order to put both in a JSON together)
    data = sign_dicts + module_dicts

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


def save_module_data(module_list, filename):
    with open(filename, 'w') as json_file:
        json.dump([module.__dict__ for module in module_list], json_file, indent=4)

def load_module_data(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        module_list = [Module(**module_data) for module_data in data]
        return module_list



def save_user_data_pickle(file_name, module_list):

    with open(file_name, "wb") as f:
        pickle.dump(module_list, f)  # Save list2


# Example usage
if __name__ == "__main__":
    """

    s1 = Sign("A", 10, 9, "alphabet1")
    s2 = Sign("B", 5, 4, "alphabet1")
    s3 = Sign("C", 10, 4, "alphabet1")

    s4 = Sign("D", 2, 1, "alphabet2")
    s5 = Sign("E", 3, 2, "alphabet2")
    s6 = Sign("F", 5, 4, "alphabet2")

    s_list1 = [s1, s2, s3]
    s_list2 = [s4, s5, s6]

    mod_list = []
    mod1 = Module("alphabet1", "model3", s_list1, 0)
    mod2 = Module("alphabet2", "model3", s_list2, 2)
    mod_list.append(mod1)
    mod_list.append(mod2)

    username = "price2"
    #save_module_data(mod_list, f"{username}.json")
    save_user_data_pickle(f"{username}.json", mod_list)

    #loaded_modules = load_module_data(f"{username}.json")
    """

    # saving test
    

    s1 = Sign("A", 10, 9, "alphabet1")
    s2 = Sign("B", 5, 4, "alphabet1")
    s3 = Sign("C", 10, 4, "alphabet1")

    s4 = Sign("D", 2, 1, "alphabet2")
    s5 = Sign("E", 3, 2, "alphabet2")
    s6 = Sign("F", 5, 4, "alphabet2")

    s_list1 = [s1, s2, s3]
    s_list2 = [s4, s5, s6]

    mod_list = []
    mod1 = Module("alphabet1", "model3", s_list1, 0)
    mod2 = Module("alphabet2", "model3", s_list2, 2)
    mod_list.append(mod1)
    mod_list.append(mod2)

    username = "price2"
    save_user_data(f"{username}.json", s_list1, mod_list)

    """
    # loading test
    username = "price2"
    loaded_module_list, loaded_sign_list = load_user_data(f"{username}.json")
    if loaded_module_list and loaded_sign_list:
        print("Loaded module_list:")
        for module in loaded_module_list:
            print(f"Module Name: {module.module_name}, Signs: {module.sign_list}")

        print("\nLoaded sign_list:")
        for sign in loaded_sign_list:
            print(f"Sign Name: {sign.sign_name}, Assessed Count: {sign.assessed_count}, Correct Count: {sign.correct_count}")
    else:
        print("Error loading data.")    
        
    """

"""
if __name__ == "__main__":
    # saving test
    mod_list = []
    mod1 = Module("alphabet1", ["A", "B", "C"], 0)
    mod2 = Module("alphabet2", ["D", "E", "F"], 2)
    mod_list.append(mod1)
    mod_list.append(mod2)

    s1 = Sign("A", 10, 99, "alphabet1")
    s2 = Sign("B", 5, 58, "alphabet1")
    s_list = [s1, s2]
    username = "price"
    save_user_data(f"{username}.json", s_list, mod_list)

"""