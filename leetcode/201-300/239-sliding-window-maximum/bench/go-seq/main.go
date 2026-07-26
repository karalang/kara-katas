// Benchmark harness for LeetCode #239 — Sliding Window Maximum.
// Mirrors sliding_window_max.kara algorithm-for-algorithm, including the
// slice-plus-head-cursor deque rather than container/list.
package main

import "fmt"

func maxSlidingWindow(nums []int64, k int64) []int64 {
	n := int64(len(nums))
	out := make([]int64, 0, n)
	dq := make([]int64, 0, n)
	var head int64

	for i := int64(0); i < n; i++ {
		for int64(len(dq)) > head {
			back := dq[len(dq)-1]
			if nums[back] <= nums[i] {
				dq = dq[:len(dq)-1]
			} else {
				break
			}
		}
		dq = append(dq, i)

		if dq[head] <= i-k {
			head++
		}

		if i >= k-1 {
			out = append(out, nums[dq[head]])
		}
	}
	return out
}

func lcg(seed int64, n int64, cap int64) []int64 {
	out := make([]int64, 0, n)
	x := seed
	for t := int64(0); t < n; t++ {
		x = (x*1103515245 + 12345) % 2147483648
		out = append(out, x%cap)
	}
	return out
}

const (
	NP    = 8
	N     = 50000
	CapV  = 100000
	K     = 64
	Iters = 300
)

func main() {
	arrays := make([][]int64, NP)
	for j := int64(0); j < NP; j++ {
		arrays[j] = lcg(j+1, N, CapV)
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % NP
		res := maxSlidingWindow(arrays[idx], K)
		for v, val := range res {
			sink = (sink + (int64(v)+1)*val) % 1000000007
		}
	}
	fmt.Println(sink)
}
