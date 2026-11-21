// LeetCode #2458: Height of Binary Tree After Subtree Removal Queries --
// the bench, the ★ arm in Go: every subtree's height, then a walk down
// carrying the height the tree keeps without each node, both kept in a
// `map` by value. The nodes are `*TreeNode`.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func height(node *TreeNode, heights map[int64]int64) int64 {
	if node == nil {
		return -1
	}
	h := 1 + max(height(node.Left, heights), height(node.Right, heights))
	heights[int64(node.Val)] = h
	return h
}

func of(node *TreeNode, heights map[int64]int64) int64 {
	if node == nil {
		return -1
	}
	return heights[int64(node.Val)]
}

func walk(node *TreeNode, depth, rest int64, heights, answers map[int64]int64) {
	if node != nil {
		answers[int64(node.Val)] = rest
		walk(node.Left, depth+1, max(rest, depth+1+of(node.Right, heights)), heights, answers)
		walk(node.Right, depth+1, max(rest, depth+1+of(node.Left, heights)), heights, answers)
	}
}

func treeQueries(root *TreeNode, queries []int64) []int64 {
	heights := map[int64]int64{}
	height(root, heights)
	answers := map[int64]int64{}
	walk(root, 0, 0, heights, answers)
	out := make([]int64, len(queries))
	for i, q := range queries {
		out[i] = answers[q]
	}
	return out
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2458

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i + 1)
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % int64(i+1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := make([]*TreeNode, n)
	for i := range nodes {
		nodes[i] = &TreeNode{Val: values[i]}
	}
	for k := 1; k < n; k++ {
		high := nextRandom()
		at := nodes[(high*32768+nextRandom())%int64(k)]
		for {
			if nextRandom()%2 == 0 {
				if at.Left != nil {
					at = at.Left
				} else {
					at.Left = nodes[k]
					break
				}
			} else {
				if at.Right != nil {
					at = at.Right
				} else {
					at.Right = nodes[k]
					break
				}
			}
		}
	}
	return nodes[0]
}

func main() {
	// 20 random trees of 10^4 nodes built once; then 60 passes, each
	// asking every tree about every value but the root's, pass p starting
	// its queries p * 101 values along
	const n = 10000
	trees := make([]*TreeNode, 20)
	for t := range trees {
		trees[t] = randomTree(n)
	}
	check := int64(0)
	for p := int64(0); p < 60; p++ {
		for _, root := range trees {
			r := int64(root.Val)
			queries := []int64{}
			for i := int64(0); i < n; i++ {
				if v := 1 + (i+p*101)%n; v != r {
					queries = append(queries, v)
				}
			}
			for _, a := range treeQueries(root, queries) {
				check = (check*31 + a + p) % 1000000007
			}
		}
	}
	fmt.Printf("60 passes over 20 trees of 10^4: checksum %d\n", check)
}
