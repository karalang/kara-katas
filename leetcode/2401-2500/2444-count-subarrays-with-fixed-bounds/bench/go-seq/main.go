// LeetCode #2444: Count Subarrays With Fixed Bounds -- the bench, the ★
// arm: one pass keeping the last value outside the bounds, the last
// `min_k` and the last `max_k`.
package main

import "fmt"

func countSubarrays(nums []int64, minK, maxK int64) int64 {
	var count int64
	bad, lastMin, lastMax := int64(-1), int64(-1), int64(-1)
	for i, x := range nums {
		k := int64(i)
		if x < minK || x > maxK {
			bad = k
		}
		if x == minK {
			lastMin = k
		}
		if x == maxK {
			lastMax = k
		}
		start := lastMin
		if lastMax < start {
			start = lastMax
		}
		if start > bad {
			count += start - bad
		}
	}
	return count
}

var seed int64 = 2444

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	arrays := make([][]int64, 10)
	for c := range arrays {
		arrays[c] = make([]int64, 100000)
		for i := range arrays[c] {
			arrays[c][i] = 1 + nextRandom()%20
		}
	}
	var check int64
	for p := int64(0); p < 100; p++ {
		for c := range arrays {
			at := (p*7919 + int64(c)*104729) % 100000
			arrays[c][at] = 1 + nextRandom()%20
			check = (check*31 + countSubarrays(arrays[c], 3, 17) + p) % 1000000007
		}
	}
	fmt.Printf("100 passes over 10 arrays of 10^5 values: checksum %d\n", check)
}
