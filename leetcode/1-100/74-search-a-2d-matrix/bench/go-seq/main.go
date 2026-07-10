// Benchmark workload — Search a 2D Matrix (LeetCode #74).
// Go single-threaded mirror of bench/search_a_2d_matrix.{kara,rs,c}. Flattened
// binary search over a 100×100 matrix built ONCE as [][]int64 (slice of slices —
// double-indirection, matching Kāra's Vec[Vec[i64]] indexing), then K=10,000,000
// queries (targets k % 20000, ~half hit) folding each hit/miss bit into a rolling
// polynomial hash. See ../README.md § Benchmarks.

package main

import "fmt"

func searchMatrix(m [][]int64, target int64) bool {
	rows := int64(len(m))
	if rows == 0 {
		return false
	}
	cols := int64(len(m[0]))
	if cols == 0 {
		return false
	}
	lo, hi := int64(0), rows*cols-1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		v := m[mid/cols][mid%cols]
		if v == target {
			return true
		} else if v < target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return false
}

func main() {
	const rows int64 = 100
	const cols int64 = 100
	const total int64 = 10000000
	const modulus int64 = 1000000007
	const rng int64 = 2 * rows * cols

	m := make([][]int64, rows)
	for i := int64(0); i < rows; i++ {
		m[i] = make([]int64, cols)
		for j := int64(0); j < cols; j++ {
			m[i][j] = (i*cols + j) * 2
		}
	}

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		target := k % rng
		var bit int64 = 0
		if searchMatrix(m, target) {
			bit = 1
		}
		acc = (acc*131 + bit) % modulus
	}
	fmt.Println(acc)
}
