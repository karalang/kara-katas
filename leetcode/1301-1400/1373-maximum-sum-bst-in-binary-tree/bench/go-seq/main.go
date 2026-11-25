// LeetCode #1373 bench -- Go: the ★ arm over plain pointers: one walk up
// from the leaves; each subtree reports whether it is a search tree, its
// smallest and largest key, and its sum.
package main

import (
	"fmt"
	"math"
)

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

type summary struct {
	search    bool
	low, high int64
	sum       int64
}

func summarize(node *TreeNode, best *int64) summary {
	if node == nil {
		// an empty tree is a search tree with no keys
		return summary{true, math.MaxInt64, math.MinInt64, 0}
	}
	l := summarize(node.Left, best)
	r := summarize(node.Right, best)
	key := int64(node.Val)
	if l.search && r.search && l.high < key && key < r.low {
		sum := l.sum + key + r.sum
		*best = max(*best, sum)
		return summary{true, min(l.low, key), max(r.high, key), sum}
	}
	return summary{false, 0, 0, 0}
}

func maxSumBST(root *TreeNode) int {
	var best int64
	summarize(root, &best)
	return int(best)
}

var seed int64 = 1373

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 4 search trees of 4 * 10^4 nodes, keys from -4 * 10^4 to 4 * 10^4
	// put in one by one, a key already there skipped, built once; then 300
	// rounds, each giving one node of one tree a new key, both drawn from
	// the checksum so far, and finding that tree's largest search tree
	const trees, count = 4, 40000
	roots := make([]*TreeNode, 0, trees)
	nodes := make([][]*TreeNode, 0, trees)
	for t := 0; t < trees; t++ {
		root := &TreeNode{Val: 0}
		all := []*TreeNode{root}
		for len(all) < count {
			a := nextRandom()
			key := int((a*32768+nextRandom())%80001 - 40000)
			at := root
			for key != at.Val {
				child := at.Right
				if key < at.Val {
					child = at.Left
				}
				if child == nil {
					node := &TreeNode{Val: key}
					if key < at.Val {
						at.Left = node
					} else {
						at.Right = node
					}
					all = append(all, node)
					break
				}
				at = child
			}
		}
		roots = append(roots, root)
		nodes = append(nodes, all)
	}
	var check int64
	for r := int64(0); r < 300; r++ {
		t := check % trees
		nodes[t][(check/trees)%count].Val = int((check/160000)%80001 - 40000)
		got := int64(maxSumBST(roots[t]))
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("300 rounds over 4 trees of 40000 nodes: checksum %d\n", check)
}
