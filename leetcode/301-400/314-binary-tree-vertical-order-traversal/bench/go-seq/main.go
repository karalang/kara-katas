// Benchmark lane for LeetCode 314 — Go mirror of bench/vertical.kara.
// Grow POOL random trees of NODES GC nodes once, then PASSES vertical-order
// traversals (extent pass + level-frontier BFS into an offset-indexed
// [][]int64), each on the tree the running checksum selects. Every column's
// length and every value is folded into the masked checksum.
package main

import "fmt"

const (
	POOL   = 8
	NODES  = 50000
	PASSES = 240
	MASK   = int64(1073741823)
)

type Node struct {
	val         int64
	left, right *Node
}

type item struct {
	n *Node
	c int64
}

func lcg(s int64) int64 { return (s*1103515245 + 12345) & 0x7fffffff }

func grow(n int64, seed *int64) *Node {
	if n <= 0 {
		return nil
	}
	*seed = lcg(*seed)
	v := *seed%1000 - 500
	*seed = lcg(*seed)
	var leftN int64
	if n > 1 {
		leftN = *seed % n
	}
	rightN := n - 1 - leftN
	l := grow(leftN, seed)
	r := grow(rightN, seed)
	return &Node{val: v, left: l, right: r}
}

func extent(t *Node, col int64, lo, hi *int64) {
	if t == nil {
		return
	}
	if col < *lo {
		*lo = col
	}
	if col > *hi {
		*hi = col
	}
	extent(t.left, col-1, lo, hi)
	extent(t.right, col+1, lo, hi)
}

func verticalOrder(root *Node) [][]int64 {
	out := [][]int64{}
	if root == nil {
		return out
	}
	var lo, hi int64
	extent(root, 0, &lo, &hi)
	for i := lo; i <= hi; i++ {
		out = append(out, []int64{})
	}
	current := []item{{root, 0}}
	for len(current) > 0 {
		next := []item{}
		for _, it := range current {
			out[it.c-lo] = append(out[it.c-lo], it.n.val)
			if it.n.left != nil {
				next = append(next, item{it.n.left, it.c - 1})
			}
			if it.n.right != nil {
				next = append(next, item{it.n.right, it.c + 1})
			}
		}
		current = next
	}
	return out
}

func main() {
	seed := int64(314159)
	pool := make([]*Node, POOL)
	for i := 0; i < POOL; i++ {
		pool[i] = grow(NODES, &seed)
	}
	checksum := int64(0)
	for pass := 0; pass < PASSES; pass++ {
		which := checksum % POOL
		cols := verticalOrder(pool[which])
		checksum = (checksum + int64(len(cols))) & MASK
		for _, col := range cols {
			checksum = (checksum*31 + int64(len(col))) & MASK
			for _, v := range col {
				checksum = (checksum + v + 500) & MASK
			}
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
