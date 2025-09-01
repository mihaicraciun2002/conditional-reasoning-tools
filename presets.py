from core import *


# Preset 1 (the classic bird/penguin example)
def preset_1():
    n = 3
    m = 6
    valuations_raw = ["1uu", "uuu", "01u", "0uu", "10u", "u00"]
    valuations = list(map(lambda x : proc_val(x), valuations_raw))

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks

# Preset 2 (the counterexample presented by Richard)
def preset_2():
    n = 2
    m = 3
    valuations_raw = ["11", "00", "u1"]
    n = len(valuations_raw[0])
    m = len(valuations_raw)
    valuations = list(map(lambda x : proc_val(x), valuations_raw))

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks

def preset_3():
    n = 4
    m = 8
    valuations_raw = ["1uuu", "01uu", "u01u", "0u1u", "00u1", "0001", "000u", "0000"]
    n = len(valuations_raw[0])
    m = len(valuations_raw)
    valuations = list(map(lambda x : proc_val(x), valuations_raw))

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks

def manual_input():
    # First, set n, m, and Vi's
    # print("Start", flush = True)
    print("Input n (number of conditionals in KB)", flush = True)
    n = int(input())
    print("Input n is", n, flush = True)
    print("Input m (number of unique valuations)", flush = True)
    m = int(input())
    print("Input m is", m, flush = True)

    valuations = []
    valuations_raw = []

    for i in range(m):
        # Read valuation i
        print("Input valuation #", i + 1, flush = True)
        vi = str(input())
        print("Input validation #", i + 1, "is", vi, flush = True)
        valuations.append(proc_val(vi))
        valuations_raw.append(vi)

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks

def preset_4():
    n = 3
    m = 6
    valuations_raw = ["111", "uuu", "01u", "0uu", "10u", "u00"]
    valuations = list(map(lambda x : proc_val(x), valuations_raw))

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks

def preset_counterexample():
    n = 3
    m = 4
    valuations_raw = ["11u", "0u1", "001", "000"]
    valuations = list(map(lambda x : proc_val(x), valuations_raw))

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks