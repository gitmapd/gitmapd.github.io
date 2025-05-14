#L=[100,4,200,1,3,2]
L=[1,2,3,4,-1,6,7,8,9,10,11,12,13,-1,15,16,17,18,19,20]
#L=[1,2,3,4,-1,6,7,8,-1,9,10]

L=sorted(L)
D=[1]*len(L)

peaks = []

for x in range(1,len(L)):
    if L[x-1]+1==L[x]:
        D[x]=1+D[x-1]

print(D)
peaks=[]
for x in range(1,len(D)):
    if D[x-1] + 1 != D[x]:
        peaks += [D[x-1]]
if D[-2] + 1 == D[-1]:
    peaks += [D[-1]]
print(peaks)
print(sorted(list(set(peaks)),reverse=True)[1])

#print(L)
#print(D)


#longest = 0

#s = set(L)

#for num in L:
#    if num -1 not in s:
#        length = 1
#        next_num = num + 1
#        while next_num in s:
#            length += 1
#            next_num +=1
#    longest = max(longest,length)
#print(longest)
        