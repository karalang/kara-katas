// Benchmark workload for LeetCode #108 — sorted array to BST, Go mirror (GC *Node).
// Build 8 sorted arrays once, then K reps of recursive middle-pick sorted_to_bst on a
// data-dependent-selected array, folding the built tree's serialization into a rolling hash.
// Each rep allocates a fresh 15-node balanced tree and lets the GC reclaim it.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
}

func build(arr []int64, lo, hi int64) *Node {
	if lo > hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &Node{
		val:   arr[mid],
		left:  build(arr, lo, mid-1),
		right: build(arr, mid+1, hi),
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

func main() {
	arrs := make([][]int64, 8)
	for t := int64(0); t < 8; t++ {
		a := make([]int64, 15)
		for i := int64(0); i < 15; i++ {
			a[i] = t*100 + i
		}
		arrs[t] = a
	}
	var acc int64 = 1
	for rep := int64(0); rep < 1200000; rep++ {
		idx := acc % 8
		root := build(arrs[idx], 0, 14)
		s := ser(root, 0)
		acc = (acc*131 + s) % MOD
	}
	fmt.Println(acc)
}
