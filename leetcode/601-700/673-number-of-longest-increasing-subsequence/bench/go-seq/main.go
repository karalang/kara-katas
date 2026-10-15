// Benchmark for #673: the length and count ending at each place, as the
// Kara ★ arm.
package main

import "fmt"

func findNumberOfLIS(nums []int64) int64 {
	n := len(nums)
	length := make([]int64, n)
	count := make([]int64, n)
	for i := range length {
		length[i] = 1
		count[i] = 1
	}
	for i := 0; i < n; i++ {
		for j := 0; j < i; j++ {
			if nums[j] < nums[i] {
				if length[j]+1 > length[i] {
					length[i] = length[j] + 1
					count[i] = count[j]
				} else if length[j]+1 == length[i] {
					count[i] += count[j]
				}
			}
		}
	}
	var best int64
	for _, v := range length {
		if v > best {
			best = v
		}
	}
	var total int64
	for i := 0; i < n; i++ {
		if length[i] == best {
			total += count[i]
		}
	}
	return total
}

func main() {
	var rounds int64 = 150
	var size int64 = 2000
	var seed int64 = 673
	var sum int64
	for r := int64(0); r < rounds; r++ {
		nums := make([]int64, 0)
		for i := int64(0); i < size; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			nums = append(nums, seed/65536)
		}
		sum = (sum*31 + findNumberOfLIS(nums)) % 1000000007
	}
	fmt.Printf("%d arrays of %d: checksum %d\n", rounds, size, sum)
}
