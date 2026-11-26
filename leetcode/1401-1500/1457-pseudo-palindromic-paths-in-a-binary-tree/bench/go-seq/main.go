// LeetCode #1457 bench in Go: the ★ arm (a walk down by recursion,
// the parity of the values on the path carried as a bit mask) on the same
// 50 trees of 10^4 nodes and 50 passes.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

// the pseudo-palindromic paths through `node`, `seen` with bit v set when
// the value v is on the path above it an odd number of times: at a leaf
// the path can be rearranged into a palindrome when at most one bit is set
func paths(node *TreeNode, seen int32) int32 {
	if node == nil {
		return 0
	}
	seen ^= 1 << node.Val
	if node.Left == nil && node.Right == nil {
		if seen&(seen-1) == 0 {
			return 1
		}
		return 0
	}
	return paths(node.Left, seen) + paths(node.Right, seen)
}

func pseudoPalindromicPaths(root *TreeNode) int32 {
	return paths(root, 0)
}

var seed int64 = 1457

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func newNode() *TreeNode {
	return &TreeNode{Val: int32(1 + nextRandom()%9)}
}

type place struct {
	node *TreeNode
	left bool
}

func build(n int, levelOrder bool) []*TreeNode {
	root := newNode()
	nodes := []*TreeNode{root}
	if levelOrder {
		level := []*TreeNode{root}
		for len(nodes) < n {
			at := level[0]
			level = level[1:]
			for side := 0; side < 2; side++ {
				if len(nodes) < n && nextRandom()%4 != 0 {
					node := newNode()
					if side == 0 {
						at.Left = node
					} else {
						at.Right = node
					}
					level = append(level, node)
					nodes = append(nodes, node)
				}
			}
			if len(level) == 0 {
				level = append(level, at)
			}
		}
	} else {
		places := []place{{root, true}, {root, false}}
		for len(nodes) < n {
			k := nextRandom() % int64(len(places))
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
	}
	return nodes
}

func main() {
	n := int64(10000)
	trees := make([][]*TreeNode, 50)
	for t := 0; t < 50; t++ {
		trees[t] = build(int(n), t%2 == 1)
	}
	var check int64
	for pass := int64(0); pass < 50; pass++ {
		for t := 0; t < 50; t++ {
			nodes := trees[t]
			nodes[check%n].Val = int32(1 + (check/7)%9)
			found := pseudoPalindromicPaths(nodes[0])
			check = (check*31 + int64(found) + pass) % 90000007
		}
	}
	fmt.Printf("50 passes over 50 trees of 10^4: checksum %d\n", check)
}
