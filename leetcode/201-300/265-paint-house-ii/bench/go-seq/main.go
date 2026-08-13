// Benchmark workload for LeetCode #265 — Paint House II (Go mirror).
// Mirrors paint_ii.kara algorithm-for-algorithm.
package main

import "fmt"

func main() {
	var n int64 = 4000
	var k int64 = 32
	var rounds int64 = 1300
	var inf int64 = 1000000000000

	cost := make([]int64, n*k)
	var state int64 = 265265
	for z := int64(0); z < n*k; z++ {
		state = (state*1103515245 + 12345) & 2147483647
		cost[z] = (state/65536)%40 + 1
	}

	prev := make([]int64, k)
	cur := make([]int64, k)

	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		start := (r * 7919) % n

		for c := int64(0); c < k; c++ {
			prev[c] = cost[start*k+c]
		}

		for i := int64(1); i < n; i++ {
			min1, idx1, min2 := inf, int64(-1), inf
			for j := int64(0); j < k; j++ {
				v := prev[j]
				if v < min1 {
					min2 = min1
					min1 = v
					idx1 = j
				} else if v < min2 {
					min2 = v
				}
			}

			row := ((start + i) % n) * k
			for t := int64(0); t < k; t++ {
				best := min1
				if t == idx1 {
					best = min2
				}
				cur[t] = cost[row+t] + best
			}

			prev, cur = cur, prev
		}

		var answer int64 = inf
		var fold int64 = 0
		for p := int64(0); p < k; p++ {
			v := prev[p]
			if v < answer {
				answer = v
			}
			fold = (fold*31 + v) % 1000000007
		}
		sink = (sink*131 + answer + fold) % 1000000007
	}

	fmt.Println(sink)
}
