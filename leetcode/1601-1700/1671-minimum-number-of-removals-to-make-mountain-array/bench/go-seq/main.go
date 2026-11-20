// LeetCode #1671: Minimum Number of Removals to Make Mountain Array -- the
// bench's Go mirror: the ★ arm on 300 arrays of 1000 values up to 10^9,
// one raised above the rest, all drawn first.
package main

import "fmt"

func minimumMountainRemovals(nums []int32) int32 {
	n := len(nums)
	up := make([]int64, n)
	down := make([]int64, n)
	for i := range up {
		up[i], down[i] = 1, 1
	}
	for i := 0; i < n; i++ {
		for j := 0; j < i; j++ {
			if nums[j] < nums[i] {
				up[i] = max(up[i], up[j]+1)
			}
		}
	}
	for i := n - 1; i >= 0; i-- {
		for j := i + 1; j < n; j++ {
			if nums[j] < nums[i] {
				down[i] = max(down[i], down[j]+1)
			}
		}
	}
	var longest int64
	for i := 1; i < n-1; i++ {
		if up[i] > 1 && down[i] > 1 {
			longest = max(longest, up[i]+down[i]-1)
		}
	}
	return int32(int64(n) - longest)
}

var seed int64 = 1671

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const arrays = 300
	const n = 1000
	const most = 1000000000
	all := make([][]int32, 0, arrays)
	for a := 0; a < arrays; a++ {
		nums := make([]int32, n)
		for i := range nums {
			nums[i] = int32((nextRandom()*32768+nextRandom())%most + 1)
		}
		peak := nextRandom()%(n-2) + 1
		nums[peak] = most + 1
		all = append(all, nums)
	}
	var total, check int64
	for _, nums := range all {
		removed := int64(minimumMountainRemovals(nums))
		total += removed
		check = (check*31 + removed) % 1000000007
	}
	fmt.Printf("%d arrays of %d values: %d removals, checksum %d\n", arrays, n, total, check)
}
