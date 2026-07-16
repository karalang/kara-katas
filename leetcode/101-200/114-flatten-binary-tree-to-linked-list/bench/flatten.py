# LeetCode #114 bench — flatten, Python mirror (smaller K, timed separately).
import sys
sys.setrecursionlimit(100000)
MOD = 1000000007
class Node:
    __slots__=("val","left","right")
    def __init__(s,v): s.val=v; s.left=None; s.right=None
def build_balanced(lo,hi):
    if lo>hi: return None
    mid=(lo+hi)//2
    n=Node(mid); n.left=build_balanced(lo,mid-1); n.right=build_balanced(mid+1,hi); return n
def flatten(root):
    curr=root
    while curr is not None:
        if curr.left is not None:
            prev=curr.left
            while prev.right is not None: prev=prev.right
            prev.right=curr.right; curr.right=curr.left; curr.left=None
        curr=curr.right
def spine_hash(root):
    h=1; c=root
    while c is not None: h=(h*131+c.val+1000)%MOD; c=c.right
    return h
def main():
    acc=1
    for _ in range(10000):
        base=acc%100
        root=build_balanced(base,base+62)
        flatten(root)
        acc=(acc*1000003 + spine_hash(root) + 1)%MOD
    print(acc)
main()
