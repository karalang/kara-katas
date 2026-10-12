// Benchmark for #446: mirror of arithmetic_slices.kara (a map of
// differences per index) on 20 random arrays of 1,000 values from -500
// to 499, built once.
package main

import "fmt"

func numberOfArithmeticSlices(nums []int64) int64 {
	n := len(nums)
	ending := make([]map[int64]int64, 0, n)
	total := int64(0)
	for i := 0; i < n; i++ {
		here := map[int64]int64{}
		for j := 0; j < i; j++ {
			d := nums[i] - nums[j]
			before := ending[j][d]
			total += before
			here[d] += before + 1
		}
		ending = append(ending, here)
	}
	return total
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n = 20, 1000
	seed := int64(446)
	arrays := make([][]int64, 0, count)
	for c := 0; c < count; c++ {
		nums := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			nums = append(nums, nextRandom(&seed)%1000-500)
		}
		arrays = append(arrays, nums)
	}
	total := int64(0)
	checksum := int64(0)
	for _, nums := range arrays {
		answer := numberOfArithmeticSlices(nums)
		total += answer
		checksum = (checksum*31 + answer%1000000007) % 1000000007
	}
	fmt.Printf("%d arrays of %d: %d slices, checksum %d\n", count, n, total, checksum)
}
