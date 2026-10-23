// LeetCode #922: Sort Array By Parity II -- bench: two pointers, in place.
// Mirrors sort_array_by_parity_ii.kara.
package main

import "fmt"

func sortArrayByParityII(nums []int64) {
	j := 1
	for i := 0; i < len(nums); i += 2 {
		if nums[i]%2 == 1 {
			for nums[j]%2 == 1 {
				j += 2
			}
			nums[i], nums[j] = nums[j], nums[i]
		}
	}
}

var seed int64 = 922

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, n = 3000, 20000
	// n / 2 even and n / 2 odd values up to 1000, shuffled, built once
	original := make([]int64, n)
	for k := range original {
		v := 2 * (nextRandom() % 500)
		if k%2 == 0 {
			original[k] = v
		} else {
			original[k] = v + 1
		}
	}
	for i := n - 1; i > 0; i-- {
		j := nextRandom() % int64(i+1)
		original[i], original[j] = original[j], original[i]
	}
	var check int64
	for r := 0; r < rounds; r++ {
		// a fresh copy each round, rearranged, and one value read back
		nums := make([]int64, n)
		copy(nums, original)
		sortArrayByParityII(nums)
		check = (check*1000003 + nums[(r*7919)%n]) % 1000000007
	}
	fmt.Printf("%d rounds over %d values: checksum %d\n", rounds, n, check)
}
