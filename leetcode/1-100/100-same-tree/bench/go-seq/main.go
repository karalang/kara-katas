// Benchmark workload for LeetCode #100 — same tree, Go mirror (*Node, read-only).
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
func isSame(p, q *Node) bool {
	if p == nil {
		return q == nil
	}
	if q == nil {
		return false
	}
	return p.val == q.val && isSame(p.left, q.left) && isSame(p.right, q.right)
}
func main() {
	base := []int64{16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30}
	bn := int64(15)
	var poolP, poolQ [8]*Node
	for i := int64(0); i < 8; i++ {
		var p, q *Node
		for k := int64(0); k < bn; k++ {
			p = insert(p, base[k])
			var bump int64 = 0
			if (i%2) == 1 && k == (i%bn) {
				bump = 1
			}
			q = insert(q, base[k]+bump)
		}
		poolP[i] = p
		poolQ[i] = q
	}
	var acc int64 = 1
	for rep := 0; rep < 6000000; rep++ {
		idx := acc % 8
		same := isSame(poolP[idx], poolQ[idx])
		b := int64(0)
		if same {
			b = 1
		}
		acc = (acc*131 + b + 1) % mod
	}
	fmt.Printf("%d\n", acc)
}
