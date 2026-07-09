// Benchmark workload — Validate Binary Search Tree (LeetCode #98).
// Go single-threaded mirror of bench/validate_bst.{kara,rs,c}. Each iteration
// builds a fresh 63-node balanced BST (GC-managed pointers), runs the ★'s
// recursive (lo,hi)-bounds validator, folds shift+valid into a rolling
// polynomial hash; the tree is left to the GC — the Go analogue of Kāra's
// per-iteration RC build/validate/drop. See ../README.md § Benchmarks.

package main

import "fmt"

type node struct {
	val         int64
	left, right *node
}

func build(lo, hi, shift int64) *node {
	if lo > hi {
		return nil
	}
	mid := lo + (hi-lo)/2
	return &node{
		val:   shift + mid,
		left:  build(lo, mid-1, shift),
		right: build(mid+1, hi, shift),
	}
}

// hasLo / hasHi model the Option[i64] bounds (nil = no bound on that side).
func isValid(n *node, lo int64, hasLo bool, hi int64, hasHi bool) bool {
	if n == nil {
		return true
	}
	if hasLo && n.val <= lo {
		return false
	}
	if hasHi && n.val >= hi {
		return false
	}
	return isValid(n.left, lo, hasLo, n.val, true) && isValid(n.right, n.val, true, hi, hasHi)
}

func main() {
	const total int64 = 200000
	const modulus int64 = 1000000007
	const size int64 = 63

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		shift := k % 1000
		root := build(0, size-1, shift)
		var bit int64 = 0
		if isValid(root, 0, false, 0, false) {
			bit = 1
		}
		acc = (acc*131 + shift + bit) % modulus
	}
	fmt.Println(acc)
}
