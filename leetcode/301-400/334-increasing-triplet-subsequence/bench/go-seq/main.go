// Benchmark workload for LeetCode #334 — Go mirror of increasing_triplet.kara.
package main

import "fmt"

const (
	values  = 1000000
	punches = 100
	modulus = 1073741789
)

func increasingTriplet(nums []int64) bool {
	hasFirst, hasSecond := false, false
	var first, second int64
	for _, x := range nums {
		if hasSecond && x > second {
			return true
		}
		if hasFirst && x > first {
			second = x
			hasSecond = true
		} else {
			first = x
			hasFirst = true
		}
	}
	return false
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := next(seed)
	return hi*32768 + next(seed)
}

func main() {
	nums := make([]int64, 0, values)
	top := int64(2 * values)
	for k := 0; k < values/2; k++ {
		nums = append(nums, top-1, top)
		top -= 2
	}
	seed := int64(334)
	sink := int64(0)
	for p := 0; p < punches; p++ {
		at := 2 + 2*(wide(&seed)%(values/2-1))
		old := nums[at]
		if p%2 == 0 {
			nums[at] = nums[at-1] + 1
		}
		answer := int64(0)
		if increasingTriplet(nums) {
			answer = 1
		}
		nums[at] = old
		sink = (sink*1000003 + answer*2000003 + at) % modulus
	}
	fmt.Println(sink)
}
