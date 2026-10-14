// Benchmark mirror for #617: the same workload and algorithm as
// merge_trees.kara (recursion, a new tree). A subtree only one tree has
// is shared by pointer, as the Kāra arm shares the `shared struct` node.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func mergeTrees(root1, root2 *TreeNode) *TreeNode {
	if root1 != nil && root2 != nil {
		return &TreeNode{
			Val:   root1.Val + root2.Val,
			Left:  mergeTrees(root1.Left, root2.Left),
			Right: mergeTrees(root1.Right, root2.Right),
		}
	}
	if root1 != nil {
		return root1
	}
	return root2
}

var seed int64 = 617

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(size, lean int64) *TreeNode {
	root := &TreeNode{Val: nextRandom()%20001 - 10000}
	for k := int64(1); k < size; k++ {
		c := &TreeNode{Val: nextRandom()%20001 - 10000}
		node := root
		for {
			if nextRandom()%100 < lean {
				if node.Left != nil {
					node = node.Left
				} else {
					node.Left = c
					break
				}
			} else {
				if node.Right != nil {
					node = node.Right
				} else {
					node.Right = c
					break
				}
			}
		}
	}
	return root
}

func walk(node *TreeNode, count, h *int64) {
	if node != nil {
		*count++
		*h = (*h*31 + node.Val + 20000) % 1000000007
		walk(node.Left, count, h)
		walk(node.Right, count, h)
	}
}

func main() {
	trees, rounds := int64(20), int64(10000)
	all := make([]*TreeNode, 0, trees)
	for t := int64(0); t < trees; t++ {
		lean := 30 + nextRandom()%41
		all = append(all, randomTree(2000, lean))
	}
	var count, checksum int64
	for r := int64(0); r < rounds; r++ {
		merged := mergeTrees(all[(r*7)%trees], all[(r*3+1)%trees])
		walk(merged, &count, &checksum)
	}
	fmt.Printf("%d trees, %d rounds: %d nodes, checksum %d\n", trees, rounds, count, checksum)
}
