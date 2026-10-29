// LeetCode #1026: Maximum Difference Between Node and Ancestor -- bench
// Mirrors ../max_ancestor_diff.kara; see ../../README.md § Benchmarks.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func maxAncestorDiff(root *TreeNode) int64 {
	if root == nil {
		return 0
	}
	return bestBelow(root, root.Val, root.Val)
}

func bestBelow(node *TreeNode, low, high int64) int64 {
	if node == nil {
		return high - low
	}
	lo := min(low, node.Val)
	hi := max(high, node.Val)
	return max(bestBelow(node.Left, lo, hi), bestBelow(node.Right, lo, hi))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomValue(seed *int64, top int64) int64 {
	high := nextRandom(seed)
	return (high*32768 + nextRandom(seed)) % top
}

func randomTree(seed *int64, n int64) *TreeNode {
	root := &TreeNode{Val: randomValue(seed, 100001)}
	placed := int64(1)
	for placed < n {
		node := root
		for {
			goLeft := nextRandom(seed)%2 == 0
			next := node.Right
			if goLeft {
				next = node.Left
			}
			if next != nil {
				node = next
			} else {
				leaf := &TreeNode{Val: randomValue(seed, 100001)}
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
	const count, rounds = 200, 50
	seed := int64(1026)
	trees := []*TreeNode{}
	var nodes int64
	for g := 0; g < count; g++ {
		n := nextRandom(&seed)%4999 + 2
		nodes += n
		trees = append(trees, randomTree(&seed, n))
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for _, tree := range trees {
			answer := maxAncestorDiff(tree)
			total += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d trees, %d nodes, %d rounds: sum %d, checksum %d\n", count, nodes, rounds, total, check)
}
