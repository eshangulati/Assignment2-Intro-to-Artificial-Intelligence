def parse_clause(clause):
    """Parse a logical clause into its components."""
    clause = clause.strip()
    
    # Handle parentheses and precedence
    if clause.startswith('(') and clause.endswith(')'):
        clause = clause[1:-1].strip()
    
    # Handle biconditional first
    if '<=>' in clause:
        left, right = clause.split('<=>', 1)
        return ('biconditional', parse_clause(left), parse_clause(right))
    
    # Handle implication next
    elif '=>' in clause:
        left, right = clause.split('=>', 1)
        return ('implication', parse_clause(left), parse_clause(right))
    
    # Handle disjunction next
    elif '||' in clause:
        left, right = clause.split('||', 1)
        return ('disjunction', parse_clause(left), parse_clause(right))
    
    # Handle conjunction next
    elif '&' in clause:
        left, right = clause.split('&', 1)
        return ('conjunction', parse_clause(left), parse_clause(right))
    
    # Handle negation
    elif clause.startswith('~'):
        return ('negation', parse_clause(clause[1:].strip()))
    
    # Handle atom
    else:
        return ('atom', clause.strip())

def evaluate_clause(clause, known_facts):
    """Evaluate a clause recursively."""
    clause_type = clause[0]
    if clause_type == 'atom':
        return clause[1] in known_facts
    elif clause_type == 'negation':
        return not evaluate_clause(clause[1], known_facts)
    elif clause_type == 'conjunction':
        return evaluate_clause(clause[1], known_facts) and evaluate_clause(clause[2], known_facts)
    elif clause_type == 'disjunction':
        return evaluate_clause(clause[1], known_facts) or evaluate_clause(clause[2], known_facts)
    elif clause_type == 'implication':
        return not evaluate_clause(clause[1], known_facts) or evaluate_clause(clause[2], known_facts)
    elif clause_type == 'biconditional':
        return evaluate_clause(clause[1], known_facts) == evaluate_clause(clause[2], known_facts)
    return False

def backward_chaining(kb, query):
    """Perform backward chaining on a knowledge base for a given query."""
    known_facts = set()
    parsed_kb = [parse_clause(clause) for clause in kb]

    def bc_recursive(goal, path):
        if goal in path:
            return False
        path.append(goal)
        
        if goal[0] == 'atom' and goal[1] in known_facts:
            return True

        for clause in parsed_kb:
            if clause[0] == 'implication' and clause[2] == goal:
                premises = [clause[1]]
                all_true = True
                for p in premises:
                    if not bc_recursive(p, path.copy()):
                        all_true = False
                        break
                if all_true:
                    known_facts.add(goal[1])
                    return True
            elif clause[0] == 'biconditional':
                left_clause, right_clause = clause[1], clause[2]
                if (bc_recursive(left_clause, path.copy()) and right_clause == goal) or \
                   (bc_recursive(right_clause, path.copy()) and left_clause == goal):
                    known_facts.add(goal[1])
                    return True
            elif clause[0] == 'conjunction':
                left_clause, right_clause = clause[1], clause[2]
                if bc_recursive(left_clause, path.copy()) and bc_recursive(right_clause, path.copy()):
                    known_facts.add(goal[1])
                    known_facts.add(goal[2])
                    return True
            elif clause[0] == 'disjunction':
                left_clause, right_clause = clause[1], clause[2]
                if bc_recursive(left_clause, path.copy()) or bc_recursive(right_clause, path.copy()):
                    known_facts.add(goal[1])
                    known_facts.add(goal[2])
                    return True
            elif clause[0] == 'atom' and clause == goal:
                known_facts.add(goal[1])
                return True
        return False

    # Handle conjunction in the query
    if '&' in query:
        subqueries = query.split('&')
    else:
        subqueries = [query]

    all_results = []
    for subquery in subqueries:
        q = subquery.strip()
        parsed_q = parse_clause(q)
        if parsed_q[0] == 'negation':
            result = not bc_recursive(parsed_q[1], [])
        else:
            result = bc_recursive(parsed_q, [])
        all_results.append(result)
        if result:
            known_facts.add(f"¬{parsed_q[1]}" if parsed_q[0] == 'negation' else parsed_q[1])

    result = all(all_results)
    inferred_set = sorted(set(known_facts))

    return f"YES: {', '.join(inferred_set)}" if result else "NO"

# Example usage
if __name__ == "__main__":
    kb = ["(a <=> (c => ~d)) & b & (b => a)", "c", "~f || g"]
    query = "~d & (~g => ~f)"
    result = backward_chaining(kb, query)
    print(result)
