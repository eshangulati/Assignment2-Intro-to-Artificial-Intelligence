import itertools

def parse_clauses(kb):
    symbols = set()
    processed_clauses = []
    for clause in kb:
        if '=>' in clause:
            premises, conclusion = clause.split('=>')
            premises = premises.strip().split('&')
            for premise in premises:
                symbols.add(premise.strip())
            symbols.add(conclusion.strip())
            processed_clauses.append((premises, conclusion.strip()))
        else:
            symbols.add(clause.strip())
            processed_clauses.append(([], clause.strip()))  # Treat as fact
    return processed_clauses, list(symbols)

def evaluate(processed_clauses, assignment):
    for premises, conclusion in processed_clauses:
        if premises:  # There are premises leading to a conclusion
            if all(assignment.get(premise.strip(), False) for premise in premises):
                if not assignment.get(conclusion, False):
                    return False
        else:  # It's a fact
            if not assignment.get(conclusion, False):
                return False
    return True

def truth_table_check(kb, query):
    processed_clauses, symbols = parse_clauses(kb)
    valid_models = []
    all_valid_models_satisfy_query = True

    for values in itertools.product([True, False], repeat=len(symbols)):
        assignment = dict(zip(symbols, values))
        if evaluate(processed_clauses, assignment):
            valid_models.append(assignment)
            # Check if the query is false in any valid model
            if not assignment.get(query, False):
                all_valid_models_satisfy_query = False

    return f"YES: {len(valid_models)}" if all_valid_models_satisfy_query and valid_models else "NO"