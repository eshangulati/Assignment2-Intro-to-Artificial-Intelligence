import itertools

def parse_expression(expression):
    """
    A recursive parser to handle expressions with negation, disjunction, and biconditionals.
    Returns a function that takes a truth assignment and computes the truth value of the expression.
    """
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
    symbols = set()
    expressions = []

    for clause in kb:
        expr_func = parse_expression(clause)
        expressions.append(expr_func)
        symbols.update(filter(str.isalpha, clause.replace("~", "").replace("&", "").replace("||", "").replace("=>", "").replace("<=>", "").replace("(", "").replace(")", "")))

    query_func = parse_expression(query)

    all_models_satisfy_query = True
    valid_models = []

    for values in itertools.product([True, False], repeat=len(symbols)):
        assignment = dict(zip(symbols, values))
        if all(expr(assignment) for expr in expressions):
            valid_models.append(assignment)
            if not query_func(assignment):
                all_models_satisfy_query = False

    return f"YES: {len(valid_models)}" if all_models_satisfy_query else "NO"
