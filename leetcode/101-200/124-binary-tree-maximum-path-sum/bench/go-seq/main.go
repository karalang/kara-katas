// LeetCode #124 benchmark mirror (Go) — GC-managed pointer tree, the GC data
// point. Same algorithm and tree construction as the other mirrors.
package main

import "fmt"

const (
	treeCount = 2048
	nodeCount = 511
	reps      = 60
)

type TreeNode struct {
	val   int64
	left  *TreeNode
	right *TreeNode
}

func nodeValue(i, seed int64) int64 {
	return ((i*37 + seed*13) % 41) - 20
}

func buildBalanced(lo, hi, seed int64) *TreeNode {
	if lo > hi {
		return nil
	}
	mid := (lo + hi) / 2
	return &TreeNode{
		val:   nodeValue(mid, seed),
		left:  buildBalanced(lo, mid-1, seed),
		right: buildBalanced(mid+1, hi, seed),
	}
}

func maxGain(node *TreeNode, best *int64) int64 {
	if node == nil {
		return 0
	}
	lg := maxGain(node.left, best)
	rg := maxGain(node.right, best)
	leftGain := lg
	if leftGain < 0 {
		leftGain = 0
	}
	rightGain := rg
	if rightGain < 0 {
		rightGain = 0
	}
	through := node.val + leftGain + rightGain
	if through > *best {
		*best = through
	}
	branch := leftGain
	if rightGain > branch {
		branch = rightGain
	}
	return node.val + branch
}

func maxPathSum(root *TreeNode) int64 {
	best := int64(-1000000000)
	maxGain(root, &best)
	return best
}

func main() {
	forest := make([]*TreeNode, treeCount)
	for t := int64(0); t < treeCount; t++ {
		forest[t] = buildBalanced(0, nodeCount-1, t+1)
	}

	var sink int64
	for k := 0; k < reps; k++ {
		for i := 0; i < treeCount; i++ {
			sink += maxPathSum(forest[i])
		}
	}
	fmt.Println(sink)
}
