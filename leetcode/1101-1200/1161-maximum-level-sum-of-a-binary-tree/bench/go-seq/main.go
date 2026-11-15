// LeetCode #1161: Maximum Level Sum of a Binary Tree -- the bench in Go,
// the ★ arm over nodes on Go's collected heap, the same 16 trees and 200
// rounds. Each level's nodes go in a fresh slice.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func maxLevelSum(root *TreeNode) int64 {
	var level []*TreeNode
	if root != nil {
		level = append(level, root)
	}
	var best, bestSum, depth int64
	for len(level) > 0 {
		depth++
		var sum int64
		var next []*TreeNode
		for _, n := range level {
			sum += int64(n.Val)
			if n.Left != nil {
				next = append(next, n.Left)
			}
			if n.Right != nil {
				next = append(next, n.Right)
			}
		}
		if best == 0 || sum > bestSum {
			best, bestSum = depth, sum
		}
		level = next
	}
	return best
}

var seed int64 = 1161

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue() int32 {
	hi := nextRandom()
	lo := nextRandom()
	return int32((hi*32768+lo)%200001 - 100000)
}

// grow hangs a new node at a random free place below the tree's nodes.
func grow(nodes []*TreeNode) []*TreeNode {
	c := &TreeNode{Val: randomValue()}
	for {
		at := nodes[nextRandom()%int64(len(nodes))]
		if nextRandom()%2 == 0 {
			if at.Left == nil {
				at.Left = c
				break
			}
		} else if at.Right == nil {
			at.Right = c
			break
		}
	}
	return append(nodes, c)
}

func main() {
	trees := make([][]*TreeNode, 0, 16)
	for j := 0; j < 16; j++ {
		nodes := []*TreeNode{{Val: randomValue()}}
		for i := 1; i < 10000; i++ {
			nodes = grow(nodes)
		}
		trees = append(trees, nodes)
	}
	var total, check int64
	for round := 0; round < 200; round++ {
		for j := range trees {
			trees[j] = grow(trees[j])
			level := maxLevelSum(trees[j][0])
			total += level
			check = (check*31 + level) % 1000000007
		}
	}
	fmt.Printf("200 rounds over 16 trees of 10^4 nodes: levels total %d, checksum %d\n", total, check)
}
