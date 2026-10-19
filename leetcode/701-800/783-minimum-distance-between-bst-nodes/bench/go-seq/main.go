// LeetCode 783 — Minimum Distance Between BST Nodes: the bench, in Go.
// Mirrors min_diff_in_bst.kara: ancestor bounds over the same 64 trees.
package main

import (
	"fmt"
	"math"
	"sort"
)

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func closest(n *TreeNode, low, high int64) int64 {
	if n == nil {
		return math.MaxInt64
	}
	best := int64(math.MaxInt64)
	if low != -1 {
		best = min(best, n.val-low)
	}
	if high != -1 {
		best = min(best, high-n.val)
	}
	best = min(best, closest(n.left, low, n.val))
	return min(best, closest(n.right, n.val, high))
}

func minDiffInBST(root *TreeNode) int64 { return closest(root, -1, -1) }

var seed int64 = 783

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func insert(root *TreeNode, v int64) *TreeNode {
	if root == nil {
		return &TreeNode{val: v}
	}
	at := root
	for {
		if v < at.val {
			if at.left != nil {
				at = at.left
			} else {
				at.left = &TreeNode{val: v}
				break
			}
		} else {
			if at.right != nil {
				at = at.right
			} else {
				at.right = &TreeNode{val: v}
				break
			}
		}
	}
	return root
}

func middleFirst(ordered []int64, lo, hi int64, out *[]int64) {
	if lo > hi {
		return
	}
	mid := (lo + hi) / 2
	*out = append(*out, ordered[mid])
	middleFirst(ordered, lo, mid-1, out)
	middleFirst(ordered, mid+1, hi, out)
}

func main() {
	trees := make([]*TreeNode, 0, 64)
	for t := 0; t < 64; t++ {
		taken := map[int64]bool{}
		values := []int64{}
		for len(values) < 100 {
			hi := nextRandom()
			v := (hi*32768 + nextRandom()) % 100001
			if !taken[v] {
				taken[v] = true
				values = append(values, v)
			}
		}
		if t%4 >= 2 {
			sort.Slice(values, func(i, j int) bool { return values[i] < values[j] })
		}
		if t%4 == 2 {
			order := []int64{}
			middleFirst(values, 0, 99, &order)
			values = order
		}
		var root *TreeNode
		for _, v := range values {
			root = insert(root, v)
		}
		trees = append(trees, root)
	}
	const rounds int64 = 2000000
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		answer := minDiffInBST(trees[r%64])
		total += answer
		check = (check*31 + answer) % 1000000007
	}
	fmt.Printf("%d rounds of 100-value trees: gaps sum to %d, checksum %d\n", rounds, total, check)
}
