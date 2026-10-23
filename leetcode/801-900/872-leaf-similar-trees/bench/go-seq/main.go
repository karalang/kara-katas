// LeetCode #872: Leaf-Similar Trees -- Go mirror of the bench program (the
// ★ arm, the leaves of each collected by recursion).
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func leafSimilar(root1, root2 *TreeNode) bool {
	var first, second []int64
	leaves(root1, &first)
	leaves(root2, &second)
	if len(first) != len(second) {
		return false
	}
	for i := range first {
		if first[i] != second[i] {
			return false
		}
	}
	return true
}

func leaves(node *TreeNode, out *[]int64) {
	if node != nil {
		if node.Left == nil && node.Right == nil {
			*out = append(*out, node.Val)
		} else {
			leaves(node.Left, out)
			leaves(node.Right, out)
		}
	}
}

var seed int64 = 872

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n, limit int64) *TreeNode {
	nodes := []*TreeNode{}
	for k := int64(0); k < n; k++ {
		node := &TreeNode{Val: nextRandom() % limit}
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

func treeWithLeaves(vals []int64, lo, hi, limit int64) *TreeNode {
	if hi-lo == 1 {
		return &TreeNode{Val: vals[lo]}
	}
	mid := lo + 1 + nextRandom()%(hi-lo-1)
	left := treeWithLeaves(vals, lo, mid, limit)
	right := treeWithLeaves(vals, mid, hi, limit)
	return &TreeNode{Val: nextRandom() % limit, Left: left, Right: right}
}

func main() {
	var as, bs []*TreeNode
	for k := 0; k < 2000; k++ {
		a := randomTree(200, 201)
		var b *TreeNode
		if k%2 == 0 {
			var vals []int64
			leaves(a, &vals)
			b = treeWithLeaves(vals, 0, int64(len(vals)), 201)
		} else {
			b = randomTree(200, 201)
		}
		as = append(as, a)
		bs = append(bs, b)
	}
	var check int64
	for _, b := range bs {
		var vals []int64
		leaves(b, &vals)
		for _, v := range vals {
			check = (check*31 + v + 1) % 1000000007
		}
	}
	similar := 0
	for r := 0; r < 50; r++ {
		for k := range as {
			if leafSimilar(as[k], bs[k]) {
				similar++
			}
		}
	}
	fmt.Printf("100000 comparisons of 2000 pairs: %d leaf-similar, leaf checksum %d\n", similar, check)
}
