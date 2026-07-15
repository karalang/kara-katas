// Benchmark workload for LeetCode #104 — max depth, Go mirror (*Node, read-only).
// Build 8 BSTs once, then K reps of recursive max_depth on a data-dependent-selected tree,
// folding each depth into a rolling hash. Read-only per-node traversal, no allocation.
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
func maxDepth(n *Node) int64 {
	if n == nil {
		return 0
	}
	lh := maxDepth(n.left)
	rh := maxDepth(n.right)
	if lh > rh {
		return 1 + lh
	}
	return 1 + rh
}

func main() {
	base := []int64{16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30}
	bn := int64(len(base))
	pool := make([]*Node, 8)
	for t := int64(0); t < 8; t++ {
		var root *Node
		for k := int64(0); k < bn; k++ {
			root = insert(root, base[(k+t)%bn])
		}
		pool[t] = root
	}
	var acc int64 = 1
	for rep := int64(0); rep < 4000000; rep++ {
		idx := acc % 8
		d := maxDepth(pool[idx])
		acc = (acc*131 + d + 1) % MOD
	}
	fmt.Println(acc)
}
