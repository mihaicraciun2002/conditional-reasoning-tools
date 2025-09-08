from constants import *

global INF

def rational_closure(input_mt, return_input = False, printing = True):
    n, m, valuations_raw, valuations, ranks = input_mt()
    def find_lowest_rank(cond_idx, value):
        lowest = -1
        for i in range(m):
            if (lowest == -1 and valuations[i][cond_idx] == value) or (valuations[i][cond_idx] == value and ranks[i] < lowest):
                lowest = ranks[i]
        return lowest

    def increase_ranks(cond_idx, value, thresh):
        for i in range(m):
            if valuations[i][cond_idx] == value and ranks[i] <= thresh:
                ranks[i] = thresh + 1

    # First, exclude the valuations that have no 1s, and all their zeros aren't attacking any ones
    for i in range(m):
        should_elim = False
        for j in range(n):
            if(valuations[i][j] == 0 and find_lowest_rank(j, 1) == -1):
                should_elim = True
        if should_elim == True:
            ranks[i] = INF

    while 1:
        # For every conditional, check if at least one 1 is lower than the lowest 0
        to_push = []
        for i in range(n):
            low_0 = find_lowest_rank(i, 0)
            if(low_0 != -1 and find_lowest_rank(i, 1) >= low_0):
                to_push.append(i)

        for cond_idx in to_push:
            increase_ranks(cond_idx, 0, find_lowest_rank(cond_idx, 1))
        if len(to_push) == 0:
            break
    # Print the rational closure
    if(printing):
        for idx in range(len(ranks)):
            print("Rank for valuation", valuations_raw[idx], "is", ranks[idx])
    if return_input == False:
        return ranks
    else:
        return n, m, valuations_raw, valuations, ranks
    
# Traditional DRC (Disjunctive Rational Closure) Extension Algorithm

def traditional_drc(input_mt, return_input = False):
    # We first obtain the Rational Closure
    n, m, valuations_raw, valuations, ranks = rational_closure(input_mt, return_input = True)

    # This is the same as max(L)
    highest_rank = -1

    for idx in range(len(ranks)):
        if highest_rank == -1 or (ranks[idx] != INF and ranks[idx] > highest_rank):
            highest_rank = ranks[idx]
    ranks_right = ranks.copy()

    def find_lowest_rank(cond_idx, value):
        lowest = -1
        for i in range(m):
            if (lowest == -1 and valuations[i][cond_idx] == value) or (valuations[i][cond_idx] == value and ranks[i] < lowest):
                lowest = ranks[i]
        return lowest

    def increase_ranks(cond_idx, value, thresh):
        for i in range(m):
            if valuations[i][cond_idx] == value and ranks[i] <= thresh:
                ranks[i] = thresh + 1

    # For every vectorised valuation, we take a look at the conditionals for which it has a 1, and then see for which of these conditionals
    # the vectorised valuation has the lowest RC rank and a 1 for them.
    for idx in range(len(ranks)):
        limit = highest_rank
        for j in range(n):
            # If the vectorised valuation has a 1 for conditional j and is "minimising" the Lower Rank conditional j, 
            # we update its upper rank
            if(valuations[idx][j] == 1 and ranks[idx] == find_lowest_rank(j, 1)):
                limit = min(limit, find_lowest_rank(j, 0) - 1)
        # We make sure the Upper Rank is >= Lower Rank
        limit = max(limit, ranks[idx])
        ranks_right[idx] = limit
    if return_input == False:
        return ranks, ranks_right
    else:
        return n, m, valuations_raw, valuations, ranks, ranks_right
    

