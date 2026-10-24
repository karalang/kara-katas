// Benchmark: LeetCode #987 Vertical Order Traversal of a Binary Tree --
// the ★ arm, every node's place sorted, on random trees of 1000 nodes,
// LeetCode's largest. Mirrors vertical_traversal.kara, .c, .rs and .py.
package main

import (
	"fmt"
	"sort"
)

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

type place struct{ col, row, val int64 }

func walk(t *TreeNode, row, col int64, out *[]place) {
	if t == nil {
		return
	}
	*out = append(*out, place{col, row, t.Val})
	walk(t.Left, row+1, col-1, out)
	walk(t.Right, row+1, col+1, out)
}

func verticalTraversal(root *TreeNode) [][]int64 {
	var places []place
	walk(root, 0, 0, &places)
	sort.Slice(places, func(i, j int) bool {
		a, b := places[i], places[j]
		if a.col != b.col {
			return a.col < b.col
		}
		if a.row != b.row {
			return a.row < b.row
		}
		return a.val < b.val
	})
	var out [][]int64
	var last int64
	for _, p := range places {
		if len(out) == 0 || p.col != last {
			out = append(out, nil)
			last = p.col
		}
		k := len(out) - 1
		out[k] = append(out[k], p.val)
	}
	return out
}

var seed int64 = 987

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	root := &TreeNode{Val: nextRandom() % 1001}
	for i := 1; i < n; i++ {
		node := &TreeNode{Val: nextRandom() % 1001}
		cur := root
		for {
			if nextRandom()%2 == 0 {
				if cur.Left != nil {
					cur = cur.Left
				} else {
					cur.Left = node
					break
				}
			} else {
				if cur.Right != nil {
					cur = cur.Right
				} else {
					cur.Right = node
					break
				}
			}
		}
	}
	return root
}

func main() {
	rounds := 500
	trees := make([]*TreeNode, 20)
	for i := range trees {
		trees[i] = randomTree(1000)
	}
	var columns, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			cols := verticalTraversal(trees[(r+i)%20])
			columns += int64(len(cols))
			mid := cols[len(cols)/2]
			check = (check*31 + int64(len(mid)) + mid[0]) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 trees of 1000 nodes: %d columns, checksum %d\n", rounds, columns, check)
}
