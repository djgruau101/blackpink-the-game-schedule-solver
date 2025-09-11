# Remaining:
# 1 signature, lucky: 4 (4)
# 2 signature, lucky: 1 (2)
# 3 signature, lucky: 4 (12)
# 4 signature, lucky: 4 (16)
# 5 signature, lucky: 1 (5)
# Need 39 more duplicates

# Duplicates:
# Jisoo: 18
# Jennie: 22
# Rosé: 20
# Lisa: 24

# 552 cakes minimum needed per member

# Limit break for 5-star cards:
# 10 cheer + 20 cheer + 15 brilliance + 20 brilliance + 25 brilliance
# 8 ice cream + 10 ice cream + 8 cake + 10 cake + 12 cake

# 10 + 30 + 100 (trendies)
# 2090 trendies left

def calculate_stardust(unit, jar, box):
    return unit + 10 * jar + 100 * box


one_to_50 = 112549
fifty_to_52 = 14076
fifty_two_to_54 = 15202
fifty_four_to_56 = 16370
fifty_six_to_58 = 17584
fifty_eight_to_60 = 9262 + 9580
fifty_to_60 = fifty_to_52 + fifty_two_to_54 + fifty_four_to_56 + fifty_six_to_58 + fifty_eight_to_60
total_5_star = one_to_50 + fifty_to_60

print(total_5_star)

stardust_left = (3 + 4 + 4 + 1 + 1 + 1) * fifty_to_60 + (4 + 3 + 1 + 3 + 3 + 2) * total_5_star + (1 + 1) * one_to_50
cur = 2159869

print(f"{stardust_left} stardust left to complete grid")
# print(f"{stardust_left_active} stardust left with current cards for now")
print(f"{stardust_left - cur} stardust left to collect")
# print(f"{stardust_left_active - cur} stardust left to collect for now")


def calc_stats():

    B35 = 3178

    # 2 signature, not lucky (Rose), yellow Z, level 56 written
    u23 = [14688, 8886, 6423, 4927, 3914] # [14519, 8803, 6376, 4901, 3903] # [14201, 8570, 6179, 4727, 3744] # [14032, 8486, 6131, 4701, 3733] # [13445, 7984, 5666, 4257, 3304] # [13284, 7904, 5620, 4233, 3294] # [12745, 7446, 5197, 3830, 2905] # [12584, 7367, 5151, 3806, 2895]

    # base signature, lucky (Lisa), red U, level 52 written
    l03 = [] # [12905, 7526, 5242, 3855, 2916] # [12744, 7446, 5197, 3830, 2905]

    def cp(l, b):
        return [i-b for i in l] 

    print("2 signature, not lucky:")
    print(cp(u23, B35))
    print("Base signature, lucky:")
    print(cp(l03,B35))

    # for i in range(51, 61):
    #     print(f"# Level {i}: " + ", ".join([str([0 for _ in range(5)]) for i in range(4)]))

# def fest(rem, ):

calc_stats()


