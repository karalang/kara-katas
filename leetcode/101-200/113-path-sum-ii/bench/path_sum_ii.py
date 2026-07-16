# Benchmark workload for LeetCode #113 — path sum II, Python mirror (smaller K, timed separately).
import sys
sys.setrecursionlimit(100000)
MOD = 1000000007
class Node:
    __slots__=("val","left","right")
    def __init__(self,val): self.val=val; self.left=None; self.right=None
def build_perfect(depth,val):
    if depth<=0: return None
    n=Node(val); n.left=build_perfect(depth-1,val); n.right=build_perfect(depth-1,val); return n
def dfs(node,target,path,out):
    if node is None: return
    path.append(node.val); rem=target-node.val
    if node.left is None and node.right is None:
        if rem==0: out.append(list(path))
    else:
        dfs(node.left,rem,path,out); dfs(node.right,rem,path,out)
    path.pop()
def main():
    pool=[build_perfect(5,t+1) for t in range(8)]
    acc=1
    for _ in range(15000):
        idx=acc%8
        out=[]; dfs(pool[idx],5*(idx+1),[],out)
        h=len(out)
        for p in out:
            for v in p: h=(h*131+v)%MOD
        acc=(acc*1000003+h+1)%MOD
    print(acc)
main()
