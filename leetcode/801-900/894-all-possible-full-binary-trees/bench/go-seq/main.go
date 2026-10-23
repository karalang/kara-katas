// LeetCode #894 bench: Go mirror of all_possible_fbt.kara (the ★ arm,
// recursion with a memo, the trees sharing their subtrees) asked 1500
// times for every full tree of 19 nodes.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func allPossibleFBT(n int64) []*TreeNode {
	memo := map[int64][]*TreeNode{}
	var build func(n int64) []*TreeNode
	build = func(n int64) []*TreeNode {
		if trees, ok := memo[n]; ok {
			return append([]*TreeNode(nil), trees...)
		}
		out := []*TreeNode{}
		if n == 1 {
			out = append(out, &TreeNode{})
		} else if n%2 == 1 {
			for left := int64(1); left < n-1; left += 2 {
				lefts := build(left)
				rights := build(n - 1 - left)
				for _, l := range lefts {
					for _, r := range rights {
						out = append(out, &TreeNode{Left: l, Right: r})
					}
				}
			}
		}
		memo[n] = append([]*TreeNode(nil), out...)
		return out
	}
	return build(n)
}

// the tree's preorder code, 1 for a node with children and 0 for a leaf,
// folded into a hash
func code(node *TreeNode, h int64) int64 {
	if node == nil {
		return h
	}
	if node.Left == nil {
		return h * 3 % 1000000007
	}
	return code(node.Right, code(node.Left, (h*3+1)%1000000007))
}

func main() {
	var trees, check int64
	for c := 0; c < 1500; c++ {
		all := allPossibleFBT(19)
		trees += int64(len(all))
		for _, t := range all {
			check = (check*131 + code(t, 1)) % 1000000007
		}
	}
	fmt.Printf("1500 calls for 19 nodes: %d trees, checksum %d\n", trees, check)
}
