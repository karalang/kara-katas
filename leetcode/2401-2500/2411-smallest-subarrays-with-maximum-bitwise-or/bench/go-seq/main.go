// LeetCode #2411: Smallest Subarrays With Maximum Bitwise OR -- the bench,
// the ★ arm in Go: walking from the right, the nearest index holding each
// of the 30 bits, the subarray from i reaching the farthest of them.

package main

import "fmt"

var seed int64 = 2411

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func smallestSubarrays(nums []int64) []int64 {
	n := len(nums)
	nearest := make([]int64, 30)
	for b := range nearest {
		nearest[b] = -1
	}
	answer := make([]int64, n)
	for i := n - 1; i >= 0; i-- {
		reach := int64(i)
		for bit := 0; bit < 30; bit++ {
			if nums[i]>>bit&1 == 1 {
				nearest[bit] = int64(i)
			}
			reach = max(reach, nearest[bit])
		}
		answer[i] = reach - int64(i) + 1
	}
	return answer
}

func main() {
	arrays := make([][]int64, 5)
	for i := range arrays {
		nums := make([]int64, 100000)
		for j := range nums {
			nums[j] = (nextRandom()*32768 + nextRandom()) % (int64(1) << (6*i + 6))
		}
		arrays[i] = nums
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for _, nums := range arrays {
			for _, a := range smallestSubarrays(nums) {
				check = (check*31 + a + p) % 1000000007
			}
		}
	}
	fmt.Printf("10 passes over 5 arrays of 10^5 values: checksum %d\n", check)
}
