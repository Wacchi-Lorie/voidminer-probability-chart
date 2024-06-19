import re

# parse java source code to python list
def javasrc_to_list(file_path, class_to_find):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    pattern = re.compile('new ' + class_to_find + r'\((.*?)\);', re.DOTALL)

    constructors_list = []

    matches = pattern.finditer(data)
    for match in matches:
        params = match.group(1).replace('\n', '').replace(' ', '').split(',')
        params = [param.strip().strip('"') for param in params if param.strip()]
        constructors_list.append(params)

    return constructors_list

# format small ore lists by removing booleans
def clean_up_list(nested_list):
    cleaned_list = []
    for item in nested_list:
        if isinstance(item, list):
            result = clean_up_list(item)
            if result:
                cleaned_list.append(result)
        elif not (isinstance(item, bool) or (isinstance(item, str) and item.lower() in ["true", "false"])):
            cleaned_list.append(item)
    return cleaned_list

file_path = 'src\GT_Worldgenloader.java'
ore_vein_lists = javasrc_to_list(file_path, "GT_Worldgen_GT_Ore_Layer")
small_ore_lists = clean_up_list(javasrc_to_list(file_path, "GT_Worldgen_GT_Ore_SmallPieces"))

# build ore veins and small ores detailed data
def extract_ore_vein_data(ore_lists):
    ore_data = {}
    for ore in ore_lists:
        if len(ore) == 14:
            ore_vein_name = ore[0].replace('ore.mix.', '')
            weight = int(ore[4])
            primary_material = ore[10].split('.')[-1].replace('Materials.', '')
            secondary_material = ore[11].split('.')[-1].replace('Materials.', '')
            between_material = ore[12].split('.')[-1].replace('Materials.', '')
            sporadic_material = ore[13].split('.')[-1].replace('Materials.', '')

            ore_data[ore_vein_name] = {
                "primary": [primary_material, weight],
                "secondary": [secondary_material, weight],
                "between": [between_material, weight / 8.0],
                "sporadic": [sporadic_material, weight / 8.0]
            }
    return ore_data

def extract_small_ore_data(small_ore_lists):
    small_ore_data = {}
    for ore in small_ore_lists:
        if len(ore) == 5:
            ore_name = ore[0].replace('ore.small.', '')
            material_name = ore[4].replace('Materials.', '')
            weight = int(ore[3])

            small_ore_data[ore_name] = {
                material_name: weight
            }

    return small_ore_data

ore_vein_data = extract_ore_vein_data(ore_vein_lists)
small_ore_data = extract_small_ore_data(small_ore_lists)
small_ore_data['tellurium'] = {'Tellurium': 8}