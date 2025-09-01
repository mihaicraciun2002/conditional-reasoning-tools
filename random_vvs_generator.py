# Utility class
# Given the number of conditionals, generate a random VVS

import random


def generate_vectorised_valuations_raw(n): # n = number of conditionals
    map_to_str = {0: "0", 1: "1", 2: "u"}
    # Validation condition : every conditional has at least one 1, and there has to be at least one valuation without any 0's
    all_vec_vals = [] # set of all vectorised valuations with n conditionals that don't have at least one 1
    vec_ones = [] # set of all vectorised valuations that have at least one 1
    num_vec_vals = (int)(3 ** n)
    for vec_val in range(num_vec_vals):
        cpy = vec_val
        bits_decomp = ""
        num_iterations = n
        has_one = False
        while num_iterations > 0:
            bits_decomp += map_to_str[cpy % 3]
            if(cpy % 3 == 1):
                has_one = True
            num_iterations -= 1
            cpy //= 3

        if(has_one):
            vec_ones.append(bits_decomp)
        else:
            all_vec_vals.append(bits_decomp)
    random.shuffle(all_vec_vals)
    random.shuffle(vec_ones)

    n1_min = 0

    for n1_start in range(1, len(vec_ones) + 1):
        who_has_ones = {}
        for index in range(n1_start):
            for index_str in range(len(vec_ones[index])):
                if vec_ones[index][index_str] == "1":
                    who_has_ones[index_str] = 1
        continue_loop = False
        for index_str in range(len(vec_ones[0])):
            if not(index_str in who_has_ones):
                continue_loop = True
                break
        if not continue_loop:
            n1_min = n1_start
            break

    n1_min2 = 0
    for index in range(len(vec_ones)):
            has_zero = False
            for index_str in range(len(vec_ones[index])):
                if vec_ones[index][index_str] == "0":
                    has_zero = True
            if not has_zero:
                n1_min2 = index + 1

    n1 = random.randint(max(n1_min, n1_min2), len(vec_ones))
    n2 = random.randint(0, len(all_vec_vals))
    return vec_ones[:n1] + all_vec_vals[:n2]

