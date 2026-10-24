// Benchmark: LeetCode #951 Flip Equivalent Binary Trees -- the ★ arm,
// both pairings tried, on pairs of trees of 100 nodes, LeetCode's
// largest. Mirrors flip_equiv.kara, .c, .rs and .py.
package main

import "fmt"

type TreeNode struct {
	Val         int64
	Left, Right *TreeNode
}

func flipEquiv(a, b *TreeNode) bool {
	if a == nil && b == nil {
		return true
	}
	if a == nil || b == nil {
		return false
	}
	return a.Val == b.Val &&
		((flipEquiv(a.Left, b.Left) && flipEquiv(a.Right, b.Right)) ||
			(flipEquiv(a.Left, b.Right) && flipEquiv(a.Right, b.Left)))
}

var seed int64 = 951

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTree(values []int64) *TreeNode {
	root := &TreeNode{Val: values[0]}
	for _, v := range values[1:] {
		node := &TreeNode{Val: v}
		cur := root
		for {
			if nextRandom()%2 == 0 {
				if cur.Left != nil {
					cur = cur.Left
				} else {
					cur.Left = node
					break
				}
			} else {
				if cur.Right != nil {
					cur = cur.Right
				} else {
					cur.Right = node
					break
				}
			}
		}
	}
	return root
}

func flippedCopy(t *TreeNode, rename []int64) *TreeNode {
	if t == nil {
		return nil
	}
	l := flippedCopy(t.Left, rename)
	r := flippedCopy(t.Right, rename)
	if nextRandom()%2 == 0 {
		return &TreeNode{rename[t.Val], l, r}
	}
	return &TreeNode{rename[t.Val], r, l}
}

func main() {
	rounds, count, n := 50000, 20, int64(100)
	firsts := make([]*TreeNode, 0, count)
	seconds := make([]*TreeNode, 0, count)
	for c := 0; c < count; c++ {
		values := make([]int64, n)
		for i := range values {
			values[i] = int64(i)
		}
		for i := int64(0); i < n; i++ {
			j := i + nextRandom()%(n-i)
			values[i], values[j] = values[j], values[i]
		}
		t := randomTree(values)
		rename := make([]int64, n)
		for i := range rename {
			rename[i] = int64(i)
		}
		if c%2 == 1 {
			a := nextRandom() % n
			b := nextRandom() % n
			rename[a] = b
			rename[b] = a
		}
		seconds = append(seconds, flippedCopy(t, rename))
		firsts = append(firsts, t)
	}
	var yes, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			var bit int64
			if flipEquiv(firsts[k], seconds[k]) {
				bit = 1
			}
			yes += bit
			check = (check*31 + bit + int64(k)) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d pairs of trees of %d nodes: %d flip equivalent, checksum %d\n", rounds, count, n, yes, check)
}
