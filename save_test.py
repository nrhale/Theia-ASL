import json

class Sign:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Module:
    def __init__(self, module_id, signs):
        self.module_id = module_id
        self.signs = signs

# Create some sample data
sign1 = Sign("Stop", "Stop sign description")
sign2 = Sign("Yield", "Yield sign description")
module1 = Module(1, [sign1, sign2])
module2 = Module(2, [sign2])

# Custom serialization method for custom classes
def custom_serializer(obj):
    if isinstance(obj, (Sign, Module)):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# Serialize to JSON with custom serialization
json_data = json.dumps([module1, module2], default=custom_serializer, indent=4)

# Save to a file
with open("modules.json", "w") as json_file:
    json_file.write(json_data)


# Load data from the JSON file
with open("modules.json", "r") as json_file:
    loaded_modules = json.load(json_file)

# Now `loaded_modules` contains the list of `Module` objects
# You can access the data as needed
for module in loaded_modules:
    print(f"Module ID: {module['module_id']}")
    for sign in module['signs']:
        print(f"Sign Name: {sign['name']}, Description: {sign['description']}")