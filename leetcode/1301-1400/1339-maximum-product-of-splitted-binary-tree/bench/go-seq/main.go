// LeetCode #1339 bench in Go: the ★ arm (one recursive walk for the total,
// a second for every subtree's sum, keeping the best product, taken modulo
// 10^9 + 7 at the end) on the same 10 trees of 5 * 10^4 nodes and 20
// passes.
package main

import "fmt"

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func total(node *TreeNode) int64 {
	if node == nil {
		return 0
	}
	return int64(node.Val) + total(node.Left) + total(node.Right)
}

func bestCut(node *TreeNode, all int64, best *int64) int64 {
	if node == nil {
		return 0
	}
	s := int64(node.Val) + bestCut(node.Left, all, best) + bestCut(node.Right, all, best)
	*best = max(*best, s*(all-s))
	return s
}

func maxProduct(root *TreeNode) int {
	all := total(root)
	var best int64
	bestCut(root, all, &best)
	return int(best % 1000000007)
}

var seed int64 = 1339

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func newNode() *TreeNode {
	return &TreeNode{Val: int(1 + nextRandom()%10000)}
}

type place struct {
	node *TreeNode
	left bool
}

func build(n int) []*TreeNode {
	root := newNode()
	nodes := []*TreeNode{root}
	places := []place{{root, true}, {root, false}}
	for len(nodes) < n {
		k := int(nextRandom() % int64(len(places)))
		p := places[k]
		places[k] = places[len(places)-1]
		places = places[:len(places)-1]
		node := newNode()
		if p.left {
			p.node.Left = node
		} else {
			p.node.Right = node
		}
		places = append(places, place{node, true}, place{node, false})
		nodes = append(nodes, node)
	}
	return nodes
}

func main() {
	n := 50000
	trees := make([][]*TreeNode, 10)
	for t := range trees {
		trees[t] = build(n)
	}
	var check int64
	for pass := int64(0); pass < 20; pass++ {
		for t := 0; t < 10; t++ {
			nodes := trees[t]
			nodes[check%int64(n)].Val = int(1 + (check/7)%10000)
			answer := maxProduct(nodes[0])
			check = (check*31 + int64(answer) + pass) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 trees of 5 * 10^4: checksum %d\n", check)
}
