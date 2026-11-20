// LeetCode #1214 bench, in Go: the ★ arm (each tree's values read in
// order, then two pointers, one climbing the first list and one coming
// down the second) on 16 pairs of balanced search trees of 5000 nodes
// each, built once; then 10 rounds over the pairs, four targets each,
// every answer folded into a checksum.
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

var seed int64 = 1214

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	hi := nextRandom()
	lo := nextRandom()
	return (hi*32768+lo)%2000000001 - 1000000000
}

func inOrder(node *TreeNode, out *[]int32) {
	if node == nil {
		return
	}
	inOrder(node.Left, out)
	*out = append(*out, node.Val)
	inOrder(node.Right, out)
}

func twoSumBSTs(root1, root2 *TreeNode, target int32) bool {
	var a, b []int32
	inOrder(root1, &a)
	inOrder(root2, &b)
	i, j := 0, len(b)-1
	for i < len(a) && j >= 0 {
		sum := a[i] + b[j]
		if sum == target {
			return true
		}
		if sum < target {
			i++
		} else {
			j--
		}
	}
	return false
}

func balanced(sorted []int32, low, high int) *TreeNode {
	if low >= high {
		return nil
	}
	mid := (low + high) / 2
	return &TreeNode{sorted[mid], balanced(sorted, low, mid), balanced(sorted, mid+1, high)}
}

func distinctValues(n int) []int32 {
	seen := map[int64]bool{}
	for len(seen) < n {
		seen[big()] = true
	}
	keys := make([]int64, 0, n)
	for k := range seen {
		keys = append(keys, k)
	}
	sort.Slice(keys, func(x, y int) bool { return keys[x] < keys[y] })
	out := make([]int32, n)
	for k, v := range keys {
		out[k] = int32(v)
	}
	return out
}

type pair struct {
	t1, t2  *TreeNode
	targets []int32
}

func main() {
	pairs := []pair{}
	for p := 0; p < 16; p++ {
		a := distinctValues(5000)
		b := distinctValues(5000)
		i := nextRandom() % 5000
		j := nextRandom() % 5000
		t3 := int32(big())
		t4 := int32(big())
		targets := []int32{a[i] + b[j], a[j] + b[i], t3, t4}
		pairs = append(pairs, pair{balanced(a, 0, 5000), balanced(b, 0, 5000), targets})
	}
	var check int64
	for round := int64(0); round < 10; round++ {
		for _, p := range pairs {
			for _, t := range p.targets {
				var answer int64 = 1
				if twoSumBSTs(p.t1, p.t2, t) {
					answer = 2
				}
				check = (check*131 + answer + round) % 1000000007
			}
		}
	}
	fmt.Printf("10 rounds over 16 pairs of 5000-node trees: checksum %d\n", check)
}
