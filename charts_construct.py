import csv
from dim_weight_process import dim_ore_data

# convert data from weight to percentage
def weight_to_prob(dim_ore_data):
    for dimension, ores in dim_ore_data.items():
        total_weight = sum(ores.values())
        if total_weight > 0:
            for ore in ores:
                ores[ore] = (ores[ore] / total_weight) * 100
        else:
            for ore in ores:
                ores[ore] = 0

    return dim_ore_data

dim_ore_prob = weight_to_prob(dim_ore_data)

# function to csv file
def generate_csv_from_data(data, output_file_path):
    all_ore_types = set()
    for ores in data.values():
        all_ore_types.update(ores.keys())
    all_ore_types = sorted(all_ore_types)
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        dimensions = list(data.keys())
        writer.writerow(['Ore Type'] + dimensions)

        for ore_type in all_ore_types:
            row = [ore_type]
            for dimension in dimensions:
                row.append(data.get(dimension, {}).get(ore_type, ''))
            writer.writerow(row)

output_file_path = 'output.csv'
generate_csv_from_data(dim_ore_prob, output_file_path)

print(f"CSV file generated successfully at {output_file_path}")