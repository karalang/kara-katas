// LeetCode #2122: Recover the Original Array -- the benchmark, the same
// algorithm as recover.kara: each positive even distance from the
// smallest number tried as 2k, smallest first, the sorted numbers paired
// by two pointers.

package main

import (
	"fmt"
	"sort"
)

func recoverArray(nums []int64) []int64 {
	sorted := append([]int64(nil), nums...)
	sort.Slice(sorted, func(a, b int) bool { return sorted[a] < sorted[b] })
	m := len(sorted)
	for i := 1; i < m; i++ {
		gap := sorted[i] - sorted[0]
		if gap == 0 || gap%2 != 0 || (i > 1 && gap == sorted[i-1]-sorted[0]) {
			continue
		}
		k := gap / 2
		used := make([]bool, m)
		original := make([]int64, 0, m/2)
		high := 0
		for low := 0; low < m; low++ {
			if used[low] {
				continue
			}
			for high < m && (used[high] || high <= low || sorted[high] < sorted[low]+2*k) {
				high++
			}
			if high == m || sorted[high] != sorted[low]+2*k {
				break
			}
			used[high] = true
			original = append(original, sorted[low]+k)
		}
		if len(original)*2 == m {
			return original
		}
	}
	return nil
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2122)
	arrays := make([][]int64, 0, 40)
	for g := 0; g < 40; g++ {
		top := []int64{1000, 10000, 100000}[g%3]
		k := nextRandom(&seed)%500 + 1
		nums := make([]int64, 0, 2000)
		for t := 0; t < 1000; t++ {
			x := (nextRandom(&seed)*32768+nextRandom(&seed))%top + 1 + k
			nums = append(nums, x-k, x+k)
		}
		for i := len(nums) - 1; i > 0; i-- {
			j := nextRandom(&seed) % int64(i+1)
			nums[i], nums[j] = nums[j], nums[i]
		}
		arrays = append(arrays, nums)
	}
	sizes := 0
	var check int64
	for r := 0; r < 200; r++ {
		for g := 0; g < 40; g++ {
			for i := range arrays[g] {
				arrays[g][i]++
			}
			original := recoverArray(arrays[g])
			sizes += len(original)
			for _, v := range original {
				check = (check*31 + v) % 1000000007
			}
		}
	}
	fmt.Printf("8000 solves: %d values recovered, checksum %d\n", sizes, check)
}
