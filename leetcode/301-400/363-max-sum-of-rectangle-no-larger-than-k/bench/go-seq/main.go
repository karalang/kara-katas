// Benchmark for #363 -- mirror of max_sum.kara (the merge-sort arm).
package main

import (
	"fmt"
	"math"
)

func max64(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func bestPair(p []int64, lo, hi int, k int64, scratch []int64) int64 {
	if hi-lo < 2 {
		return math.MinInt64
	}
	mid := (lo + hi) / 2
	best := max64(bestPair(p, lo, mid, k, scratch), bestPair(p, mid, hi, k, scratch))
	j := mid
	for i := lo; i < mid; i++ {
		for j < hi && p[j] <= p[i]+k {
			j++
		}
		if j > mid {
			best = max64(best, p[j-1]-p[i])
		}
	}
	a, b, out := lo, mid, lo
	for a < mid || b < hi {
		if b == hi || (a < mid && p[a] <= p[b]) {
			scratch[out] = p[a]
			a++
		} else {
			scratch[out] = p[b]
			b++
		}
		out++
	}
	copy(p[lo:hi], scratch[lo:hi])
	return best
}

func maxSumSubmatrix(matrix [][]int64, k int64) int64 {
	rows, cols := len(matrix), len(matrix[0])
	best := int64(math.MinInt64)
	scratch := make([]int64, cols+1)
	for top := 0; top < rows; top++ {
		sums := make([]int64, cols)
		for bottom := top; bottom < rows; bottom++ {
			for c := 0; c < cols; c++ {
				sums[c] += matrix[bottom][c]
			}
			prefix := make([]int64, cols+1)
			for c := 0; c < cols; c++ {
				prefix[c+1] = prefix[c] + sums[c]
			}
			best = max64(best, bestPair(prefix, 0, cols+1, k, scratch))
		}
	}
	return best
}

func main() {
	var seed int64 = 363
	var checksum int64
	for it := 0; it < 20; it++ {
		matrix := make([][]int64, 0, 100)
		var least int64 = 100
		for r := 0; r < 100; r++ {
			row := make([]int64, 0, 100)
			for c := 0; c < 100; c++ {
				seed = (seed*1103515245 + 12345) % 2147483648
				v := (seed/65536)%201 - 100
				if v < least {
					least = v
				}
				row = append(row, v)
			}
			matrix = append(matrix, row)
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		k := max64(least, (seed/65536)%20001-10000)
		checksum = (checksum*31 + maxSumSubmatrix(matrix, k) + 1000000) % 1000000007
	}
	fmt.Printf("checksum %d\n", checksum)
}
