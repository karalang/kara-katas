// LeetCode #863: All Nodes Distance K in Binary Tree -- Go mirror of the
// bench program (the ★ arm, parents, then a breadth-first search).
package main

import (
	"fmt"
	"sort"
)

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func distanceK(root *TreeNode, target, k int64) []int64 {
	parent := map[int64]*TreeNode{}
	var start *TreeNode
	var stack []*TreeNode
	if root != nil {
		stack = append(stack, root)
	}
	for len(stack) > 0 {
		node := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if node.Val == target {
			start = node
		}
		if node.Left != nil {
			parent[node.Left.Val] = node
			stack = append(stack, node.Left)
		}
		if node.Right != nil {
			parent[node.Right.Val] = node
			stack = append(stack, node.Right)
		}
	}
	found := []int64{}
	if start == nil {
		return found
	}
	seen := map[int64]bool{start.Val: true}
	level := []*TreeNode{start}
	for step := int64(0); step < k; step++ {
		var next []*TreeNode
		for _, node := range level {
			var near []*TreeNode
			if node.Left != nil {
				near = append(near, node.Left)
			}
			if node.Right != nil {
				near = append(near, node.Right)
			}
			if up, ok := parent[node.Val]; ok {
				near = append(near, up)
			}
			for _, m := range near {
				if !seen[m.Val] {
					seen[m.Val] = true
					next = append(next, m)
				}
			}
		}
		level = next
	}
	for _, node := range level {
		found = append(found, node.Val)
	}
	sort.Slice(found, func(i, j int) bool { return found[i] < found[j] })
	return found
}

var seed int64 = 863

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int64) *TreeNode {
	vals := make([]int64, n)
	for v := range vals {
		vals[v] = int64(v)
	}
	for i := int64(1); i < n; i++ {
		j := nextRandom() % (i + 1)
		vals[i], vals[j] = vals[j], vals[i]
	}
	var nodes []*TreeNode
	for k := int64(0); k < n; k++ {
		node := &TreeNode{Val: vals[k]}
		if k > 0 {
			for {
				parent := nodes[nextRandom()%int64(len(nodes))]
				if nextRandom()%2 == 0 {
					if parent.Left == nil {
						parent.Left = node
						break
					}
				} else if parent.Right == nil {
					parent.Right = node
					break
				}
			}
		}
		nodes = append(nodes, node)
	}
	if n == 0 {
		return nil
	}
	return nodes[0]
}

func main() {
	var n int64 = 500
	queries := 200000
	root := randomTree(n)
	var total, check int64
	for q := 0; q < queries; q++ {
		target := nextRandom() % n
		k := nextRandom() % 20
		found := distanceK(root, target, k)
		total += int64(len(found))
		for _, v := range found {
			check = (check*31 + v + 1) % 1000000007
		}
	}
	fmt.Printf("%d queries on %d nodes: %d nodes found, checksum %d\n", queries, n, total, check)
}
