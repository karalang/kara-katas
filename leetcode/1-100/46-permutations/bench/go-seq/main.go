// LeetCode #46 bench mirror — Go, the used-array mutable-path backtracker (★).
//
// Mirrors bench/permutations.kara: a DFS that picks any still-unused element (tracked by a
// `used` bool slice) alongside a mutable path, snapshotting into a [][]int64 at each leaf.
// Same workload + checksum as every other mirror.
package main

import "fmt"

func backtrack(nums []int64, used []bool, path *[]int64, out *[][]int64) {
	n := len(nums)
	if len(*path) == n {
		snap := make([]int64, len(*path))
		copy(snap, *path)
		*out = append(*out, snap)
		return
	}
	for i := 0; i < n; i++ {
		if !used[i] {
			used[i] = true
			*path = append(*path, nums[i])
			backtrack(nums, used, path, out)
			*path = (*path)[:len(*path)-1]
			used[i] = false
		}
	}
}

func permute(nums []int64) [][]int64 {
	used := make([]bool, len(nums))
	path := []int64{}
	out := [][]int64{}
	backtrack(nums, used, &path, &out)
	return out
}

func main() {
	var total int64 = 300
	var modulus int64 = 1000000007
	var n int64 = 7
	nums := make([]int64, n)
	for b := int64(0); b < n; b++ {
		nums[b] = b + 1
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		nums[k%n] = 1 + (k % 9)
		perms := permute(nums)

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
