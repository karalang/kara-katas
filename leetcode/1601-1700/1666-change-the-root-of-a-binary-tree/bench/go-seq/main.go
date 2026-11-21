// LeetCode #1666: Change the Root of a Binary Tree -- the bench's Go
// mirror: the ★ arm on 30 random trees of 100000 nodes with parent links,
// each turned 50000 times to hang from a leaf reached by a random walk
// down from a random node, the start nodes drawn first.
package main

import "fmt"

type Node struct {
	Val    int32
	Left   *Node
	Right  *Node
	Parent *Node
}

func flipBinaryTree(root, leaf *Node) *Node {
	cur := leaf
	var below *Node
	for {
		p := cur.Parent
		cur.Parent = below
		if p == nil {
			break
		}
		if p.Left == cur {
			p.Left = nil
		} else {
			p.Right = nil
		}
		if cur.Left != nil {
			cur.Right = cur.Left
		}
		cur.Left = p
		below = cur
		cur = p
	}
	return leaf
}

var seed int64 = 1666

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
		nodes  []*Node
		starts []int64
	}
	trees := make([]tree, 0, 30)
	for t := 0; t < 30; t++ {
		nodes := randomTree(100000)
		starts := make([]int64, 0, 50000)
		for k := 0; k < 50000; k++ {
			starts = append(starts, (nextRandom() * 32768 + nextRandom())%100000)
		}
		trees = append(trees, tree{nodes, starts})
	}
	var check, steps int64
	for _, t := range trees {
		root := t.nodes[0]
		for _, s := range t.starts {
			at := t.nodes[s]
			for {
				var first *Node
				if nextRandom()%2 == 0 {
					first = at.Left
				} else {
					first = at.Right
				}
				child := first
				if child == nil {
					child = at.Left
				}
				if child == nil {
					child = at.Right
				}
				if child == nil {
					break
				}
				at = child
				steps++
			}
			root = flipBinaryTree(root, at)
			check = (check*31 + int64(root.Val) + 1) % 1000000007
		}
	}
	fmt.Printf("30 trees of 100000 nodes, 50000 turns each: %d steps down, checksum %d\n", steps, check)
}
