// LeetCode #1305 bench in Go: the ★ arm (each tree read in order into its
// own slice, then the two merged) on the same 20 pairs of search trees and
// 100 passes.
package main

import "fmt"

type TreeNode struct {
	Val   int32
	Left  *TreeNode
	Right *TreeNode
}

func inOrder(node *TreeNode, out *[]int32) {
	if node != nil {
		inOrder(node.Left, out)
		*out = append(*out, node.Val)
		inOrder(node.Right, out)
	}
}

func getAllElements(root1, root2 *TreeNode) []int32 {
	var a, b, out []int32
	inOrder(root1, &a)
	inOrder(root2, &b)
	i, j := 0, 0
	for i < len(a) || j < len(b) {
		if j == len(b) || (i < len(a) && a[i] <= b[j]) {
			out = append(out, a[i])
			i++
		} else {
			out = append(out, b[j])
			j++
		}
	}
	return out
}

var seed int64 = 1305

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func insert(root *TreeNode, v int32) {
	at := root
	for {
		if v == at.Val {
			return
		}
		next := &at.Right
		if v < at.Val {
			next = &at.Left
		}
		if *next == nil {
			*next = &TreeNode{Val: v}
			return
		}
		at = *next
	}
}

func randomBst(n int) *TreeNode {
	root := &TreeNode{Val: int32(nextRandom()%200001 - 100000)}
	for k := 1; k < n; k++ {
		insert(root, int32(nextRandom()%200001-100000))
	}
	return root
}

func main() {
	var firsts, seconds [20]*TreeNode
	for p := 0; p < 20; p++ {
		firsts[p] = randomBst(4900)
		seconds[p] = randomBst(4900)
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		for p := 0; p < 20; p++ {
			insert(firsts[p], int32(check%200001-100000))
			got := getAllElements(firsts[p], seconds[p])
			x := int64(got[check%int64(len(got))])
			check = (check*31 + x + 100000 + int64(len(got)) + pass) % 1000000007
		}
	}
	fmt.Printf("100 passes over 20 pairs of trees: checksum %d\n", check)
}
