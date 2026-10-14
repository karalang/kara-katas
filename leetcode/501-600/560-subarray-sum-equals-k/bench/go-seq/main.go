// Benchmark for #560: Go mirror of the ★ arm (prefix sums in a map); see
// ../subarray_sum.kara.
package main

import "fmt"

func subarraySum(nums []int64, k int64) int64 {
	seen := map[int64]int64{0: 1}
	var sum, count int64
	for _, x := range nums {
		sum += x
		count += seen[sum-k]
		seen[sum]++
	}
	return count
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 100
	const n = 20000
	const rounds = 20
	var seed int64 = 560
	arrays := make([][]int64, 0)
	for a := 0; a < count; a++ {
		nums := make([]int64, 0)
		for i := 0; i < n; i++ {
			nums = append(nums, step(&seed)%2001-1000)
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			k := step(&seed)%2001 - 1000
			c := subarraySum(arrays[(round*7+g)%count], k)
			total += c
			checksum = (checksum*31 + c) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: %d subarrays, checksum %d\n", count, n, rounds, total, checksum)
}
