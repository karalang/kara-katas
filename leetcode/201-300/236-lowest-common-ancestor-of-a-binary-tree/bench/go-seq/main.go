// Benchmark harness for LeetCode #236 — LCA of a Binary Tree.
// Mirrors lca_binary_tree.kara algorithm-for-algorithm, including the
// index-pool tree and the recursive post-order search.
package main

import "fmt"

type Node struct {
	val   int64
	left  int64
	right int64
}

func lca(nodes []Node, cur int64, p int64, q int64) int64 {
	if cur == -1 {
		return -1
	}
	if nodes[cur].val == p || nodes[cur].val == q {
		return cur
	}
	l := lca(nodes, nodes[cur].left, p, q)
	r := lca(nodes, nodes[cur].right, p, q)
	if l != -1 && r != -1 {
		return cur
	}
	if l != -1 {
		return l
	}
	return r
}

const (
	N     = 100000
	Iters = 600
)

func main() {
	nodes := make([]Node, 0, N)
	for i := int64(0); i < N; i++ {
		lc := 2*i + 1
		rc := 2*i + 2
		l := int64(-1)
		if lc < N {
			l = lc
		}
		r := int64(-1)
		if rc < N {
			r = rc
		}
		nodes = append(nodes, Node{val: i, left: l, right: r})
	}

	var sink int64
	y := int64(2024)
	for it := 0; it < Iters; it++ {
		y = (y*1103515245 + 12345) % 2147483648
		wd1 := y / 65536
		y = (y*1103515245 + 12345) % 2147483648
		p := (wd1 * 32768 + y / 65536) % N
		y = (y*1103515245 + 12345) % 2147483648
		wd0 := y / 65536
		y = (y*1103515245 + 12345) % 2147483648
		q := (wd0 * 32768 + y / 65536) % N
		ans := lca(nodes, 0, p, q)
		v := int64(-1)
		if ans != -1 {
			v = nodes[ans].val
		}
		sink = (sink + v) % 1000000007
	}
	fmt.Println(sink)
}
