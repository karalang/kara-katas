// Benchmark workload for LeetCode #103 — construct binary tree, Go mirror (GC *Node).
// Build 8 (preorder, inorder) input pairs once, then K reps of the recursive index-bounds
// reconstruction on a data-dependent-selected pair, folding the rebuilt tree's serialization
// into a rolling hash. Each rep allocates a fresh 15-node tree and lets the GC reclaim it.
// Linear inorder scan (O(n^2)) for parity.
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
func findIn(in []int64, lo, hi, target int64) int64 {
	for i := lo; i <= hi; i++ {
		if in[i] == target {
			return i
		}
	}
	return -1
}
func build(pre, in []int64, plo, phi, ilo, ihi int64) *Node {
	if plo > phi {
		return nil
	}
	rv := pre[plo]
	mid := findIn(in, ilo, ihi, rv)
	lsize := mid - ilo
	return &Node{
		val:   rv,
		left:  build(pre, in, plo+1, plo+lsize, ilo, mid-1),
		right: build(pre, in, plo+lsize+1, phi, mid+1, ihi),
	}
}
func ser(n *Node, acc int64) int64 {
	if n == nil {
		return (acc*131 + 1) % MOD
	}
	acc = (acc*131 + (n.val + 2)) % MOD
	acc = ser(n.left, acc)
	acc = ser(n.right, acc)
	return acc
}
func preorderOf(n *Node, out *[]int64) {
	if n == nil {
		return
	}
	*out = append(*out, n.val)
	preorderOf(n.left, out)
	preorderOf(n.right, out)
}
func inorderOf(n *Node, out *[]int64) {
	if n == nil {
		return
	}
	inorderOf(n.left, out)
	*out = append(*out, n.val)
	inorderOf(n.right, out)
}

func main() {
	base := []int64{8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15}
	bn := int64(len(base))
	pres := make([][]int64, 8)
	inos := make([][]int64, 8)
	for t := int64(0); t < 8; t++ {
		var root *Node
		for k := int64(0); k < bn; k++ {
			root = insert(root, base[(k+t)%bn])
		}
		var pre, ino []int64
		preorderOf(root, &pre)
		inorderOf(root, &ino)
		pres[t] = pre
		inos[t] = ino
	}
	var acc int64 = 1
	for rep := int64(0); rep < 800000; rep++ {
		idx := acc % 8
		rebuilt := build(pres[idx], inos[idx], 0, bn-1, 0, bn-1)
		s := ser(rebuilt, 0)
		acc = (acc*131 + s) % MOD
	}
	fmt.Println(acc)
}
