// LeetCode #2302: Count Subarrays With Score Less Than K -- the bench,
// the ★ arm in Go. A sliding window, narrowed at the left while its score
// is k or more, counting every subarray ending at its right end.
package main

import "fmt"

func countSubarrays(nums []int64, k int64) int64 {
	var count, sum, left int64
	for right := int64(0); right < int64(len(nums)); right++ {
		sum += nums[right]
		for sum*(right-left+1) >= k {
			sum -= nums[left]
			left++
		}
		count += right - left + 1
	}
	return count
}

var seed int64 = 2302

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 20)
	for a := range arrays {
		nums := make([]int64, 100000)
		for i := range nums {
			hi := nextRandom()
			nums[i] = (hi*32768+nextRandom())%100000 + 1
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 30; p++ {
		for a := int64(0); a < 20; a++ {
			check = (check*31 + countSubarrays(arrays[a], 1000000000*(a+1)+p)) % 1000000007
		}
	}
	fmt.Printf("30 passes over 20 arrays of 10^5: checksum %d\n", check)
}
