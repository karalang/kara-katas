// Benchmark workload for LeetCode #270 — Closest BST Value (Go mirror).
// Mirrors bst_close.kara algorithm-for-algorithm, including the hand-written
// native absolute value (see that file for why hand-writing it was wrong).
package main

import (
	"fmt"
	"math"
)

func main() {
	var n int64 = 30000
	var queries int64 = 100000
	var rounds int64 = 22

	val := make([]int64, 0, n)
	left := make([]int64, 0, n)
	right := make([]int64, 0, n)
	var state int64 = 270270

	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		hi := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		v := (hi*32768 + state/65536) % 1000000
		if len(val) == 0 {
			val = append(val, v)
			left = append(left, -1)
			right = append(right, -1)
		} else {
			cur := int64(0)
			for {
				if v < val[cur] {
					if left[cur] < 0 {
						val = append(val, v)
						left = append(left, -1)
						right = append(right, -1)
						left[cur] = int64(len(val)) - 1
						break
					}
					cur = left[cur]
				} else {
					if right[cur] < 0 {
						val = append(val, v)
						left = append(left, -1)
						right = append(right, -1)
						right[cur] = int64(len(val)) - 1
						break
					}
					cur = right[cur]
				}
			}
		}
	}

	targets := make([]float64, queries)
	for q := int64(0); q < queries; q++ {
		state = (state*1103515245 + 12345) & 2147483647
		th := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		whole := (th*32768+state/65536)%1100000 - 50000
		state = (state*1103515245 + 12345) & 2147483647
		frac := float64((state/65536)%1000) / 1000.0
		targets[q] = float64(whole) + frac
	}

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		for t := int64(0); t < queries; t++ {
			target := targets[t]
			best := val[0]
			bestDiff := math.Abs(float64(val[0]) - target)
			cur := int64(0)
			for cur >= 0 {
				v := val[cur]
				d := math.Abs(float64(v) - target)
				if d < bestDiff || (d == bestDiff && v < best) {
					best = v
					bestDiff = d
				}
				if float64(v) < target {
					cur = right[cur]
				} else {
					cur = left[cur]
				}
			}
			sink = (sink*31 + best) % 1000000007
		}
	}
	fmt.Println(sink)
}
