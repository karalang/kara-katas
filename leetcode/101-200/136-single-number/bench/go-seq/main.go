package main

import "fmt"

func singleNumber(nums []int64) int64 {
	var acc int64 = 0
	for _, x := range nums {
		acc ^= x
	}
	return acc
}

func main() {
	var pairs int64 = 140000
	var passes int64 = 3400
	n := 2*pairs + 1

	nums := make([]int64, 0, n)
	var state int64 = 12345
	for k := int64(0); k < pairs; k++ {
		state = (state*1103515245 + 12345) & 2147483647
		v := state >> 16
		nums = append(nums, v, v)
	}
	state = (state*1103515245 + 12345) & 2147483647
	nums = append(nums, state>>16)

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		idx := (p*97 + 13) % n
		nums[idx] ^= 1 << (p % 14)
		sink += singleNumber(nums)
	}
	fmt.Println(sink)
}
