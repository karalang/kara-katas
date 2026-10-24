// LeetCode #938: Range Sum of BST -- bench: recursion that skips
// subtrees. Mirrors range_sum_bst.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func rangeSumBST(root *TreeNode, low, high int64) int64 {
	if root == nil {
		return 0
	}
	if root.Val < low {
		return rangeSumBST(root.Right, low, high)
	}
	if root.Val > high {
		return rangeSumBST(root.Left, low, high)
	}
	return root.Val + rangeSumBST(root.Left, low, high) + rangeSumBST(root.Right, low, high)
}

var seed int64 = 938

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds = 20
	const count = 20
	const queries = 50
	trees := []*TreeNode{}
	lows := []int64{}
	highs := []int64{}
	pool := make([]int64, 100000)
	for v := range pool {
		pool[v] = int64(v + 1)
	}
	for c := 0; c < count; c++ {
		for i := int64(0); i < 20000; i++ {
			j := i + nextRandom()%(100000-i)
			pool[i], pool[j] = pool[j], pool[i]
		}
		root := &TreeNode{Val: pool[0]}
		for _, v := range pool[1:20000] {
			cur := root
			for {
				if v < cur.Val {
					if cur.Left == nil {
						cur.Left = &TreeNode{Val: v}
						break
					}
					cur = cur.Left
				} else {
					if cur.Right == nil {
						cur.Right = &TreeNode{Val: v}
						break
					}
					cur = cur.Right
				}
			}
		}
		trees = append(trees, root)
		for q := 0; q < queries; q++ {
			a := 1 + nextRandom()%100000
			b := 1 + nextRandom()%100000
			lows = append(lows, min(a, b))
			highs = append(highs, max(a, b))
		}
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			c := (r + i) % count
			for q := 0; q < queries; q++ {
				s := rangeSumBST(trees[c], lows[c*queries+q], highs[c*queries+q])
				total += s
				check = (check*1000003 + s) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d trees of 20000 nodes, %d ranges each: sums adding to %d, checksum %d\n", rounds, count, queries, total, check)
}
