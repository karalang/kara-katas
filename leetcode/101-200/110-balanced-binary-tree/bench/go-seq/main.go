// Benchmark workload for LeetCode #110 — balanced binary tree, Go mirror (*Node, read-only).
// Build 8 balanced 31-node trees once, then K reps of bottom-up single-pass is_balanced on a
// data-dependent-selected tree, folding each verdict into a rolling hash. Read-only per-node
// post-order traversal, no allocation.
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
func check(n *Node) int64 {
	if n == nil {
		return 0
	}
	lh := check(n.left)
	if lh == -1 {
		return -1
	}
	rh := check(n.right)
	if rh == -1 {
		return -1
	}
	diff := lh - rh
	if diff < 0 {
		diff = -diff
	}
	if diff > 1 {
		return -1
	}
	if lh > rh {
		return 1 + lh
	}
	return 1 + rh
}
func isBalanced(root *Node) bool { return check(root) != -1 }

func main() {
	pool := make([]*Node, 8)
	for t := int64(0); t < 8; t++ {
		pool[t] = buildBalanced(t*100, t*100+30)
	}
	var acc int64 = 1
	for rep := int64(0); rep < 3000000; rep++ {
		idx := acc % 8
		bit := int64(0)
		if isBalanced(pool[idx]) {
			bit = 1
		}
		acc = (acc*131 + bit + 1) % MOD
	}
	fmt.Println(acc)
}
