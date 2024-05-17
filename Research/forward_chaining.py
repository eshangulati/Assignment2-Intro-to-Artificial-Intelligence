def forward_chaining(kb, query):
    """Perform forward chaining on a knowledge base for a given query."""
    known_facts = set()
    rules = []

    def parse_clause(clause):
        clause = clause.strip()
        if '<=>' in clause:
            left, right = clause.split('<=>', 1)
            return ('biconditional', parse_clause(left), parse_clause(right))
        elif '=>' in clause:
            left, right = clause.split('=>', 1)
            return ('implication', parse_clause(left), parse_clause(right))
        elif '||' in clause:
            left, right = clause.split('||', 1)
            return ('disjunction', parse_clause(left), parse_clause(right))
        elif '&' in clause:
            left, right = clause.split('&', 1)
            return ('conjunction', parse_clause(left), parse_clause(right))
        elif clause.startswith('~'):
            return ('negation', parse_clause(clause[1:].strip()))
        else:
            return ('atom', clause)

    def eval_clause(clause, facts):
        if clause[0] == 'atom':
            return clause[1] in facts
        elif clause[0] == 'negation':
            return not eval_clause(clause[1], facts)
        elif clause[0] == 'conjunction':
            return eval_clause(clause[1], facts) and eval_clause(clause[2], facts)
        elif clause[0] == 'disjunction':
            return eval_clause(clause[1], facts) or eval_clause(clause[2], facts)
        elif clause[0] == 'implication':
            return not eval_clause(clause[1], facts) or eval_clause(clause[2], facts)
        elif clause[0] == 'biconditional':
            return eval_clause(clause[1], facts) == eval_clause(clause[2], facts)
        return False

    def add_known_fact(fact):
        if fact[0] == 'atom':
            known_facts.add(fact[1])
        elif fact[0] == 'negation':
            known_facts.add(f'¬{fact[1][1]}')

    print("Initial Knowledge Base:")
    for clause in kb:
        print(clause)

    for clause in kb:
        parsed_clause = parse_clause(clause)
        if parsed_clause[0] == 'atom' or parsed_clause[0] == 'negation':
            add_known_fact(parsed_clause)
        else:
            rules.append(parsed_clause)

    print("Initial Known Facts:", known_facts)
    print("Initial Rules:")
    for rule in rules:
        print(rule)

    new_facts = True
    while new_facts:
        new_facts = False
        for rule in rules:
            if rule[0] == 'implication':
                if eval_clause(rule[1], known_facts) and not eval_clause(rule[2], known_facts):
                    print(f"Rule {rule} triggered")
                    add_known_fact(rule[2])
                    new_facts = True
            elif rule[0] == 'biconditional':
                if eval_clause(rule[1], known_facts) == eval_clause(rule[2], known_facts):
                    print(f"Rule {rule} triggered")
                    add_known_fact(rule[1])
                    add_known_fact(rule[2])
                    new_facts = True

        print("Updated Known Facts:", known_facts)

    # Check if the query can be derived
    query_clauses = query.split('&')
    for q in query_clauses:
        parsed_q = parse_clause(q.strip())
        if not eval_clause(parsed_q, known_facts):
            return "NO"

    inferred_set = sorted(known_facts)

    return f"YES: {', '.join(inferred_set)}"

# Example usage
kb = [
    "(a <=> (c => ~d)) & b & (b => a)",
    "c",
    "¬f || g"
]
query = "¬d & (¬g => ¬f)"

print(forward_chaining(kb, query))
