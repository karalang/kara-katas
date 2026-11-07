// LeetCode #1060: Missing Element in Sorted Array -- the benchmark, the
// same algorithm as missing.kara.
package main

import "fmt"

func missingElement(nums []int64, k int64) int64 {
	missing := func(i int64) int64 { return nums[i] - nums[0] - i }
	last := int64(len(nums)) - 1
	if missing(last) < k {
		return nums[last] + k - missing(last)
	}
	// missing(lo) < k <= missing(hi)
	lo, hi := int64(0), last
	for hi-lo > 1 {
		mid := lo + (hi-lo)/2
		if missing(mid) < k {
			lo = mid
		} else {
			hi = mid
		}
	}
	return nums[lo] + k - missing(lo)
}

var seed int64 = 1060

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 50 arrays of 50000 values, built once; 200000 values of k each
	var calls, sum, check int64
	for a := int64(0); a < 50; a++ {
		nums := []int64{nextRandom()%100 + 1}
		for i := 1; i < 50000; i++ {
			gap := 1 + nextRandom()%(2+a*3)
			nums = append(nums, nums[len(nums)-1]+gap)
		}
		span := nums[49999] - nums[0] - 49999
		for j := 0; j < 200000; j++ {
			hi := nextRandom() * 32768
			k := 1 + (hi+nextRandom())%(span+1000)
			answer := missingElement(nums, k)
			sum += answer
			check = (check*31 + answer%1000003) % 1000000007
			calls++
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
