def forward_chaining(kb, query):
    # Extract initial facts and structure the knowledge base
    facts = [clause for clause in kb if "=>" not in clause]
    rules = [clause.split("=>") for clause in kb if "=>" in clause]
    inferred = set(facts)
    derived_facts = []

    # Format the rules list with stripped premises and conclusion
    formatted_rules = []
    for premises, conclusion in rules:
        premises = set(prem.strip() for prem in premises.split('&'))
        formatted_rules.append((premises, conclusion.strip()))

    # Process the facts
    while facts:
        current_fact = facts.pop(0)
        derived_facts.append(current_fact)
        
        if current_fact == query:
            return f"YES: {', '.join(sorted(inferred))}"
        
        # Update the knowledge base based on the current fact
        for premises, conclusion in formatted_rules[:]:
            if current_fact in premises:
                premises.discard(current_fact)
                if not premises:
                    if conclusion == query:
                        inferred.add(conclusion)
                        return f"YES: {', '.join(sorted(inferred))}"
                    if conclusion not in inferred:
                        inferred.add(conclusion)
                        facts.append(conclusion)
                        derived_facts.append(conclusion)
    
    return "NO"
