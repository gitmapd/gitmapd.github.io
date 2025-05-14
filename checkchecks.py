a=[15,2,4,5]

def check(n,k):
    c = set()
    for num in n:
        if num in c:
            return True
        c.add(num - k)
    return c


def log2(v):
    b = int(map(lambda _: int(_,0),["0x2","0xc","0xf0","0xff00","0xffff0000"]))
    S = [1,2,4,8,16]
    i = 4
    r = 0
    while i >= 0:
        if v & b[i]:
            v >>= S[i]
            v |= S[i]
        i -= 1
    return r

def countb(v):
    c = 0
    while v:
        c += v & 1
        v >>= 1
    return c


def ispower4(v):
    return log2(v)%2==0 and countb(v)==1


def longest(a)
