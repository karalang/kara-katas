// LeetCode #2471: Minimum Number of Operations to Sort a Binary Tree by
// Level -- the bench, the ★ arm in Go: the levels by a breadth-first
// walk, and in each the cycles of the permutation that sorts it, a `map`
// from each value to its sorted place. The nodes are `*TreeNode`.
package main

import (
	"fmt"
	"sort"
)

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func minimumOperations(root *TreeNode) int64 {
	var total int64
	var level []*TreeNode
	if root != nil {
		level = append(level, root)
	}
	for len(level) > 0 {
		values := make([]int64, len(level))
		for i, n := range level {
			values[i] = int64(n.Val)
		}
		sorted := append([]int64(nil), values...)
		sort.Slice(sorted, func(a, b int) bool { return sorted[a] < sorted[b] })
		target := map[int64]int{}
		for i, v := range sorted {
			target[v] = i
		}
		seen := make([]bool, len(values))
		for i := range values {
			var length int64
			at := i
			for !seen[at] {
				seen[at] = true
				at = target[values[at]]
				length++
			}
			if length > 1 {
				total += length - 1
			}
		}
		var next []*TreeNode
		for _, n := range level {
			if n.Left != nil {
				next = append(next, n.Left)
			}
			if n.Right != nil {
				next = append(next, n.Right)
			}
		}
		level = next
	}
	return total
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2471

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

// the nodes of a random tree, the root first: the values 1 to `n` in a
// random order, each node after the first hung below a random earlier
// one, a random side taken down from it until a free one is found
func randomTree(n int64) []*TreeNode {
	values := make([]int32, n)
	for i := range values {
		values[i] = int32(i + 1)
	}
	for i := n - 1; i > 0; i-- {
		j := wide() % (i + 1)
		values[i], values[j] = values[j], values[i]
	}
	nodes := make([]*TreeNode, n)
	for i, v := range values {
		nodes[i] = &TreeNode{Val: v}
	}
	for k := int64(1); k < n; k++ {
		at := nodes[wide()%k]
		for {
			if nextRandom()%2 == 0 {
				if at.Left != nil {
					at = at.Left
				} else {
					at.Left = nodes[k]
					break
				}
			} else {
				if at.Right != nil {
					at = at.Right
				} else {
					at.Right = nodes[k]
					break
				}
			}
		}
	}
	return nodes
}

func main() {
	// 20 random trees of 10^4 nodes built once; then 110 passes, each
	// answering every tree, folding the count plus the pass into the
	// checksum, then swapping two of its values chosen by the checksum
	var n int64 = 10000
	trees := make([][]*TreeNode, 20)
	for i := range trees {
		trees[i] = randomTree(n)
	}
	var check int64
	for p := int64(0); p < 110; p++ {
		for _, nodes := range trees {
			check = (check*31 + minimumOperations(nodes[0]) + p) % 1000000007
			a := nodes[check%n]
			b := nodes[(check/n+p)%n]
			a.Val, b.Val = b.Val, a.Val
		}
	}
	fmt.Printf("110 passes over 20 trees of 10^4: checksum %d\n", check)
}
