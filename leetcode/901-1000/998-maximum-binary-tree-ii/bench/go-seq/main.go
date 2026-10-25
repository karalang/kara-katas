// Benchmark: LeetCode #998 Maximum Binary Tree II -- the ★ arm, down the
// right spine by recursion, on maximum trees of 99 values, LeetCode's
// largest. Mirrors insert_into_max_tree.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val   int64
	Left  *TreeNode
	Right *TreeNode
}

func insertIntoMaxTree(root *TreeNode, val int64) *TreeNode {
	if root == nil {
		return &TreeNode{Val: val}
	}
	if val > root.Val {
		return &TreeNode{Val: val, Left: root}
	}
	root.Right = insertIntoMaxTree(root.Right, val)
	return root
}

var seed int64 = 998

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func build(a []int64, lo, hi int) *TreeNode {
	if lo >= hi {
		return nil
	}
	m := lo
	for i := lo + 1; i < hi; i++ {
		if a[i] > a[m] {
			m = i
		}
	}
	return &TreeNode{Val: a[m], Left: build(a, lo, m), Right: build(a, m+1, hi)}
}

// Take val out again, from where the insert put it on the right spine,
// and return the tree as it was with how deep val sat.
func takeOut(root *TreeNode, val int64) (*TreeNode, int64) {
	if root.Val == val {
		return root.Left, 0
	}
	above := root
	depth := int64(1)
	for {
		next := above.Right
		if next.Val == val {
			above.Right = next.Left
			return root, depth
		}
		above = next
		depth++
	}
}

func main() {
	const rounds = 100000
	// 20 trees of the 99 values from 1 to 100 but one: the even ones in a
	// random order, the odd ones falling, which makes a chain of 99
	trees := make([]*TreeNode, 20)
	vals := make([]int64, 20)
	for t := 0; t < 20; t++ {
		val := 1 + nextRandom()%100
		a := make([]int64, 0, 99)
		for v := int64(0); v < 100; v++ {
			if 100-v != val {
				a = append(a, 100-v)
			}
		}
		if t%2 == 0 {
			for i := int64(98); i > 0; i-- {
				j := nextRandom() % (i + 1)
				a[i], a[j] = a[j], a[i]
			}
		}
		trees[t] = build(a, 0, 99)
		vals[t] = val
	}
	var depths, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := (r + i) % 20
			got := insertIntoMaxTree(trees[k], vals[k])
			tree, depth := takeOut(got, vals[k])
			trees[k] = tree
			depths += depth
			check = (check*31 + depth + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 trees of 99 values: depth total %d, checksum %d\n", rounds, depths, check)
}
