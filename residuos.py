import math
def derivative(f, z, order=1,h=1e-5):
    if order == 1:
        return (f(z + h) - f(z - h)) / (2 * h)
    else:
        return (derivative(f,z+h,order-1,h) - derivative(f,z-h,order-1,h)) / (2 *h)

def residue_general(f, z0, n):
    """
    Compute the residue of f(z) at z0, a pole of order n.
    
    Parameters:
    f   : function, complex function f(z)
    z0  : complex, location of the pole
    n   : int, order of the pole
    
    Returns:
    complex, residue at z0
    """
    from math import factorial
    def g(z):
        return (z - z0)**n * f(z)
    
    return derivative(g, z0, order=n-1) / factorial(n - 1)

# Example: f(z) = 1 / (z^2 * (z - 1)) has a pole of order 2 at z = 0
def f(z):
    return (math.sin(z) / z**2)

z0 = 0
n = 2
res = residue_general(f, z0, n)
print(f"Residue at z = {z0} (order {n}) is approximately {res}")

print(2 * math.pi * 1j)