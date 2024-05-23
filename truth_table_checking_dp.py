def parse_clause(clause):
    """
    Parses a clause into a list of literals. Assumes literals are separated by '||' and handles negation.
    """
    clause = clause.replace(" ", "")
    if clause.startswith("(") and clause.endswith(")"):
        clause = clause[1:-1]
    literals = clause.split("||")
    return literals

def parse_kb(kb):
    """
    Parses the knowledge base into a list of clauses.
    """
    parsed_kb = []
    for clause in kb:
        # Handle conjunctions within each clause
        if '&' in clause:
            parts = clause.split('&')
            for part in parts:
                parsed_kb.append(parse_clause(part))
        else:
            parsed_kb.append(parse_clause(clause))
    return parsed_kb

def is_literal_true(literal, assignment):
    """
    Evaluates whether a literal is true under the given assignment.
    """
    if literal.startswith("~"):
        return not assignment.get(literal[1:], False)
    return assignment.get(literal, False)

def unit_propagate(clauses, assignment):
    """
    Applies unit propagation to simplify the clauses.
    """
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        literal = unit[0]
        var = literal[1:] if literal.startswith("~") else literal
        value = not literal.startswith("~")
        assignment[var] = value

        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            new_clause = [l for l in clause if l != "~" + var and l != var]
            new_clauses.append(new_clause)
        
        clauses = new_clauses
        unit_clauses = [c for c in clauses if len(c) == 1]
    return clauses, assignment

def pure_literal_elimination(clauses, assignment):
    """
    Applies pure literal elimination to simplify the clauses.
    """
    literals = [l for clause in clauses for l in clause]
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
    """
    DPLL recursive function.
    """
    print(f"DPLL invoked with clauses: {clauses} and assignment: {assignment}")
    clauses, assignment = unit_propagate(clauses, assignment)
    print(f"After unit propagation: {clauses} and assignment: {assignment}")
    if not clauses:
        return assignment
    if any([not clause for clause in clauses]):
        return False

    clauses, assignment = pure_literal_elimination(clauses, assignment)
    print(f"After pure literal elimination: {clauses} and assignment: {assignment}")
    
    if not clauses:
        return assignment
    if any([not clause for clause in clauses]):
        return False

    var = next(l for clause in clauses for l in clause if l not in assignment)
    new_assignment = assignment.copy()

    for value in [True, False]:
        new_assignment[var] = value
        print(f"Trying {var} = {value}")
        result = dpll(clauses, new_assignment)
        if result:
            return result

    return False

def dpll_satisfiable(kb):
    clauses = parse_kb(kb)
    assignment = {}
    result = dpll(clauses, assignment)
    return result if result else False

def parse_expression(expression):
    expression = expression.replace(" ", "")
    if "<=>" in expression:
        parts = expression.split("<=>", 1)
        left, right = map(parse_expression, parts)
        return lambda v: left(v) == right(v)
    if "=>" in expression:
        parts = expression.split("=>", 1)
        left, right = map(parse_expression, parts)
        return lambda v: not left(v) or right(v)
    if "||" in expression:
        parts = expression.split("||")
        sub_expressions = list(map(parse_expression, parts))
        return lambda v: any(sub_expr(v) for sub_expr in sub_expressions)
    if "&" in expression:
        parts = expression.split("&")
        sub_expressions = list(map(parse_expression, parts))
        return lambda v: all(sub_expr(v) for sub_expr in sub_expressions)
    if expression.startswith("~"):
        subexpr = parse_expression(expression[1:])
        return lambda v: not subexpr(v)
    return lambda v: v.get(expression, False)

def truth_table_check(kb, query):
    query_negated = "~" + query
    extended_kb = kb + [query_negated]
    print("Extended KB for satisfiability check:")
    print(extended_kb)
    return "YES" if not dpll_satisfiable(extended_kb) else "NO"
