from photocard import *
import csv

CSV_FILE = "photocards.csv"

def update_csv(photocards_data, csv_file):
    """Input is a list of dictionaries, each dictionary representing a photocard"""
    
    fieldnames = ["Name", "Level", "Signature", "Trendy Up", "Piece Shape", "Piece Color"]

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write the data rows
        for photocard in photocards_data:
            writer.writerow(photocard)


# Read photocards
photocards = []
photocards_dicts = []
with open(CSV_FILE, "r", newline="", encoding='iso-8859-1') as photocards_data:
    reader = csv.DictReader(photocards_data)
    print("So far so good!")
    print(reader)
    data = list(reader)
for row in data:
    row = {k: v for k, v in row.items() if v is not None and v != ''}  # remove entries that have no value
    if int(row["Level"]) > 0:
        photocards_dicts.append(row)
        if any([row["Name"].startswith(suit) for suit in suits]):
            photocards.append(Photocard1to4Stars(row["Name"], int(row["Level"])))
        else:
            piece_shape = FiveSquareShape(five_square_shapes_strings.index(row["Piece Shape"]) + 1)
            piece_color = Color(piece_colors.index(row["Piece Color"]) + 1)
            
            photocards.append(Photocard5Stars(row["Name"], int(row["Level"]),
                                                piece_shape, piece_color,
                                                int(row["Signature"]), int(row["Trendy Up"])))
assert len(photocards) == len(photocards_dicts)
photocards_name_by_object = dict(zip([p.get_photocard_name() for p in photocards], photocards))

# Main menu
print("Welcome to Blackpink: The Game Schedule Solver!\n")
while True:
    print("MAIN MENU")
    print("Select option:\n")
    print("Manage photocards (p)\nSolve schedules (s)\nExit (e)")
    option = input()
    print()
    if option == 'p':
        while True:
            print("PHOTOCARD MANAGEMENT MENU")
            print("Add photocard (a)\nRemove photocard (r)\nView photocard data (v)\nReturn to main menu (m)")
            photocard_option = input()
            print()
            if photocard_option == "a":
                name = input("Enter photocard name: ")
                if name in photocards_name_by_object.keys():
                    print(f"Photocard of name '{name}' already exists!\n")
                    continue
                level = int(input("Enter photocard level: "))
                photocard_dict = {"Name": name, "Level": level}
                if any([name.startswith(s) for s in suits]):
                    new_photocard = Photocard1to4Stars(name, level)
                else:
                    piece_shape_string = input(f"Enter piece shape (either of {', '.join(five_square_shapes_strings)}): ")
                    piece_shape = FiveSquareShape(five_square_shapes_strings.index(piece_shape_string) + 1)
                    piece_color_string = input(f"Enter piece color (either of {', '.join(piece_colors)}): ").strip().capitalize()
                    if piece_color_string not in piece_colors:
                        raise ValueError("The piece color should either be green, yellow, blue or red")
                    piece_color = Color(piece_colors.index(piece_color_string) + 1)
                    signature = int(input("Enter Signature number (from 0 to 5): "))
                    trendy_up = int(input("Enter Trendy Up number (from 0 to 3): "))
                    new_photocard = Photocard5Stars(name, level, piece_shape, piece_color, signature, trendy_up)
                    photocard_dict["Signature"] = signature
                    photocard_dict["Trendy Up"] = trendy_up
                    photocard_dict["Piece Shape"] = piece_shape_string
                    photocard_dict["Piece Color"] = piece_color_string
                photocards_name_by_object[name] = new_photocard
                photocards_dicts.append(photocard_dict)
                update_csv(photocards_dicts, CSV_FILE)
                print("Photocard added.\n")
            if photocard_option == "v":
                while True:
                    name = input("Enter name of the photocard you want to view, or enter 'e' to exit: ")
                    if name == 'e':
                        break
                    print()
                    if name not in photocards_name_by_object.keys():
                        print(f"No photocard of name {name}\n")
                        continue
                    photocards_name_by_object[name].display_photocard_info()
                    print()
            if photocard_option == "m":
                break
    
    if option == 'e':
        break
                


# Test trendy up Dawn Walk JENNIE #2, JENNIE's Tree Decorating
# Test add Candle JISOO #2