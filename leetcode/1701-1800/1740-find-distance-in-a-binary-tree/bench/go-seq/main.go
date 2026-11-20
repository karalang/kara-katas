// LeetCode #1740: Find Distance in a Binary Tree -- the bench's Go
// mirror: the ★ arm on one tree of 10000 nodes asked about 1000 pairs of
// values, all drawn first, each asked 4 times. Nodes are pointers.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func findDistance(root *TreeNode, p, q int32) int32 {
	ancestor := common(root, p, q)
	return depth(ancestor, p) + depth(ancestor, q)
}

func common(node *TreeNode, p, q int32) *TreeNode {
	if node == nil {
		return nil
	}
	if node.Val == p || node.Val == q {
		return node
	}
	left := common(node.Left, p, q)
	right := common(node.Right, p, q)
	if left != nil && right != nil {
		return node
	}
	if left != nil {
		return left
	}
	return right
}

func depth(node *TreeNode, value int32) int32 {
	if node == nil {
		return -1
	}
	if node.Val == value {
		return 0
	}
	below := max(depth(node.Left, value), depth(node.Right, value))
	if below < 0 {
		return -1
	}
	return below + 1
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1740

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int64) []*TreeNode {
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
	return nodes
}

func main() {
	const n, queries, rounds = 10000, 1000, 4
	nodes := randomTree(n)
	root := nodes[0]
	ps := make([]int32, queries)
	qs := make([]int32, queries)
	for i := 0; i < queries; i++ {
		ps[i] = int32(nextRandom() % n)
		qs[i] = int32(nextRandom() % n)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for i := 0; i < queries; i++ {
			found := int64(findDistance(root, ps[i], qs[i]))
			total += found
			check = (check*31 + found + r) % 1000000007
		}
	}
	fmt.Printf("%d nodes, %d pairs, %d rounds: distances sum to %d, checksum %d\n", n, queries, rounds, total, check)
}
