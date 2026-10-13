// Benchmark for #515: Go mirror of the ★ arm (level by level); see
// ../largest_values.kara. The queue is a fresh slice for every call,
// read from the front.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func largestValues(root *TreeNode) []int64 {
	var largest []int64
	var queue []*TreeNode
	if root != nil {
		queue = append(queue, root)
	}
	for len(queue) > 0 {
		best := int64(-1 << 63)
		width := len(queue)
		for i := 0; i < width; i++ {
			node := queue[0]
			queue = queue[1:]
			if node.val > best {
				best = node.val
			}
			if node.left != nil {
				queue = append(queue, node.left)
			}
			if node.right != nil {
				queue = append(queue, node.right)
			}
		}
		largest = append(largest, best)
	}
	return largest
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
	seed := int64(515)
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
	var rows, checksum int64
	for r := 0; r < 50; r++ {
		for t := 0; t < trees; t++ {
			largest := largestValues(all[t])
			rows += int64(len(largest))
			for _, v := range largest {
				checksum = (checksum*31 + v + 2147483648) % 1000000007
			}
		}
	}
	fmt.Printf("%d trees of 10000 nodes, 50 times each: %d rows, checksum %d\n", trees, rows, checksum)
}
