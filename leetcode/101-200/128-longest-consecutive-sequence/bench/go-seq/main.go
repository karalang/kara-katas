// Benchmark harness for LeetCode #128 — Longest Consecutive Sequence.
// Mirrors longest_consecutive.kara algorithm-for-algorithm.
package main

import "fmt"

func longestConsecutive(nums []int64) int64 {
	s := make(map[int64]struct{}, len(nums))
	for _, v := range nums {
		s[v] = struct{}{}
	}
	var best int64
	for _, v := range nums {
		if _, ok := s[v-1]; !ok {
			length := int64(1)
			cur := v
			for {
				if _, ok := s[cur+1]; !ok {
					break
				}
				cur++
				length++
			}
			if length > best {
				best = length
			}
		}
	}
	return best
}

func lcg(seed int64, n int64, cap int64) []int64 {
	out := make([]int64, 0, n)
	x := seed
	for k := int64(0); k < n; k++ {
		x = (x*1103515245 + 12345) % 2147483648
		out = append(out, x%cap)
	}
	return out
}

const (
	NP    = 8
	N     = 20000
	CapV  = 25000
	Iters = 150
)

func main() {
	arrays := make([][]int64, NP)
	for j := int64(0); j < NP; j++ {
		arrays[j] = lcg(j+1, N, CapV)
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % NP
		sink += longestConsecutive(arrays[idx])
	}
	fmt.Println(sink)
}
