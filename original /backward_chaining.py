def backward_chaining(kb, query):
    def bc_recursive(q, path):
        if q in path:
            return False, path
        if q in kb:
            return True, path + [q]
        new_path = path.copy()
        for clause in kb:
            if '=>' in clause:
                premises, conclusion = map(str.strip, clause.split('=>'))
                if conclusion == q:
                    premises = [premise.strip() for premise in premises.split('&')]
                    all_true = True
                    all_paths = []
                    for p in premises:
                        res, res_path = bc_recursive(p, new_path.copy())
                        all_true = all_true and res
                        all_paths.extend(res_path)
                        if not all_true:
                            break
                    if all_true:
                        return True, all_paths + [q]
        return False, path

    result, path = bc_recursive(query, [])
    path = sorted(set(path), key=path.index)  # To maintain the order and remove duplicates
    return "YES: " + ", ".join(path) if result else "NO"