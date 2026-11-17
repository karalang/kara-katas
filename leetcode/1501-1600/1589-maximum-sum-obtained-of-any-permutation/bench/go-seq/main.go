// LeetCode #1589: Maximum Sum Obtained of Any Permutation -- the bench in
// Go, mirroring max_sum.kara. Each request is its own slice.
package main

import (
	"fmt"
	"sort"
)

func maxSumRangeQuery(nums []int32, requests [][]int32) int32 {
	n := len(nums)
	asked := make([]int64, n+1)
	for _, r := range requests {
		asked[r[0]]++
		asked[r[1]+1]--
	}
	for i := 1; i < n; i++ {
		asked[i] += asked[i-1]
	}
	asked = asked[:n]
	sort.Slice(asked, func(i, j int) bool { return asked[i] < asked[j] })
	values := append([]int32(nil), nums...)
	sort.Slice(values, func(i, j int) bool { return values[i] < values[j] })
	var total int64
	for i := range asked {
		total = (total + asked[i]*int64(values[i])) % 1000000007
	}
	return int32(total)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	a := nextRandom(seed)
	return a*32768 + nextRandom(seed)
}

func main() {
	seed := int64(1589)
	n := int64(100000)
	var allNums [][]int32
	var allRequests [][][]int32
	for p := 0; p < 20; p++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32(wide(&seed) % 100001)
		}
		requests := make([][]int32, 0)
		for k := 0; k < 100000; k++ {
			a := wide(&seed) % n
			b := wide(&seed) % n
			lo, hi := a, b
			if b < a {
				lo, hi = b, a
			}
			requests = append(requests, []int32{int32(lo), int32(hi)})
		}
		allNums = append(allNums, nums)
		allRequests = append(allRequests, requests)
	}
	var check int64
	for p := range allNums {
		check = (check*31 + int64(maxSumRangeQuery(allNums[p], allRequests[p])) + 1) % 1000000007
	}
	fmt.Printf("20 problems of 100000 values and 100000 requests: checksum %d\n", check)
}
