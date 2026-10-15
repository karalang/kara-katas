// Benchmark for #671: a pruned walk, as the Kara ★ arm.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func smallestAbove(n *TreeNode, low int64) int64 {
	if n == nil {
		return -1
	}
	if n.Val > low {
		return n.Val
	}
	a := smallestAbove(n.Left, low)
	b := smallestAbove(n.Right, low)
	if a == -1 {
		return b
	}
	if b == -1 {
		return a
	}
	if a < b {
		return a
	}
	return b
}

func findSecondMinimumValue(root *TreeNode) int64 {
	if root == nil {
		return -1
	}
	return smallestAbove(root, root.Val)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func special(levels, val, spread int64, seed *int64) *TreeNode {
	n := &TreeNode{Val: val}
	if levels > 1 {
		other := val + nextRandom(seed)%(spread+1)
		n.Left = special(levels-1, val, spread, seed)
		n.Right = special(levels-1, other, spread, seed)
	}
	return n
}

func main() {
	seed := int64(671)
	trees := make([]*TreeNode, 16)
	for t := int64(0); t < 16; t++ {
		spread := t
		if t%4 == 0 {
			spread = 0
		}
		trees[t] = special(16, 7+t, spread, &seed)
	}
	rounds := int64(2000)
	sum := int64(0)
	for r := int64(0); r < rounds; r++ {
		s := findSecondMinimumValue(trees[r%16])
		sum = (sum*31 + s + 1) % 1000000007
	}
	fmt.Printf("16 trees of 65535 nodes, %d rounds: checksum %d\n", rounds, sum)
}
