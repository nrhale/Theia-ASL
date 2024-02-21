import json

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


# Custom serialization method for custom classes
def custom_serializer(obj):
    if isinstance(obj, (Sign, Module)):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def save_module_data(modules, file_name):

    # Serialize to JSON with custom serialization
    json_data = json.dumps(modules, default=custom_serializer, indent=4)

    # Save to a file
    with open(f"{file_name}.json", "w") as json_file:
        json_file.write(json_data)

def load_module_data_dict(file_name):
    # Load data from the JSON file
    with open(f"{file_name}.json", "r") as json_file:
        loaded_modules_dicts = json.load(json_file)
        return loaded_modules_dicts

def load_mod_user_data(loaded_module_dicts):
    mods = []
    for module_dict in loaded_module_dicts:
        s_list = []
        for sign in module_dict['sign_list']:
            new_sign = Sign(sign['sign_name'], sign['assessed_count'], sign['correct_count'], sign['associated_module'])
            s_list.append(new_sign)

        new_mod = Module(module_dict['module_name'], module_dict['model'], s_list, module_dict['high_score'])
        mods.append(new_mod)
    return mods

def load_module_objects(file_name):
    module_dicts = load_module_data_dict(file_name)
    mods = load_mod_user_data(module_dicts)
    return mods

def print_module_stats(loaded_modules):
    for module in loaded_modules:
        print(f"\nModule Name: {module['module_name']}")
        print(f"Module Model: {module['model']}")
        for sign in module['sign_list']:
            accuracy = round(sign['correct_count'] / sign['assessed_count'] * 100)
            print(f"Sign Name: {sign['sign_name']}, Times Asked: {sign['assessed_count']}, Accuracy: {accuracy}%")


# Now `loaded_modules` contains the list of `Module` objects
# You can access the data as needed

if __name__ == "__main__":

    # Create some sample data
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

    save_module_data(mod_list, "mod_user_data")


    loaded_modules = load_module_data_dict("mod_user_data")

    for module in loaded_modules:
        print(f"\nModule Name: {module['module_name']}")
        print(f"Module Model: {module['model']}")
        for sign in module['sign_list']:
            accuracy = round(sign['correct_count'] / sign['assessed_count'] * 100)
            print(f"Sign Name: {sign['sign_name']}, Times Asked: {sign['assessed_count']}, Accuracy: {accuracy}%")

    load = load_module_objects("mod_user_data")
    #print("hi")


    """
    loaded_modules = load_module_data_dict("mod_user_data")

    mods = []
    for module_dict in loaded_modules:
        s_list = []
        for sign in module_dict['sign_list']:
            new_sign = Sign(sign['sign_name'], sign['assessed_count'], sign['correct_count'], sign['associated_module'])
            s_list.append(new_sign)

        new_mod = Module(module_dict['module_name'], module_dict['model'], s_list, module_dict['high_score'])
        mods.append(new_mod)
    #print("hi")
    """