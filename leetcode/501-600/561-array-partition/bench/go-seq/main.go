// Benchmark for #561: Go mirror of the ★ arm (sort, then every other
// number); see ../array_partition.kara. Each call sorts a fresh copy
// with `slices.Sort`.
package main

import (
	"fmt"
	"slices"
)

func arrayPairSum(nums []int64) int64 {
	slices.Sort(nums)
	var sum int64
	for i := 0; i < len(nums); i += 2 {
		sum += nums[i]
	}
	return sum
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 100
	const n = 20000
	const rounds = 50
	var seed int64 = 561
	arrays := make([][]int64, 0)
	for a := 0; a < count; a++ {
		nums := make([]int64, 0)
		for i := 0; i < n; i++ {
			nums = append(nums, step(&seed)%20001-10000)
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			s := arrayPairSum(slices.Clone(arrays[(round*7+g)%count]))
			total += s
			checksum = (checksum*31 + s + 1000000000) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d, %d rounds: total %d, checksum %d\n", count, n, rounds, total, checksum)
}
