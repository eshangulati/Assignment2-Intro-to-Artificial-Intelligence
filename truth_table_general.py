import itertools

def parse_expression(expr):
    expr = expr.replace(' ', '')
    if '<=>' in expr:
        parts = expr.split('<=>')
        return f"(({parse_expression(parts[0])}) & ({parse_expression(parts[1])})) | (~({parse_expression(parts[0])}) & ~({parse_expression(parts[1])}))"
    elif '=>' in expr:
        parts = expr.split('=>')
        return f"(~({parse_expression(parts[0])}) || ({parse_expression(parts[1])}))"
    elif '&' in expr:
        parts = expr.split('&')
        return ' & '.join(parse_expression(part) for part in parts)
    elif '||' in expr:
        parts = expr.split('||')
        return ' || '.join(parse_expression(part) for part in parts)
    elif expr.startswith('~'):
        return f"~({parse_expression(expr[1:])})"
    return expr

def parse_clauses(kb):
    symbols = set()
    processed_clauses = []
    for clause in kb:
        clause = clause.strip()
        if clause:
            cnf_clause = parse_expression(clause)
            parts = cnf_clause.split(' & ')
            for part in parts:
                inner_parts = part.strip('()').split(' || ')
                processed_clauses.append([p.strip('~') for p in inner_parts])
                for symbol in inner_parts:
                    symbols.add(symbol.strip('~'))
    return processed_clauses, list(symbols)

def evaluate(processed_clauses, assignment):
    for clause in processed_clauses:
        if not any(assignment.get(literal.strip('~'), False) if '~' in literal else not assignment.get(literal, False) for literal in clause):
            return False
    return True

def truth_table_check_general(kb, query):
    processed_clauses, symbols = parse_clauses(kb)
    query_clauses, _ = parse_clauses([query])  # Ensure query is passed as a list
    all_valid_models_satisfy_query = True
    valid_models_count = 0

    for values in itertools.product([True, False], repeat=len(symbols)):
        assignment = dict(zip(symbols, values))
        if evaluate(processed_clauses, assignment):
            valid_models_count += 1
            if not evaluate(query_clauses, assignment):
                all_valid_models_satisfy_query = False

    return f"YES: {valid_models_count}" if all_valid_models_satisfy_query else "NO"
