// Benchmark workload for LeetCode #111 — minimum depth, Go mirror (*Node, read-only).
// Build 8 balanced 31-node trees once, then K reps of recursive min_depth on a data-dependent-
// selected tree, folding each min depth into a rolling hash. Read-only per-node post-order.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
}

func buildBalanced(lo, hi int64) *Node {
	if lo > hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &Node{
		val:   mid,
		left:  buildBalanced(lo, mid-1),
		right: buildBalanced(mid+1, hi),
	}
}
func minDepth(n *Node) int64 {
	if n == nil {
		return 0
	}
	ld := minDepth(n.left)
	rd := minDepth(n.right)
	if ld == 0 {
		return 1 + rd
	}
	if rd == 0 {
		return 1 + ld
	}
	if ld < rd {
		return 1 + ld
	}
	return 1 + rd
}

func main() {
	pool := make([]*Node, 8)
	for t := int64(0); t < 8; t++ {
		pool[t] = buildBalanced(t*100, t*100+30)
	}
	var acc int64 = 1
	for rep := int64(0); rep < 3000000; rep++ {
		idx := acc % 8
		d := minDepth(pool[idx])
		acc = (acc*131 + d + 1) % MOD
	}
	fmt.Println(acc)
}
