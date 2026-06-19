// LeetCode #47 bench mirror — Go, the sorted used-array adjacent-skip backtracker (★).
//
// Mirrors bench/permutations_ii.kara: sort a working copy, then a DFS that picks any still-unused
// element (tracked by a `used` bool slice) with a same-level adjacent-duplicate skip, snapshotting
// into a [][]int64 at each leaf. Same workload + checksum as every other mirror.
package main

import (
	"fmt"
	"sort"
)

func backtrack(nums []int64, used []bool, path *[]int64, out *[][]int64) {
	n := len(nums)
	if len(*path) == n {
		snap := make([]int64, len(*path))
		copy(snap, *path)
		*out = append(*out, snap)
		return
	}
	for i := 0; i < n; i++ {
		if used[i] {
			continue
		}
		if i > 0 && nums[i] == nums[i-1] && !used[i-1] {
			continue
		}
		used[i] = true
		*path = append(*path, nums[i])
		backtrack(nums, used, path, out)
		*path = (*path)[:len(*path)-1]
		used[i] = false
	}
}

func permuteUnique(nums []int64) [][]int64 {
	xs := make([]int64, len(nums))
	copy(xs, nums)
	sort.Slice(xs, func(a, b int) bool { return xs[a] < xs[b] })
	used := make([]bool, len(xs))
	path := []int64{}
	out := [][]int64{}
	backtrack(xs, used, &path, &out)
	return out
}

func main() {
	var total int64 = 600
	var modulus int64 = 1000000007
	var n int64 = 8
	nums := make([]int64, n)
	for b := int64(0); b < n; b++ {
		nums[b] = 1 + (b % 4)
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		nums[k%n] = 1 + (k % 4)
		perms := permuteUnique(nums)

		var sig int64 = 0
		for _, perm := range perms {
			var s int64 = 0
			for i := 0; i < len(perm); i++ {
				s += perm[i] * (int64(i) + 1)
			}
			sig = (sig*31 + s) % modulus
		}
		sig = (sig + int64(len(perms))) % modulus
		acc = (acc*131 + sig) % modulus
	}

	fmt.Println(acc)
}
