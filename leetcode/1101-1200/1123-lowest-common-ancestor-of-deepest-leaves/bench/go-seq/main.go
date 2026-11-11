// LeetCode #1123: Lowest Common Ancestor of Deepest Leaves -- the bench in
// Go, the ★ arm over nodes on Go's collected heap, the same 16 trees and 200
// rounds.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func walk(n *TreeNode) (int64, *TreeNode) {
	if n == nil {
		return 0, nil
	}
	ld, la := walk(n.Left)
	rd, ra := walk(n.Right)
	if ld == rd {
		return ld + 1, n
	}
	if ld > rd {
		return ld + 1, la
	}
	return rd + 1, ra
}

func lcaDeepestLeaves(root *TreeNode) *TreeNode {
	_, a := walk(root)
	return a
}

var seed int64 = 1123

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomValue() int32 {
	hi := nextRandom()
	lo := nextRandom()
	return int32((hi*32768 + lo) % 100001)
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
			answer := lcaDeepestLeaves(trees[j][0])
			total += int64(answer.Val)
			check = (check*31 + int64(answer.Val)) % 1000000007
		}
	}
	fmt.Printf("200 rounds over 16 trees of 10^4 nodes: answers total %d, checksum %d\n", total, check)
}
