// LeetCode #2321: Maximum Score Of Spliced Array -- the bench, the ★ arm
// in Go. Each array's sum plus the largest subarray sum of the
// differences the other array would bring, by Kadane's walk, both ways
// round. O(n).
package main

import "fmt"

func bestGain(into, from []int64) int64 {
	var best, here int64
	for i := range into {
		here = max(here+from[i]-into[i], 0)
		best = max(best, here)
	}
	return best
}

func maximumsSplicedArray(nums1, nums2 []int64) int64 {
	var sum1, sum2 int64
	for _, x := range nums1 {
		sum1 += x
	}
	for _, x := range nums2 {
		sum2 += x
	}
	return max(sum1+bestGain(nums1, nums2), sum2+bestGain(nums2, nums1))
}

var seed int64 = 2321

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 100000
	firsts := make([][]int64, 10)
	seconds := make([][]int64, 10)
	for k := 0; k < 10; k++ {
		firsts[k] = make([]int64, n)
		for i := range firsts[k] {
			firsts[k][i] = nextRandom()%10000 + 1
		}
		seconds[k] = make([]int64, n)
		for i := range seconds[k] {
			seconds[k][i] = nextRandom()%10000 + 1
		}
	}
	var check int64
	for p := 0; p < 200; p++ {
		for k := 0; k < 10; k++ {
			i := nextRandom() % n
			firsts[k][i] = nextRandom()%10000 + 1
			check = (check*31 + maximumsSplicedArray(firsts[k], seconds[k])) % 1000000007
		}
	}
	fmt.Printf("200 passes over 10 pairs of 10^5 numbers: checksum %d\n", check)
}
