// LeetCode #889 bench: Go mirror of construct_from_pre_post.kara (the ★
// arm, recursion with a table of postorder positions) on the same 4000
// trees.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func constructFromPrePost(preorder, postorder []int64) *TreeNode {
	at := make([]int64, len(preorder)+1)
	for i, v := range postorder {
		at[v] = int64(i)
	}
	return build(preorder, at, 0, int64(len(preorder))-1, 0)
}

// the subtree whose preorder is preorder[lo..=hi] and whose postorder
// starts at postLo
func build(preorder, at []int64, lo, hi, postLo int64) *TreeNode {
	if lo > hi {
		return nil
	}
	node := &TreeNode{Val: preorder[lo]}
	if lo < hi {
		size := at[preorder[lo+1]] - postLo + 1
		node.Left = build(preorder, at, lo+1, lo+size, postLo)
		node.Right = build(preorder, at, lo+size+1, hi, postLo+size)
	}
	return node
}

var seed int64 = 889

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func walk(n *TreeNode, pre, post *[]int64) {
	if n == nil {
		return
	}
	*pre = append(*pre, n.Val)
	walk(n.Left, pre, post)
	walk(n.Right, pre, post)
	*post = append(*post, n.Val)
}

// as in the Kāra bench: a random tree of n nodes holding 1 to n
func randomTree(n int64, full bool) *TreeNode {
	vals := make([]int64, n)
	for v := int64(0); v < n; v++ {
		vals[v] = v + 1
	}
	for i := int64(1); i < n; i++ {
		j := nextRandom() % (i + 1)
		vals[i], vals[j] = vals[j], vals[i]
	}
	nodes := []*TreeNode{{Val: vals[0]}}
	if full {
		leaves := []*TreeNode{nodes[0]}
		for int64(len(nodes))+2 <= n {
			k := nextRandom() % int64(len(leaves))
			leaf := leaves[k]
			leaves[k] = leaves[len(leaves)-1]
			leaves = leaves[:len(leaves)-1]
			a := &TreeNode{Val: vals[len(nodes)]}
			b := &TreeNode{Val: vals[len(nodes)+1]}
			leaf.Left = a
			leaf.Right = b
			nodes = append(nodes, a, b)
			leaves = append(leaves, a, b)
		}
	} else {
		for k := int64(1); k < n; k++ {
			node := &TreeNode{Val: vals[k]}
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
			nodes = append(nodes, node)
		}
	}
	return nodes[0]
}

func main() {
	var total, check int64
	for c := 0; c < 4000; c++ {
		full := c%2 == 0
		n := int64(1000)
		if full {
			n = 999
		}
		tree := randomTree(n, full)
		pre := []int64{}
		post := []int64{}
		walk(tree, &pre, &post)
		root := constructFromPrePost(pre, post)
		// the rebuilt tree in level order, 0 for a missing child
		queue := []*TreeNode{}
		if root != nil {
			check = (check*131 + root.Val) % 1000000007
			queue = append(queue, root)
		}
		for head := 0; head < len(queue); head++ {
			node := queue[head]
			total++
			if node.Left != nil {
				check = (check*131 + node.Left.Val) % 1000000007
				queue = append(queue, node.Left)
			} else {
				check = check * 131 % 1000000007
			}
			if node.Right != nil {
				check = (check*131 + node.Right.Val) % 1000000007
				queue = append(queue, node.Right)
			} else {
				check = check * 131 % 1000000007
			}
		}
	}
	fmt.Printf("4000 trees of up to 1000 nodes: %d nodes rebuilt, checksum %d\n", total, check)
}
