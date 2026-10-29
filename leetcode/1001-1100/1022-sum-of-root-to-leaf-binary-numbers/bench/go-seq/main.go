// LeetCode #1022: Sum of Root To Leaf Binary Numbers -- bench
// Mirrors ../sum_root_to_leaf.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func sumRootToLeaf(root *TreeNode) int64 {
	return sumFrom(root, 0)
}

func sumFrom(node *TreeNode, above int64) int64 {
	if node == nil {
		return 0
	}
	value := above*2 + node.Val
	if node.Left == nil && node.Right == nil {
		return value
	}
	return sumFrom(node.Left, value) + sumFrom(node.Right, value)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomTree(seed *int64, n int64) *TreeNode {
	root := &TreeNode{Val: nextRandom(seed) % 2}
	placed := int64(1)
	for placed < n {
		node := root
		level := 1
		for {
			goLeft := nextRandom(seed)%2 == 0
			next := node.Right
			if goLeft {
				next = node.Left
			}
			if next != nil {
				node = next
				level++
				if level == 31 {
					break
				}
			} else {
				leaf := &TreeNode{Val: nextRandom(seed) % 2}
				if goLeft {
					node.Left = leaf
				} else {
					node.Right = leaf
				}
				placed++
				break
			}
		}
	}
	return root
}

func main() {
	const count, rounds = 200, 500
	seed := int64(1022)
	trees := []*TreeNode{}
	var nodes int64
	for g := 0; g < count; g++ {
		n := nextRandom(&seed)%1000 + 1
		nodes += n
		trees = append(trees, randomTree(&seed, n))
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, tree := range trees {
			answer := sumRootToLeaf(tree)
			total += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d trees, %d nodes, %d rounds: sum %d, checksum %d\n", count, nodes, rounds, total, check)
}
