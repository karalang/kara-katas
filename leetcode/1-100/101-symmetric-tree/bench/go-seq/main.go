// Benchmark workload for LeetCode #101 — symmetric tree, Go mirror (*Node, read-only).
package main

import "fmt"

const mod = 1000000007

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
func mirror(n *Node) *Node {
	if n == nil {
		return nil
	}
	return &Node{val: n.val, left: mirror(n.right), right: mirror(n.left)}
}
func copyTree(n *Node) *Node {
	if n == nil {
		return nil
	}
	return &Node{val: n.val, left: copyTree(n.left), right: copyTree(n.right)}
}
func isMirror(a, b *Node) bool {
	if a == nil {
		return b == nil
	}
	if b == nil {
		return false
	}
	return a.val == b.val && isMirror(a.left, b.right) && isMirror(a.right, b.left)
}
func isSymmetric(root *Node) bool {
	if root == nil {
		return true
	}
	return isMirror(root.left, root.right)
}
func main() {
	base := []int64{8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15}
	bn := int64(15)
	var pool [8]*Node
	for i := int64(0); i < 8; i++ {
		var sub *Node
		for k := int64(0); k < bn; k++ {
			sub = insert(sub, base[(k+i)%bn])
		}
		root := &Node{val: 0, left: sub}
		if (i % 2) == 0 {
			root.right = mirror(sub)
		} else {
			root.right = copyTree(sub)
		}
		pool[i] = root
	}
	var acc int64 = 1
	for rep := 0; rep < 8000000; rep++ {
		idx := acc % 8
		sym := isSymmetric(pool[idx])
		b := int64(0)
		if sym {
			b = 1
		}
		acc = (acc*131 + b + 1) % mod
	}
	fmt.Printf("%d\n", acc)
}
