// LeetCode #2771: Longest Non-decreasing Subarray From Two Arrays -- the
// bench in Go: the ★ arm over 20 pairs of 10^5 numbers, all drawn first,
// then each answered 10 times.
package main

import "fmt"

func maxNonDecreasingLength(nums1, nums2 []int64) int64 {
	n := len(nums1)
	one, two := int64(1), int64(1)
	best := int64(1)
	for i := 1; i < n; i++ {
		nextOne, nextTwo := int64(1), int64(1)
		if nums1[i-1] <= nums1[i] {
			nextOne = max(nextOne, one+1)
		}
		if nums2[i-1] <= nums1[i] {
			nextOne = max(nextOne, two+1)
		}
		if nums1[i-1] <= nums2[i] {
			nextTwo = max(nextTwo, one+1)
		}
		if nums2[i-1] <= nums2[i] {
			nextTwo = max(nextTwo, two+1)
		}
		one = nextOne
		two = nextTwo
		best = max(best, one, two)
	}
	return best
}

var seed int64 = 2771

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20
	rounds := 10
	n := int64(100000)
	ones := make([][]int64, count)
	twos := make([][]int64, count)
	for c := 0; c < count; c++ {
		noise := nextRandom()%200 + 1
		ones[c] = make([]int64, n)
		for i := int64(0); i < n; i++ {
			ones[c][i] = i*10 + nextRandom()%noise + 1
		}
		twos[c] = make([]int64, n)
		for i := int64(0); i < n; i++ {
			twos[c][i] = wide()%1000000000 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			a := maxNonDecreasingLength(ones[c], twos[c])
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d pairs of 10^5, %d rounds: lengths sum to %d, checksum %d\n", count, rounds, total, check)
}
