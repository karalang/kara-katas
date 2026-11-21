// LeetCode #1650: Lowest Common Ancestor of a Binary Tree III -- the
// bench's Go mirror: the ★ arm on 30 random trees of 100000 nodes with
// parent links, each asked about 50000 pairs of its nodes, all drawn
// first.
package main

import "fmt"

type Node struct {
	Val    int32
	Left   *Node
	Right  *Node
	Parent *Node
}

func lowestCommonAncestor(p, q *Node) *Node {
	a, b := p, q
	for a.Val != b.Val {
		if a.Parent != nil {
			a = a.Parent
		} else {
			a = q
		}
		if b.Parent != nil {
			b = b.Parent
		} else {
			b = p
		}
	}
	return a
}

var seed int64 = 1650

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int64) []*Node {
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i)
	}
	for i := n - 1; i >= 1; i-- {
		j := (nextRandom() * 32768 + nextRandom()) % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := make([]*Node, 0, n)
	for i := int64(0); i < n; i++ {
		node := &Node{Val: values[i]}
		if i > 0 {
			at := nodes[(nextRandom() * 32768 + nextRandom())%i]
			for {
				if nextRandom()%2 == 0 {
					if at.Left != nil {
						at = at.Left
					} else {
						node.Parent = at
						at.Left = node
						break
					}
				} else {
					if at.Right != nil {
						at = at.Right
					} else {
						node.Parent = at
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
	type tree struct {
		nodes []*Node
		pairs [][2]int64
	}
	trees := make([]tree, 0, 30)
	for t := 0; t < 30; t++ {
		nodes := randomTree(100000)
		pairs := make([][2]int64, 0, 50000)
		for k := 0; k < 50000; k++ {
			p := (nextRandom() * 32768 + nextRandom()) % 100000
			q := (nextRandom() * 32768 + nextRandom()) % 100000
			if q == p {
				q = (q + 1) % 100000
			}
			pairs = append(pairs, [2]int64{p, q})
		}
		trees = append(trees, tree{nodes, pairs})
	}
	var check, total int64
	for _, t := range trees {
		for _, pq := range t.pairs {
			found := int64(lowestCommonAncestor(t.nodes[pq[0]], t.nodes[pq[1]]).Val)
			total += found
			check = (check*31 + found + 1) % 1000000007
		}
	}
	fmt.Printf("30 trees of 100000 nodes, 50000 pairs each: answers sum to %d, checksum %d\n", total, check)
}
