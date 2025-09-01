import random

# Utility class
# Generate a Knowledge Base, given a Vectorised Valuations Set

# Proposition class
class proposition:
    def __init__(self):
        self.type = -1 # Type of proposition - can be a
        #p.v., (0)
        # a negation of a proposition, (1)
        # a conjunction of propositions, (2)
        # a disjunction of propositions (3)
        # Top (4)
        # Bottom (5)
        self.objects = [] # Reference to the objects that this proposition is referencing, for example the negation of a proposition will reference the object of that prop
        self.literal = None
    def is_initialised(self):
        return self.type != -1
    def copy(self):
        new_obj = proposition()
        new_obj.type = self.type
        new_obj.objects = self.objects.copy()
        new_obj.literal = self.literal
        return new_obj

def conjunction(a : proposition, b : proposition):
    new_prop = proposition()
    new_prop.type = 2
    new_prop.objects = [a, b]
    return new_prop
def disjunction(a : proposition, b : proposition):
    new_prop = proposition()
    new_prop.type = 3
    new_prop.objects = [a, b]
    return new_prop
def negation(a : proposition):
    new_prop = proposition()
    new_prop.type = 1
    new_prop.objects = [a]
    return new_prop
def pv(literal = None):
    new_prop = proposition()
    new_prop.type = 0
    if not(literal is None):
        new_prop.literal = (ord)(literal)
    else:
        new_prop.literal = None
    return new_prop

def show_proposition(prop : proposition):
    curr_pv = (ord)("a")
    used_literals = {}

    # See if the proposition already has literal names for its variables
    def find_used_literals(prop : proposition):
        nonlocal used_literals
        if(prop.type == 0):
            if not (prop.literal is None):
                used_literals[prop.literal] = 1
        if(prop.type == 1):
            find_used_literals(prop.objects[0])
        if(prop.type == 2):
            find_used_literals(prop.objects[0])
            find_used_literals(prop.objects[1])
        if(prop.type == 3):
            find_used_literals(prop.objects[0])
            find_used_literals(prop.objects[1])

    # Generate the string representing the proposition
    def proc(prop : proposition, level, origin):
        nonlocal curr_pv
        nonlocal used_literals
        if(prop.type == 0):
            if not (prop.literal is None):
                return (chr)(prop.literal)
            else:
                while curr_pv in used_literals:
                    curr_pv += 1
                curr_pv += 1
                return (chr)(curr_pv - 1)
        par1 = ""
        par2 = ""
        if level > 0 and (origin != prop.type):
            par1 = "("
            par2 = ")"

        if(prop.type == 1):
            ans1 = proc(prop.objects[0], level + 1, prop.type)
            return "\\neg " + ans1
        if(prop.type == 2):
            ans1 = proc(prop.objects[0], level + 1, prop.type)
            ans2 = proc(prop.objects[1], level + 1, prop.type)
            return par1 + ans1 + " " + "\\land " + ans2 + par2
        if(prop.type == 3):
            ans1 = proc(prop.objects[0], level + 1, prop.type)
            ans2 = proc(prop.objects[1], level + 1, prop.type)
            return par1 + ans1 + " " + "\\lor " + ans2 + par2
        if (prop.type == 4):
            return "\\top"
        if (prop.type == 5):
            return "\\bottom"
    return proc(prop, 0, prop.type)

# Function that given a set of vectorised valuations, constructs a knowledge base

def construct_kb(input_mt, use_random = True):
    n, m, valuations_raw, valuations, ranks = input_mt()
    # Compute the minimum number of propositional variables
    num_props = 1
    num_valuations = 2
    while(num_valuations < m):
        num_props += 1
        num_valuations *= 2
    valuations_original = []
    # Generate the non-vectorised valuations
    for valuation in range(num_valuations):
        cpy = valuation
        bits_decomp = []
        num_iterations = num_props
        while num_iterations > 0:
            bits_decomp.append(cpy % 2)
            num_iterations -= 1
            cpy //= 2
        bits_decomp = bits_decomp[::-1]
        # print(bits_decomp)
        valuations_original.append(bits_decomp)
    # Shuffle the non-vectorised valuations
    if use_random:
        random.shuffle(valuations_original)
    # Create the assigments for the vectorised valuations
    assignments = [[] for _ in range(len(valuations))]
    index_non_vec = 0
    # Make sure each vectorised valuation has at least one assigned non-vectorised valuation
    for index in range(len(valuations)):
        assignments[index].append(valuations_original[index])
        index_non_vec += 1
    # Assign the rest of the non-vectorised valuations, if any remain, to random vectorised valuations
    while index_non_vec < len(valuations_original):
        if use_random:
            vectorised_idx = random.randint(0, len(valuations) - 1)
        else:
            vectorised_idx = 0
        # print(vectorised_idx, len(valuations), len(assignments))
        assignments[vectorised_idx].append(
            valuations_original[index_non_vec])
        index_non_vec += 1

    # Now, to generate the KB
    KB = []

    for conditional_idx in range(n):
        # The left hand side will be composed of a conjunction of negated undef valuations, so a conjunction of disjunctions
        LHS = proposition()
        for index in range(len(valuations)):
            # If the current conditional is evaluated as undef by the current vectorised valuation
            if(valuations[index][conditional_idx] == 2):
                # Go through the corresponding non-vectorised valuations, and make a conjunction of disjunctions containing
                # negated literals
                for valuation_original in assignments[index]:
                    prop_to_add = proposition()
                    curr_literal = (ord)("a")
                    for idx_pv in range(num_props):
                        # If it's a negated p.v., add it non-negated (so that the literal is negated)
                        if valuation_original[idx_pv] == 0:
                            if not prop_to_add.is_initialised():
                                prop_to_add = pv(literal = (chr)(curr_literal))
                            else:
                                prop_to_add = disjunction(prop_to_add, pv(literal = (chr)(curr_literal)))
                        else:
                            if not prop_to_add.is_initialised():
                                prop_to_add = negation(pv(literal = (chr)(curr_literal)))
                            else:
                                prop_to_add = disjunction(prop_to_add, negation(pv(literal = (chr)(curr_literal))))
                        curr_literal += 1
                    if not LHS.is_initialised():
                        LHS = prop_to_add
                    else:
                        LHS = conjunction(LHS, prop_to_add)
        if LHS.type == -1:
            # Make the default LHS top
            LHS.type = 4

        # The right hand side will be composed of a disjunction of a conjunction of non-negated literals
        RHS = proposition()
        for index in range(len(valuations)):
            # If the current conditional is evaluated as undef by the current vectorised valuation
            if(valuations[index][conditional_idx] == 1):
                # Go through the corresponding non-vectorised valuations, and make a conjunction of disjunctions containing
                # negated literals
                for valuation_original in assignments[index]:
                    prop_to_add = proposition()
                    curr_literal = (ord)("a")
                    for idx_pv in range(num_props):
                        # If it's a negated p.v., add it non-negated (so that the literal is negated)
                        if valuation_original[idx_pv] == 1:
                            if not prop_to_add.is_initialised():
                                prop_to_add = pv(literal = (chr)(curr_literal))
                            else:
                                prop_to_add = conjunction(prop_to_add, pv(literal = (chr)(curr_literal)))
                        else:
                            if not prop_to_add.is_initialised():
                                prop_to_add = negation(pv(literal = (chr)(curr_literal)))
                            else:
                                prop_to_add = conjunction(prop_to_add, negation(pv(literal = (chr)(curr_literal))))
                        curr_literal += 1
                    if not RHS.is_initialised():
                        RHS = prop_to_add
                    else:
                        RHS = disjunction(RHS, prop_to_add)
        if RHS.type == -1:
            RHS.type = 5 # RHS is by default bottom
        KB.append((LHS, RHS))
    return KB

def print_kb(KB):
    for conditional in KB:
        print(show_proposition(conditional[0]), " \\vsim ", show_proposition(conditional[1]))