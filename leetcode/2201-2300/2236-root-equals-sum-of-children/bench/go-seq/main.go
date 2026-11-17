// LeetCode #2236: Root Equals Sum of Children -- the benchmark's Go
// mirror of check.kara: 10^6 trees of three nodes built and checked,
// the nodes left to the garbage collector.
package main

import "fmt"

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func checkTree(root *TreeNode) bool {
	if root == nil || root.Left == nil || root.Right == nil {
		return false
	}
	return root.Val == root.Left.Val+root.Right.Val
}

func tree(root, left, right int64) *TreeNode {
	return &TreeNode{Val: int(root), Left: &TreeNode{Val: int(left)}, Right: &TreeNode{Val: int(right)}}
}

var seed int64 = 2236

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	holding, check := int64(0), int64(0)
	for i := 0; i < 1000000; i++ {
		left := nextRandom()%101 - 50
		right := nextRandom()%101 - 50
		root := left + right + nextRandom()%3 - 1
		holds := checkTree(tree(root, left, right))
		b := int64(0)
		if holds {
			holding++
			b = 1
		}
		check = (check*2 + b) % 1000000007
	}
	fmt.Printf("10^6 trees: %d hold, checksum %d\n", holding, check)
}
