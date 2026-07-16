// LeetCode #114 bench — flatten, Go mirror (GC *Node, iterative Morris rewiring).
package main
import "fmt"
const MOD int64 = 1000000007
type Node struct { val int64; left, right *Node }
func buildBalanced(lo, hi int64) *Node {
    if lo > hi { return nil }
    mid := (lo + hi) / 2
    return &Node{val: mid, left: buildBalanced(lo, mid-1), right: buildBalanced(mid+1, hi)}
}
func flatten(root *Node) {
    curr := root
    for curr != nil {
        if curr.left != nil {
            prev := curr.left
            for prev.right != nil { prev = prev.right }
            prev.right = curr.right; curr.right = curr.left; curr.left = nil
        }
        curr = curr.right
    }
}
func spineHash(root *Node) int64 {
    var h int64 = 1
    for c := root; c != nil; c = c.right { h = (h*131 + c.val + 1000) % MOD }
    return h
}
func main() {
    var acc int64 = 1
    for rep := 0; rep < 200000; rep++ {
        base := acc % 100
        root := buildBalanced(base, base+62)
        flatten(root)
        h := spineHash(root)
        acc = (acc*1000003 + h + 1) % MOD
    }
    fmt.Println(acc)
}
