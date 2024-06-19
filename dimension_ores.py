import pandas as pd
import re

# parse .cfg data for lookup
file_path = 'src\WorldGeneration.cfg'
with open(file_path, 'r') as file:
    content = file.readlines()

def custom_parser(content):
    current_section = []
    config_dict = {}

    for line in content:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        elif line.endswith('{'):
            section_name = line[:-2].strip()
            current_section.append(section_name)
        elif line == '}':
            if current_section:
                current_section.pop()
        else:
            key, value = line.split('=')
            full_section_name = '.'.join(current_section)
            config_dict.setdefault(full_section_name, {})[key.strip()] = value.strip()

    return config_dict

def clean_keys(ore_data):
    cleaned_data = {}
    for ore, properties in ore_data.items():
        cleaned_properties = {}
        for key, value in properties.items():
            # Remove '_false' or '_true' and any confusing info from keys
            new_key = re.sub(r'_false|_true', '', key.replace('"', ''))
            cleaned_properties[new_key] = value
        cleaned_data[ore] = cleaned_properties
    return cleaned_data

config_data = clean_keys(custom_parser(content))

# build ore data for use
ore_vein_data = {}
small_ore_data = {}

for key, values in config_data.items():
    if "worldgen.ore.mix" in key:
        ore_vein = key.split('.')[-1]
        ore_vein_data[ore_vein] = values
    elif "worldgen.ore.small" in key:
        small_ore = key.split('.')[-1]
        small_ore_data[small_ore] = values

# define all dims
dimensions = [
    'Overworld', 'Nether', 'Twillight Forest', 'End', 'End Astorid', 'Moon', 'Deimos', 'Mars', 'Phobos', 'Asteroids', 'Callisto', 'Ceres', 'Europa', 'Ganymede', 'Io', 'Mercury', 'Venus', 'Enceladus', 'Miranda', 'Oberon', 'Titan', 'Proteus', 'Triton', 'Haumea', 'Kuiper Belt', 'Makemake', 'Pluto', 'aCentauriBb', 'BarnardaC', 'BarnardaE', 'BarnardaF', 'TCetiE', 'VegaB', 'Horus', 'Maahes', 'Anubis', 'Neper', 'Seth', 'Mehen Belt'
]
parsed_dimensions = [
    'B:Overworld', 'B:Nether', 'B:"Twilight Forest', 'B:"The End', 'B:Vanilla_EndAsteroids', 'B:GalacticraftCore_Moon', 'B:GalaxySpace_Deimos', 'B:GalacticraftMars_Mars', 'B:GalaxySpace_Phobos', 'B:GalacticraftMars_Asteroids','B:GalaxySpace_Callisto', 'B:GalaxySpace_Ceres', 'B:GalaxySpace_Europa', 'B:GalaxySpace_Ganymede', 'B:GalaxySpace_Io', 'B:GalaxySpace_Mercury', 'B:GalaxySpace_Venus', 'B:GalaxySpace_Enceladus', 'B:GalaxySpace_Miranda', 'B:GalaxySpace_Oberon','B:GalaxySpace_Titan', 'B:GalaxySpace_Proteus', 'B:GalaxySpace_Triton', 'B:GalaxySpace_Haumea', 'B:GalaxySpace_Kuiperbelt', 'B:GalaxySpace_MakeMake', 'B:GalaxySpace_Pluto', 'B:GalaxySpace_CentauriA', 'B:GalaxySpace_BarnardC','B:GalaxySpace_BarnardE', 'B:GalaxySpace_BarnardF', 'B:GalaxySpace_TcetiE', 'B:GalaxySpace_VegaB', 'B:GalacticraftAmunRa_Horus', 'B:GalacticraftAmunRa_Maahes', 'B:GalacticraftAmunRa_Anubis', 'B:GalacticraftAmunRa_Neper', 'B:GalacticraftAmunRa_Seth', 'B:"GalacticraftAmunRa_Mehen Belt'
]

# build ore lists in certain dim
def determine_ore_presence(ore_data, dimensions, parsed_dimensions):
    ore_presence = {dim: [] for dim in dimensions}

    cleaned_ore_data = clean_keys(ore_data)

    for dim, parsed_dim in zip(dimensions, parsed_dimensions):
        cleaned_dim = parsed_dim.replace('"', '')
        for ore, values in cleaned_ore_data.items():
            if cleaned_dim in values and values[cleaned_dim].lower() == 'true':
                ore_presence[dim].append(ore)

    return ore_presence

dimension_ore_veins_presence = determine_ore_presence(ore_vein_data, dimensions, parsed_dimensions)
dimension_small_ore_presence = determine_ore_presence(small_ore_data, dimensions, parsed_dimensions)
dimension_small_ore_presence['Overworld'].append('tellurium')