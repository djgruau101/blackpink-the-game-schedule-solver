from photocard import *
import csv

CSV_FILE = "photocards.csv"

def update_csv(photocards_data, csv_file):
    """Input is a list of dictionaries, each dictionary representing a photocard"""
    
    fieldnames = ["Name", "Level", "Signature", "Trendy Up", "Piece Shape", "Piece Color"]

    with open(csv_file, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write the data rows
        for photocard in photocards_data:
            writer.writerow(photocard)


# Read photocards
photocards_dicts = []
photocards_name_by_object = {}
with open(CSV_FILE, "r", newline="", encoding="utf-8") as photocards_data:
    reader = csv.DictReader(photocards_data)
    data = list(reader)
for row in data:
    row = {k: v for k, v in row.items() if v is not None and v != ''}  # remove entries that have no value
    if int(row["Level"]) > 0:
        photocard_name = row["Name"]
        if "ROS" in row["Name"]:
            words = row["Name"].split(" ")
            photocard_name = " ".join(["ROSÉ's" if (word.startswith("ROS") and word.endswith("'s"))
                                        else "ROSÉ" if word.startswith("ROS")
                                        else word for word in words])  # fix encoding problem with ROSÉ's name
            row["Name"] = photocard_name
        photocards_dicts.append(row)
        if any([row["Name"].startswith(suit) for suit in suits]):
            photocards_name_by_object[row["Name"]] = Photocard1to4Stars(row["Name"], int(row["Level"]))
        else:
            piece_shape = FiveSquareShape(five_square_shapes_strings.index(row["Piece Shape"]) + 1)
            piece_color = Color(piece_colors.index(row["Piece Color"]) + 1)
            
            photocards_name_by_object[row["Name"]] = Photocard5Stars(row["Name"], int(row["Level"]),
                                                    piece_shape, piece_color,
                                                    int(row["Signature"]), int(row["Trendy Up"]))

print(list(photocards_name_by_object.keys()))
# Main menu
print("Welcome to Blackpink: The Game Schedule Solver!\n")
while True:
    print("MAIN MENU")
    print(f"You have {len(photocards_name_by_object)} photocards.")
    print("Select option:\n")
    print("Manage photocards (p)\nSolve schedules (s)\nExit (e)")
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
                photocards_dicts.append(photocard_dict)
                update_csv(photocards_dicts, CSV_FILE)
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
                    photocards_name_by_object.pop(name)
                    photocards_dicts = list(filter(lambda d: d["Name"] != name, photocards_dicts))
                    update_csv(photocards_dicts, CSV_FILE)
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
                            if signature not in [str(s) for s in range(4)]:
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
                        update_csv(photocards_dicts, CSV_FILE)


            if photocard_option == "mm":
                break
    
    if option == 'e':
        break
