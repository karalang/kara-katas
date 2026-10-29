// LeetCode #1008 bench: the ★ arm (recursion with an upper bound) over 50
// preorders of 100 values, drawn once; each of 4000 rounds builds every
// tree, starting from a different preorder, and folds it into a checksum.
package main

import (
	"fmt"
	"math"
)

type TreeNode struct {
	val         int64
	left, right *TreeNode
}

func bstFromPreorder(preorder []int64) *TreeNode {
	next := 0
	return build(preorder, &next, math.MaxInt64)
}

func build(preorder []int64, next *int, bound int64) *TreeNode {
	if *next == len(preorder) || preorder[*next] >= bound {
		return nil
	}
	val := preorder[*next]
	*next++
	left := build(preorder, next, val)
	right := build(preorder, next, bound)
	return &TreeNode{val, left, right}
}

func fold(node *TreeNode, depth int64) int64 {
	if node == nil {
		return 0
	}
	return (node.val*depth + fold(node.left, depth+1)*3 + fold(node.right, depth+1)*7) % 1000000007
}

var seed int64 = 1008

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomPreorder(n int, most int64) []int64 {
	seen := make([]bool, most+1)
	vals := []int64{}
	left := []int{}
	right := []int{}
	for len(vals) < n {
		v := 1 + nextRandom()%most
		if seen[v] {
			continue
		}
		seen[v] = true
		vals = append(vals, v)
		left = append(left, -1)
		right = append(right, -1)
		me := len(vals) - 1
		if me > 0 {
			at := 0
			for {
				if v < vals[at] {
					if left[at] == -1 {
						left[at] = me
						break
					}
					at = left[at]
				} else {
					if right[at] == -1 {
						right[at] = me
						break
					}
					at = right[at]
				}
			}
		}
	}
	out := []int64{}
	stack := []int{0}
	for len(stack) > 0 {
		at := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		out = append(out, vals[at])
		if right[at] != -1 {
			stack = append(stack, right[at])
		}
		if left[at] != -1 {
			stack = append(stack, left[at])
		}
	}
	return out
}

func main() {
	count, rounds := 50, 4000
	preorders := make([][]int64, count)
	for k := range preorders {
		preorders[k] = randomPreorder(100, 1000)
	}
	var check int64
	for r := 0; r < rounds; r++ {
		for k := 0; k < count; k++ {
			tree := bstFromPreorder(preorders[(r+k)%count])
			check = (check*31 + fold(tree, 1)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d preorders of 100 values: checksum %d\n", rounds, count, check)
}
