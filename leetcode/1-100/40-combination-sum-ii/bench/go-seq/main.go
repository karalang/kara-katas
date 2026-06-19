// LeetCode #40 bench mirror — Go, the sorted same-level-dedup backtracker (★).
//
// Mirrors bench/combination_sum_ii.kara: sort once, index-bounded DFS at i+1 with the
// same-level duplicate skip and suffix break, snapshotting into a [][]int64 at each leaf.
// Same workload + checksum as every other mirror.
package main

import (
	"fmt"
	"sort"
)

func backtrack(candidates []int64, start int, remaining int64, path *[]int64, out *[][]int64) {
	if remaining == 0 {
		snap := make([]int64, len(*path))
		copy(snap, *path)
		*out = append(*out, snap)
		return
	}
	n := len(candidates)
	for i := start; i < n; i++ {
		c := candidates[i]
		if c > remaining {
			break
		}
		if i > start && c == candidates[i-1] {
			continue
		}
		*path = append(*path, c)
		backtrack(candidates, i+1, remaining-c, path, out)
		*path = (*path)[:len(*path)-1]
	}
}

func combinationSum2(candidates []int64, target int64) [][]int64 {
	out := [][]int64{}
	path := []int64{}
	backtrack(candidates, 0, target, &path, &out)
	return out
}

func main() {
	var total int64 = 30000
	var modulus int64 = 1000000007
	candidates := []int64{1, 1, 2, 2, 3, 3, 4, 5, 6, 7}
	sort.Slice(candidates, func(i, j int) bool { return candidates[i] < candidates[j] })

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		target := 10 + (k % 13)
		combos := combinationSum2(candidates, target)

		var sig int64 = 0
		for _, combo := range combos {
			var s int64 = 0
			for i := 0; i < len(combo); i++ {
				s += combo[i] * (int64(i) + 1)
			}
			sig = (sig*31 + s) % modulus
		}
		sig = (sig + int64(len(combos))) % modulus
		acc = (acc*131 + sig) % modulus
	}

	fmt.Println(acc)
}
