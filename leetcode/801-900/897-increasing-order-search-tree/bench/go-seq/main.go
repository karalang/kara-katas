// LeetCode #897 bench: the ★ arm (an in-order walk that relinks as it
// goes) on 200,000 search trees of 100 nodes, LeetCode's largest, each
// made by putting in 100 random values from 0 to 1000; each chain is
// walked into a checksum. The same algorithm as increasing_bst.kara.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func relink(node *TreeNode, tail **TreeNode) {
	if node != nil {
		relink(node.Left, tail)
		node.Left = nil
		(*tail).Right = node
		*tail = node
		relink(node.Right, tail)
	}
}

func increasingBST(root *TreeNode) *TreeNode {
	head := &TreeNode{Val: -1}
	tail := head
	relink(root, &tail)
	return head.Right
}

var seed int64 = 897

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var nodes, check int64
	for t := 0; t < 200000; t++ {
		root := &TreeNode{Val: nextRandom() % 1001}
		for k := 1; k < 100; k++ {
			v := nextRandom() % 1001
			cur := root
			for {
				if v < cur.Val {
					if cur.Left != nil {
						cur = cur.Left
					} else {
						cur.Left = &TreeNode{Val: v}
						break
					}
				} else {
					if cur.Right != nil {
						cur = cur.Right
					} else {
						cur.Right = &TreeNode{Val: v}
						break
					}
				}
			}
		}
		for cur := increasingBST(root); cur != nil; cur = cur.Right {
			nodes++
			check = (check*31 + cur.Val) % 1000000007
		}
	}
	fmt.Printf("200000 trees of 100 nodes: %d in the chains, checksum %d\n", nodes, check)
}
