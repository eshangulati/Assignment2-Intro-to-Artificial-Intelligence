def backward_chaining(kb, query):
    def bc_recursive(q, path):
        if q in path:
            return False, path
        path.append(q)
        for clause in kb:
            if '=>' in clause:
                premises, conclusion = map(str.strip, clause.split('=>'))
                if conclusion == q:
                    premises = premises.split('&')
                    all_true = True
                    for p in premises:
                        res, new_path = bc_recursive(p.strip(), path.copy())
                        all_true = all_true and res
                        if not all_true:
                            break
                    if all_true:
                        return True, path + new_path
        if q in kb:
            return True, path
        return False, path

    result, path = bc_recursive(query, [])
    return "YES: " + ", ".join(sorted(set(path))) if result else "NO"
