// LeetCode #1644: Lowest Common Ancestor of a Binary Tree II -- the bench's
// Go mirror: the ★ arm on 60 random trees of 10000 nodes, each asked about
// 50 pairs of values, one in five of them not in the tree, all drawn
// first.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func countBelow(node *TreeNode, p, q int32, found **TreeNode) int64 {
	if node == nil {
		return 0
	}
	var here int64
	if node.Val == p || node.Val == q {
		here = 1
	}
	count := countBelow(node.Left, p, q, found) + countBelow(node.Right, p, q, found) + here
	if count == 2 && *found == nil {
		*found = node
	}
	return count
}

func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
	var found *TreeNode
	countBelow(root, p.Val, q.Val, &found)
	return found
}

var seed int64 = 1644

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int64) *TreeNode {
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i)
	}
	for i := n - 1; i >= 1; i-- {
		j := nextRandom() % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := make([]*TreeNode, 0, n)
	for i := int64(0); i < n; i++ {
		node := &TreeNode{Val: values[i]}
		if i > 0 {
			at := nodes[nextRandom()%i]
			for {
				if nextRandom()%2 == 0 {
					if at.Left != nil {
						at = at.Left
					} else {
						at.Left = node
						break
					}
				} else {
					if at.Right != nil {
						at = at.Right
					} else {
						at.Right = node
						break
					}
				}
			}
		}
		nodes = append(nodes, node)
	}
	return nodes[0]
}

func main() {
	type tree struct {
		root  *TreeNode
		pairs [][2]int32
	}
	trees := make([]tree, 0, 60)
	for t := 0; t < 60; t++ {
		root := randomTree(10000)
		pairs := make([][2]int32, 0, 50)
		for k := 0; k < 50; k++ {
			p := nextRandom() % 12500
			q := nextRandom() % 12500
			if q == p {
				q = (q + 1) % 12500
			}
			pairs = append(pairs, [2]int32{int32(p), int32(q)})
		}
		trees = append(trees, tree{root, pairs})
	}
	var check, total int64
	for _, t := range trees {
		for _, pq := range t.pairs {
			node := lowestCommonAncestor(t.root, &TreeNode{Val: pq[0]}, &TreeNode{Val: pq[1]})
			found := int64(-1)
			if node != nil {
				found = int64(node.Val)
			}
			total += found + 1
			check = (check*31 + found + 2) % 1000000007
		}
	}
	fmt.Printf("60 trees of 10000 nodes, 50 pairs each: answers sum to %d, checksum %d\n", total, check)
}
