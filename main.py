from photocard import *
from member import *
import csv
from enum import Enum


class UpdateCSVOption(Enum):
    PHOTOCARD = 1
    MEMBER = 2


PHOTOCARDS_CSV_FILE = "photocards.csv"
MEMBERS_CSV_FILE = "members.csv"

members_dicts = []
photocards_dicts = []

STAT_MAX_LEVEL = 16  # will update it once I know the scores of the higher stat levels

def update_csv(option):
    """'data' is a list of dictionaries, each dictionary representing either a member or photocard"""

    PHOTOCARDS_FIELDNAMES = ["Name", "Level", "Signature", "Trendy Up", "Piece Shape", "Piece Color"]
    MEMBERS_FIELDNAMES = ["Name", "Music", "Acting", "Fashion", "Charm"]

    if option == UpdateCSVOption.PHOTOCARD:
        csv_file = PHOTOCARDS_CSV_FILE
        fieldnames = PHOTOCARDS_FIELDNAMES
        data = photocards_dicts
    else:
        csv_file = MEMBERS_CSV_FILE
        fieldnames = MEMBERS_FIELDNAMES
        data = members_dicts

    with open(csv_file, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write the data rows
        for item in data:
            writer.writerow(item)


members_name_by_object = {}
with open(MEMBERS_CSV_FILE, "r", newline="") as members_data:
    reader = csv.DictReader(members_data)
    data = list(reader)
for row in data:
    if row["Name"].startswith("ROS"):
        row["Name"] = "ROSÉ"  # avoids encoding problem
    members_dicts.append(row)
    new_member = Member(row["Name"], int(row["Music"]), int(row["Acting"]), int(row["Fashion"]), int(row["Charm"]))
    members_name_by_object[row["Name"]] = new_member

# Read photocards
photocards_name_by_object = {}
with open(PHOTOCARDS_CSV_FILE, "r", newline="", encoding="utf-8") as photocards_data:
    reader = csv.DictReader(photocards_data)
    data = list(reader)
for row in data:
    row = {k: v for k, v in row.items() if v is not None and v != ''}  # remove entries that have no value
    if int(row["Level"]) > 0:
        photocard_name = row["Name"]
        if "ROS" in row["Name"]:  # assuming that any word that starts with 'ROS' implies 'ROSÉ'
            words = row["Name"].split(" ")
            photocard_name = " ".join(["ROSÉ's" if (word.startswith("ROS") and word.endswith("'s"))
                                        else "ROSÉ" if word.startswith("ROS")
                                        else word for word in words])  # fix encoding problem with ROSÉ's name
            row["Name"] = photocard_name
        photocards_dicts.append(row)
        if any([row["Name"].startswith(suit) for suit in suits]):
            photocard = Photocard1to4Stars(row["Name"], int(row["Level"]))
        else:
            piece_shape = FiveSquareShape(five_square_shapes_strings.index(row["Piece Shape"]) + 1)
            piece_color = Color(piece_colors.index(row["Piece Color"]) + 1)
            photocard = Photocard5Stars(row["Name"], int(row["Level"]),
                                        piece_shape, piece_color,
                                        int(row["Signature"]), int(row["Trendy Up"]))
        photocards_name_by_object[row["Name"]] = photocard
        members_name_by_object[photocard.get_member_name()].add_photocard(photocard)

# Main menu
print("Welcome to Blackpink: The Game Schedule Solver!\n")
while True:
    print("MAIN MENU")
    print(f"You have {len(photocards_name_by_object)} photocards.")
    for member in members_name_by_object:
        print(f"{members_name_by_object[member].get_number_of_photocards()} {member} photocards")
    print("Select option:\n")
    print("Manage photocards (p)\nManage member (m)\nSolve schedules (s)\nExit (e)")
    option = input().lower()
    print()
    if option == 'p':
        while True:
            print("PHOTOCARD MANAGEMENT MENU")
            print("Add photocard (a)\nRemove photocard (r)\nManage existing photocard (view stats, change level, trend up, signature) (m)\nReturn to main menu (mm)")
            photocard_option = input().lower()
            print()
            if photocard_option == "a":
                name = input("Enter photocard name: ")
                print()
                if name in photocards_name_by_object.keys():
                    print(f"Photocard of name '{name}' already exists!\n")
                    photocards_name_by_object[name].display_photocard_info()
                    print()
                    continue
                level = int(input("Enter photocard level: "))
                photocard_dict = {"Name": name, "Level": level}
                if any([name.startswith(s) for s in suits]):
                    new_photocard = Photocard1to4Stars(name, level)
                else:
                    piece_shape_string = input(f"Enter piece shape (either of {', '.join(five_square_shapes_strings)}): ").upper()
                    piece_shape = FiveSquareShape(five_square_shapes_strings.index(piece_shape_string) + 1)
                    piece_color_string = input(f"Enter piece color (either of {', '.join(piece_colors)}): ").strip().capitalize()
                    if piece_color_string not in piece_colors:
                        raise ValueError("The piece color should either be green, yellow, blue or red")
                    piece_color = Color(piece_colors.index(piece_color_string) + 1)
                    signature = input("Enter Signature number (from 0 to 5): ")
                    if signature not in [str(n) for n in range(6)]:
                        raise ValueError("Signature value must be from 0 to 5")
                    trendy_up = input("Enter Trendy Up number (from 0 to 3): ")
                    if trendy_up not in [str(n) for n in range(4)]:
                        raise ValueError("Trendy Up value must be from 0 to 3")
                    new_photocard = Photocard5Stars(name, level, piece_shape, piece_color, int(signature), int(trendy_up))
                    photocard_dict["Signature"] = signature
                    photocard_dict["Trendy Up"] = trendy_up
                    photocard_dict["Piece Shape"] = piece_shape_string
                    photocard_dict["Piece Color"] = piece_color_string
                photocards_name_by_object[name] = new_photocard
                members_name_by_object[new_photocard.get_member_name()].add_photocard(new_photocard) 
                photocards_dicts.append(photocard_dict)
                update_csv(UpdateCSVOption.PHOTOCARD)
                print("Photocard added\n")
                new_photocard.display_photocard_info()
                print()
            if photocard_option == "r":
                if len(photocards_name_by_object) == 0:
                    print("There are no photocards")
                    print()
                while len(photocards_name_by_object) > 0:
                    name = input("Enter name of the photocard you want to remove, or enter 'e' to exit: ")
                    print()
                    if name == 'e':
                        break
                    if name not in photocards_name_by_object.keys():
                        print(f"No photocard of name {name}\n")
                        continue
                    photocard_to_remove = photocards_name_by_object.pop(name)
                    members_name_by_object[photocard_to_remove.get_member_name()].remove_photocard(photocard_to_remove) 
                    photocards_dicts = list(filter(lambda d: d["Name"] != name, photocards_dicts))
                    update_csv(UpdateCSVOption.PHOTOCARD)
                    print("Photocard removed\n")
            if photocard_option == "m":
                manage_photocard_option = ""
                while manage_photocard_option != "mm":
                    name = input("Enter name of the photocard you want to manage, or enter 'e' to exit: ")
                    if name == 'e':
                        print()
                        break
                    print()
                    if name not in photocards_name_by_object.keys():
                        print(f"No photocard of name {name}\n")
                        continue
                    while True:
                        photocard_options = ["sl", "c"]
                        level_changed = False
                        signature_changed = False
                        trendy_up_changed = False
                        photocard = photocards_name_by_object[name]
                        photocard.display_photocard_info()
                        print()
                        print("Set photocard level (sl)")
                        if not photocard.is_max_level():
                            photocard_options += ["l", "ml"]
                            print("Level up photocard (l)")
                            print("Set photocard to max level (ml)")
                        if isinstance(photocard, Photocard5Stars):
                            photocard_options += ["ss", "st"]
                            print("Set signature (ss)")
                            if not photocard.is_max_signature():
                                photocard_options += ["as", "ms"]
                                print("Add signature (as)")
                                print("Set signature to max (ms)")
                            print("Set Trendy Up (st)")
                            if not photocard.is_max_trendy_up():
                                photocard_options += ["at", "mt"]
                                print("Add Trendy Up (at)")
                                print("Set Trendy Up to max (mt)")
                        print("Change photocard/exit (c)")
                        manage_photocard_option = input().lower()
                        print()
                        if manage_photocard_option not in photocard_options:
                            print(f"'{manage_photocard_option}' is not an option\n")
                            continue
                        if manage_photocard_option == "c":
                            break
                        elif manage_photocard_option == "sl":
                            level_changed = True
                            level = input(f"Enter the level that {photocard.get_photocard_name()} will be set to (between 1 and {photocard.get_max_level()}): ")
                            if level not in [str(l) for l in range(1, photocard.get_max_level() + 1)]:
                                print(f"{photocard.get_photocard_name()} can only range from level 1 to {photocard.get_max_level()}")
                                continue
                            photocard.set_level(int(level))
                        elif manage_photocard_option == "l":
                            level_changed = True
                            photocard.level_up()
                        elif manage_photocard_option == "ml":
                            level_changed = True
                            photocard.set_to_max_level()
                        # Update database
                        if level_changed:
                            for d in photocards_dicts:
                                if d["Name"] == photocard.get_photocard_name():
                                    d["Level"] = str(photocard.get_level())
                                    print()
                                    break
                        if manage_photocard_option == "ss":
                            signature_changed = True
                            signature = input(f"Enter the signature level that {photocard.get_photocard_name()} will be set to (between 0 and 5): ")
                            if signature not in [str(s) for s in range(6)]:
                                print("Signature for 5-star photocards can only range from 0 to 5")
                                continue
                            photocard.set_signature(int(signature))
                        elif manage_photocard_option == "as":
                            signature_changed = True
                            photocard.add_signature()
                        elif manage_photocard_option == "ms":
                            signature_changed = True
                            photocard.set_to_max_signature()
                        if signature_changed:
                            for d in photocards_dicts:
                                if d["Name"] == photocard.get_photocard_name():
                                    d["Signature"] = str(photocard.get_signature())
                                    print()
                                    break
                        if manage_photocard_option == "st":
                            trendy_up_changed = True
                            trendy_up = input(f"Enter the Trendy Up level that {photocard.get_photocard_name()} will be set to (between 0 and 3): ")
                            if trendy_up not in [str(s) for s in range(4)]:
                                print("Trendy Up for 5-star photocards can only range from 0 to 3")
                                continue
                            photocard.set_trendy_up(int(trendy_up))
                        elif manage_photocard_option == "at":
                            trendy_up_changed = True
                            photocard.add_trendy_up()
                        elif manage_photocard_option == "mt":
                            trendy_up_changed = True
                            photocard.set_to_max_trendy_up()
                        if trendy_up_changed:
                            for d in photocards_dicts:
                                if d["Name"] == photocard.get_photocard_name():
                                    d["Trendy Up"] = str(photocard.get_trendy_up())
                                    print()
                                    break
                        update_csv(UpdateCSVOption.PHOTOCARD)

            if photocard_option == "mm":
                break

    if option == 'm':
        while True:
            for member in members_name_by_object:
                members_name_by_object[member].display_member_info()
                print()
            print("MEMBER MANAGEMENT MENU\n")
            print("For each row, enter your desired selection. Separate each selection by a space.")
            print(" | ".join([f"{member_name} ({number})" for number, member_name in enumerate(members_name_by_object, start=1)]))
            print(" | ".join([f"{stat_name} ({number})" for number, stat_name in enumerate(stats_names, start=1)]))
            print("Set stat level (sl) | Level up stat (l)\nExample: '4 1 l' means LISA Music Level Up\n\nOR Return to main menu (mm)")
            member_option = input()
            if member_option == "mm":
                break
            if len(member_option.split(" ")) == 3:
                print()
                all_valid = True
                member_number, stat_number, operation = member_option.split(" ")
                if member_number not in [str(n) for n in range(1, 5)]:
                    all_valid = False
                    print("The member number must be from 1 to 4.")
                if stat_number not in [str(n) for n in range(1, 5)]:
                    all_valid = False
                    print("The stat number must be from 1 to 4.")
                operation = operation.lower()
                if operation not in ["sl", "l"]:
                    all_valid = False
                    print("The last option must be either 'sl' or 'l'.")
                if all_valid:
                    member_to_update = members_name_by_object[member_names[int(member_number) - 1]]
                    stat_to_update = None  # initialize
                    stat_number = int(stat_number)
                    for stat in Stat:
                        if stat.value == stat_number:
                            stat_to_update = stat
                            break
                    if operation == "sl":
                        level = input(f"Enter the level that {member_to_update.get_name()}'s {stats_names[stat_number - 1]} stat will be set to: ")
                        if level not in [str(l) for l in range(1, STAT_MAX_LEVEL + 1)]:  # I don't know the scores for higher stat levels yet
                            print(f"Stats can only range from level 1 to {STAT_MAX_LEVEL}")
                            continue
                        member_to_update.set_stat_level(stat_to_update, int(level))
                    else:
                        level = member_to_update.get_stats_levels()[stat_to_update] + 1
                        member_to_update.level_up_stat(stat_to_update)
                    for d in members_dicts:
                        if d["Name"] == member_to_update.get_name():
                            d[stats_names[stat_number - 1]] = str(level)
                            print()
                            break
                    update_csv(UpdateCSVOption.MEMBER)
            else:
                print("Please enter 3 prompts separated by a space")
            print()

    if option == 'e':
        break
