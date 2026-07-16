// Benchmark workload for LeetCode #113 — path sum II, Go mirror (GC *Node + slice accumulator).
package main
import "fmt"
const MOD int64 = 1000000007
type Node struct { val int64; left, right *Node }
func buildPerfect(depth, val int64) *Node {
    if depth <= 0 { return nil }
    return &Node{val: val, left: buildPerfect(depth-1, val), right: buildPerfect(depth-1, val)}
}
func dfs(node *Node, target int64, path *[]int64, out *[][]int64) {
    if node == nil { return }
    *path = append(*path, node.val)
    rem := target - node.val
    if node.left == nil && node.right == nil {
        if rem == 0 {
            cp := make([]int64, len(*path)); copy(cp, *path); *out = append(*out, cp)
        }
    } else {
        dfs(node.left, rem, path, out); dfs(node.right, rem, path, out)
    }
    *path = (*path)[:len(*path)-1]
}
func main() {
    pool := make([]*Node, 8)
    for t := int64(0); t < 8; t++ { pool[t] = buildPerfect(5, t+1) }
    var acc int64 = 1
    for rep := 0; rep < 300000; rep++ {
        idx := acc % 8
        var out [][]int64
        var path []int64
        dfs(pool[idx], 5*(idx+1), &path, &out)
        h := int64(len(out))
        for _, p := range out { for _, v := range p { h = (h*131 + v) % MOD } }
        acc = (acc*1000003 + h + 1) % MOD
    }
    fmt.Println(acc)
}
