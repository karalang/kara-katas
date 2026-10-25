// LeetCode #992: Subarrays with K Different Integers -- bench, the ★ arm
// (at most k, less at most k - 1), the same algorithm and workload as
// subarrays_with_k_distinct.kara.
package main

import "fmt"

func atMost(nums []int64, k int64) int64 {
	count := make([]int64, len(nums)+1)
	var distinct, total int64
	left := 0
	for right := 0; right < len(nums); right++ {
		if count[nums[right]] == 0 {
			distinct++
		}
		count[nums[right]]++
		for distinct > k {
			count[nums[left]]--
			if count[nums[left]] == 0 {
				distinct--
			}
			left++
		}
		total += int64(right - left + 1)
	}
	return total
}

func subarraysWithKDistinct(nums []int64, k int64) int64 {
	return atMost(nums, k) - atMost(nums, k-1)
}

var seed int64 = 992

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 100
	arrays := make([][]int64, 20)
	for i := range arrays {
		arrays[i] = make([]int64, 20000)
		for j := range arrays[i] {
			arrays[i][j] = 1 + nextRandom()%100
		}
	}
	var found, check int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < 20; i++ {
			k := int64(1 + (r*7+i)%60)
			got := subarraysWithKDistinct(arrays[(r+i)%20], k)
			found += got
			check = (check*31 + got + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds over 20 arrays of 20000 numbers: %d subarrays, checksum %d\n", rounds, found, check)
}
