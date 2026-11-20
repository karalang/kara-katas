// LeetCode #2331: Evaluate Boolean Binary Tree -- the bench, the ★ arm in
// Go. A leaf is its own truth, and an OR or an AND node its two subtrees
// evaluated recursively and joined by `||` or `&&`, which stop at the
// first child that settles it. O(n).
package main

import "fmt"

type TreeNode struct {
	Val         int32
	Left, Right *TreeNode
}

func evaluateTree(node *TreeNode) bool {
	if node == nil {
		return false
	}
	switch node.Val {
	case 0:
		return false
	case 1:
		return true
	case 2:
		return evaluateTree(node.Left) || evaluateTree(node.Right)
	default:
		return evaluateTree(node.Left) && evaluateTree(node.Right)
	}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomTree(seed *int64, depth int64) *TreeNode {
	if depth == 0 || nextRandom(seed)%8 == 0 {
		return &TreeNode{Val: int32(nextRandom(seed) % 2)}
	}
	op := int32(nextRandom(seed)%2 + 2)
	left := randomTree(seed, depth-1)
	right := randomTree(seed, depth-1)
	return &TreeNode{Val: op, Left: left, Right: right}
}

func main() {
	seed := int64(2331)
	trees := make([]*TreeNode, 200)
	for k := range trees {
		trees[k] = randomTree(&seed, 14)
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for k := 0; k < 200; k++ {
			var truth int64 = 2
			if evaluateTree(trees[k]) {
				truth = 1
			}
			check = (check*3 + truth + p) % 1000000007
		}
	}
	fmt.Printf("500 passes over 200 trees of depth up to 14: checksum %d\n", check)
}
