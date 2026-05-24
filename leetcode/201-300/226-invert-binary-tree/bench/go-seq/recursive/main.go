// LeetCode 226 — recursive DFS invert, Go single-threaded mirror.
// Algorithmic peer of bench/recursive.{kara,rs,c,py}. Stdout sink: 2666665501.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func invert(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}
	newLeft := invert(root.right)
	newRight := invert(root.left)
	root.left = newLeft
	root.right = newRight
	return root
}

func buildTree(n int64) *TreeNode {
	if n <= 0 {
		return nil
	}
	nodes := make([]*TreeNode, n)
	for i := int64(0); i < n; i++ {
		nodes[i] = &TreeNode{val: i}
	}
	state := int64(12345)
	for i := int64(1); i < n; i++ {
		cur := nodes[0]
		for {
			state = (state*1103515245 + 12345) & 2147483647
			bit := state & 1
			if bit == 0 {
				if cur.left == nil {
					cur.left = nodes[i]
					break
				}
				cur = cur.left
			} else {
				if cur.right == nil {
					cur.right = nodes[i]
					break
				}
				cur = cur.right
			}
		}
	}
	return nodes[0]
}

func bfsSink(root *TreeNode) int64 {
	if root == nil {
		return 0
	}
	queue := []*TreeNode{root}
	var sum, pos int64
	for len(queue) > 0 {
		cur := queue[0]
		queue = queue[1:]
		pos++
		sum += cur.val * pos
		if cur.left != nil {
			queue = append(queue, cur.left)
		}
		if cur.right != nil {
			queue = append(queue, cur.right)
		}
	}
	return sum
}

func main() {
	root := buildTree(2000)
	for k := 0; k < 10; k++ {
		root = invert(root)
	}
	fmt.Println(bfsSink(root))
}
