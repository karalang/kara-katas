// LeetCode #1120: Maximum Average Subtree -- the bench in Go, the ★ arm
// over nodes on Go's collected heap, the same 16 trees and 200 rounds.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func walk(n *TreeNode, best *float64) (int64, int64) {
	if n == nil {
		return 0, 0
	}
	ls, lc := walk(n.Left, best)
	rs, rc := walk(n.Right, best)
	sum := ls + rs + int64(n.Val)
	count := lc + rc + 1
	average := float64(sum) / float64(count)
	if average > *best {
		*best = average
	}
	return sum, count
}

func maximumAverageSubtree(root *TreeNode) float64 {
	best := 0.0
	walk(root, &best)
	return best
}

var seed int64 = 1120

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue() int32 {
	hi := nextRandom()
	lo := nextRandom()
	return int32((hi*32768 + lo) % 100001)
}

func randomTree() []*TreeNode {
	nodes := []*TreeNode{{Val: randomValue()}}
	for i := 1; i < 10000; i++ {
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
		nodes = append(nodes, c)
	}
	return nodes
}

func main() {
	trees := make([][]*TreeNode, 16)
	for j := range trees {
		trees[j] = randomTree()
	}
	total := 0.0
	var check int64
	for round := int64(0); round < 200; round++ {
		for j := range trees {
			at := (round*7919 + int64(j)*104729) % 10000
			n := trees[j][at]
			n.Val = int32((int64(n.Val)*7 + round) % 100001)
			answer := maximumAverageSubtree(trees[j][0])
			total += answer
			check = (check*31 + int64(answer*1000.0)) % 1000000007
		}
	}
	fmt.Printf("200 rounds over 16 trees of 10^4 nodes: answers total %.3f, checksum %d\n", total, check)
}
