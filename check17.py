a= [12, 15, 3, 7]

def check(a,n):
    sol = set()
    for s in a:
        if s in sol:
            return True
        sol.add(n-s)
    return False

print(check(a,17))