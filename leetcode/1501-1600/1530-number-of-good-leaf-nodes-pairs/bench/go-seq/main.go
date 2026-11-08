// LeetCode #1530: Number of Good Leaf Nodes Pairs -- bench: the ★ arm
// over 1000 random trees of 1 to 1024 nodes, built once and answered 10
// times, each with its own distance from 1 to 10.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func leavesBelow(node *TreeNode, distance int64, pairs *int64) []int64 {
	counts := make([]int64, distance)
	if node != nil {
		if node.Left == nil && node.Right == nil {
			counts[0] = 1
		} else {
			l := leavesBelow(node.Left, distance, pairs)
			r := leavesBelow(node.Right, distance, pairs)
			for i := int64(0); i < distance; i++ {
				for j := int64(0); j < distance-i-1; j++ {
					*pairs += l[i] * r[j]
				}
			}
			for i := int64(0); i < distance-1; i++ {
				counts[i+1] = l[i] + r[i]
			}
		}
	}
	return counts
}

func countPairs(root *TreeNode, distance int64) int64 {
	var pairs int64
	leavesBelow(root, distance, &pairs)
	return pairs
}

func build(at int64, vals, left, right []int64) *TreeNode {
	if at < 0 {
		return nil
	}
	return &TreeNode{vals[at], build(left[at], vals, left, right), build(right[at], vals, left, right)}
}

var seed int64 = 1530

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func randomTree(most int64) *TreeNode {
	n := nextRandom()%most + 1
	vals := make([]int64, 0, n)
	left := make([]int64, 0, n)
	right := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		vals = append(vals, nextRandom()%100+1)
		left = append(left, -1)
		right = append(right, -1)
		if i > 0 {
			at := nextRandom() % i
			for {
				if nextRandom()%2 == 0 {
					if left[at] < 0 {
						left[at] = i
						break
					}
					at = left[at]
				} else {
					if right[at] < 0 {
						right[at] = i
						break
					}
					at = right[at]
				}
			}
		}
	}
	return build(0, vals, left, right)
}

func main() {
	roots := make([]*TreeNode, 0, 1000)
	dists := make([]int64, 0, 1000)
	for c := 0; c < 1000; c++ {
		roots = append(roots, randomTree(1024))
		dists = append(dists, nextRandom()%10+1)
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for c := range roots {
			check = mix(check, countPairs(roots[c], dists[c]))
		}
	}
	fmt.Printf("10 passes over 1000 trees of up to 1024 nodes: checksum %d\n", check)
}
