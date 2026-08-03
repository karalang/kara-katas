# Randomized differential oracle for the #243/#244/#245 family.
# 4000 random lists over a tiny alphabet (so collisions and same-word pairs are
# dense), every query answered by all three algorithms; prints one rolling hash.
def lcg(s): return (s * 1103515245 + 12345) & 2147483647

def unified(words, w1, w2):
    n=len(words); same=w1==w2; best=n; prev=-1
    for i in range(n):
        if words[i]==w1 or words[i]==w2:
            if prev!=-1 and (same or words[prev]!=words[i]):
                if i-prev<best: best=i-prev
            prev=i
    return best

def split(words, w1, w2):
    n=len(words); best=n
    if w1==w2:
        prev=-1
        for i in range(n):
            if words[i]==w1:
                if prev!=-1 and i-prev<best: best=i-prev
                prev=i
        return best
    l1=l2=-1
    for i in range(n):
        if words[i]==w1:
            l1=i
            if l2>=0 and l1-l2<best: best=l1-l2
        elif words[i]==w2:
            l2=i
            if l1>=0 and l2-l1<best: best=l2-l1
    return best

def lists(words, w1, w2):
    n=len(words); best=n
    p1=[i for i,w in enumerate(words) if w==w1]
    if w1==w2:
        for a in range(1,len(p1)):
            if p1[a]-p1[a-1]<best: best=p1[a]-p1[a-1]
        return best
    p2=[i for i,w in enumerate(words) if w==w2]
    a=b=0
    while a<len(p1) and b<len(p2):
        d=abs(p1[a]-p2[b])
        if d<best: best=d
        if p1[a]<p2[b]: a+=1
        else: b+=1
    return best

alpha=["a","b","c"]
acc=0; s=1; mismatches=0
for case in range(4000):
    s=lcg(s); n=1+(s//65536)%9
    words=[]
    for _ in range(n):
        s=lcg(s); words.append(alpha[(s//65536)%3])
    s=lcg(s); w1=alpha[(s//65536)%3]
    s=lcg(s); w2=alpha[(s//65536)%3]
    u,sp,li = unified(words,w1,w2), split(words,w1,w2), lists(words,w1,w2)
    if not (u==sp==li):
        mismatches+=1
        if mismatches<=3: print("MISMATCH", words, w1, w2, u, sp, li)
    acc=(acc*131+u)%1000000007
print("algorithms disagree on", mismatches, "of 4000 cases")
print(acc)
