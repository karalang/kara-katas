// Benchmark harness for LeetCode #268 — Missing Number.
// Mirrors missing_number.kara algorithm-for-algorithm.

package main

import "fmt"

func missingNumber(nums []int64) int64 {
	n := int64(len(nums))
	acc := n
	for i := int64(0); i < n; i++ {
		acc = acc ^ i ^ nums[i]
	}
	return acc
}

func main() {
	const np int64 = 4
	const n int64 = 1000000
	const iters int64 = 850

	arrays := make([][]int64, 0, np)
	for p := int64(0); p < np; p++ {
		missing := 200000*p + 137

		arr := make([]int64, 0, n)
		for z := int64(0); z < n; z++ {
			arr = append(arr, 0)
		}
		v := int64(0)
		for t := int64(0); t < n; t++ {
			if v == missing {
				v++
			}
			idx := (t * 499979) % n
			arr[idx] = v
			v++
		}
		arrays = append(arrays, arr)
	}

	var sink int64 = 0
	for it := int64(0); it < iters; it++ {
		idx := (it * 3) % np
		sink = (sink*31 + missingNumber(arrays[idx])) % 1000000007
	}
	fmt.Println(sink)
}
