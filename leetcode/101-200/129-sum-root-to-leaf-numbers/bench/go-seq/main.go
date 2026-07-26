// Benchmark harness for LeetCode #129 — Sum Root to Leaf Numbers.
// Mirrors sum_numbers.kara algorithm-for-algorithm.
//
// Uses GC'd pointer-linked nodes — Go's native model. Unlike kara
// (`shared struct`, reference counted) and the Rust mirror (Rc), this lane pays
// no retain/release traffic during the traversal. See ../README.md.
package main

import "fmt"

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func sumDfs(node *TreeNode, acc int64) int64 {
	if node == nil {
		return 0
	}
	cur := acc*10 + node.val
	if node.left == nil && node.right == nil {
		return cur
	}
	return sumDfs(node.left, cur) + sumDfs(node.right, cur)
}

func digit(i int64, seed int64) int64 { return ((i*7 + seed*3) % 9) + 1 }

func buildBalanced(lo int64, hi int64, seed int64) *TreeNode {
	if lo > hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &TreeNode{
		val:   digit(mid, seed),
		left:  buildBalanced(lo, mid-1, seed),
		right: buildBalanced(mid+1, hi, seed),
	}
}

const (
	NP    = 4
	N     = 2047
	Iters = 40000
)

func main() {
	trees := make([]*TreeNode, NP)
	for j := int64(0); j < NP; j++ {
		trees[j] = buildBalanced(0, N-1, j+1)
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % NP
		sink = (sink + sumDfs(trees[idx], 0)) % 1000000007
	}
	fmt.Println(sink)
}
