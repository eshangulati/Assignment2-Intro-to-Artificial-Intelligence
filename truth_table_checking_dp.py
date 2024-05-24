def parse_expression_to_cnf(expression):
    """ Recursively converts logical expressions into CNF. """
    expression = expression.replace(" ", "")
    if "<=>" in expression:
        parts = expression.split("<=>")
        left_cnf = parse_expression_to_cnf(parts[0])
        right_cnf = parse_expression_to_cnf(parts[1])
        # Equivalent to (left_cnf and right_cnf) or (not left_cnf and not right_cnf)
        return f"(({left_cnf}) & ({right_cnf})) | (~({left_cnf}) & ~({right_cnf}))"
    elif "=>" in expression:
        parts = expression.split("=>")
        left_cnf = parse_expression_to_cnf(parts[0])
        right_cnf = parse_expression_to_cnf(parts[1])
        # Equivalent to not left_cnf or right_cnf
        return f"(~({left_cnf}) || ({right_cnf}))"
    elif "&" in expression:
        parts = expression.split("&")
        return ' & '.join(parse_expression_to_cnf(part) for part in parts)
    elif "||" in expression:
        parts = expression.split("||")
        return ' || '.join(parse_expression_to_cnf(part) for part in parts)
    elif expression.startswith("~"):
        sub_expr = expression[1:]
        return f"~({parse_expression_to_cnf(sub_expr)})"
    return expression

def parse_kb(kb):
    """ Parses the knowledge base into a list of CNF clauses. """
    parsed_kb = []
    for clause in kb:
        cnf_clause = parse_expression_to_cnf(clause)
        # Simplify parsing of clauses
        parts = cnf_clause.split(' & ')
        for part in parts:
            inner_parts = part.strip('()').split(' || ')
            parsed_kb.append(inner_parts)
    return parsed_kb

def unit_propagate(clauses, assignment):
    """ Applies unit propagation to simplify the clauses. """
    while True:
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        if not unit_clauses:
            break
        for unit in unit_clauses:
            literal = unit[0]
            var = literal[1:] if literal.startswith("~") else literal
            value = not literal.startswith("~")
            assignment[var] = value
            clauses = [c for c in clauses if literal not in c]
            clauses = [[l for l in clause if l != f"~{var}" and l != var] for clause in clauses]
    return clauses, assignment

def pure_literal_elimination(clauses, assignment):
    """ Applies pure literal elimination to simplify the clauses. """
    literals = {l for clause in clauses for l in clause}
    pure_literals = set(literals)
    for literal in literals:
        if "~" + literal in pure_literals:
            pure_literals.discard(literal)
            pure_literals.discard("~" + literal)
    
    for literal in pure_literals:
        var = literal[1:] if literal.startswith("~") else literal
        value = not literal.startswith("~")
        assignment[var] = value
        clauses = [clause for clause in clauses if literal not in clause]
    
    return clauses, assignment

def dpll(clauses, assignment):
    """ DPLL recursive function. """
    clauses, assignment = unit_propagate(clauses, assignment)
    if not clauses:
        return True, assignment
    if any(not clause for clause in clauses):
        return False, None

    clauses, assignment = pure_literal_elimination(clauses, assignment)
    if not clauses:
        return True, assignment
    if any(not clause for clause in clauses):
        return False, None

    var = next(l for clause in clauses for l in clause if l not in assignment)
    new_assignment = assignment.copy()
    for value in [True, False]:
        new_assignment[var] = value
        result, final_assignment = dpll(clauses, new_assignment)
        if result:
            return True, final_assignment
    return False, None

def dpll_satisfiable(kb):
    """ Checks if the knowledge base is satisfiable using DPLL. """
    clauses = parse_kb(kb)
    result, assignment = dpll(clauses, {})
    return result, assignment

def truth_table_check(kb, query):
    """ Checks if the negation of the query is satisfiable, which implies the KB does not entail the query. """
    extended_kb = kb[:]
    extended_kb.append(f"~({query})")
    satisfiable, assignment = dpll_satisfiable(extended_kb)
    return "NO" if satisfiable else "YES"
