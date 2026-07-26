// Benchmark harness for LeetCode #260 — Single Number III.
// Mirrors single_number_iii.kara algorithm-for-algorithm.

package main

import "fmt"

func twoSingles(nums []int64) [2]int64 {
	var x int64 = 0
	for i := 0; i < len(nums); i++ {
		x ^= nums[i]
	}
	bit := x & (0 - x)

	var a int64 = 0
	var b int64 = 0
	for j := 0; j < len(nums); j++ {
		if nums[j]&bit != 0 {
			a ^= nums[j]
		} else {
			b ^= nums[j]
		}
	}
	if a <= b {
		return [2]int64{a, b}
	}
	return [2]int64{b, a}
}

func main() {
	const np int64 = 4
	const k int64 = 100000
	const iters int64 = 2600

	arrays := make([][]int64, 0, np)
	for p := int64(0); p < np; p++ {
		vals := make([]int64, 0, k)
		x := p + 1
		for t := int64(0); t < k; t++ {
			x = (x*1103515245 + 12345) % 2147483648
			vals = append(vals, (x/65536)%100000)
		}
		arr := make([]int64, 0, 2*k+2)
		for pass := 0; pass < 2; pass++ {
			for q := int64(0); q < k; q++ {
				arr = append(arr, vals[q])
			}
		}
		arr = append(arr, 999983+p)
		arr = append(arr, 1000003+p)
		arrays = append(arrays, arr)
	}

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		idx := (it * 3) % np
		r := twoSingles(arrays[idx])
		sink = (sink*31 + r[0] + r[1]*7) % 1000000007
	}
	fmt.Println(sink)
}
