from ore_materials import ore_vein_data, small_ore_data
from dimension_ores import dimension_ore_veins_presence, dimension_small_ore_presence

# functions to process vein data
def dim_to_ore_by_vein(dim_veins, vein_ores):
    data_fin = {}
    for dim, veins in dim_veins.items():
        data_ore = {}
        # use vein data to construct current dim's ore weight data
        for i in veins:
            curr_vein = vein_ores[i]
            for layer in curr_vein:
                curr_add = curr_vein[layer]
                if curr_add[0] in data_ore:
                    data_ore[curr_add[0]] += curr_add[1]
                else:
                    data_ore[curr_add[0]] = curr_add[1]
        data_fin[dim] = {k: data_ore[k] for k in sorted(data_ore)}
    return data_fin

# functions to process small ore data
def dim_to_ore_by_small(dim_small, small_ore):
    data_fin = {}
    for dim, smalls in dim_small.items():
        data_ore = {}
        for small in smalls:
            curr_small = small_ore[small]
            ore, weight = next(iter(curr_small.items()))
            if ore in data_ore:
                data_ore[ore] += weight
            else:
                data_ore[ore] = weight
        data_fin[dim] = {k: data_ore[k] for k in sorted(data_ore)}
    return data_fin

dim_ore_data_1 = dim_to_ore_by_vein(dimension_ore_veins_presence, ore_vein_data)
dim_ore_data_2 = dim_to_ore_by_small(dimension_small_ore_presence, small_ore_data)

# function to conbine two data sets
def merge_ore_data(data1, data2):
    combined_data = {}
    def add_to_combined(data, key):
        if key in combined_data:
            for ore, weight in data[key].items():
                if ore in combined_data[key]:
                    combined_data[key][ore] += weight
                else:
                    combined_data[key][ore] = weight
        else:
            combined_data[key] = data[key]
    for dimension in data1:
        add_to_combined(data1, dimension)
    for dimension in data2:
        add_to_combined(data2, dimension)
    for dimension in combined_data:
        combined_data[dimension] = {k: combined_data[dimension][k] for k in sorted(combined_data[dimension])}
    return combined_data

dim_ore_data = merge_ore_data(dim_ore_data_1, dim_ore_data_2)