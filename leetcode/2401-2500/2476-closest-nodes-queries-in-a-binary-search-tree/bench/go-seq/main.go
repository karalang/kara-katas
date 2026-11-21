// LeetCode #2476: Closest Nodes Queries in a Binary Search Tree -- the
// bench, the ★ arm in Go: an in-order walk reads the values ascending,
// and a bisection by hand finds the first value at least each query. The
// nodes are `*TreeNode`.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func walk(node *TreeNode, values *[]int64) {
	if node == nil {
		return
	}
	walk(node.Left, values)
	*values = append(*values, int64(node.Val))
	walk(node.Right, values)
}

func closestNodes(root *TreeNode, queries []int64) [][2]int64 {
	var values []int64
	walk(root, &values)
	answers := make([][2]int64, 0, len(queries))
	for _, q := range queries {
		lo, hi := 0, len(values)
		for lo < hi {
			mid := (lo + hi) / 2
			if values[mid] < q {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		var ceiling int64 = -1
		if lo < len(values) {
			ceiling = values[lo]
		}
		var floor int64 = -1
		if lo < len(values) && values[lo] == q {
			floor = q
		} else if lo > 0 {
			floor = values[lo-1]
		}
		answers = append(answers, [2]int64{floor, ceiling})
	}
	return answers
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2476

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

// the search tree of `n` distinct random values from 1 to 10^6, inserted
// in the order drawn
func randomSearchTree(n int) *TreeNode {
	used := map[int64]bool{}
	var root *TreeNode
	for len(used) < n {
		v := 1 + wideRandom()%1000000
		if used[v] {
			continue
		}
		used[v] = true
		if root == nil {
			root = &TreeNode{Val: int32(v)}
			continue
		}
		at := root
		for {
			if v < int64(at.Val) {
				if at.Left != nil {
					at = at.Left
				} else {
					at.Left = &TreeNode{Val: int32(v)}
					break
				}
			} else {
				if at.Right != nil {
					at = at.Right
				} else {
					at.Right = &TreeNode{Val: int32(v)}
					break
				}
			}
		}
	}
	return root
}

func main() {
	// 10 random search trees of 10^4 nodes built once; then 220 passes,
	// each asking every tree 1000 values stepped from the checksum so far,
	// folding every answer and the pass into the checksum
	trees := make([]*TreeNode, 10)
	for t := range trees {
		trees[t] = randomSearchTree(10000)
	}
	var check int64
	queries := make([]int64, 1000)
	for p := int64(0); p < 220; p++ {
		for _, root := range trees {
			for i := range queries {
				queries[i] = 1 + (check+997*int64(i))%1000000
			}
			for _, pair := range closestNodes(root, queries) {
				check = (check*31 + pair[0] + pair[1] + 2 + p) % 1000000007
			}
		}
	}
	fmt.Printf("220 passes over 10 trees of 10^4: checksum %d\n", check)
}
