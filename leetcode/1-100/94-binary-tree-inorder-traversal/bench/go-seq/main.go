// Benchmark workload — Binary Tree Inorder Traversal (LeetCode #94).
// Go mirror of ../inorder.kara. Each of K=320,000 iterations builds a fresh 63-node
// balanced tree (GC-managed *Node) and folds a recursive inorder walk into a rolling
// hash in visit order. K=320,000. See ../README.md § Benchmarks.
package main

import "fmt"

type Node struct {
	val         int64
	left, right *Node
}

func build(lo, hi, shift int64) *Node {
	if lo > hi {
		return nil
	}
	mid := lo + (hi-lo)/2
	return &Node{
		val:   shift + mid,
		left:  build(lo, mid-1, shift),
		right: build(mid+1, hi, shift),
	}
}

func inorderFold(node *Node, acc *int64) {
	if node == nil {
		return
	}
	inorderFold(node.left, acc)
	*acc = (*acc*131 + (node.val + 1)) % 1000000007
	inorderFold(node.right, acc)
}

func main() {
	const total = 320000
	const modulus = 1000000007
	const size = 63
	var sum int64 = 0
	for k := int64(0); k < total; k++ {
		shift := k % 1000
		root := build(0, size-1, shift)
		var acc int64 = 0
		inorderFold(root, &acc)
		sum = (sum*131 + acc) % modulus
	}
	fmt.Println(sum)
}
