// LeetCode #1372 bench -- Go: one walk up from the leaves, each node
// reporting the longest zigzag starting at it going left and going right,
// each one more than its child's the other way.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

// the longest zigzag from node going left first, going right first
func lengths(node *TreeNode, best *int64) (int64, int64) {
	var left, right int64
	if node.Left != nil {
		_, r := lengths(node.Left, best)
		left = 1 + r
	}
	if node.Right != nil {
		l, _ := lengths(node.Right, best)
		right = 1 + l
	}
	if left > *best {
		*best = left
	}
	if right > *best {
		*best = right
	}
	return left, right
}

func longestZigZag(root *TreeNode) int32 {
	var best int64
	if root != nil {
		lengths(root, &best)
	}
	return int32(best)
}

var seed int64 = 1372

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type place struct {
	node *TreeNode
	left bool
}

func hang(free []place, k int64) []place {
	p := free[k]
	free[k] = free[len(free)-1]
	free = free[:len(free)-1]
	node := &TreeNode{Val: 1}
	if p.left {
		p.node.Left = node
	} else {
		p.node.Right = node
	}
	return append(free, place{node, true}, place{node, false})
}

func main() {
	// 20 trees of 5 * 10^4 nodes, the constraints' most, each node hung
	// on a random empty child place, built once; then 300 rounds, each
	// hanging one more leaf on one tree, on a place drawn from the
	// checksum so far, and finding that tree's longest zigzag
	roots := make([]*TreeNode, 20)
	places := make([][]place, 20)
	for t := range roots {
		root := &TreeNode{Val: 1}
		free := []place{{root, true}, {root, false}}
		for i := 1; i < 50000; i++ {
			free = hang(free, nextRandom()%int64(len(free)))
		}
		roots[t] = root
		places[t] = free
	}
	var check int64
	for r := int64(0); r < 300; r++ {
		t := check % 20
		places[t] = hang(places[t], (check/20)%int64(len(places[t])))
		got := int64(longestZigZag(roots[t]))
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("300 rounds over 20 trees of 50000 nodes: checksum %d\n", check)
}
