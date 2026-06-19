// LeetCode #39 bench mirror — Go, the mutable-path backtracking solver (★).
//
// Mirrors bench/combination_sum.kara: index-bounded DFS with one mutable path (push/pop),
// snapshotting into a [][]int64 at each target-hit leaf. Same workload + checksum as every
// other mirror.
package main

import "fmt"

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
		if c <= remaining {
			*path = append(*path, c)
			backtrack(candidates, i, remaining-c, path, out)
			*path = (*path)[:len(*path)-1]
		}
	}
}

func combinationSum(candidates []int64, target int64) [][]int64 {
	out := [][]int64{}
	path := []int64{}
	backtrack(candidates, 0, target, &path, &out)
	return out
}

func main() {
	var total int64 = 30000
	var modulus int64 = 1000000007
	candidates := []int64{2, 3, 5, 7}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		target := 18 + (k % 13)
		combos := combinationSum(candidates, target)

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
