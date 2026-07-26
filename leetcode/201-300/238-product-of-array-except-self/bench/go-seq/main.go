// Benchmark harness for LeetCode #238 — Product of Array Except Self.
// Mirrors product_except_self.kara algorithm-for-algorithm.
package main

import "fmt"

func productExceptSelf(nums []int64) []int64 {
	n := len(nums)
	out := make([]int64, 0, n)

	prefix := int64(1)
	for i := 0; i < n; i++ {
		out = append(out, prefix)
		prefix *= nums[i]
	}

	suffix := int64(1)
	for j := n - 1; j >= 0; j-- {
		out[j] *= suffix
		suffix *= nums[j]
	}

	return out
}

func lcgVals(seed int64, n int64) []int64 {
	out := make([]int64, 0, n)
	x := seed
	for t := int64(0); t < n; t++ {
		x = (x*1103515245 + 12345) % 2147483648
		out = append(out, 1-2*((x/65536)%2))
	}
	return out
}

const (
	NP    = 8
	N     = 100000
	Iters = 400
)

func main() {
	arrays := make([][]int64, NP)
	for j := int64(0); j < NP; j++ {
		arrays[j] = lcgVals(j+1, N)
	}

	var sink int64
	for it := int64(0); it < Iters; it++ {
		idx := (it * 3) % NP
		res := productExceptSelf(arrays[idx])
		for v, val := range res {
			sink = (sink + (int64(v)+1)*val) % 1000000007
		}
	}
	fmt.Println(sink)
}
