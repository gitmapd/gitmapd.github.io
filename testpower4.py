import math
#n = 4
#print([ n for n in range(10000) if n & (n-1) == 0])

#f'4**{int(math.log(n,4))}={n}'
#print(4 & 3 == 0 and 0 % 3 == 1)


#options=[]
#x=4
#while x <= 1<<32:
#    options.append(x)
#    x*=4
#print(options)
#N=int(input().strip())
#print(N in options)

for p in range(0,32,2):
    print(1<<p)

def log2(v):
    # convert hex to decimal
    b=list(map(lambda _:int(_,0),["0x2","0xc","0xf0","0xff00","0xffff0000"]))
    S=[1,2,4,8,16]
    i=4
    r=0
    while i>=0:
        if v & b[i]:
            v >>= S[i]
            r  |= S[i]
        i-=1
    return r

def countb(v):
    c = 0
    while v:
        c += v & 1
        v >>= 1
    return c

def ispow4(v):
    return log2(v)%2==0 and countb(v)==1

print(ispow4(16))
print(ispow4(17))