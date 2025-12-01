def exec_expr(expr: str):
    allowed = {'min': min, 'max': max, 'sum': sum}
    return eval(expr, {'__builtins__': {}}, allowed)
