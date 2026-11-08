// LeetCode #2025: Maximum Number of Ways to Partition an Array -- the ★ arm
// in Go, the same algorithm and workload as partition.kara.
package main

import "fmt"

func waysToPartition(nums []int64, k int64) int64 {
	n := len(nums)
	var total int64
	for _, x := range nums {
		total += x
	}
	d := make([]int64, 0, n)
	var left int64
	for p := 1; p < n; p++ {
		left += nums[p-1]
		d = append(d, left-(total-left))
	}
	right := map[int64]int64{}
	for _, x := range d {
		right[x]++
	}
	best := right[0]
	seen := map[int64]int64{}
	for i := 0; i < n; i++ {
		if i >= 1 {
			x := d[i-1]
			right[x]--
			seen[x]++
		}
		delta := k - nums[i]
		ways := right[-delta] + seen[delta]
		if ways > best {
			best = ways
		}
	}
	return best
}

var seed int64 = 2025

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rs := []int64{1, 2, 3, 10, 100, 1000, 10000, 100000}
	arrays := make([][]int64, 0, 20)
	ks := make([]int64, 0, 20)
	for a := 0; a < 20; a++ {
		r := rs[a%8]
		arr := make([]int64, 50000)
		for i := range arr {
			arr[i] = nextRandom()%(2*r+1) - r
		}
		arrays = append(arrays, arr)
		ks = append(ks, nextRandom()%(2*r+1)-r)
	}
	var calls, total, check int64
	for r := 0; r < 10; r++ {
		for a := 0; a < 20; a++ {
			best := waysToPartition(arrays[a], ks[a])
			calls++
			total += best
			check = (check*31 + best) % 1000000007
		}
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, check)
}
