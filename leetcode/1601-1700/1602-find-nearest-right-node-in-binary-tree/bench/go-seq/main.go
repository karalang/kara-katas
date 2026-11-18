// LeetCode #1602: Find Nearest Right Node in Binary Tree -- the bench in
// Go, mirroring nearest_right.kara: breadth first, a level at a time,
// over a slice used as a queue.
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func findNearestRightNode(root, u *TreeNode) *TreeNode {
	var queue []*TreeNode
	if root != nil {
		queue = append(queue, root)
	}
	for len(queue) > 0 {
		width := len(queue)
		for i := 0; i < width; i++ {
			node := queue[0]
			queue = queue[1:]
			if node == u {
				if i+1 < width {
					return queue[0]
				}
				return nil
			}
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
	}
	return nil
}

var seed int64 = 1602

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
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i + 1)
	}
	for i := n - 1; i >= 1; i-- {
		j := big() % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := []*TreeNode{{Val: values[0]}}
	free := []slot{{nodes[0], true}, {nodes[0], false}}
	for _, v := range values[1:] {
		k := big() % int64(len(free))
		s := free[k]
		free[k] = free[len(free)-1]
		free = free[:len(free)-1]
		child := &TreeNode{Val: v}
		if s.left {
			s.parent.Left = child
		} else {
			s.parent.Right = child
		}
		free = append(free, slot{child, true}, slot{child, false})
		nodes = append(nodes, child)
	}
	return nodes
}

func main() {
	var trees [][]*TreeNode
	var picks [][]int64
	for t := 0; t < 10; t++ {
		trees = append(trees, randomTree(100000))
		us := make([]int64, 100)
		for k := range us {
			us[k] = big() % 100000
		}
		picks = append(picks, us)
	}
	var check, found int64
	for t, tree := range trees {
		for _, k := range picks[t] {
			var a int64
			if n := findNearestRightNode(tree[0], tree[k]); n != nil {
				a = int64(n.Val)
			}
			if a > 0 {
				found++
			}
			check = mix(check, a)
		}
	}
	fmt.Printf("10 trees of 100000 nodes: 1000 queries, %d found, checksum %d\n", found, check)
}
