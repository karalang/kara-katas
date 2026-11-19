// LeetCode #1660: Correct a Binary Tree -- the bench's Go mirror: the ★
// arm on 40 random trees of 100000 nodes, each broken once, all built
// first. The values met are a map[int32]struct{}.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func correct(node *TreeNode, seen map[int32]struct{}) *TreeNode {
	if node == nil {
		return nil
	}
	if node.Right != nil {
		if _, ok := seen[node.Right.Val]; ok {
			return nil
		}
	}
	seen[node.Val] = struct{}{}
	node.Right = correct(node.Right, seen)
	node.Left = correct(node.Left, seen)
	return node
}

func correctBinaryTree(root *TreeNode) *TreeNode {
	return correct(root, map[int32]struct{}{})
}

var seed int64 = 1660

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
	node *TreeNode
	left bool
}

func randomTree(n int64) *TreeNode {
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i)
	}
	for i := n - 1; i >= 1; i-- {
		j := big() % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	root := &TreeNode{Val: values[0]}
	free := []slot{{root, true}, {root, false}}
	for i := int64(1); i < n; i++ {
		k := big() % int64(len(free))
		s := free[k]
		free[k] = free[len(free)-1]
		free = free[:len(free)-1]
		child := &TreeNode{Val: values[i]}
		if s.left {
			s.node.Left = child
		} else {
			s.node.Right = child
		}
		free = append(free, slot{child, true}, slot{child, false})
	}
	return root
}

func breakTree(root *TreeNode) bool {
	var pairs int64
	level := []*TreeNode{root}
	var levels [][]*TreeNode
	for len(level) > 0 {
		var below []*TreeNode
		for i, node := range level {
			if node.Right == nil {
				pairs += int64(len(level) - 1 - i)
			}
			if node.Left != nil {
				below = append(below, node.Left)
			}
			if node.Right != nil {
				below = append(below, node.Right)
			}
		}
		levels = append(levels, level)
		level = below
	}
	if pairs == 0 {
		return false
	}
	k := big() % pairs
	for _, level := range levels {
		for i, node := range level {
			if node.Right == nil {
				after := int64(len(level) - 1 - i)
				if k < after {
					node.Right = level[i+1+int(k)]
					return true
				}
				k -= after
			}
		}
	}
	return false
}

func fold(root *TreeNode, check *int64) int64 {
	var count int64
	queue := []*TreeNode{root}
	for head := 0; head < len(queue); head++ {
		node := queue[head]
		if node == nil {
			*check = mix(*check, 0)
		} else {
			count++
			*check = mix(*check, int64(node.Val)+1)
			queue = append(queue, node.Left, node.Right)
		}
	}
	return count
}

func main() {
	var roots []*TreeNode
	for len(roots) < 40 {
		root := randomTree(100000)
		if breakTree(root) {
			roots = append(roots, root)
		}
	}
	var check, kept int64
	for _, root := range roots {
		kept += fold(correctBinaryTree(root), &check)
	}
	fmt.Printf("40 trees of 100000 nodes: %d nodes kept, checksum %d\n", kept, check)
}
