// Benchmark mirror for #637: the same workload and algorithm as
// average_of_levels.kara (breadth first, one level at a time). The queue
// is a slice taken from the front.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func averageOfLevels(root *TreeNode) []float64 {
	var averages []float64
	var queue []*TreeNode
	if root != nil {
		queue = append(queue, root)
	}
	for len(queue) > 0 {
		count := len(queue)
		var sum int64
		for i := 0; i < count; i++ {
			node := queue[0]
			queue = queue[1:]
			sum += node.Val
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		averages = append(averages, float64(sum)/float64(count))
	}
	return averages
}

var seed int64 = 637

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue() int64 {
	high := nextRandom() % 65536
	low := nextRandom() % 65536
	return high*65536 + low - 2147483648
}

func randomTree(size int) *TreeNode {
	var root *TreeNode
	for k := 0; k < size; k++ {
		c := &TreeNode{Val: randomValue()}
		if root == nil {
			root = c
			continue
		}
		node := root
		for {
			if nextRandom()%2 == 0 {
				if node.Left != nil {
					node = node.Left
				} else {
					node.Left = c
					break
				}
			} else {
				if node.Right != nil {
					node = node.Right
				} else {
					node.Right = c
					break
				}
			}
		}
	}
	return root
}

func main() {
	var trees []*TreeNode
	for i := 0; i < 10; i++ {
		trees = append(trees, randomTree(10000))
	}
	levels := 0
	total := 0.0
	for r := 0; r < 4000; r++ {
		for _, a := range averageOfLevels(trees[r%10]) {
			levels++
			total += a
		}
	}
	fmt.Printf("10 trees of 10000 nodes, 4000 rounds: %d levels, sum of averages %.3f\n", levels, total)
}
