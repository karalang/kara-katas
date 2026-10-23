// LeetCode #919: Complete Binary Tree Inserter -- bench: a queue of the
// nodes with a free child slot. Mirrors cbt_inserter.kara.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

type CBTInserter struct {
	root *TreeNode
	open []*TreeNode
}

func Constructor(root *TreeNode) CBTInserter {
	var open []*TreeNode
	walk := []*TreeNode{root}
	for i := 0; i < len(walk); i++ {
		node := walk[i]
		if node.Left != nil {
			walk = append(walk, node.Left)
		}
		if node.Right != nil {
			walk = append(walk, node.Right)
		}
		if node.Left == nil || node.Right == nil {
			open = append(open, node)
		}
	}
	return CBTInserter{root, open}
}

func (c *CBTInserter) Insert(val int64) int64 {
	child := &TreeNode{Val: val}
	parent := c.open[0]
	if parent.Left == nil {
		parent.Left = child
	} else {
		parent.Right = child
		c.open = c.open[1:]
	}
	c.open = append(c.open, child)
	return parent.Val
}

func (c *CBTInserter) GetRoot() *TreeNode {
	return c.root
}

var seed int64 = 919

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// A complete tree holding vals in level order.
func completeTree(vals []int64) *TreeNode {
	nodes := make([]*TreeNode, len(vals))
	for i, v := range vals {
		nodes[i] = &TreeNode{Val: v}
	}
	for i := 1; i < len(nodes); i++ {
		parent := nodes[(i-1)/2]
		if i%2 == 1 {
			parent.Left = nodes[i]
		} else {
			parent.Right = nodes[i]
		}
	}
	return nodes[0]
}

func main() {
	const rounds, n, m = 200, 1000, 50000
	var total, check int64
	for r := 0; r < rounds; r++ {
		// a fresh tree of n values, then m inserts into it
		vals := make([]int64, n)
		for i := range vals {
			vals[i] = nextRandom() % 100000
		}
		inserter := Constructor(completeTree(vals))
		var parents int64
		for j := 0; j < m; j++ {
			parents += inserter.Insert(nextRandom() % 100000)
		}
		root := inserter.GetRoot()
		total += parents
		check = (check*1000003 + parents + root.Val) % 1000000007
	}
	fmt.Printf("%d rounds of %d inserts into trees of %d: parents summing to %d, checksum %d\n", rounds, m, n, total, check)
}
