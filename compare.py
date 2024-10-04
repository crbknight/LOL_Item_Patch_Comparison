import csv
import os

def load_items(file_path):
    # Loads item data from a CSV file into a dictionary where key is item name.
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return {row['Name']: row for row in reader}

def compare_items(old_items, new_items, stats_columns, output_file):
    # Compares two dictionaries of items and writes results to a text file.
    old_item_names = set(old_items.keys())
    new_item_names = set(new_items.keys())

    with open(output_file, 'w') as f:
        # Find removed items
        removed_items = old_item_names - new_item_names
        if removed_items:
            f.write("Removed Items:\n")
            for item in removed_items:
                f.write(f"  - {item}\n")
        else:
            f.write("No items removed.\n")

        # Find added items
        added_items = new_item_names - old_item_names
        if added_items:
            f.write("\nAdded Items:\n")
            for item in added_items:
                f.write(f"  - {item}\n")
        else:
            f.write("No items added.\n")

        # Find changed items
        common_items = old_item_names & new_item_names
        if common_items:
            f.write("\nChanged Items:\n")
            for item in common_items:
                old_item = old_items[item]
                new_item = new_items[item]

                # Track changes in stats and gold efficiency
                stat_changes = []
                for stat in stats_columns:
                    old_stat_value = old_item.get(stat, '0')
                    new_stat_value = new_item.get(stat, '0')

                    # Handle cases where the stat values are missing or non-numeric
                    try:
                        old_stat_value = float(old_stat_value)
                    except ValueError:
                        old_stat_value = 0.0

                    try:
                        new_stat_value = float(new_stat_value)
                    except ValueError:
                        new_stat_value = 0.0

                    # Compare old and new stat values
                    if old_stat_value != new_stat_value:
                        # Append [N] for nerf and [B] for buff
                        change_flag = "[N] " if new_stat_value < old_stat_value else "[B] "
                        stat_changes.append(f"{change_flag}{stat}: {old_stat_value} -> {new_stat_value}")

                old_ge = float(old_item['Gold Efficiency'])
                new_ge = float(new_item['Gold Efficiency'])

                # Display changes if any stats or gold efficiency changed
                if stat_changes or old_ge != new_ge:
                    f.write(f"  - {item}:\n")
                    if stat_changes:
                        f.write(f"    Stat Changes:\n")
                        for change in stat_changes:
                            f.write(f"      {change}\n")
                    if old_ge != new_ge:
                        # Prepend [N] for nerf and [B] for buff in GE
                        change_flag_ge = "[N] " if new_ge < old_ge else "[B] "
                        f.write(f"    Gold Efficiency: {change_flag_ge}{old_ge} -> {new_ge}\n")
        else:
            f.write("No items changed.\n")


def find_csv_file(folder):
    # Find the first CSV file in the specified folder.
    for file_name in os.listdir(folder):
        if file_name.endswith('.csv'):
            return os.path.join(folder, file_name)
    return None

stats_columns = [
    'Attack Damage', 'Abilty Power', 'Attack Speed', 'Ability Haste', 
    'Armor', 'Magic Resist', 'Health', 'Mana', 'Health Regen', 
    'Mana Regen', 'Crit Chance', 'Movement Speed (Flat)', '% Movement Speed', 
    'Lethality', '% Armor Pen', 'Magic Pen (Flat)', '% Magic Pen', 
    'Heal/Shield Power', 'Lifesteal', 'Tenacity'
]

# Define the directories for old and new patches
old_patch_folder = 'old_patch'
new_patch_folder = 'new_patch'

# Find the CSV files in each folder
old_file = find_csv_file(old_patch_folder)
new_file = find_csv_file(new_patch_folder)

# Ensure both files are found
if old_file and new_file:
    # Load the old and new CSV files
    old_items = load_items(old_file)
    new_items = load_items(new_file)

    # Compare the two files and write the output to a text file
    output_file = 'output.txt'
    compare_items(old_items, new_items, stats_columns, output_file)
    
    print(f"Comparison complete. Results written to {output_file}")
else:
    if not old_file:
        print(f"No CSV file found in {old_patch_folder}")
    if not new_file:
        print(f"No CSV file found in {new_patch_folder}")
