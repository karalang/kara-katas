// LeetCode #1609: Even Odd Tree -- the bench in Go, mirroring
// even_odd.kara: breadth first, a level at a time, over a slice used as
// a queue.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func isEvenOddTree(root *TreeNode) bool {
	var queue []*TreeNode
	if root != nil {
		queue = append(queue, root)
	}
	even := true
	for len(queue) > 0 {
		hasPrev := false
		var prev int32
		width := len(queue)
		for i := 0; i < width; i++ {
			node := queue[0]
			queue = queue[1:]
			v := node.Val
			var ok bool
			if even {
				ok = v%2 == 1 && (!hasPrev || v > prev)
			} else {
				ok = v%2 == 0 && (!hasPrev || v < prev)
			}
			if !ok {
				return false
			}
			hasPrev = true
			prev = v
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		even = !even
	}
	return true
}

var seed int64 = 1609

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

type slot struct {
	parent *TreeNode
	left   bool
}

func randomTree(n int64) []*TreeNode {
	nodes := []*TreeNode{{}}
	free := []slot{{nodes[0], true}, {nodes[0], false}}
	for i := int64(1); i < n; i++ {
		k := big() % int64(len(free))
		s := free[k]
		free[k] = free[len(free)-1]
		free = free[:len(free)-1]
		child := &TreeNode{}
		if s.left {
			s.parent.Left = child
		} else {
			s.parent.Right = child
		}
		free = append(free, slot{child, true}, slot{child, false})
		nodes = append(nodes, child)
	}
	level := []*TreeNode{nodes[0]}
	depth := 0
	for len(level) > 0 {
		var v int32
		if depth%2 == 0 {
			v = 1 + 2*int32(nextRandom()%5)
		} else {
			v = 1000000 - 2*int32(nextRandom()%5)
		}
		var below []*TreeNode
		for _, node := range level {
			node.Val = v
			step := 2 * int32(nextRandom()%2+1)
			if depth%2 == 0 {
				v += step
			} else {
				v -= step
			}
			if node.Left != nil {
				below = append(below, node.Left)
			}
			if node.Right != nil {
				below = append(below, node.Right)
			}
		}
		level = below
		depth++
	}
	return nodes
}

func main() {
	var trees [][]*TreeNode
	var picks [][][2]int64
	for t := 0; t < 20; t++ {
		trees = append(trees, randomTree(100000))
		pairs := [][2]int64{{0, 0}}
		for k := 0; k < 20; k++ {
			a := big() % 100000
			b := big() % 100000
			pairs = append(pairs, [2]int64{a, b})
		}
		picks = append(picks, pairs)
	}
	var check, checks, evenOdd int64
	for t, tree := range trees {
		for _, p := range picks[t] {
			a, b := tree[p[0]], tree[p[1]]
			a.Val, b.Val = b.Val, a.Val
			yes := isEvenOddTree(tree[0])
			a.Val, b.Val = b.Val, a.Val
			if yes {
				evenOdd++
			}
			var x int64
			if yes {
				x = 1
			}
			check = mix(check, x)
			checks++
		}
	}
	fmt.Printf("20 trees of 100000 nodes: %d checks, %d even-odd, checksum %d\n", checks, evenOdd, check)
}
