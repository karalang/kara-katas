// Benchmark workload for LeetCode #99 — recover BST, Go mirror (*Node tree).
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
func collect(node *Node, arr *[]*Node) {
	if node == nil {
		return
	}
	collect(node.left, arr)
	*arr = append(*arr, node)
	collect(node.right, arr)
}
func sumInorder(node *Node, acc *int64) {
	if node == nil {
		return
	}
	sumInorder(node.left, acc)
	*acc = (*acc*131 + node.val) % mod
	sumInorder(node.right, acc)
}
func recover_(root *Node, n int64) {
	buf := make([]*Node, 0, n)
	collect(root, &buf)
	var fi, si int64 = -1, -1
	for i := int64(1); i < int64(len(buf)); i++ {
		if buf[i-1].val > buf[i].val {
			if fi < 0 {
				fi = i - 1
			}
			si = i
		}
	}
	if fi >= 0 {
		buf[fi].val, buf[si].val = buf[si].val, buf[fi].val
	}
}
func corrupt2(root *Node, a, b, n int64) {
	buf := make([]*Node, 0, n)
	collect(root, &buf)
	if a != b {
		buf[a].val, buf[b].val = buf[b].val, buf[a].val
	}
}
func main() {
	vals := []int64{16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31}
	n := int64(31)
	var root *Node
	for _, v := range vals {
		root = insert(root, v)
	}
	var acc int64 = 1
	for rep := 0; rep < 700000; rep++ {
		a, b := acc%n, (acc*7+3)%n
		corrupt2(root, a, b, n)
		var cs int64 = 0
		sumInorder(root, &cs)
		acc = (acc*131 + cs) % mod
		recover_(root, n)
	}
	fmt.Printf("%d\n", acc)
}
