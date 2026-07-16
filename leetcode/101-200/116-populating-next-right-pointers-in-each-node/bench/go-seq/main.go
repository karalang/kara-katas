// LeetCode #116 — Go mirror (raw *Node, GC), O(1)-space next-pointer population.
// Same algorithm + workload as connect.kara: depth-9 perfect tree, data-dependent base, K = 40000.
// The GC data point — per-rep tree allocation feeds the collector.
package main

import "fmt"

const MOD int64 = 1000000007

type Node struct {
	val         int64
	left, right *Node
	next        *Node
}

func buildPerfect(idx, maxIdx, base int64) *Node {
	if idx > maxIdx {
		return nil
	}
	n := &Node{val: idx + base}
	n.left = buildPerfect(2*idx, maxIdx, base)
	n.right = buildPerfect(2*idx+1, maxIdx, base)
	return n
}

func connect(root *Node) {
	leftmost := root
	for leftmost != nil && leftmost.left != nil {
		head := leftmost
		for head != nil {
			head.left.next = head.right
			if head.next != nil {
				head.right.next = head.next.left
			}
			head = head.next
		}
		leftmost = leftmost.left
	}
}

func levelHash(root *Node) int64 {
	var h int64 = 1
	leftmost := root
	for leftmost != nil {
		cur := leftmost
		for cur != nil {
			h = (h*131 + cur.val + 1) % MOD
			cur = cur.next
		}
		h = (h*31 + 7) % MOD
		leftmost = leftmost.left
	}
	return h
}

func main() {
	const maxIdx int64 = 511 // depth-9 perfect tree
	var acc int64 = 0
	for rep := 0; rep < 40000; rep++ {
		base := acc % 100
		root := buildPerfect(1, maxIdx, base)
		connect(root)
		h := levelHash(root)
		acc = (acc*131 + h) % MOD
	}
	fmt.Println(acc)
}
