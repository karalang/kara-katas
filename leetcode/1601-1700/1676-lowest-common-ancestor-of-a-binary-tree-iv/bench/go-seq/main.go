// LeetCode #1676: Lowest Common Ancestor of a Binary Tree IV -- the bench's
// Go mirror: the ★ arm on one tree of 10000 nodes asked about 500 sets of
// 1 to 50 nodes, all drawn first, each asked 10 times. Pointer nodes; the
// values in a map used as a set.

package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func lowestCommonAncestor(root *TreeNode, nodes []*TreeNode) *TreeNode {
	wanted := make(map[int32]struct{}, len(nodes))
	for _, n := range nodes {
		wanted[n.Val] = struct{}{}
	}
	return search(root, wanted)
}

func search(node *TreeNode, wanted map[int32]struct{}) *TreeNode {
	if node == nil {
		return nil
	}
	if _, ok := wanted[node.Val]; ok {
		return node
	}
	left := search(node.Left, wanted)
	right := search(node.Right, wanted)
	if left != nil && right != nil {
		return node
	}
	if left != nil {
		return left
	}
	return right
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1676

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
	const n = 10000
	const queries = 500
	const rounds = 10
	nodes := randomTree(n)
	root := nodes[0]
	sets := make([][]*TreeNode, 0, queries)
	for q := 0; q < queries; q++ {
		k := nextRandom()%50 + 1
		for i := int64(0); i < k; i++ {
			j := i + nextRandom()%(n-i)
			nodes[i], nodes[j] = nodes[j], nodes[i]
		}
		set := make([]*TreeNode, k)
		copy(set, nodes[:k])
		sets = append(sets, set)
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, set := range sets {
			found := int64(lowestCommonAncestor(root, set).Val)
			total += found
			check = (check*31 + found + r) % 1000000007
		}
	}
	fmt.Printf("%d nodes, %d sets, %d rounds: answers sum to %d, checksum %d\n", n, queries, rounds, total, check)
}
