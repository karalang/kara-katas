// LeetCode #687: Longest Univalue Path -- one walk, two arms per node.
// Bench.
//
// 100 random trees of up to 16 levels, values 1 and 2, are built once;
// then 30 rounds answer every tree.
package main

import "fmt"

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

// The node's longest downward path of its own value, in edges; `best`
// takes the longest path that bends at the node.
func arm(node *TreeNode, best *int64) int64 {
	if node == nil {
		return 0
	}
	l := arm(node.left, best)
	r := arm(node.right, best)
	var left, right int64
	if node.left != nil && node.left.val == node.val {
		left = l + 1
	}
	if node.right != nil && node.right.val == node.val {
		right = r + 1
	}
	if left+right > *best {
		*best = left + right
	}
	if left > right {
		return left
	}
	return right
}

func longestUnivaluePath(root *TreeNode) int64 {
	var best int64
	arm(root, &best)
	return best
}

var seed int64 = 687

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(levels int64) *TreeNode {
	n := &TreeNode{val: 1 + nextRandom()%2}
	if levels > 1 {
		if nextRandom()%100 < 88 {
			n.left = randomTree(levels - 1)
		}
		if nextRandom()%100 < 88 {
			n.right = randomTree(levels - 1)
		}
	}
	return n
}

func main() {
	const count, rounds = 100, 30
	trees := make([]*TreeNode, count)
	for c := range trees {
		trees[c] = randomTree(16)
	}
	var sum int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			k := longestUnivaluePath(trees[c])
			sum = (sum*31 + k + r) % 1000000007
		}
	}
	fmt.Printf("%d trees answered, checksum %d\n", count*rounds, sum)
}
