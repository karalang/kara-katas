// Benchmark workload — Remove Duplicates from Sorted Array II (LeetCode #80).
// Go mirror of ../remove_duplicates_ii.kara. The generalized run-scan computes the
// at-most-2 dedup and folds each kept value through a rolling polynomial hash — the
// loop-carried hash serialises the scan, and a fixed heap slice built once avoids
// per-iteration allocation. N=3000 sorted array with mixed run lengths, scanned
// K=67000 times, seeded by the iteration index.
package main

import "fmt"

func build(n int64) []int64 {
	arr := make([]int64, 0, n)
	var val int64 = 0
	var pos int64 = 0
	for pos < n {
		runlen := (val % 3) + 1
		for r := int64(0); r < runlen && pos < n; r++ {
			arr = append(arr, val)
			pos++
		}
		val++
	}
	return arr
}

func scanFold(arr []int64, n, seed int64) int64 {
	acc := seed
	var i int64 = 0
	for i < n {
		v := arr[i]
		var run int64 = 0
		for i < n && arr[i] == v {
			if run < 2 {
				acc = (acc*131 + (v + 1)) % 1000000007
			}
			run++
			i++
		}
	}
	return acc
}

func main() {
	const n = 3000
	const total = 67000
	const modulus = 1000000007
	arr := build(n)
	var sum int64 = 0
	for iter := int64(0); iter < total; iter++ {
		r := scanFold(arr, n, iter)
		sum = (sum + r) % modulus
	}
	fmt.Println(sum)
}
