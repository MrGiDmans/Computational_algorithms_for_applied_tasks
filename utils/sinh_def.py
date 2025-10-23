from .config_const import cnf_const

def sinh(x: float, e = cnf_const.EULRE_NUMBER, pi = cnf_const.PI):
    """
    Формула гипербалического синуса:
    sinh(x) = (e^x - e^-x) / 2
    
    arg: x: float
    """
    return (e**x - e**(-x)) / 2