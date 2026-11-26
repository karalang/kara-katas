// LeetCode #1775: Equal Sum Arrays With Minimum Number of Operations --
// the bench in Go, mirroring min_operations.kara: the gains counted by size
// and the largest taken first.
package main

import "fmt"

func minOperations(nums1, nums2 []int32) int32 {
	var sum1, sum2 int32
	for _, x := range nums1 {
		sum1 += x
	}
	for _, x := range nums2 {
		sum2 += x
	}
	if sum1 == sum2 {
		return 0
	}
	low, high := nums1, nums2
	if sum1 > sum2 {
		low, high = nums2, nums1
	}
	gap := sum1 - sum2
	if gap < 0 {
		gap = -gap
	}
	gains := make([]int32, 6)
	for _, x := range low {
		gains[6-x]++
	}
	for _, x := range high {
		gains[x-1]++
	}
	var ops int32
	for g := 5; g >= 1; g-- {
		for gains[g] > 0 && gap > 0 {
			gap -= int32(g)
			gains[g]--
			ops++
		}
	}
	if gap > 0 {
		return -1
	}
	return ops
}

var seed int64 = 1775

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int32, 40)
	for r := range lists {
		low := 1 + nextRandom()%3
		high := 4 + nextRandom()%3
		v := make([]int32, 100000)
		for i := range v {
			v[i] = int32(low + nextRandom()%(high-low+1))
		}
		lists[r] = v
	}
	var check int64
	for call := int64(0); call < 400; call++ {
		a := (check + call) % 40
		b := (check/40 + call*7) % 40
		check = (check*31 + int64(minOperations(lists[a], lists[b])) + 1) % 1000000007
	}
	fmt.Printf("400 calls over 40 lists: checksum %d\n", check)
}
