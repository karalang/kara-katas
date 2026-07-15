// Benchmark workload for LeetCode #107 — bottom-up level order, Go mirror (GC *Node).
// Build 8 BSTs once, then K reps of DFS-with-depth bottom-up level order on a data-dependent-
// selected tree, building a fresh [][]int64 output (rows deepest-first, mirroring the kara
// `out` allocation) and folding it into a rolling hash.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
}

func insert(root *Node, v int64) *Node {
	if root == nil {
		return &Node{val: v}
	}
	if v < root.val {
		root.left = insert(root.left, v)
	} else {
		root.right = insert(root.right, v)
	}
	return root
}
func dfs(node *Node, depth int, rows *[][]int64) {
	if node == nil {
		return
	}
	if depth == len(*rows) {
		*rows = append(*rows, []int64{})
	}
	(*rows)[depth] = append((*rows)[depth], node.val)
	dfs(node.left, depth+1, rows)
	dfs(node.right, depth+1, rows)
}
func levelOrderBottom(root *Node) [][]int64 {
	var rows [][]int64
	dfs(root, 0, &rows)
	out := make([][]int64, 0, len(rows))
	for d := len(rows) - 1; d >= 0; d-- {
		newrow := make([]int64, 0, len(rows[d]))
		newrow = append(newrow, rows[d]...)
		out = append(out, newrow)
	}
	return out
}

func main() {
	base := []int64{16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30}
	bn := len(base)
	pool := make([]*Node, 8)
	for t := 0; t < 8; t++ {
		var root *Node
		for k := 0; k < bn; k++ {
			root = insert(root, base[(k+t)%bn])
		}
		pool[t] = root
	}
	var acc int64 = 1
	for rep := int64(0); rep < 1000000; rep++ {
		idx := acc % 8
		levels := levelOrderBottom(pool[idx])
		acc = (acc*131 + int64(len(levels))) % MOD
		for _, lvl := range levels {
			acc = (acc*131 + int64(len(lvl))) % MOD
			for _, v := range lvl {
				acc = (acc*131 + v) % MOD
			}
		}
	}
	fmt.Println(acc)
}
