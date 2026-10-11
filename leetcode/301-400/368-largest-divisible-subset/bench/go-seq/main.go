// Benchmark for #368 -- mirror of largest_subset.kara.
package main

import (
	"fmt"
	"sort"
)

func largestDivisibleSubset(nums []int64) []int64 {
	a := append([]int64(nil), nums...)
	sort.Slice(a, func(i, j int) bool { return a[i] < a[j] })
	n := len(a)
	size := make([]int64, n)
	next := make([]int, n)
	for i := range size {
		size[i] = 1
		next[i] = -1
	}
	for i := n - 1; i >= 0; i-- {
		for k := i + 1; k < n; k++ {
			if a[k]%a[i] == 0 && size[k]+1 > size[i] {
				size[i] = size[k] + 1
				next[i] = k
			}
		}
	}
	start := 0
	for i := 1; i < n; i++ {
		if size[i] > size[start] {
			start = i
		}
	}
	var out []int64
	for at := start; at != -1; at = next[at] {
		out = append(out, a[at])
	}
	return out
}

func main() {
	var seed int64 = 368
	var total, checksum int64
	for s := 0; s < 200; s++ {
		taken := make([]bool, 100001)
		var nums []int64
		for len(nums) < 1000 {
			seed = (seed*1103515245 + 12345) % 2147483648
			high := seed / 65536
			seed = (seed*1103515245 + 12345) % 2147483648
			v := 1 + (high*32768+seed/65536)%100000
			if !taken[v] {
				taken[v] = true
				nums = append(nums, v)
			}
		}
		out := largestDivisibleSubset(nums)
		total += int64(len(out))
		for _, v := range out {
			checksum = (checksum*31 + v) % 1000000007
		}
	}
	fmt.Printf("%d numbers in the answers, checksum %d\n", total, checksum)
}
