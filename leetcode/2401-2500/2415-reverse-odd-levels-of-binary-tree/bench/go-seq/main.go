// LeetCode #2415: Reverse Odd Levels of Binary Tree -- the bench, the ★ arm
// in Go: mirror pairs walked down together, the values of each pair on an
// odd level swapped.

package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func swapPairs(a, b *TreeNode, odd bool) {
	if a != nil && b != nil {
		if odd {
			a.Val, b.Val = b.Val, a.Val
		}
		swapPairs(a.Left, b.Right, !odd)
		swapPairs(a.Right, b.Left, !odd)
	}
}

func reverseOddLevels(root *TreeNode) *TreeNode {
	if root != nil {
		swapPairs(root.Left, root.Right, true)
	}
	return root
}

var seed int64 = 2415

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func edge(root *TreeNode, left bool) int64 {
	at := root
	for {
		next := at.Right
		if left {
			next = at.Left
		}
		if next == nil {
			return int64(at.Val)
		}
		at = next
	}
}

func main() {
	roots := make([]*TreeNode, 0, 10)
	for t := 0; t < 10; t++ {
		nodes := make([]*TreeNode, 16383)
		for i := range nodes {
			hi := nextRandom()
			lo := nextRandom()
			nodes[i] = &TreeNode{Val: int32((hi*32768 + lo) % 100000)}
		}
		for i := 0; i < 8191; i++ {
			nodes[i].Left = nodes[2*i+1]
			nodes[i].Right = nodes[2*i+2]
		}
		roots = append(roots, nodes[0])
	}
	var check int64
	for p := int64(0); p < 1000; p++ {
		for _, root := range roots {
			r := reverseOddLevels(root)
			check = (check*31 + int64(r.Left.Val) + p) % 1000000007
			check = (check*31 + int64(r.Right.Val) + edge(r, true) + edge(r, false)) % 1000000007
		}
	}
	fmt.Printf("1000 passes over 10 trees of 2^14 - 1 nodes: checksum %d\n", check)
}
