def exec_code(expr: str, context: dict = None):
    # VERY small, restricted exec helper. In production, replace with sandbox.
    allowed = {'min': min, 'max': max, 'sum': sum}
    # Evaluate simple arithmetic expressions safely by limiting globals
    return eval(expr, {'__builtins__': {}}, allowed)
