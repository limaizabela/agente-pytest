def soma(a, b):
    """
    Soma dois números inteiros ou floats.
    """
    return a + b

def divisao(a, b):
    """
    Divide um número por outro.
    Lança ValueError se o divisor for zero.
    """
    if b == 0:
        raise ValueError("Divisor não pode ser zero.")
    return a / b