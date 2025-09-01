# Problem specification:
# Given:
# n - number of conditionals
# m - number of unique vectorised valuations (at most 2^num_prop_vars, at least 1)
# Vi, for i from 1 to m - a vector in the format (vi1,...vin), with vij = 1 if it verifies the jth conditional, 0 if it doesn't, and u if it's undecided

# Given n, m, and Vi's, first get the rational closure, then the Initial Disjunctive Rational Closure, then see if it can be extended even further

# Given a valuation in the string format (e.g. "101u"), returns a valuation in the array format (e.g. [1,0,1,2]).
def proc_val(vi):
    valuation = []
    idx = 0
    for ch in vi:
        valuation.append(0)
        if ch == '0':
            valuation[idx] = 0
        elif ch == '1':
            valuation[idx] = 1
        else:
            valuation[idx] = 2
        idx += 1
    return valuation

# Function to construct a preset given a set of valuations
def construct_preset(valuations_raw):
  # print(valuations_raw)
  def preset():
    n = len(valuations_raw[0])
    m = len(valuations_raw)
    valuations = list(map(lambda x : proc_val(x), valuations_raw))

    ranks = [0 for _ in range(m)]
    return n, m, valuations_raw, valuations, ranks
  return preset

