// Benchmark for #501: Go mirror of the ★ arm (in-order with a running
// count); see ../find_mode.kara.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

type Walk struct {
	prev, run, best int64
	modes           []int64
}

func visit(n *TreeNode, w *Walk) {
	if n == nil {
		return
	}
	visit(n.left, w)
	if w.run > 0 && n.val == w.prev {
		w.run++
	} else {
		w.prev = n.val
		w.run = 1
	}
	if w.run > w.best {
		w.best = w.run
		w.modes = w.modes[:0]
		w.modes = append(w.modes, n.val)
	} else if w.run == w.best {
		w.modes = append(w.modes, n.val)
	}
	visit(n.right, w)
}

func findMode(root *TreeNode) []int64 {
	w := Walk{}
	visit(root, &w)
	return w.modes
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
	// 100 random search trees of 10,000 values, drawn from 1 to 10
	// values, 1,000 values, or the whole range -100,000 to 100,000 in
	// turn, built once. Then the modes of each tree are found 30 times.
	trees := 100
	seed := int64(501)
	all := make([]*TreeNode, 0, trees)
	for t := 0; t < trees; t++ {
		var rng int64
		if t%3 == 0 {
			rng = 1 + nextRandom(&seed)%10
		} else if t%3 == 1 {
			rng = 1000
		} else {
			rng = 200001
		}
		values := make([]int64, 10000)
		for k := range values {
			v := nextRandom(&seed) * 7 % rng
			if rng == 200001 {
				v -= 100000
			}
			values[k] = v
		}
		all = append(all, build(values, &seed))
	}
	modes, checksum := int64(0), int64(0)
	for r := 0; r < 30; r++ {
		for t := 0; t < trees; t++ {
			for _, m := range findMode(all[t]) {
				modes++
				checksum = (checksum*31 + m + 100000) % 1000000007
			}
		}
	}
	fmt.Printf("%d trees of 10000 values, 30 times each: %d modes, checksum %d\n", trees, modes, checksum)
}
