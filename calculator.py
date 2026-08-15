def calculator(expression):
    if not expression:
        return "Error: No Expression"
    try:

        return eval(expression)
    except Exception as e:
        return f"Error: {e}"