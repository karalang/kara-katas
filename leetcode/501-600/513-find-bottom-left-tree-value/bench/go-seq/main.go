// Benchmark for #513: Go mirror of the ★ arm (level by level); see
// ../find_bottom_left_value.kara. The queue is a fresh slice for every
// call, read from the front.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func findBottomLeftValue(root *TreeNode) int64 {
	queue := []*TreeNode{root}
	leftmost := root.val
	for len(queue) > 0 {
		leftmost = queue[0].val
		width := len(queue)
		for i := 0; i < width; i++ {
			node := queue[0]
			queue = queue[1:]
			if node.left != nil {
				queue = append(queue, node.left)
			}
			if node.right != nil {
				queue = append(queue, node.right)
			}
		}
	}
	return leftmost
}

// ---- benchmark --------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func build(values []int64, lo, hi int64, seed *int64) *TreeNode {
	if lo >= hi {
		return nil
	}
	mid := lo + nextRandom(seed)%(hi-lo)
	left := build(values, lo, mid, seed)
	right := build(values, mid+1, hi, seed)
	return &TreeNode{val: values[mid], left: left, right: right}
}

func main() {
	// 100 random trees of 10,000 nodes, the values from the whole range
	// -2^31 to 2^31 - 1, built once. Then each is solved 50 times.
	trees := 100
	seed := int64(513)
	all := make([]*TreeNode, 0, trees)
	values := make([]int64, 10000)
	for t := 0; t < trees; t++ {
		for k := range values {
			a := nextRandom(&seed)
			b := nextRandom(&seed)
			c := nextRandom(&seed)
			values[k] = a*65536 + b*2 + c%2 - 2147483648
		}
		all = append(all, build(values, 0, 10000, &seed))
	}
	var checksum int64
	for r := 0; r < 50; r++ {
		for t := 0; t < trees; t++ {
			checksum = (checksum*31 + findBottomLeftValue(all[t]) + 2147483648) % 1000000007
		}
	}
	fmt.Printf("%d trees of 10000 nodes, 50 times each: checksum %d\n", trees, checksum)
}
