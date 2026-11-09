// LeetCode #2040: Kth Smallest Product of Two Sorted Arrays -- the ★ arm in
// Go, the same algorithm and workload as product.kara: binary search on the
// answer, the products at most `x` counted by sort.Search.
package main

import (
	"fmt"
	"sort"
)

func countAtMost(nums1, nums2 []int64, x int64) int64 {
	var count int64
	m := len(nums2)
	for _, a := range nums1 {
		if a > 0 {
			count += int64(sort.Search(m, func(i int) bool { return a*nums2[i] > x }))
		} else if a < 0 {
			count += int64(m - sort.Search(m, func(i int) bool { return a*nums2[i] <= x }))
		} else if x >= 0 {
			count += int64(m)
		}
	}
	return count
}

func floorHalf(v int64) int64 {
	if v >= 0 {
		return v / 2
	}
	return -((-v + 1) / 2)
}

func kthSmallestProduct(nums1, nums2 []int64, k int64) int64 {
	lo, hi := int64(-10000000000), int64(10000000000)
	for lo < hi {
		mid := lo + floorHalf(hi-lo)
		if countAtMost(nums1, nums2, mid) >= k {
			hi = mid
		} else {
			lo = mid + 1
		}
	}
	return lo
}

var seed int64 = 2040

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func sortedValues(n, top int64) []int64 {
	v := make([]int64, n)
	for i := range v {
		hi := nextRandom()
		v[i] = (hi*32768+nextRandom())%(2*top+1) - top
	}
	sort.Slice(v, func(i, j int) bool { return v[i] < v[j] })
	return v
}

func main() {
	n := int64(50000)
	tops := []int64{100000, 3, 1000, 100000}
	as := make([][]int64, 4)
	bs := make([][]int64, 4)
	for r := 0; r < 4; r++ {
		as[r] = sortedValues(n, tops[r])
		bs[r] = sortedValues(n, tops[r])
	}
	var calls, sum, check int64
	for round := int64(0); round < 3; round++ {
		for r := int64(0); r < 4; r++ {
			k := (round*4+r+1)*(n*n/13) + 1
			answer := kthSmallestProduct(as[r], bs[r], k)
			calls++
			sum += answer
			m := answer % 1000000007
			if m < 0 {
				m += 1000000007
			}
			check = (check*31 + m) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
