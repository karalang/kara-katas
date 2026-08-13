// Benchmark workload for LeetCode #255 — Verify Preorder Sequence in BST (Go mirror).
// Mirrors verify_preorder.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"math"
)

func main() {
	var n int64 = 200000
	var rounds int64 = 250

	val := make([]int64, 0, n)
	left := make([]int64, 0, n)
	right := make([]int64, 0, n)
	var state int64 = 255255

	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		v := state
		if len(val) == 0 {
			val = append(val, v)
			left = append(left, -1)
			right = append(right, -1)
		} else {
			var cur int64 = 0
			placed := false
			for !placed {
				if v == val[cur] {
					placed = true
				} else if v < val[cur] {
					if left[cur] == -1 {
						val = append(val, v)
						left = append(left, -1)
						right = append(right, -1)
						left[cur] = int64(len(val)) - 1
						placed = true
					} else {
						cur = left[cur]
					}
				} else {
					if right[cur] == -1 {
						val = append(val, v)
						left = append(left, -1)
						right = append(right, -1)
						right[cur] = int64(len(val)) - 1
						placed = true
					} else {
						cur = right[cur]
					}
				}
			}
		}
	}

	preorder := make([]int64, 0, len(val))
	walk := []int64{0}
	for len(walk) > 0 {
		node := walk[len(walk)-1]
		walk = walk[:len(walk)-1]
		if node != -1 {
			preorder = append(preorder, val[node])
			if right[node] != -1 {
				walk = append(walk, right[node])
			}
			if left[node] != -1 {
				walk = append(walk, left[node])
			}
		}
	}

	m := len(preorder)
	var sink int64 = 0
	stack := make([]int64, 0, m)
	for r := int64(0); r < rounds; r++ {
		stack = stack[:0]
		lower := int64(math.MinInt64)
		ok := true
		for k := 0; k < m; k++ {
			x := preorder[k]
			if x < lower {
				ok = false
			}
			for len(stack) > 0 && stack[len(stack)-1] < x {
				lower = stack[len(stack)-1]
				stack = stack[:len(stack)-1]
			}
			stack = append(stack, x)
		}
		if ok {
			sink = (sink*31 + 1) % 1000000007
		} else {
			sink = (sink * 31) % 1000000007
		}
		sink = (sink*131 + (lower % 1000000007)) % 1000000007
	}
	fmt.Println(m, sink)
}
