// LeetCode #1302 bench in Go: the ★ arm (a breadth-first walk a level at a
// time, the queue a slice read from a moving head) on the same 50 trees of
// 10^4 nodes and 50 passes.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func deepestLeavesSum(root *TreeNode) int32 {
	queue := []*TreeNode{}
	if root != nil {
		queue = append(queue, root)
	}
	head := 0
	var sum int32
	for head < len(queue) {
		sum = 0
		end := len(queue)
		for head < end {
			node := queue[head]
			head++
			sum += node.Val
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
	}
	return sum
}

var seed int64 = 1302

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func newNode() *TreeNode {
	return &TreeNode{Val: int32(1 + nextRandom()%100)}
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
			nodes[check%n].Val = int32(1 + (check/7)%100)
			sum := deepestLeavesSum(nodes[0])
			check = (check*31 + int64(sum) + pass) % 1000000007
		}
	}
	fmt.Printf("50 passes over 50 trees of 10^4: checksum %d\n", check)
}
