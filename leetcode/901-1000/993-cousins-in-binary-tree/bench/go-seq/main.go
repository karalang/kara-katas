// Benchmark: LeetCode #993 Cousins in Binary Tree -- the ★ arm, a
// breadth-first search a level at a time, on random trees of 100 nodes,
// LeetCode's largest. Mirrors is_cousins.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

type entry struct {
	node   *TreeNode
	parent int64
}

func isCousins(root *TreeNode, x, y int64) bool {
	level := []entry{{root, -1}}
	for len(level) > 0 {
		px, py := int64(-1), int64(-1)
		var next []entry
		for _, e := range level {
			if e.node.Val == x {
				px = e.parent
			}
			if e.node.Val == y {
				py = e.parent
			}
			if e.node.Left != nil {
				next = append(next, entry{e.node.Left, e.node.Val})
			}
			if e.node.Right != nil {
				next = append(next, entry{e.node.Right, e.node.Val})
			}
		}
		if px >= 0 && py >= 0 {
			return px != py
		}
		if px >= 0 || py >= 0 {
			return false
		}
		level = next
	}
	return false
}

var seed int64 = 993

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(n int) *TreeNode {
	vals := make([]int64, n)
	for i := range vals {
		vals[i] = int64(i + 1)
	}
	for i := n - 1; i > 0; i-- {
		j := nextRandom() % int64(i+1)
		vals[i], vals[j] = vals[j], vals[i]
	}
	root := &TreeNode{Val: vals[0]}
	for k := 1; k < n; k++ {
		node := &TreeNode{Val: vals[k]}
		cur := root
		for {
			if nextRandom()%2 == 0 {
				if cur.Left != nil {
					cur = cur.Left
				} else {
					cur.Left = node
					break
				}
			} else {
				if cur.Right != nil {
					cur = cur.Right
				} else {
					cur.Right = node
					break
				}
			}
		}
	}
	return root
}

func main() {
	rounds := 500
	trees := make([]*TreeNode, 20)
	for i := range trees {
		trees[i] = randomTree(100)
	}
	var found, check int64
	for r := 0; r < rounds; r++ {
		for t := 0; t < 20; t++ {
			d := int64(1 + (r*7+t)%99)
			for x := int64(1); x <= 100; x++ {
				y := 1 + (x-1+d)%100
				got := isCousins(trees[(r+t)%20], x, y)
				var bit int64 = 1
				if got {
					found++
					bit = 2
				}
				check = (check*31 + bit) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over 20 trees of 100 nodes: %d cousin pairs, checksum %d\n", rounds, found, check)
}
