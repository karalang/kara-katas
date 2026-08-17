// Benchmark harness for LeetCode #235 — Lowest Common Ancestor of a BST.
// Mirrors lca_bst.kara algorithm-for-algorithm, including the index-pool tree
// (slice of structs with int64 child indices, -1 = null) rather than
// pointer-linked nodes.
package main

import "fmt"

type Node struct {
	val   int64
	left  int64
	right int64
}

func lca(nodes []Node, root int64, p int64, q int64) int64 {
	cur := root
	for cur != -1 {
		v := nodes[cur].val
		if p < v && q < v {
			cur = nodes[cur].left
		} else if p > v && q > v {
			cur = nodes[cur].right
		} else {
			return v
		}
	}
	return -1
}

const (
	N     = 200000
	Iters = 8000000
)

func main() {
	vals := make([]int64, 0, N)
	x := int64(7)
	for i := 0; i < N; i++ {
		x = (x*1103515245 + 12345) % 2147483648
		hi := x / 65536
		x = (x*1103515245 + 12345) % 2147483648
		vals = append(vals, (hi*32768+x/65536)%1000000)
	}

	nodes := make([]Node, 0, N)
	root := int64(-1)
	for b := 0; b < N; b++ {
		v := vals[b]
		if root == -1 {
			nodes = append(nodes, Node{val: v, left: -1, right: -1})
			root = 0
		} else {
			cur := root
			for {
				if v < nodes[cur].val {
					l := nodes[cur].left
					if l == -1 {
						idx := int64(len(nodes))
						nodes = append(nodes, Node{val: v, left: -1, right: -1})
						nodes[cur].left = idx
						break
					}
					cur = l
				} else {
					r := nodes[cur].right
					if r == -1 {
						idx := int64(len(nodes))
						nodes = append(nodes, Node{val: v, left: -1, right: -1})
						nodes[cur].right = idx
						break
					}
					cur = r
				}
			}
		}
	}

	var sink int64
	y := int64(99)
	for it := 0; it < Iters; it++ {
		y = (y*1103515245 + 12345) % 2147483648
		phi := y / 65536
		y = (y*1103515245 + 12345) % 2147483648
		pi := (phi*32768 + y/65536) % N
		y = (y*1103515245 + 12345) % 2147483648
		qhi := y / 65536
		y = (y*1103515245 + 12345) % 2147483648
		qi := (qhi*32768 + y/65536) % N
		a := lca(nodes, root, vals[pi], vals[qi])
		sink = (sink + a) % 1000000007
	}
	fmt.Println(sink)
}
