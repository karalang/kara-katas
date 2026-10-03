// Benchmark workload for LeetCode #330 — mirrors patching_array.kara.
package main

import (
	"fmt"
	"sort"
)

const (
	LEN     = 100000
	PUNCHES = 1500
	MODULUS = 1073741789
)

var seed int64 = 330

func next() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func minPatches(nums []int64, n int64) int64 {
	var miss, patches int64 = 1, 0
	i := 0
	for miss <= n {
		if i < len(nums) && nums[i] <= miss {
			miss += nums[i]
			i++
		} else {
			miss += miss
			patches++
		}
	}
	return patches
}

func main() {
	nums := make([]int64, 0, LEN)
	var total int64
	for k := 0; k < LEN; k++ {
		v := next()%1001 + 50
		nums = append(nums, v)
		total += v
	}
	sort.Slice(nums, func(a, b int) bool { return nums[a] < nums[b] })
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		hi := next()
		lo := next()
		n := (hi*32768+lo)%(2*total) + 1
		answer := minPatches(nums, n)
		sink = (sink*1000003 + answer*64 + n%64) % MODULUS
	}
	fmt.Println(sink)
}
