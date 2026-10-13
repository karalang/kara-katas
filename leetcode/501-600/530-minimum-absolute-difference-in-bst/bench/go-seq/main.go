// Benchmark for #530: Go mirror of the ★ arm (in-order, recursively);
// see ../get_minimum_difference.kara.
package main

import (
	"fmt"
	"math"
)

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

type Walk struct {
	hasPrev    bool
	prev, best int64
}

func visit(n *TreeNode, w *Walk) {
	if n == nil {
		return
	}
	visit(n.left, w)
	if w.hasPrev && n.val-w.prev < w.best {
		w.best = n.val - w.prev
	}
	w.prev = n.val
	w.hasPrev = true
	visit(n.right, w)
}

func getMinimumDifference(root *TreeNode) int64 {
	w := Walk{best: math.MaxInt64}
	visit(root, &w)
	return w.best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func build(values []int64, seed *int64) *TreeNode {
	root := &TreeNode{val: values[0]}
	for _, v := range values[1:] {
		node := root
		for {
			if v < node.val || (v == node.val && nextRandom(seed)%2 == 0) {
				if node.left != nil {
					node = node.left
				} else {
					node.left = &TreeNode{val: v}
					break
				}
			} else {
				if node.right != nil {
					node = node.right
				} else {
					node.right = &TreeNode{val: v}
					break
				}
			}
		}
	}
	return root
}

func main() {
	// 100 random search trees of 10,000 different values, drawn from 0
	// to 10,000, 0 to 20,000, ... up to 0 to 100,000 in turn, built once.
	// Then the answer for each tree is found 50 times.
	trees := 100
	seed := int64(530)
	all := make([]*TreeNode, 0, trees)
	for t := 0; t < trees; t++ {
		rng := int64(10000*(1+t%10) + 1)
		pool := make([]int64, rng)
		for v := range pool {
			pool[v] = int64(v)
		}
		for i := int64(0); i < 10000; i++ {
			high := nextRandom(&seed)
			j := i + (high*32768+nextRandom(&seed))%(rng-i)
			pool[i], pool[j] = pool[j], pool[i]
		}
		values := pool[:10000]
		all = append(all, build(values, &seed))
	}
	total, checksum := int64(0), int64(0)
	for r := 0; r < 50; r++ {
		for t := 0; t < trees; t++ {
			answer := getMinimumDifference(all[t])
			total += answer
			checksum = (checksum*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d trees of 10000 values, 50 times each: total %d, checksum %d\n", trees, total, checksum)
}
