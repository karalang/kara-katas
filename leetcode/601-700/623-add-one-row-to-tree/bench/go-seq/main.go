// LeetCode #623: Add One Row to Tree -- Go mirror of the Kāra bench.
//
// The ★ arm's recursion with the level, on the same trees and rounds,
// each row taken out again by the same `undo`.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func addOneRow(root *TreeNode, val, depth int64) *TreeNode {
	if depth == 1 {
		return &TreeNode{Val: val, Left: root}
	}
	insert(root, val, depth, 1)
	return root
}

func insert(n *TreeNode, val, depth, level int64) {
	if n == nil {
		return
	}
	if level == depth-1 {
		n.Left = &TreeNode{Val: val, Left: n.Left}
		n.Right = &TreeNode{Val: val, Right: n.Right}
	} else {
		insert(n.Left, val, depth, level+1)
		insert(n.Right, val, depth, level+1)
	}
}

var seed int64 = 623

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(size, lean int64) *TreeNode {
	root := &TreeNode{Val: nextRandom()%201 - 100}
	for i := int64(1); i < size; i++ {
		c := &TreeNode{Val: nextRandom()%201 - 100}
		node := root
		for {
			if nextRandom()%100 < lean {
				if node.Left == nil {
					node.Left = c
					break
				}
				node = node.Left
			} else {
				if node.Right == nil {
					node.Right = c
					break
				}
				node = node.Right
			}
		}
	}
	return root
}

var count, checksum int64

func undo(n *TreeNode, depth, level int64) {
	if n == nil {
		return
	}
	if level == depth-1 {
		l, r := n.Left, n.Right
		count += 2
		checksum = (checksum*31 + l.Val + r.Val + 400000) % 1000000007
		n.Left = l.Left
		n.Right = r.Right
	} else {
		undo(n.Left, depth, level+1)
		undo(n.Right, depth, level+1)
	}
}

func main() {
	const trees = 20
	const rounds = 4000
	all := make([]*TreeNode, 0, trees)
	for i := 0; i < trees; i++ {
		lean := 30 + nextRandom()%41
		all = append(all, randomTree(10000, lean))
	}
	for r := int64(0); r < rounds; r++ {
		depth := 2 + (r/trees)%20
		root := addOneRow(all[r%trees], r%201-100, depth)
		undo(root, depth, 1)
	}
	fmt.Printf("%d trees, %d rounds: %d row nodes, checksum %d\n", trees, rounds, count, checksum)
}
