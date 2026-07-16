// Benchmark workload for LeetCode #112 — path sum, Go mirror (*Node, read-only).
// Build 8 balanced 31-node trees once, then K reps of has_path_sum against an unachievable
// target (full traversal) on a data-dependent-selected tree, folding each verdict.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
}

func build(lo, hi int64) *Node {
	if lo > hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &Node{val: mid, left: build(lo, mid-1), right: build(mid+1, hi)}
}
func hasPathSum(n *Node, target int64) bool {
	if n == nil {
		return false
	}
	rem := target - n.val
	if n.left == nil && n.right == nil {
		return rem == 0
	}
	return hasPathSum(n.left, rem) || hasPathSum(n.right, rem)
}

func main() {
	pool := make([]*Node, 8)
	for t := int64(0); t < 8; t++ {
		pool[t] = build(t*100, t*100+30)
	}
	var acc int64 = 1
	for rep := int64(0); rep < 6000000; rep++ {
		idx := acc % 8
		bit := int64(0)
		if hasPathSum(pool[idx], 1000000000) {
			bit = 1
		}
		acc = (acc*131 + bit + 1) % MOD
	}
	fmt.Println(acc)
}
