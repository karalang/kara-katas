// LeetCode #2461: Maximum Sum of Distinct Subarrays With Length K -- the
// bench, the ★ arm in Go: a sliding window of `k` with a `map` counting
// each value in it and the window's sum.
package main

import "fmt"

func maximumSubarraySum(nums []int64, k int) int64 {
	count := map[int64]int64{}
	sum, best := int64(0), int64(0)
	for i := range nums {
		count[nums[i]]++
		sum += nums[i]
		if i >= k {
			out := nums[i-k]
			count[out]--
			if count[out] == 0 {
				delete(count, out)
			}
			sum -= out
		}
		if i+1 >= k && len(count) == k {
			best = max(best, sum)
		}
	}
	return best
}

var seed int64 = 2461

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 10 arrays of 10^5 values from 1 to 2000 built once; then 28
	// passes, each setting one value of every array from the checksum so
	// far, then answering every array with k = 5 + 7 p % 40, folding the
	// answer plus the pass into the checksum
	arrays := make([][]int64, 10)
	for a := range arrays {
		arrays[a] = make([]int64, 100000)
		for i := range arrays[a] {
			arrays[a][i] = 1 + nextRandom()%2000
		}
	}
	check := int64(0)
	for p := int64(0); p < 28; p++ {
		k := int(5 + 7*p%40)
		for a := range arrays {
			arrays[a][(check+int64(a))%100000] = 1 + check%2000
			check = (check*31 + maximumSubarraySum(arrays[a], k) + p) % 1000000007
		}
	}
	fmt.Printf("28 passes over 10 arrays of 10^5: checksum %d\n", check)
}
