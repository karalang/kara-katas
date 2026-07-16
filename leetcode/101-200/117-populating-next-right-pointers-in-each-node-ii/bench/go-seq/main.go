// LeetCode #117 — Go mirror (raw *Node, GC), O(1)-space next-pointer population on an arbitrary tree.
// Same algorithm + workload as connect.kara: ~500-node BST (fixed shape, data-dependent value base),
// dummy-head + tail threading, K = 16000. The GC data point — per-rep tree allocation feeds the GC.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
	next        *Node
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

func buildBST(count, base int64) *Node {
	var root *Node
	var s int64 = 88172645
	for i := int64(0); i < count; i++ {
		s = (s*1103515245 + 12345) % 2147483648
		root = insert(root, (s%100000)+base)
	}
	return root
}

func connect(root *Node) {
	leftmost := root
	for leftmost != nil {
		var dummy Node
		tail := &dummy
		cur := leftmost
		for cur != nil {
			if cur.left != nil {
				tail.next = cur.left
				tail = cur.left
			}
			if cur.right != nil {
				tail.next = cur.right
				tail = cur.right
			}
			cur = cur.next
		}
		leftmost = dummy.next
	}
}

func levelHash(root *Node) int64 {
	var h int64 = 1
	head := root
	for head != nil {
		cur := head
		for cur != nil {
			h = (h*131 + cur.val + 1) % MOD
			cur = cur.next
		}
		h = (h*31 + 7) % MOD
		var nh *Node
		scan := head
		for scan != nil {
			if scan.left != nil {
				nh = scan.left
				break
			}
			if scan.right != nil {
				nh = scan.right
				break
			}
			scan = scan.next
		}
		head = nh
	}
	return h
}

func main() {
	var acc int64 = 0
	for rep := 0; rep < 16000; rep++ {
		base := acc % 100
		root := buildBST(500, base)
		connect(root)
		h := levelHash(root)
		acc = (acc*131 + h) % MOD
	}
	fmt.Println(acc)
}
