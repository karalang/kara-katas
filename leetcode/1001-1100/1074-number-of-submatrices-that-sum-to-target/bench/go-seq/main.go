// LeetCode #1074: Number of Submatrices That Sum to Target -- the
// benchmark's Go mirror of submatrix_sum.kara: the same row pairs and a
// map of running totals, over 30 matrices of 100 by 100 built once, each
// counted for three targets.
package main

import "fmt"

func numSubmatrixSumTarget(matrix [][]int64, target int64) int64 {
	m, n := len(matrix), len(matrix[0])
	var count int64
	for top := 0; top < m; top++ {
		column := make([]int64, n)
		for bottom := top; bottom < m; bottom++ {
			for c := 0; c < n; c++ {
				column[c] += matrix[bottom][c]
			}
			seen := map[int64]int64{0: 1}
			var total int64
			for c := 0; c < n; c++ {
				total += column[c]
				count += seen[total-target]
				seen[total] = seen[total] + 1
			}
		}
	}
	return count
}

var seed int64 = 1074

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	matrices := make([][][]int64, 30)
	for k := range matrices {
		matrices[k] = make([][]int64, 100)
		for r := range matrices[k] {
			matrices[k][r] = make([]int64, 100)
			for c := range matrices[k][r] {
				matrices[k][r][c] = nextRandom()%7 - 3
			}
		}
	}
	var total, check int64
	for _, matrix := range matrices {
		for _, target := range []int64{-5, 0, 7} {
			x := numSubmatrixSumTarget(matrix, target)
			total += x
			check = (check*31 + x) % 1000000007
		}
	}
	fmt.Printf("90 calls: %d submatrices, checksum %d\n", total, check)
}
