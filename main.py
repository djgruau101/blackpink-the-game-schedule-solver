from photocard import *
import csv

# Read photocards
photocards = []
with open("photocards.csv", "r", newline="", encoding="utf-8-sig") as photocards_data:
    reader = csv.DictReader(photocards_data)
    data = list(reader)
for row in data:
    row = {k: v for k, v in row.items() if v is not None and v != ''}  # remove entries that have no value
    if int(row["Level"]) > 0:
        if any([row["Name"].startswith(suit) for suit in suits]):
            photocards.append(Photocard1to4Stars(row["Name"], int(row["Level"])))
        else:
            piece_shape = FiveSquareShape(five_square_shapes_strings.index(row["Piece Shape"]) + 1)
            piece_color = Color(piece_colors.index(row["Piece Color"]) + 1)
            
            photocards.append(Photocard5Stars(row["Name"], int(row["Level"]),
                                                piece_shape, piece_color,
                                                int(row["Signature"]), int(row["Trendy Up"])))
# photocards.sort(key = lambda photocard: photocard.get_photocard_name())
# for photocard in photocards:
#     print(photocard.get_photocard_name(), photocard.get_stats())

# Test trendy up Dawn Walk JENNIE #2, JENNIE's Tree Decorating
# Test add Candle JISOO #2